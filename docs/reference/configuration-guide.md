# Configuration Guide

This guide lists implemented configuration options and how to access them via GUI and CLI.

## Access

- GUI: Settings → Configuration
- CLI: `snid config show|get|set|reset`

## Categories (implemented)

- Analysis: redshift/age bounds, rlapmin, lapmin, wavelength tolerance, output limits
- Processing: smoothing, flattening, masks (A-band, skylines), apodization
- Display: theme, plot style/DPI, grid/markers
- Templates: paths.templates_dir
- LLM: enable, provider, model_name, api_key, max_tokens, temperature

## Examples

```powershell
snid config show
snid config set templates.default_dir C:\\data\\snid_templates
snid config get analysis.rlapmin; snid config set analysis.rlapmin 5.0
```

## Notes

- Settings are stored in a user config file; manual edits are rarely needed
- Unlisted categories are experimental or not available in this release

 