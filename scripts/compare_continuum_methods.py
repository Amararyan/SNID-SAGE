import argparse
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
import matplotlib.pyplot as plt

from snid_sage.snid.io import read_spectrum
from snid_sage.snid.preprocessing import (
    init_wavelength_grid,
    log_rebin,
    fit_continuum,
    apodize,
)


def _extend_continuum_edges(continuum: np.ndarray) -> np.ndarray:
    """Extend a continuum array to edges using edge values where it is zeroed.

    The Gaussian continuum fitter may zero the continuum outside the valid range.
    For display/reconstruction we need a non-zero continuum across the full grid.
    """
    cont = np.asarray(continuum, dtype=float).copy()
    try:
        nz = (cont > 0).nonzero()[0]
        if nz.size:
            c0, c1 = int(nz[0]), int(nz[-1])
            if c0 > 0:
                cont[:c0] = cont[c0]
            if c1 < cont.size - 1:
                cont[c1 + 1 :] = cont[c1]
    except Exception:
        # If anything goes wrong, return original
        return continuum
    return cont


def _compute_display_versions(
    log_wave: np.ndarray,
    log_flux: np.ndarray,
    method: str,
    *,
    knotnum: int = 13,
    sigma: Optional[float] = None,
    apodize_percent: float = 10.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute (flat_tapered, display_flux, continuum) for a given continuum method."""
    if method == "spline":
        flat, cont = fit_continuum(log_flux, method="spline", knotnum=knotnum)
    elif method == "gaussian":
        flat, cont = fit_continuum(log_flux, method="gaussian", sigma=sigma)
    else:
        raise ValueError("method must be 'spline' or 'gaussian'")

    # Apodize flattened spectrum over its non-zero region
    nz = np.flatnonzero(flat)
    if nz.size:
        l1, l2 = int(nz[0]), int(nz[-1])
    else:
        l1, l2 = 0, len(flat) - 1
    flat_tapered = apodize(flat, l1, l2, percent=apodize_percent)

    # Reconstruct flux display using extended continuum
    recon_cont = _extend_continuum_edges(cont)
    display_flux = (flat_tapered + 1.0) * recon_cont

    return flat_tapered, display_flux, cont


def _range_stats(arr: np.ndarray, mask: np.ndarray | None = None) -> tuple[float, float, float]:
    """Return (min, max, std) with optional mask."""
    a = np.asarray(arr, dtype=float)
    if mask is not None:
        a = a[mask]
    if a.size == 0:
        return float("nan"), float("nan"), float("nan")
    return float(np.nanmin(a)), float(np.nanmax(a)), float(np.nanstd(a))


def run_one(input_path: Path, out_dir: Path, apodize_percent: float = 10.0) -> None:
    name = input_path.stem
    wave, flux = read_spectrum(str(input_path))

    # Standard grid
    init_wavelength_grid(1024)
    log_wave, log_flux = log_rebin(wave, flux)

    # Compute display versions for spline and gaussian
    flat_spline, flux_spline, cont_spline = _compute_display_versions(
        log_wave, log_flux, method="spline", knotnum=13, apodize_percent=apodize_percent
    )
    flat_gauss, flux_gauss, cont_gauss = _compute_display_versions(
        log_wave, log_flux, method="gaussian", sigma=None, apodize_percent=apodize_percent
    )

    # Stats and comparisons
    # For fair flux comparison, restrict to region where either continuum is positive
    mask_flux = (_extend_continuum_edges(cont_spline) > 0) | (_extend_continuum_edges(cont_gauss) > 0)
    s_min, s_max, s_std = _range_stats(flux_spline, mask_flux)
    g_min, g_max, g_std = _range_stats(flux_gauss, mask_flux)

    fs_min, fs_max, fs_std = _range_stats(flat_spline, flat_spline != 0)
    fg_min, fg_max, fg_std = _range_stats(flat_gauss, flat_gauss != 0)

    print("=== Flux (display) ranges ===")
    print(f"Spline:   min={s_min:.6g}  max={s_max:.6g}  std={s_std:.6g}")
    print(f"Gaussian: min={g_min:.6g}  max={g_max:.6g}  std={g_std:.6g}")

    print("\n=== Flat (tapered) ranges ===")
    print(f"Spline:   min={fs_min:.6g} max={fs_max:.6g} std={fs_std:.6g}")
    print(f"Gaussian: min={fg_min:.6g} max={fg_max:.6g} std={fg_std:.6g}")

    # Simple heuristics to flag potential issues
    def _flag(label: str, a_std: float, b_std: float, a_range: float, b_range: float):
        ratio_std = (max(a_std, b_std) / max(min(a_std, b_std), 1e-12)) if np.isfinite(a_std) and np.isfinite(b_std) else np.nan
        ratio_rng = (max(a_range, b_range) / max(min(a_range, b_range), 1e-12)) if np.isfinite(a_range) and np.isfinite(b_range) else np.nan
        if ratio_std > 2.0 or ratio_rng > 2.0:
            print(f"[!] {label} mismatch: std ratio ~ {ratio_std:.3g}, range ratio ~ {ratio_rng:.3g}")

    _flag(
        "Flux",
        s_std,
        g_std,
        (s_max - s_min),
        (g_max - g_min),
    )
    _flag(
        "Flat",
        fs_std,
        fg_std,
        (fs_max - fs_min),
        (fg_max - fg_min),
    )

    # Plot comparison
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)
    ax = axes[0, 0]
    ax.plot(log_wave, flux_spline, lw=1.0, label="Flux (spline)")
    ax.plot(log_wave, flux_gauss, lw=1.0, label="Flux (gaussian)")
    ax.set_title("Display Flux (reconstructed)")
    ax.set_ylabel("Flux")
    ax.legend()

    ax = axes[0, 1]
    ax.plot(log_wave, flat_spline, lw=1.0, label="Flat (spline)")
    ax.plot(log_wave, flat_gauss, lw=1.0, label="Flat (gaussian)")
    ax.axhline(0.0, color="#888", lw=0.8)
    ax.set_title("Flattened (apodized)")
    ax.legend()

    ax = axes[1, 0]
    ax.plot(log_wave, cont_spline, lw=1.0, label="Continuum (spline)")
    ax.plot(log_wave, cont_gauss, lw=1.0, label="Continuum (gaussian)")
    ax.set_title("Continuum")
    ax.set_xlabel("log-λ grid index")
    ax.legend()

    ax = axes[1, 1]
    # Differences over valid flux mask
    diff_flux = flux_gauss - flux_spline
    diff_flat = flat_gauss - flat_spline
    ax.plot(log_wave, diff_flux, lw=1.0, label="Flux (gauss - spline)")
    ax.plot(log_wave, diff_flat, lw=1.0, label="Flat (gauss - spline)")
    ax.set_title("Differences")
    ax.set_xlabel("log-λ grid index")
    ax.legend()

    fig.suptitle(name)
    fig.tight_layout()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}_compare_continuum.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)

    print(f"Saved comparison plot to: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Compare spline vs gaussian continuum for flat and flux views.")
    parser.add_argument("spectrum", type=Path, help="Path to input spectrum (e.g., ggi.dat)")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/compare_continuum"),
        help="Output directory for plots",
    )
    parser.add_argument(
        "--apodize",
        type=float,
        default=10.0,
        help="Apodization percent applied to flattened spectrum (default: 10)",
    )
    args = parser.parse_args()

    run_one(args.spectrum, args.out, apodize_percent=args.apodize)


if __name__ == "__main__":
    main()


