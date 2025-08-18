## Preprocessing (GUI)

How to prepare spectra before analysis.

### Quick SNID Preprocessing
- Purpose: Minimal steps to prepare a spectrum for SNID.
- Actions: log rebinning, optional smoothing, apodization, continuum handling.
- When to use: Most cases; fastest path to classification.

### Manual Preprocessing
- Open via: Preprocessing → Manual wizard
- Steps (subset; tooltips in dialog):

1. Input and range
   - Wavelength range (`wmin`, `wmax`): leave blank for auto
2. Smoothing
   - Savitzky–Golay window (`savgol_window`): 0 disables; typical 11–21
   - Savitzky–Golay order (`savgol_order`): default 3
3. Telluric and sky features
   - Remove A-band (`aband_remove`): masks ~7600–7650 Å
   - Sky line clipping (`skyclip`)
   - Emission line clipping redshift (`emclip_z`): -1 disables
   - Emission width (`emwidth`, Å)
4. Apodization
   - Apodize percent (`apodize_percent`): typical 5–15%
5. Masks
   - Custom wavelength masks: e.g. 6550:6600 7600:7700

### Best practices
- Inspect S/N before aggressive smoothing
- Prefer specific masks over broad ranges
- Keep `apodize_percent` modest to preserve edges

### CLI parity
GUI options map to `sage` flags:

```bash
sage spectrum.dat --output-dir results/ \
  --savgol-window 11 --savgol-order 3 \
  --aband-remove --skyclip \
  --emclip-z 0.02 --emwidth 40 \
  --wavelength-masks 6550:6600 7600:7700
```

