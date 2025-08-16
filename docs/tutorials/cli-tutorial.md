# CLI Tutorial: Command-Line Analysis with SNID SAGE

This tutorial walks you through using SNID SAGE's command-line interface for spectrum analysis, covering practical usage, input parameters, and expected outputs.

## Prerequisites

- SNID SAGE installed (`pip install snid-sage`)
- Sample spectrum files for testing
- Basic familiarity with command-line tools

## Quick Start

### Basic Analysis
```bash
# Analyze a single spectrum
snid data/sn2024ggi.dat

# With output directory
snid data/sn2024ggi.dat --output-dir results/
```

### Expected Output
```
SNID SAGE Analysis Results
==========================

File: data/sn2024ggi.dat
Analysis completed in 2.3 seconds

Classification Results:
- Type: Ia
- Subtype: normal
- Confidence: 0.92

Redshift Analysis:
- Best redshift: 0.0452 ± 0.0012
- Age: -2.3 ± 1.1 days (from maximum)

Top Template Matches:
1. SN1994D (Ia-norm) - rlap: 0.89, z: 0.0451
2. SN2011fe (Ia-norm) - rlap: 0.87, z: 0.0453
3. SN2005cf (Ia-norm) - rlap: 0.85, z: 0.0449

Results saved to: results/sn2024ggi_analysis/
```

## Input Parameters Guide

### Essential Parameters

#### `--output-dir DIR`
Specify where to save results:
```bash
snid spectrum.dat --output-dir my_results/
```
**Output**: Creates organized directory structure with all analysis files

#### `--forced-redshift Z`
Use known redshift (speeds up analysis):
```bash
snid spectrum.dat --forced-redshift 0.045
```
**When to use**: When you have a reliable redshift from other sources
**Benefit**: Faster analysis, more accurate age determination

#### `--complete`
Generate detailed GUI-style outputs:
```bash
snid spectrum.dat --complete
```
**Output**: Additional plots, detailed data files, comprehensive analysis

### Analysis Parameters

#### `--min-correlation THRESHOLD`
Set minimum correlation threshold (default: 0.7):
```bash
snid spectrum.dat --min-correlation 0.8
```
**Effect**: Higher threshold = stricter matching, fewer false positives
**Trade-off**: May miss weak but real matches

#### `--max-redshift Z`
Limit redshift search range:
```bash
snid spectrum.dat --max-redshift 0.1
```
**Use case**: When you know the object is nearby
**Benefit**: Faster analysis, avoids spurious high-z matches

#### `--age-min DAYS` and `--age-max DAYS`
Limit template age range:
```bash
snid spectrum.dat --age-min -10 --age-max 30
```
**Use case**: Focus on specific phases (e.g., early or late)
**Example**: `--age-min 0 --age-max 50` for post-maximum analysis

### Preprocessing Parameters

#### `--smooth-window N`
Apply smoothing (default: 5):
```bash
snid spectrum.dat --smooth-window 7
```
**When to use**: Noisy spectra, low signal-to-noise
**Effect**: Reduces noise, may smooth out real features

#### `--smooth-order N`
Polynomial order for smoothing (default: 3):
```bash
snid spectrum.dat --smooth-window 5 --smooth-order 2
```
**Higher order**: More aggressive smoothing
**Lower order**: Preserves more features

#### `--telluric-correction`
Apply telluric absorption correction:
```bash
snid spectrum.dat --telluric-correction
```
**When to use**: Ground-based observations, visible wavelength spectra
**Effect**: Removes atmospheric absorption features

### Template Selection

#### `--type-filter TYPE`
Limit to specific supernova types:
```bash
# Type Ia only
snid spectrum.dat --type-filter Ia

# Core-collapse only
snid spectrum.dat --type-filter "II,Ib,Ic"

# Multiple types
snid spectrum.dat --type-filter "Ia,Ib,Ic"
```

**Important Note**: SNID SAGE analysis is very fast, so limiting templates usually doesn't provide significant speed benefits. You might miss rare or unusual objects! Consider using all templates unless you have a very specific reason to filter.

#### `--template-dir DIR`
Use custom template directory:
```bash
snid spectrum.dat --template-dir /path/to/my/templates/
```

## Output Structure

### Standard Mode Output
```
results/
├── sn2024ggi_analysis/
│   ├── classification.txt          # Main results summary
│   ├── redshift_age.txt           # Redshift and age analysis
│   ├── template_matches.txt       # Ranked template matches
│   ├── correlation_plot.png       # Correlation vs redshift plot
│   ├── spectrum_plot.png          # Input spectrum plot
│   ├── best_match_plot.png        # Best template comparison
│   └── data/
│       ├── spectrum.dat           # Processed spectrum
│       ├── correlation_data.txt   # Raw correlation data
│       └── template_data.txt      # Template match details
```

