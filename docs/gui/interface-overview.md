# GUI Interface Overview (PySide6/Qt)

The SNID SAGE graphical interface is built with PySide6/Qt and `pyqtgraph`, providing an intuitive, high-performance environment for supernova spectrum analysis. This guide covers all interface components and workflows.

## Main Window Layout

The interface is organized into distinct regions for efficient workflow:

### Interface Regions
1. **Header Panel** - Logo, status indicators, and theme controls
2. **Control Panel** - Analysis parameters and workflow buttons
3. **Spectrum Display** - Interactive plotting area with modern styling
4. **Status Bar** - Progress indicators and system information

## Workflow Buttons

Order of operations:
1) Load Spectrum → 2) Preprocessing → 3) SNID Analysis → 4) Optional tools (redshift mode, overlays, summaries) → 5) AI Assistant (optional)

Always available:
- Load Spectrum, Reset, Settings

After loading: Preprocessing

After preprocessing: SNID Analysis and Redshift (manual or range search)

After analysis: Results dialogs, overlays, clustering, AI Assistant

## Control Panel (key items)

Most options are set here. For a compact list of parameters and defaults, see the [Parameters Reference](../reference/parameters.md).

- Input: file path, redshift (manual or auto), wavelength range
- Preprocessing: smoothing (window/order), telluric A-band, skyline clipping, custom masks
- Templates: type filters, age range, minimum correlation, wavelength overlap

## Spectrum Display

- Pan: drag; Zoom: wheel or box; Reset: double-click
- Toggle view: flux vs flattened; show/hide grid and legend
- Overlays: template matches, masks, line IDs, optional errors

## Results

- Status area: type, best template, confidence, redshift, age
- Dialogs: cluster summary, subtype proportions, redshift–age
- Export: save figures and data from dialogs

## AI Assistant

- Quick Summary, Detailed Analysis, Scientific Context, Publication text
- Configure API key and model in Settings → AI

## Keyboard Shortcuts

- Ctrl+O load; Ctrl+S save; Ctrl+Q quit
- Ctrl+Enter quick preprocess + analysis; F5 run analysis; F6 preprocessing
- Esc cancel; Space toggle view; Tab/Enter navigate

## Theme

Light and dark themes; toggle in header.

## Notes

GUI: PySide6 (Qt). Plotting: pyqtgraph.

## Tips

- Follow the button order; check S/N and wavelength range first
- Use type filters for speed; close unused dialogs
- Review multiple top matches before finalizing

## Troubleshooting

- Buttons disabled: ensure prior step done (load → preprocess → analyze)
- Plot not updating: toggle view or refresh; check status messages
- Slow: reduce template set; close apps; check memory
- AI not working: set API key; ensure analysis completed

See [Troubleshooting](../reference/troubleshooting.md).

## Next Steps

- ??? tip "Common parameters"
    Frequent controls and defaults are summarized in the [Parameters Reference](../reference/parameters.md). Use this as a quick cheat sheet while exploring the GUI.

- [Quick Start Tutorial](../quickstart/first-analysis.md) - Your first analysis
- [Advanced Analysis](../tutorials/advanced-analysis.md) - Deep dive into tools
- [CLI Reference](../cli/command-reference.md) - Command-line alternative 