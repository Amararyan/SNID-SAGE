## Redshift and Age in SNID SAGE (GUI)

This guide explains redshift handling and age estimation in the GUI, including the Redshift Mode dialog.

### Redshift selection workflow
1. Preprocess spectrum
2. Choose redshift:
   - Manual entry (known host z)
   - Automatic determination (default)
3. Confirm in Redshift Mode dialog

### Redshift Mode dialog
Appears after manual redshift selection:
- Force Exact Redshift: fixes z during matching (faster, precise)
- Search Around Redshift: scans ±Δz around selected z
  - Adjustable range (e.g., ±0.0005)
  - Shows computed interval [zmin, zmax]

### Best practices
- Use force mode when host z is well measured
- Use search mode when z is approximate or from spectrum
- For very low-z objects, consider narrower ±Δz to avoid aliasing

### Age estimation
- Based on best-matching templates in the winning cluster (GUI-style)
- Weighted by analysis quality metric (RLAP-CCC when available)
- Typical validity range: -20 to +100 days

### CLI parity
Map GUI choices to CLI flags:

```powershell
# Force exact redshift
snid spectrum.dat --output-dir results/ --forced-redshift 0.045

# Search in range
snid spectrum.dat --output-dir results/ --zmin 0.04 --zmax 0.05
```

