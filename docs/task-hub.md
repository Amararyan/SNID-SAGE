## Task Hub

Quick links to common workflows with one-liners and deep links.

### Analyze spectra
- Single file (GUI): Open SNID SAGE → Load Spectrum → Preprocess → Analyze
- Single file (CLI):
  ```powershell
  sage data\sn2003jo.dat --output-dir results\
  ```
- Directory (CLI):
  ```powershell
  sage batch "data/*.dat" templates/ --output-dir results/
  ```
- Supported formats: FITS (.fits, .fit), ASCII (.dat, .txt, .csv, .flm)
See: Supported Formats → `reference/supported-formats.md`

### Use a known redshift
```powershell
sage spectrum.dat --output-dir results/ --forced-redshift 0.045
```

### Improve a noisy spectrum
```powershell
sage spectrum.dat --output-dir results/ --savgol-window 15 --savgol-order 3
```
See: Preprocessing → `gui/preprocessing.md`

### Filter templates by type and age
```powershell
sage spectrum.dat --output-dir results/ --type-filter Ia --age-min -5 --age-max 25
```
See: Parameters → `reference/parameters.md`

### Generate all plots (publication-ready)
```powershell
sage spectrum.dat --output-dir pub\ --complete
```
See: Results & Plots → `gui/results-and-plots.md`

### Configure defaults (paths, analysis)
```powershell
sage config show
sage config set paths.templates_dir C:\data\snid_templates
```
See: Settings & Configuration → `gui/settings-configuration.md`

### Manage templates (GUI)
- Open Templates Manager → browse, create, compare
See: `gui/templates-manager.md`

### Manage spectral lines (GUI)
- Open Lines Manager → add/edit lines and presets → overlay on a test spectrum
See: `gui/lines-manager.md`

### Enable AI and get a summary
1. Settings → AI → set API key
2. Run analysis → AI Assistant → Quick Summary
See: `gui/ai-assistant.md`

