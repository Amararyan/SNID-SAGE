# CLI Command Reference

SNID SAGE provides a powerful command-line interface for automated spectrum analysis, batch processing, and scripting workflows.

## Quick Start

```bash
# Basic analysis
snid spectrum.dat --output-dir results/

# Basic analysis with explicit templates
snid identify spectrum.dat templates/ --output-dir results/

# Get help
snid --help

# Command-specific help
snid identify --help
```

!!! note "Windows PowerShell users"
    - Do not use `&&` to chain commands; use `;` between commands.
    - For multi-line commands, use the PowerShell backtick (`) as a line continuation.

```powershell
# Basic analysis (PowerShell)
snid spectrum.dat --output-dir results/

# Command-specific help
snid identify --help

# Multi-line example (use backticks)
snid identify data\sn2003jo.dat --output-dir results\ `
  --complete `
  --savgol-window 11 --savgol-order 3
```

## Command Structure

!!! tip "PowerShell basics"
    - Use `;` to chain commands (instead of `&&`).
    - Use the backtick (`` ` ``) for line continuation.

```bash
snid [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS] [ARGUMENTS]
```

### Global Options
- `--version` - Show version information

## Auto-Discovery

SNID SAGE automatically discovers the templates directory if not specified:

```bash
# Auto-discover templates directory
snid spectrum.dat --output-dir results/

# Explicit templates directory
snid spectrum.dat templates/ --output-dir results/
```

**Note**: Auto-discovery works when templates are installed in standard locations or configured in your SNID SAGE settings.

## identify - Spectrum Identification

Analyze a single spectrum against the template library with cluster-aware analysis and comprehensive outputs.

### Basic Usage
```bash
snid identify SPECTRUM_FILE [TEMPLATES_DIR] --output-dir OUTPUT_DIR [OPTIONS]
```

### Required Arguments
- `SPECTRUM_FILE` - Path to spectrum file (FITS, ASCII, etc.)
- `TEMPLATES_DIR` - Path to directory containing template spectra (optional)
- `--output-dir DIR` - Output directory for results (required)

### Processing Modes
```bash
--minimal               # Minimal mode: Main result file only, no additional outputs or plots
--complete              # Complete mode: All outputs including comprehensive GUI-style plots
# (default)             # Standard mode: Main outputs without comprehensive plots
```

### Core Options

#### Analysis Parameters
```bash
--zmin ZMIN             # Minimum redshift to consider (default: -0.01)
--zmax ZMAX             # Maximum redshift to consider (default: 1.0)
--forced-redshift Z     # Force analysis to this specific redshift (skips search)
--rlapmin RLAP          # Minimum rlap value required (default: 5.0)
--lapmin LAP            # Minimum overlap fraction required (default: 0.3)
```

#### Template Selection
```bash
--type-filter TYPES     # Only use templates of these types (Ia,Ib,Ic,II,etc.)
--template-filter NAMES # Only use specific templates (by name)
--age-min MIN           # Minimum template age in days
--age-max MAX           # Maximum template age in days
```

#### Preprocessing
```bash
--savgol-window SIZE    # Savitzky-Golay filter window size in pixels (0 = no filtering)
--savgol-order ORDER    # Savitzky-Golay filter polynomial order (default: 3)
--savgol-fwhm FWHM      # Savitzky-Golay filter FWHM in Angstroms (alternative to window)
--aband-remove          # Remove telluric A-band
--skyclip               # Clip sky emission lines
--emclip-z Z            # Redshift at which to clip emission lines (-1 to disable)
--emwidth WIDTH         # Width in Angstroms for emission line clipping (default: 40.0)
--apodize-percent PCT   # Percentage of spectrum ends to apodize (default: 10.0)
--wavelength-masks RANGES # Wavelength ranges to mask (format: 6550:6600 7600:7700)
```

### Examples

#### Basic Analysis
```bash
# Standard mode - main outputs without comprehensive plots
snid data/sn2003jo.dat --output-dir results/

# With explicit templates directory
snid identify data/sn2003jo.dat templates/ --output-dir results/

# Minimal mode - main result file only
snid data/sn2003jo.dat --output-dir results/ --minimal

# Complete mode - all outputs including comprehensive GUI-style plots
snid data/sn2003jo.dat --output-dir results/ --complete

# With verbose output
snid data/sn2003jo.dat --output-dir results/ --verbose
```

