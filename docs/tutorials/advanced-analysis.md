# Advanced Analysis Techniques

Practical ways to go beyond a basic run while staying within supported features.

## Template selection

- Filter by type and age to focus and speed up matching
- Example (CLI):
```bash
snid identify spectrum.dat --output-dir results/ \
  --type-filter Ia Ib \
  --age-min -5 --age-max 30
```

## Redshift strategies

- Known host redshift: use a fixed value
```powershell
snid identify spectrum.dat --output-dir results/ --forced-redshift 0.045
```
- Unknown redshift: narrow search range when possible
```powershell
snid identify spectrum.dat --output-dir results/ --zmin 0.0 --zmax 0.1
```

## Preprocessing tuning

- Apply modest smoothing on noisy data; prefer specific wavelength masks over broad ranges
```bash
snid identify spectrum.dat --output-dir results/ \
  --savgol-window 11 --savgol-order 3 \
  --aband-remove --skyclip \
  --wavelength-masks 6550:6600 7600:7700
```

## Reviewing clusters and matches (GUI)

- Use the Results dialogs to inspect cluster summaries and top matches
- Compare overlays and confidence before finalizing

## Plots and exports

- Use Complete mode for publication-ready figures
```powershell
snid identify spectrum.dat --output-dir results/ --complete
```
- Export PNG for quick sharing; PDF/SVG for publications

## Performance notes

- Restrict templates (types/ages) to cut runtime and memory
- Start with `--minimal` for surveys; rerun interesting cases with `--complete`

## Common pitfalls

- Over-smoothing low S/N spectra
- Using too narrow a wavelength overlap
- Ignoring alternative matches and confidence

See also:
- GUI → Results and Plots
- Data → Supported Formats; Data Preparation (Essentials)