# CLI Command Reference

SNID SAGE provides a command-line interface for automated spectrum analysis, batch processing, and scripting workflows.

## Overview

The CLI offers:
- Single spectrum analysis with detailed outputs
- Batch processing of multiple spectra
- Configuration management
- Template and data management

## Installation

### Install SNID SAGE CLI
```bash
pip install snid-sage
```

### Verify Installation
```bash
snid --version
snid --help
```

## Core Commands

### `snid`

Analyze a single spectrum against the template library with cluster-aware analysis and detailed outputs.

#### Basic Usage
```bash
snid <spectrum_file> [options]
```

#### Examples
```bash
# Basic analysis
snid data/sn2024ggi.dat

# With output directory
snid data/sn2024ggi.dat --output-dir results/

# With specific redshift
snid data/sn2024ggi.dat --forced-redshift 0.045

# Complete mode with all plots
snid data/sn2024ggi.dat --complete
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
snid data/sn2024ggi.dat --output-dir results/

# Complete mode - all outputs including detailed GUI-style plots
snid data/sn2024ggi.dat --output-dir results/ --complete
```

### `snid batch`

Process multiple spectra simultaneously with optimized workflows and detailed reporting.

#### Basic Usage
```bash
snid batch <input_pattern> [options]
```

#### Examples
```bash
# Process all .dat files in a directory
snid batch "data/*.dat" --output-dir batch_results/

# Process specific files
snid batch "data/sn2024*.dat" --output-dir results/

# With template directory
snid batch "data/*.dat" templates/ --output-dir results/

# Parallel processing
snid batch "data/*.dat" --output-dir results/ --parallel 4
```

#### Batch Options
```bash
--parallel N            # Use N parallel processes
--output-dir DIR        # Output directory for results
--template-dir DIR      # Custom template directory
--type-filter TYPE      # Filter templates by type
--age-min DAYS          # Minimum template age
--age-max DAYS          # Maximum template age
```

### `snid config`

Manage SNID SAGE configuration settings.

#### Basic Usage
```bash
snid config <command> [options]
```

#### Commands
```bash
snid config show                    # Show current configuration
snid config set <key> <value>       # Set configuration value
snid config get <key>               # Get configuration value
snid config reset                   # Reset to defaults
snid config export                  # Export configuration
snid config import <file>           # Import configuration
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
snid config show

# Set template directory
snid config set paths.templates_dir /path/to/templates

# Set analysis parameters
snid config set analysis.min_correlation 0.8
snid config set analysis.max_redshift 0.1

# Export configuration
snid config export > my_config.yaml
```

### `snid templates`

Manage template library and template-related operations.

#### Basic Usage
```bash
snid templates <command> [options]
```

#### Commands
```bash
snid templates list                  # List available templates
snid templates info <template>       # Show template information
snid templates search <query>        # Search templates
snid templates validate              # Validate template library
snid templates update                # Update template library
```

#### Examples
```bash
# List all templates
snid templates list

# Search for Type Ia templates
snid templates search "Ia"

# Show template information
snid templates info "SN1994D"

# Validate template library
snid templates validate
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
    snid identify "$file" \
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

snid batch "data/*.dat" \
    --output-dir batch_results/ \
    --parallel 4 \
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
snid config set paths.templates_dir /path/to/templates

# Set analysis parameters
snid config set analysis.min_correlation 0.85
snid config set analysis.max_redshift 0.1
snid config set analysis.age_range "-10,30"

# Set preprocessing parameters
snid config set preprocessing.smoothing_window 15
snid config set preprocessing.smoothing_order 3

# Export configuration
snid config export > analysis_config.yaml
```

### Integration with Other Tools

#### Python Integration
```python
import subprocess
import json

def analyze_spectrum(spectrum_file, output_dir):
    """Analyze spectrum using SNID SAGE CLI"""
    
    cmd = [
        'snid', 'identify', spectrum_file,
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
    snid identify "$file" --output-dir "results/$(basename "$file" .dat)"
    
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
snid config get paths.templates_dir

# Validate templates
snid templates validate

# Update templates
snid templates update
```

#### Analysis Failures
```bash
# Check input file format
file data/sn2024ggi.dat

# Run with verbose output
snid identify data/sn2024ggi.dat --verbose

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
- Use `--parallel` for batch processing
- Set appropriate `--min-correlation` threshold
- Use `--type-filter` to limit template search
- Enable `--quiet` for scripted workflows

### Resource Management
- Monitor memory usage for large batch jobs
- Use appropriate number of parallel processes
- Clean up temporary files regularly
- Use SSD storage for better I/O performance

## Related Documentation

- [Batch Processing Guide](batch-processing.md) - Advanced batch workflows
- [Configuration Guide](../reference/configuration-guide.md) - Detailed configuration options
- [Troubleshooting](../reference/troubleshooting.md) - Common issues and solutions 