#### Custom Parameters
```bash
# Specific redshift range
snid data/sn2003jo.dat --output-dir results/ --zmin 0.0 --zmax 0.1

# Only Type Ia templates with age constraint
snid data/sn2003jo.dat --output-dir results/ \
    --type-filter Ia --age-min -5 --age-max 30

# Forced redshift analysis with complete outputs
snid data/sn2003jo.dat --output-dir results/ \
    --forced-redshift 0.045 --complete
```

#### Preprocessing Options
```bash
# Apply preprocessing with complete analysis
snid data/sn2003jo.dat --output-dir results/ --complete \
    --aband-remove --skyclip --savgol-window 11 \
    --wavelength-masks 6550:6600 7600:7700
```

## batch - Batch Processing

Process multiple spectra simultaneously with optimized workflows and comprehensive reporting.

### Basic Usage
```bash
snid batch INPUT_PATTERN TEMPLATES_DIR [OPTIONS]
```

### Required Arguments
- `INPUT_PATTERN` - Glob pattern for input spectrum files (e.g., "spectra/*", "*.dat")
- `TEMPLATES_DIR` - Path to directory containing template spectra

### Processing Modes
```bash
--minimal               # Minimal mode: main result files + summary report (flat directory)
--complete              # Complete mode: all outputs + GUI-style plots (organized subdirectories)
# Default mode          # Main outputs + summary (organized subdirectories)
```

### Analysis Parameters
```bash
--zmin ZMIN             # Minimum redshift to consider (default: -0.01)
--zmax ZMAX             # Maximum redshift to consider (default: 1.0)
--forced-redshift Z     # Force analysis to this specific redshift
--type-filter TYPES     # Only use templates of these types
--template-filter NAMES # Only use specific templates (by name)
```

### Processing Options
```bash
--output-dir DIR        # Output directory for all results (required)
--stop-on-error         # Stop processing if any spectrum fails
--verbose, -v           # Print detailed processing information
```

### Examples

#### Basic Batch Processing
```bash
# Minimal mode - main result files + summary report
snid batch "spectra/*" templates/ --output-dir results/ --minimal

# Complete mode - all outputs + GUI-style plots
snid batch "spectra/*" templates/ --output-dir results/ --complete

# Default mode - main outputs + summary
snid batch "spectra/*" templates/ --output-dir results/ --stop-on-error
```

#### Custom Redshift Analysis
```bash
# Custom redshift range
snid batch "data/*.dat" templates/ --zmin 0.0 --zmax 0.5 --output-dir results/

# Forced redshift analysis
snid batch "spectra/*.fits" templates/ --forced-redshift 0.1 --output-dir results/

# High-z search
snid batch "high_z/*.dat" templates/ --zmin 0.5 --zmax 2.0 --output-dir high_z_results/
```

#### Advanced Options
```bash
# Filtering with verbose output
snid batch "spectra/*" templates/ \
    --type-filter Ia Ib Ic --output-dir results/ --verbose

# Complete analysis with custom range
snid batch "data/*.dat" templates/ --complete \
    --zmin -0.01 --zmax 1.2 --stop-on-error \
    --output-dir full_analysis/
```

#### Output Structure
Each processed spectrum generates:
- **Minimal mode**: Only `batch_summary.txt` 
- **Default mode**: Individual `.output`, `.fluxed`, `.flattened` files + summary
- **Complete mode**: All files + plots (`snid_comparison.png`, `snid_3d_clustering.png`, etc.)

#### Plot Outputs (Complete Mode)
The `--complete` mode generates GUI-style plots:
- `snid_comparison.png` - Main spectrum comparison (winning cluster templates only)
- `snid_3d_clustering.png` - 3D type-specific GMM clustering visualization  
- `snid_subtype_analysis.png` - Subtype proportions from winning cluster
- `snid_clustering_statistics.png` - Detailed clustering statistics
- `snid_redshift_age.png` - Redshift vs age distribution



## template - Template Management

Manage the template library and create custom templates.

For detailed template management documentation, see **[Template Management](template-management.md)**.

## config - Configuration Management

Manage SNID SAGE configuration settings.

### Subcommands

#### show - Display Configuration
```bash
snid config show [SECTION]

# Examples
snid config show              # All settings
snid config show analysis     # Analysis section
snid config show templates    # Template settings
```

