# CLI Command Reference

SNID SAGE provides a command-line interface for automated spectrum analysis, batch processing, and scripting workflows.

## Overview

The CLI offers:
- Single spectrum analysis with detailed outputs
- Batch processing of multiple spectra
- Configuration management
- Template and data management

### Supported input formats

SNID SAGE accepts common text and binary spectrum formats:
- .txt, .dat, .ascii, .asci
- .csv
- .flm
- .fits, .fit

Files can have header rows; CSVs with headers (e.g., wave,flux,flux_err) are supported.

## Installation

### Install SNID SAGE CLI
```bash
pip install snid-sage
```

### Verify Installation
```bash
sage --version
sage --help
```

## Core Commands

### `sage`

Analyze a single spectrum against the template library with cluster-aware analysis and detailed outputs.

#### Basic Usage
```bash
sage <spectrum_file> [options]
```

#### Examples
```bash
# Basic analysis
sage data/SN2018bif.csv

# With output directory
sage data/SN2018bif.csv --output-dir results/

# With specific redshift
sage data/SN2018bif.csv --forced-redshift 0.018

# Complete mode with all plots
sage data/SN2018bif.csv --complete
```

#### Output Modes
```bash
--complete              # Complete mode: All outputs including detailed GUI-style plots
# (default)             # Standard mode: Main outputs without detailed plots
```

#### Standard Outputs
- Classification results (type, subtype, confidence)
- Redshift and age estimates
- Template matches and correlation scores
- Basic plots and data files

#### Complete Outputs
- All standard outputs
- Detailed GUI-style plots
- Additional analysis visualizations
- Comprehensive data exports

#### Examples
```bash
# Standard mode - main outputs without detailed plots
sage data/SN2018bif.csv --output-dir results/

# Complete mode - all outputs including detailed GUI-style plots
sage data/SN2018bif.csv --output-dir results/ --complete
```

### `sage batch`

Process multiple spectra simultaneously with optimized workflows and detailed reporting.

#### Basic Usage
```bash
sage batch <input_pattern> [templates/] [options]
sage batch --list-csv <file.csv> [templates/] [options]
```

#### Examples
```bash
# Process all .dat files in a directory
sage batch "data/*.dat" --output-dir batch_results/

# Process specific files
sage batch "data/sn2024*.dat" --output-dir results/

# With template directory
sage batch "data/*.dat" templates/ --output-dir results/

# Batch processing
sage batch "data/*.dat" --output-dir results/

# List-based batch from CSV (per-row redshift when present)
sage batch --list-csv "data/spectra_list.csv" --output-dir results/

# Custom column names in CSV
sage batch --list-csv input.csv --path-column "Spectrum Path" --redshift-column "Host Redshift" --output-dir results/
```

#### Batch Options
```bash
--output-dir DIR          # Output directory for results
--type-filter TYPE...     # Filter templates by type
--template-filter NAME... # Restrict to specific templates
--zmin FLOAT              # Min redshift for search (default: -0.01)
--zmax FLOAT              # Max redshift for search (default: 1.0)
--forced-redshift FLOAT   # Force a fixed redshift for all spectra
--list-csv FILE           # CSV list of spectra (columns: path[, redshift])
--path-column NAME        # Column name for spectrum paths in --list-csv (default: path)
--redshift-column NAME    # Column name for per-row redshift in --list-csv (default: redshift)
```

Outputs:
- Per spectrum result files; summary includes a `zFixed` column indicating whether a fixed redshift was used for that spectrum.

### `sage config`

Manage SNID SAGE configuration settings.

#### Basic Usage
```bash
sage config <command> [options]
```

#### Commands
```bash
sage config show                    # Show current configuration
sage config set <key> <value>       # Set configuration value
sage config get <key>               # Get configuration value
sage config reset                   # Reset to defaults
sage config export                  # Export configuration
sage config import <file>           # Import configuration
```

#### Configuration Keys
```bash
# Paths
paths.templates_dir                 # Template directory
paths.output_dir                    # Default output directory
paths.data_dir                      # Data directory

# Analysis
analysis.min_correlation            # Minimum correlation threshold
analysis.max_redshift               # Maximum redshift range
analysis.age_range                  # Template age range

# Preprocessing
preprocessing.smoothing_window      # Smoothing window size
preprocessing.smoothing_order       # Smoothing polynomial order
preprocessing.telluric_correction   # Telluric correction
```

#### Examples
```bash
# Show current configuration
sage config show

# Set template directory
sage config set paths.templates_dir /path/to/templates

# Set analysis parameters
sage config set analysis.min_correlation 0.8
sage config set analysis.max_redshift 0.1

# Export configuration
sage config export > my_config.yaml
```

### `sage templates`

Manage template library and template-related operations.

#### Basic Usage
```bash
sage templates <command> [options]
```

#### Commands
```bash
sage templates list                  # List available templates
sage templates info <template>       # Show template information
sage templates search <query>        # Search templates
sage templates validate              # Validate template library
sage templates update                # Update template library
```

#### Examples
```bash
# List all templates
sage templates list

# Search for Type Ia templates
sage templates search "Ia"

# Show template information
sage templates info "SN1994D"

# Validate template library
sage templates validate
```

## Advanced Options

