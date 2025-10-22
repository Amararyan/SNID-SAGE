"""
Template Service (HDF5-only)
============================

Centralized service for HDF5-only template storage and index management.

Responsibilities:
- Manage a user-writable template library in the user's config directory
  (e.g., `<config_dir>/templates/User_templates/`)
- Append templates to per-type HDF5 files (rebinned to the standard grid)
- Maintain a user index (`template_index.user.json`) and merge with built-in index
- Provide a small API for the GUI (creator, browser, manager)

Notes:
- Legacy .lnw support is intentionally removed. All new templates are written
  directly to HDF5 and indexed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import json
import threading
from importlib import resources
import os

import numpy as np
import h5py


def _compute_builtin_dir() -> Path:
    """Resolve the packaged templates directory robustly (installed or dev)."""
    # Prefer importlib.resources traversal of the installed package
    try:
        with resources.as_file(resources.files('snid_sage') / 'templates') as tpl_dir:
            if tpl_dir.exists():
                return tpl_dir
    except Exception:
        pass
    # Fallback: use the repo-relative path for editable installs
    try:
        return Path(__file__).resolve().parents[3] / "templates"
    except Exception:
        return Path("snid_sage/templates").resolve()


_BUILTIN_DIR = _compute_builtin_dir()
from snid_sage.shared.utils.paths.user_templates import get_user_templates_dir

def _user_index_path() -> Optional[Path]:
    p = get_user_templates_dir(strict=True)
    return (p / "template_index.user.json") if p else None

_USER_INDEX = _user_index_path()
_BUILTIN_INDEX = _BUILTIN_DIR / "template_index.json"


@dataclass
class StandardGrid:
    num_points: int = 1024
    min_wave: float = 2500.0
    max_wave: float = 10000.0

    @property
    def dlog(self) -> float:
        return float(np.log(self.max_wave / self.min_wave) / self.num_points)

    def wavelength(self) -> np.ndarray:
        # Same construction used by TemplateFFTStorage
        idx = np.arange(self.num_points) + 0.5
        return self.min_wave * np.exp(idx * self.dlog)


class TemplateService:
    """
    HDF5-only template service.

    Thread-safe for write operations via an internal lock.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        try:
            p = get_user_templates_dir(strict=True)
            if p is not None:
                p.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        # Lazy cache
        self._standard_grid = StandardGrid()
        self._standard_wave = self._standard_grid.wavelength()

    # ---- Public API ----
    def get_merged_index(self) -> Dict[str, Any]:
        """Return the merged built-in + user index for the GUI browser."""
        builtin = self._read_json(_BUILTIN_INDEX) or {
            "templates": {},
            "by_type": {},
            "template_count": 0,
        }
        idx_path = _user_index_path()
        user = self._read_json(idx_path) or {
            "templates": {},
            "by_type": {},
            "template_count": 0,
        }

        merged_templates: Dict[str, Any] = {}
        merged_templates.update(builtin.get("templates", {}))
        merged_templates.update(user.get("templates", {}))

        # Recompute by_type from merged templates
        by_type: Dict[str, Any] = {}
        for name, meta in merged_templates.items():
            ttype = meta.get("type", "Unknown")
            bucket = by_type.setdefault(ttype, {"count": 0, "storage_file": meta.get("storage_file", ""), "template_names": []})
            bucket["count"] += 1
            bucket["template_names"].append(name)
            # Prefer an existing storage_file reference; do not overwrite with empty
            if not bucket.get("storage_file") and meta.get("storage_file"):
                bucket["storage_file"] = meta["storage_file"]

        return {
            "version": user.get("version") or builtin.get("version") or "2.0",
            "template_count": len(merged_templates),
            "templates": merged_templates,
            "by_type": by_type,
        }

    def get_user_templates_dir(self) -> Optional[str]:
        """Return absolute path to the active user templates directory or None if unset."""
        p = get_user_templates_dir(strict=True)
        return str(p) if p else None

    def get_builtin_index(self) -> Dict[str, Any]:
        """Return only the built-in index (no user templates)."""
        data = self._read_json(_BUILTIN_INDEX) or {
            "version": "2.0",
            "template_count": 0,
            "templates": {},
            "by_type": {},
        }
        # Ensure counts if missing
        if "by_type" not in data or not isinstance(data.get("by_type"), dict):
            data["by_type"] = {}
        if "templates" not in data or not isinstance(data.get("templates"), dict):
            data["templates"] = {}
        if not data.get("template_count"):
            data["template_count"] = len(data.get("templates", {}))
        return data

    def get_user_index(self) -> Dict[str, Any]:
        """Return only the user index (no built-in templates)."""
        idx_path = _user_index_path()
        data = self._read_json(idx_path) or {
            "version": "2.0",
            "template_count": 0,
            "templates": {},
            "by_type": {},
        }
        if "by_type" not in data or not isinstance(data.get("by_type"), dict):
            data["by_type"] = {}
        if "templates" not in data or not isinstance(data.get("templates"), dict):
            data["templates"] = {}
        if not data.get("template_count"):
            data["template_count"] = len(data.get("templates", {}))
        return data

    def has_user_templates(self) -> bool:
        """Return True if any user templates exist."""
        idx_path = _user_index_path()
        data = self._read_json(idx_path) or {}
        templates = (data.get("templates") or {})
        return bool(templates)

    def add_template_from_arrays(
        self,
        *,
        name: str,
        ttype: str,
        subtype: str,
        age: float,
        redshift: float,
        wave: np.ndarray,
        flux: np.ndarray,
        combine_only: bool = False,
    ) -> bool:
        """
        Append a template to the per-type user HDF5 and update the user index.
        Data are rebinned to the standard grid and FFT is precomputed.
        """
        if not isinstance(wave, np.ndarray) or not isinstance(flux, np.ndarray):
            return False
        if wave.size == 0 or flux.size == 0:
            return False
        try:
            with self._lock:
                h5_abs_path = self._ensure_user_h5_for_type(ttype)

                # Rebin to the standard grid
                rebinned_flux = self._rebin_to_standard_grid(wave, flux)
                fft = np.fft.fft(rebinned_flux)

                # Write (append/combine or create) to HDF5
                final_name, combined, epochs_count, status = self._append_to_h5(
                    h5_abs_path,
                    name,
                    ttype,
                    subtype,
                    age,
                    redshift,
                    rebinned_flux,
                    fft,
                    allow_suffix=(not combine_only),
                )
                if combine_only and not combined:
                    # Do not create a suffixed template when explicitly adding to existing
                    return False

                # Update user index (omit non-essential fields like phase/age/rebinned)
                idx_path = _user_index_path()
                index = self._read_json(idx_path) or {
                    "version": "2.0",
                    "templates": {},
                    "by_type": {},
                    "template_count": 0,
                }
                index_templates = index.setdefault("templates", {})
                if combined and final_name in index_templates:
                    # Update epochs count; preserve existing metadata, enforce storage_file
                    entry = index_templates[final_name]
                    entry["epochs"] = int(epochs_count)
                    entry["storage_file"] = str(h5_abs_path).replace("\\", "/")
                else:
                    index_templates[final_name] = {
                        "type": ttype,
                        "subtype": subtype,
                        "redshift": float(redshift),
                        "epochs": 1 if not combined else int(epochs_count),
                        "storage_file": str(h5_abs_path).replace("\\", "/"),
                    }

                # Recompute by_type summary
                index["by_type"] = self._compute_by_type(index_templates)
                index["template_count"] = len(index_templates)

                if idx_path is not None:
                    self._write_json_atomic(idx_path, index)
            return True
        except Exception:
            return False

    def update_metadata(self, name: str, changes: Dict[str, Any]) -> bool:
        """Update metadata attributes for a user template and its index entry."""
        try:
            with self._lock:
                idx_path = _user_index_path()
                index = self._read_json(idx_path) or {}
                tmpl = (index.get("templates") or {}).get(name)
                if not tmpl:
                    return False  # only user templates can be edited
                storage_abs = Path(tmpl.get("storage_file", ""))
                if not storage_abs:
                    return False
                if not storage_abs.exists():
                    return False
                # Update HDF5 attrs
                with h5py.File(storage_abs, "a") as f:
                    g = f["templates"].get(name)
                    if g is None:
                        return False
                    for k, v in changes.items():
                        if k in {"type", "subtype"} and isinstance(v, str):
                            g.attrs[k] = v
                        elif k in {"age", "redshift"}:
                            try:
                                g.attrs[k] = float(v)
                            except Exception:
                                pass
                # Update index entry (omit phase/age which are HDF5-only)
                for k in ["type", "subtype", "redshift"]:
                    if k in changes:
                        tmpl[k] = changes[k]
                # Write back
                index["by_type"] = self._compute_by_type(index.get("templates", {}))
                if idx_path is not None:
                    self._write_json_atomic(idx_path, index)
            return True
        except Exception:
            return False

    def delete(self, name: str) -> bool:
        """Delete a user template group and its index entry."""
        try:
            with self._lock:
                idx_path = _user_index_path()
                index = self._read_json(idx_path) or {}
                templates = index.get("templates") or {}
                meta = templates.get(name)
                # If missing in index, try to find and delete from any user H5
                storage_abs = None
                if meta:
                    storage_abs = Path(meta.get("storage_file", "")).resolve()
                else:
                    user_dir = get_user_templates_dir(strict=True)
                    if not user_dir:
                        return False
                    for h5_path in (user_dir.glob("templates_*.user.hdf5")):
                        try:
                            with h5py.File(h5_path, "r") as f:
                                if "templates" in f and name in f["templates"]:
                                    storage_abs = h5_path.resolve()
                                    break
                        except Exception:
                            continue
                    if storage_abs is None:
                        return False
                if not storage_abs.exists():
                    return False
                with h5py.File(storage_abs, "a") as f:
                    tgroup = f["templates"]
                    if name in tgroup:
                        del tgroup[name]
                        try:
                            m = f["metadata"]
                            m.attrs["template_count"] = max(0, int(m.attrs.get("template_count", 1)) - 1)
                        except Exception:
                            pass
                    # After deletion, if no templates remain, close file and delete it
                    try:
                        remaining = len(f["templates"].keys())
                    except Exception:
                        remaining = 0
                # Remove from index
                if meta:
                    templates.pop(name, None)
                    index["by_type"] = self._compute_by_type(templates)
                    index["template_count"] = len(templates)
                    if idx_path is not None:
                        self._write_json_atomic(idx_path, index)
                # Delete empty H5 file and rebuild index if needed
                if storage_abs.exists():
                    try:
                        with h5py.File(storage_abs, "r") as fchk:
                            empty_now = ("templates" in fchk and len(fchk["templates"].keys()) == 0)
                    except Exception:
                        empty_now = False
                    if empty_now:
                        try:
                            storage_abs.unlink()
                        except Exception:
                            pass
                        # Rebuild user index to drop references to deleted file
                        try:
                            self.rebuild_user_index()
                        except Exception:
                            pass
            return True
        except Exception:
            return False

    def cleanup_unused(self, delete_empty_files: bool = True) -> Dict[str, int]:
        """Remove H5 template groups not referenced in the user index.

        Returns a summary: {"removed_groups": int, "deleted_files": int}
        """
        summary = {"removed_groups": 0, "deleted_files": 0}
        try:
            with self._lock:
                idx_path = _user_index_path()
                index = self._read_json(idx_path) or {"templates": {}}
                referenced = set((index.get("templates") or {}).keys())
                user_dir = get_user_templates_dir(strict=True)
                if not user_dir:
                    return summary
                for h5_path in (user_dir.glob("templates_*.user.hdf5")):
                    removed_here = 0
                    try:
                        with h5py.File(h5_path, "a") as f:
                            if "templates" not in f:
                                continue
                            tgroup = f["templates"]
                            # Collect unreferenced groups
                            names = list(tgroup.keys())
                            for nm in names:
                                if nm not in referenced:
                                    del tgroup[nm]
                                    removed_here += 1
                            if removed_here:
                                try:
                                    m = f["metadata"]
                                    m.attrs["template_count"] = max(0, int(m.attrs.get("template_count", 0)) - removed_here)
                                except Exception:
                                    pass
                    except Exception:
                        continue
                    summary["removed_groups"] += removed_here
                    # Optionally delete file if empty
                    if delete_empty_files and h5_path.exists():
                        try:
                            with h5py.File(h5_path, "r") as fchk:
                                is_empty = ("templates" in fchk and len(fchk["templates"].keys()) == 0)
                        except Exception:
                            is_empty = False
                        if is_empty:
                            try:
                                h5_path.unlink()
                                summary["deleted_files"] += 1
                            except Exception:
                                pass
                # Rebuild index to reflect cleanup
                self.rebuild_user_index()
        except Exception:
            return summary
        return summary

    # Cleanup helpers were removed after one-time migration

    def rename(self, old_name: str, new_name: str) -> bool:
        """Renaming/duplication is disabled for built-in or user templates by policy."""
        return False

    def duplicate(self, name: str, new_name: str) -> bool:
        """Duplication is disabled by policy."""
        return False

    def rebuild_user_index(self) -> bool:
        """Re-scan user HDF5 files and rebuild the user index from scratch."""
        try:
            templates: Dict[str, Any] = {}
            user_dir = get_user_templates_dir(strict=True)
            if not user_dir:
                return False
            for h5_path in (user_dir.glob("templates_*.user.hdf5")):
                with h5py.File(h5_path, "r") as f:
                    if "templates" not in f:
                        continue
                    tg = f["templates"]
                    for name in tg.keys():
                        g = tg[name]
                        attrs = dict(g.attrs)
                        templates[name] = {
                            "type": attrs.get("type", "Unknown"),
                            "subtype": attrs.get("subtype", "Unknown"),
                            "redshift": float(attrs.get("redshift", 0.0)),
                            "epochs": int(attrs.get("epochs", 1)),
                            "storage_file": str(h5_path).replace("\\", "/"),
                        }
            index = {
                "version": "2.0",
                "templates": templates,
                "by_type": self._compute_by_type(templates),
                "template_count": len(templates),
            }
            with self._lock:
                idx_path = _user_index_path()
                if idx_path is None:
                    return False
                self._write_json_atomic(idx_path, index)
            return True
        except Exception:
            return False

    # ---- Internals ----
    def _rebin_to_standard_grid(self, wave: np.ndarray, flux: np.ndarray) -> np.ndarray:
        """Rebin flux onto the standard logarithmic grid by interpolation in log space."""
        # Guard inputs
        wave = np.asarray(wave, dtype=float)
        flux = np.asarray(flux, dtype=float)
        # Enforce strictly positive wavelengths
        mask = np.isfinite(wave) & np.isfinite(flux) & (wave > 0)
        wave, flux = wave[mask], flux[mask]
        if wave.size < 2:
            # Not enough data to interpolate; pad with median
            out = np.full(self._standard_wave.shape, np.median(flux) if flux.size else 0.0, dtype=float)
            return out
        # Interpolate flux in log-lambda domain
        logw = np.log(wave)
        target_logw = np.log(self._standard_wave)
        # Use linear interpolation in log space; out-of-bounds filled with nearest value
        rebinned = np.interp(target_logw, logw, flux, left=float(flux[0]), right=float(flux[-1]))
        # Normalize by median to emulate flattened spectra expectation
        med = float(np.median(rebinned)) if rebinned.size else 1.0
        if med != 0.0 and np.isfinite(med):
            rebinned = rebinned / med
        return rebinned.astype(float, copy=False)

    def _ensure_user_h5_for_type(self, ttype: str) -> Path:
        """Ensure the per-type user HDF5 exists; return absolute path in user config dir."""
        safe_type = ttype.replace("/", "_").replace("-", "_").replace(" ", "_")
        user_dir = get_user_templates_dir(strict=True)
        if user_dir is None:
            raise RuntimeError("User templates directory is not set. Please configure it in the GUI settings.")
        abs_path = user_dir / f"templates_{safe_type}.user.hdf5"
        if not abs_path.exists():
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            with h5py.File(abs_path, "w") as f:
                meta = f.create_group("metadata")
                grid = self._standard_grid
                meta.attrs["version"] = "2.0"
                meta.attrs["created_date"] = float(np.floor(np.datetime64("now").astype("datetime64[s]").astype(int)))
                meta.attrs["template_count"] = 0
                meta.attrs["supernova_type"] = ttype
                meta.attrs["grid_rebinned"] = True
                meta.attrs["NW"] = grid.num_points
                meta.attrs["W0"] = grid.min_wave
                meta.attrs["W1"] = grid.max_wave
                meta.attrs["DWLOG"] = grid.dlog
                meta.create_dataset("standard_wavelength", data=self._standard_wave)
                f.create_group("templates")
        return abs_path

    def _append_to_h5(
        self,
        h5_path: Path,
        name: str,
        ttype: str,
        subtype: str,
        age: float,
        redshift: float,
        flux: np.ndarray,
        fft: np.ndarray,
        allow_suffix: bool = True,
    ) -> tuple[str, bool, int, str]:
        """Append or combine into an existing template group if same name and redshift.

        Returns (final_name, combined, epochs_count)
        """
        with h5py.File(h5_path, "a") as f:
            templates_group = f["templates"]
            # Combine if same name exists and redshift matches
            if name in templates_group:
                g = templates_group[name]
                try:
                    existing_z = float(g.attrs.get("redshift", float("nan")))
                except Exception:
                    existing_z = float("nan")
                if np.isfinite(existing_z) and abs(existing_z - float(redshift)) < 1e-6:
                    # Multi-epoch combine (only if no duplicate epoch age)
                    # Check duplicate ages (tolerance)
                    age_tol = 1e-3
                    duplicate_age = False
                    existing_ages: list[float] = []
                    try:
                        if "epochs" in g:
                            for ek in g["epochs"].keys():
                                try:
                                    existing_ages.append(float(g["epochs"][ek].attrs.get("age", float("nan"))))
                                except Exception:
                                    continue
                        else:
                            existing_ages.append(float(g.attrs.get("age", float("nan"))))
                    except Exception:
                        existing_ages = []
                    try:
                        for ea in existing_ages:
                            if np.isfinite(ea) and abs(ea - float(age)) < age_tol:
                                duplicate_age = True
                                break
                    except Exception:
                        duplicate_age = False
                    if not duplicate_age:
                        # Ensure epochs group exists, move current data if needed
                        if "epochs" not in g:
                            eg = g.create_group("epochs")
                            eg0 = eg.create_group("epoch_0")
                            eg0.create_dataset("flux", data=g["flux"][:])
                            eg0.create_dataset("fft_real", data=g["fft_real"][:])
                            eg0.create_dataset("fft_imag", data=g["fft_imag"][:])
                            eg0.attrs["age"] = float(g.attrs.get("age", 0.0))
                            eg0.attrs["rebinned"] = True
                        # Append new epoch
                        eg = g["epochs"]
                        new_epoch_idx = len(list(eg.keys()))
                        egn = eg.create_group(f"epoch_{new_epoch_idx}")
                        egn.create_dataset("flux", data=flux)
                        egn.create_dataset("fft_real", data=np.asarray(fft.real))
                        egn.create_dataset("fft_imag", data=np.asarray(fft.imag))
                        egn.attrs["age"] = float(age)
                        egn.attrs["rebinned"] = True
                        # Update epochs count and latest age
                        g.attrs["epochs"] = new_epoch_idx + 1
                        g.attrs["age"] = float(age)
                        # Keep top-level flux/fft as last epoch for compatibility
                        try:
                            del g["flux"]
                            del g["fft_real"]
                            del g["fft_imag"]
                        except Exception:
                            pass
                        g.create_dataset("flux", data=flux)
                        g.create_dataset("fft_real", data=np.asarray(fft.real))
                        g.create_dataset("fft_imag", data=np.asarray(fft.imag))
                    return name, True, int(g.attrs.get("epochs", 1)), "combined"
                    # else: fall through to create a suffixed new template name
                else:
                    # z mismatch
                    if not allow_suffix:
                        return name, False, 0, "z_mismatch"
            # Otherwise, create new (handle name collision by suffixing)
            final_name = name
            suffix = 1
            while final_name in templates_group:
                if not allow_suffix:
                    return name, False, 0, "name_taken"
                final_name = f"{name}_{suffix}"
                suffix += 1
            g = templates_group.create_group(final_name)
            g.create_dataset("flux", data=flux)
            g.create_dataset("fft_real", data=np.asarray(fft.real))
            g.create_dataset("fft_imag", data=np.asarray(fft.imag))
            g.attrs["type"] = ttype
            g.attrs["subtype"] = subtype
            g.attrs["age"] = float(age)
            g.attrs["redshift"] = float(redshift)
            g.attrs["epochs"] = 1
            g.attrs["rebinned"] = True
            # bump count
            meta = f["metadata"]
            try:
                meta.attrs["template_count"] = int(meta.attrs.get("template_count", 0)) + 1
            except Exception:
                meta.attrs["template_count"] = 1
            return final_name, False, 1, "created"

    def _compute_by_type(self, templates: Dict[str, Any]) -> Dict[str, Any]:
        by_type: Dict[str, Any] = {}
        for name, meta in templates.items():
            ttype = meta.get("type", "Unknown")
            bucket = by_type.setdefault(ttype, {"count": 0, "storage_file": meta.get("storage_file", ""), "template_names": []})
            bucket["count"] += 1
            bucket["template_names"].append(name)
            if not bucket.get("storage_file") and meta.get("storage_file"):
                bucket["storage_file"] = meta["storage_file"]
        return by_type

    @staticmethod
    def _read_json(path: Path) -> Optional[Dict[str, Any]]:
        try:
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            return None
        return None

    @staticmethod
    def _write_json_atomic(path: Path, data: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp.replace(path)


# Global singleton
_template_service: Optional[TemplateService] = None


def get_template_service() -> TemplateService:
    global _template_service
    if _template_service is None:
        _template_service = TemplateService()
    return _template_service