#### set - Set Configuration
```bash
snid config set KEY VALUE

# Examples
snid config set analysis.correlation_method fft
snid config set templates.default_dir /path/to/templates
snid config set ai.api_key your_key_here
```

#### get - Get Configuration
```bash
snid config get KEY

# Examples
snid config get analysis.redshift_range
snid config get templates.quality_min
```

#### reset - Reset Configuration
```bash
snid config reset [SECTION]

# Examples
snid config reset             # Reset all
snid config reset analysis   # Reset analysis section
```

## AI Analysis

AI-powered analysis is available through the GUI interface. The CLI currently does not have direct AI commands, but AI features can be accessed through the GUI after running analysis.

### Using AI Features

1. **Run analysis using CLI**:
```bash
snid identify spectrum.dat --output-dir results/
```

2. **Launch GUI for AI analysis**:
```bash
snid-sage
```

3. **In GUI**:
   - Load the analysis results
   - Click "AI Assistant" button
   - Choose analysis type and model
   - Get AI-powered insights

### Future CLI AI Features

Future releases may include CLI commands for:
- Direct AI analysis of results
- Batch AI processing
- Command-line chat interface

For now, please use the GUI for all AI features.

## Output Files

### Analysis Results

The identify command generates the following files:

#### Standard Mode
- `{spectrum_name}.output` - Main SNID output file with best matches
- `{spectrum_name}.fluxed` - Fluxed spectrum data
- `{spectrum_name}.flattened` - Flattened spectrum data

#### Complete Mode (additional files)
- `snid_comparison.png` - Spectrum comparison plot
- `snid_3d_clustering.png` - 3D clustering visualization
- `snid_subtype_analysis.png` - Subtype analysis plot
- `snid_clustering_statistics.png` - Clustering statistics
- `snid_redshift_age.png` - Redshift vs age plot
- `{spectrum_name}_correlation_*.dat` - Correlation data for top templates

### Batch Processing Results
- `batch_summary.txt` - Summary of all processed spectra
- Individual spectrum results in subdirectories (default/complete mode)
- Individual spectrum results in flat structure (minimal mode)

## Advanced Usage

### Pipeline Commands
```powershell
# Complete analysis pipeline (PowerShell)
snid identify spectrum.dat --output-dir results/ --complete;
snid-sage  # Launch GUI for AI analysis
```

### Configuration Scripts
```bash
# Setup analysis parameters
snid config set analysis.correlation_method fft
snid config set analysis.redshift_range "0.0,0.5"
snid config set templates.quality_min 5.0

# Run analysis with saved config
snid identify spectrum.dat --output-dir results/
```

### Batch Analysis Script
```bash
#!/bin/bash
# Process all spectra in directory
for spectrum in data/*.dat; do
    echo "Processing $spectrum..."
    snid identify "$spectrum" \
        --output-dir "results/$(basename $spectrum .dat)/" \
        --complete
done

# Generate batch summary
snid batch "data/*.dat" templates/ --output-dir batch_results/
```

```powershell
# PowerShell: process all .dat spectra
Get-ChildItem -Path data -Filter *.dat | ForEach-Object {
  $s = $_.FullName;
  Write-Host "Processing $s";
  snid identify $s `
    --output-dir ("results/" + [System.IO.Path]::GetFileNameWithoutExtension($s) + "/") `
    --complete
}

# Summary
snid batch "data/*.dat" templates/ --output-dir batch_results/
```

## Troubleshooting

### Common Issues

**Command not found:**
- Ensure SNID SAGE is installed:
  ```powershell
  python -m pip install --upgrade pip
  python -m pip install snid-sage
  ```
- Check that scripts are in PATH

**Templates directory not found:**
- Specify templates directory explicitly: `snid identify spectrum.dat /path/to/templates/`
- Set default in config: `snid config set templates.default_dir /path/to/templates`

**Output directory errors:**
- Always specify `--output-dir` for identify command
- Ensure write permissions in output directory

**Memory errors with batch processing:**
- Use `--stop-on-error` to identify problematic files
- Process smaller batches

### Getting Help
- Use `--help` flag with any command
- Check error messages for specific issues
- See [Troubleshooting Guide](../reference/troubleshooting.md)

## Next Steps

- [Quick Start Tutorial](../quickstart/first-analysis.md) - Step-by-step first analysis
- [Batch Processing Guide](batch-processing.md) - Advanced batch workflows
- [GUI Interface](../gui/interface-overview.md) - Using the graphical interface 