### Analysis Parameters
```bash
--min-correlation FLOAT     # Minimum correlation threshold (default: 0.8)
--max-redshift FLOAT        # Maximum redshift range (default: 0.1)
--age-min DAYS              # Minimum template age (default: -20)
--age-max DAYS              # Maximum template age (default: 50)
--type-filter TYPE          # Filter templates by type
--wavelength-min ANGSTROM   # Minimum wavelength (default: 3500)
--wavelength-max ANGSTROM   # Maximum wavelength (default: 9000)
```

### Preprocessing Options
```bash
--savgol-window INT         # Savitzky-Golay window size (default: 11)
--savgol-order INT          # Savitzky-Golay polynomial order (default: 3)
--telluric-correction       # Apply telluric correction
--skyline-clipping          # Apply skyline clipping
--custom-mask FILE          # Custom wavelength mask file
```

### Output Options
```bash
--output-dir DIR            # Output directory
--output-format FORMAT      # Output format (json, yaml, txt)
--save-plots                # Save analysis plots
--save-data                 # Save analysis data
--verbose                   # Verbose output
--quiet                     # Quiet output
```

## Advanced Usage

### Scripting Examples

#### Basic Analysis Script
```bash
#!/bin/bash
# Analyze multiple spectra with different parameters

for file in data/*.dat; do
    echo "Analyzing $file..."
    sage identify "$file" \
        --output-dir "results/$(basename "$file" .dat)" \
        --min-correlation 0.85 \
        --save-plots
done
```

#### Batch Processing with Error Handling
```bash
#!/bin/bash
# Batch processing with error handling and logging

mkdir -p batch_results
log_file="batch_results/analysis.log"

echo "Starting batch analysis at $(date)" > "$log_file"

sage batch "data/*.dat" \
    --output-dir batch_results/ \
    --min-correlation 0.8 \
    --save-plots \
    2>&1 | tee -a "$log_file"

echo "Batch analysis completed at $(date)" >> "$log_file"
```

#### Configuration Management
```bash
#!/bin/bash
# Set up analysis configuration

# Set template directory
sage config set paths.templates_dir /path/to/templates

# Set analysis parameters
sage config set analysis.min_correlation 0.85
sage config set analysis.max_redshift 0.1
sage config set analysis.age_range "-10,30"

# Set preprocessing parameters
sage config set preprocessing.smoothing_window 15
sage config set preprocessing.smoothing_order 3

# Export configuration
sage config export > analysis_config.yaml
```

### Integration with Other Tools

#### Python Integration
```python
import subprocess
import json

def analyze_spectrum(spectrum_file, output_dir):
    """Analyze spectrum using SNID SAGE CLI"""
    
    cmd = [
        'sage', 'identify', spectrum_file,
        '--output-dir', output_dir,
        '--output-format', 'json',
        '--min-correlation', '0.8'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Parse JSON output
        with open(f"{output_dir}/results.json") as f:
            return json.load(f)
    else:
        raise RuntimeError(f"Analysis failed: {result.stderr}")
```

#### Shell Scripting
```bash
#!/bin/bash
# Process spectra and generate summary report

echo "SNID SAGE Analysis Report" > report.txt
echo "=========================" >> report.txt
echo "" >> report.txt

for file in data/*.dat; do
    echo "Processing $file..." >> report.txt
    
    # Run analysis
    sage identify "$file" --output-dir "results/$(basename "$file" .dat)"
    
    # Extract results
    if [ -f "results/$(basename "$file" .dat)/results.json" ]; then
        type=$(jq -r '.classification.type' "results/$(basename "$file" .dat)/results.json")
        redshift=$(jq -r '.redshift.value' "results/$(basename "$file" .dat)/results.json")
        confidence=$(jq -r '.classification.confidence' "results/$(basename "$file" .dat)/results.json")
        
        echo "  Type: $type" >> report.txt
        echo "  Redshift: $redshift" >> report.txt
        echo "  Confidence: $confidence" >> report.txt
        echo "" >> report.txt
    fi
done
```

## Troubleshooting

### Common Issues

#### Command Not Found
```bash
# Check installation
pip list | grep snid-sage

# Reinstall if needed
pip install --upgrade snid-sage
```

#### Template Library Issues
```bash
# Check template directory
sage config get paths.templates_dir

# Validate templates
sage templates validate

# Update templates
sage templates update
```

#### Analysis Failures
```bash
# Check input file format
file data/SN2018bif.csv

# Run with verbose output
sage identify data/SN2018bif.csv --verbose

# Check error logs
cat results/error.log
```

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Template library not found` | Missing template directory | Set `paths.templates_dir` in config |
| `Invalid spectrum format` | Unsupported file format | Convert to supported format |
| `No templates match criteria` | Template filters too restrictive | Adjust `--type-filter` or age range |
| `Analysis failed` | Input data quality issues | Check spectrum quality and preprocessing |

## Performance Tips

### Optimization
- Set appropriate `--min-correlation` threshold
- Use `--type-filter` to limit template search
- Enable `--quiet` for scripted workflows

### Resource Management
- Monitor memory usage for large batch jobs
- Clean up temporary files regularly
- Use SSD storage for better I/O performance

## Related Documentation

- [Batch Processing Guide](batch-processing.md) - Advanced batch workflows
- [Configuration Guide](../reference/configuration-guide.md) - Detailed configuration options
- [Troubleshooting](../reference/troubleshooting.md) - Common issues and solutions 