### Complete Mode Output
```
results/
├── sn2024ggi_analysis/
│   ├── [all standard outputs]
│   ├── detailed_plots/
│   │   ├── correlation_3d.png     # 3D correlation surface
│   │   ├── age_analysis.png       # Age vs redshift analysis
│   │   ├── template_comparison.png # Multiple template comparison
│   │   └── feature_analysis.png   # Spectral feature analysis
│   ├── data/
│   │   ├── [all standard data]
│   │   ├── preprocessing_log.txt  # Preprocessing steps
│   │   ├── analysis_parameters.txt # Used parameters
│   │   └── quality_metrics.txt    # Data quality assessment
│   └── reports/
│       ├── analysis_report.html   # HTML summary report
│       └── analysis_report.json   # Machine-readable results
```

## Practical Examples

### Example 1: Quick Classification
```bash
# Fast analysis for initial classification
snid data/sn2024ggi.dat --output-dir quick_results/
```

**Use case**: Initial screening, time-critical observations
**Output**: Basic classification, redshift, age estimate

### Example 2: Detailed Analysis
```bash
# Comprehensive analysis with all outputs
snid data/sn2024ggi.dat \
  --output-dir detailed_results/ \
  --complete \
  --min-correlation 0.75
```

**Use case**: Publication-quality analysis, detailed investigation
**Output**: Full analysis suite with detailed plots and data

### Example 3: Known Redshift Analysis
```bash
# Use known redshift for better age determination
snid data/sn2024ggi.dat \
  --forced-redshift 0.045 \
  --age-min -5 \
  --age-max 20 \
  --output-dir fixed_z_results/
```

**Use case**: When redshift is known from host galaxy
**Benefit**: More accurate age determination, faster analysis

### Example 4: Noisy Spectrum
```bash
# Handle low signal-to-noise spectrum
snid data/noisy_spectrum.dat \
  --smooth-window 7 \
  --smooth-order 2 \
  --min-correlation 0.6 \
  --output-dir noisy_results/
```

**Use case**: Poor quality data, ground-based observations
**Effect**: Reduced noise, more tolerant matching

### Example 5: Telluric Correction
```bash
# Remove atmospheric absorption features
snid data/ground_based.dat \
  --telluric-correction \
  --output-dir corrected_results/
```

**Use case**: Ground-based observations, visible wavelengths
**Effect**: Cleaner spectrum, better template matching

## Batch Processing

### Basic Batch Analysis
```bash
# Process all spectra in directory
snid batch "data/*.dat" --output-dir batch_results/
```

### Parallel Processing
```bash
# Use 4 parallel processes
snid batch "data/*.dat" --output-dir batch_results/ --parallel 4
```

### Filtered Batch Processing
```bash
# Process only Type Ia candidates with known redshifts
snid batch "data/ia_candidates/*.dat" \
  --type-filter Ia \
  --max-redshift 0.1 \
  --output-dir ia_results/
```

## Best Practices

### 1. Start Simple
```bash
# Begin with basic analysis
snid spectrum.dat --output-dir results/
```

### 2. Use Known Information
```bash
# Leverage known redshift when available
snid spectrum.dat --forced-redshift 0.045
```

### 3. Handle Data Quality
```bash
# Adjust parameters for poor quality data
snid noisy.dat --smooth-window 7 --min-correlation 0.6
```

### 4. Organize Outputs
```bash
# Use descriptive output directories
snid spectrum.dat --output-dir results/2024_spectra/sn2024ggi/
```

### 5. Document Parameters
```bash
# Save analysis parameters for reproducibility
snid spectrum.dat --complete --output-dir results/
# Check analysis_parameters.txt in output
```

## Troubleshooting

### Common Issues

**"No templates found"**
```bash
# Check template installation
snid templates list

# Verify template directory
snid config get paths.templates_dir
```

**"Analysis failed"**
```bash
# Check data format
head -5 spectrum.dat

# Try with preprocessing
snid spectrum.dat --smooth-window 5
```

**"Poor correlation scores"**
```bash
# Lower correlation threshold
snid spectrum.dat --min-correlation 0.5

# Apply smoothing
snid spectrum.dat --smooth-window 7
```

### Performance Tips

1. **Use `--forced-redshift`** when redshift is known
2. **Limit age range** for specific phase analysis
3. **Use parallel processing** for batch analysis
4. **Skip `--complete`** for quick screening

## Next Steps

1. **Practice**: Try different parameter combinations
2. **Batch Processing**: Process multiple spectra efficiently
3. **Custom Templates**: Add your own template library
4. **Integration**: Use CLI in your analysis pipelines

## Related Documentation

- [CLI Command Reference](../cli/command-reference.md) - Complete command reference
- [Batch Processing](../cli/batch-processing.md) - Advanced batch workflows
- [Configuration Guide](../reference/configuration-guide.md) - Customize SNID SAGE
- [Troubleshooting](../reference/troubleshooting.md) - Solve common issues
