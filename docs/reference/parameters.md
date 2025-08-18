## Parameters Reference

Unified reference of configurable parameters across GUI and CLI.

### Analysis
- redshift_min, redshift_max: redshift search bounds
- rlapmin: correlation threshold
- lapmin: overlap fraction threshold
- age_min, age_max: template phase bounds (days)
- max_output_templates: max templates saved per run
- wavelength_tolerance: matching tolerance (Å)
- emclip_z: emission clipping redshift (-1 disables)
- emwidth: emission clipping width (Å)

### Processing
- savgol_window: Savitzky–Golay window (pixels; 0 disables)
- savgol_order: polynomial order
- median_fwmed: weighted median filter FWHM (Å)
- medlen: fixed median filter length (px)
- apodize_percent: FFT taper percentage
- aband_remove: remove telluric A-band
- skyclip: clip sky lines
- wavelength_masks: list of ranges (WMIN:WMAX)

### Templates
- type_filter: allowed SN types (Ia, Ib, Ic, II, …)
- template_filter: allowed template names
- exclude_templates: names to exclude

### Display
- theme: light/dark
- plot_style: matplotlib style
- plot_dpi: saved figure DPI
- show_grid, show_markers: booleans

### LLM
- enable_llm, llm_provider, model_name, api_key
- max_tokens, temperature

### Paths
- templates_dir, output_dir, data_dir, config_dir

### CLI mappings (identify)
```bash
sage spectrum.dat --output-dir results/ \
  --zmin 0.0 --zmax 0.1 \
  --rlapmin 5.0 --lapmin 0.3 \
  --age-min -5 --age-max 30 \
  --savgol-window 11 --savgol-order 3 \
  --aband-remove --skyclip \
  --wavelength-masks 6550:6600 7600:7700 \
  --type-filter Ia Ib Ic
```

