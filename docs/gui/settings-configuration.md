## Settings (GUI)

Centralized settings used by GUI and CLI. Saved in the user config.

### Paths
- Templates Directory (`paths.templates_dir`)
- Output Directory (`paths.output_dir`)
- Data Directory (`paths.data_dir`)

### Analysis
- Redshift/age bounds; thresholds (rlapmin, lapmin, fraction_coverage)
- Output limits; emission clipping (emclip_z, emwidth)

### Processing
- Flattening/smoothing/median filters; A-band removal; skyline clipping; apodization

### Display
- Theme (light/dark), plot style, DPI, grid/markers

### LLM
- Enable, provider, model, API key, tokens, temperature

### Profiles
- Save, load, and delete named profiles

### CLI parity
Use `snid config` to show/set/get the same settings:

```powershell
snid config show
snid config set paths.templates_dir C:\data\snid_templates
snid config get analysis.rlapmin
```

