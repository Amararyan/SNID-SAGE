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
sage data/SN2018bif.fits

# With output directory
sage data/SN2018bif.fits --output-dir results/
```

### Expected Output
```
SN2018bif: II IIP z=0.018335 RLAP-CCC=19.4 🎯
```

### Detailed Results
```
SNID-SAGE CLASSIFICATION RESULTS
==================================================

File: SN2018bif

Best Template: sn2012ec
   └─ Type: II, Subtype: IIP
   └─ RLAP-CCC: 19.4 | z=0.018543 ± 0.000330 | age=7.0

Best Type: II (Quality: High; Confidence: High; margin over next-best type Ic: +376.8%)
Best Subtype: IIP (confidence: High; margin over next-best subtype IIn: +293.9% based on weighted voting)
Redshift: 0.018335 ± 0.000341 (weighted from 132 IIP subtype templates)
Age: 3.9 ± 15.4 days (weighted from 132 IIP subtype templates)

TEMPLATE MATCHES (from Best Cluster (Auto-Selected)):
  # Template         Type   Subtype   RLAP-CCC    Redshift      ±Error    Age
-----------------------------------------------------------------------------
  1 sn2012ec         II     IIP           19.4    0.018543    0.000330    7.0
  2 sn1999em         II     IIP           17.3    0.016971    0.000391    2.4
  3 sn2018ldu        II     IIP           16.5    0.016347    0.000416  -42.0
  4 sn2018kpo        II     IIP           15.0    0.018616    0.000496  -15.0
  5 sn2004et         II     IIP           14.6    0.016836    0.000404    1.0

Results saved to: results/tutorial_analysis/
```

## Input Parameters Guide

### Essential Parameters

#### `--output-dir DIR`
Specify where to save results:
```bash
sage spectrum.dat --output-dir my_results/
```
**Output**: Creates organized directory structure with all analysis files

#### `--forced-redshift Z`
Use known redshift (speeds up analysis):
```bash
sage spectrum.dat --forced-redshift 0.045
```
**When to use**: When you have a reliable redshift from other sources
**Benefit**: Faster analysis, more accurate age determination

#### `--complete`
Generate detailed GUI-style outputs:
```bash
sage spectrum.dat --complete
```
**Output**: Additional plots, detailed data files, comprehensive analysis

### Analysis Parameters

#### `--min-correlation THRESHOLD`
Set minimum correlation threshold (default: 0.7):
```bash
sage spectrum.dat --min-correlation 0.8
```
**Effect**: Higher threshold = stricter matching, fewer false positives
**Trade-off**: May miss weak but real matches

#### `--max-redshift Z`
Limit redshift search range:
```bash
sage spectrum.dat --max-redshift 0.1
```
**Use case**: When you know the object is nearby
**Benefit**: Faster analysis, avoids spurious high-z matches

#### `--age-min DAYS` and `--age-max DAYS`
Limit template age range:
```bash
sage spectrum.dat --age-min -10 --age-max 30
```
**Use case**: Focus on specific phases (e.g., early or late)
**Example**: `--age-min 0 --age-max 50` for post-maximum analysis

### Preprocessing Parameters

#### `--smooth-window N`
Apply smoothing (default: 5):
```bash
sage spectrum.dat --smooth-window 7
```
**When to use**: Noisy spectra, low signal-to-noise
**Effect**: Reduces noise, may smooth out real features

#### `--smooth-order N`
Polynomial order for smoothing (default: 3):
```bash
sage spectrum.dat --smooth-window 5 --smooth-order 2
```
**Higher order**: More aggressive smoothing
**Lower order**: Preserves more features

#### `--telluric-correction`
Apply telluric absorption correction:
```bash
sage spectrum.dat --telluric-correction
```
**When to use**: Ground-based observations, visible wavelength spectra
**Effect**: Removes atmospheric absorption features

### Template Selection

#### `--type-filter TYPE`
Limit to specific supernova types:
```bash
# Type Ia only
sage spectrum.dat --type-filter Ia

# Core-collapse only
sage spectrum.dat --type-filter "II,Ib,Ic"

# Multiple types
sage spectrum.dat --type-filter "Ia,Ib,Ic"
```

**Important Note**: SNID SAGE analysis is very fast, so limiting templates usually doesn't provide significant speed benefits. You might miss rare or unusual objects! Consider using all templates unless you have a very specific reason to filter.

#### `--template-dir DIR`
Use custom template directory:
```bash
sage spectrum.dat --template-dir /path/to/my/templates/
```

## Output Structure

### Standard Mode Output
```
results/
├── tutorial_analysis/
│   ├── SN2018bif.output           # Main results summary
│   ├── SN2018bif_flux_spectrum.png # Input spectrum plot
│   ├── SN2018bif_flattened_spectrum.png # Processed spectrum
│   └── SN2018bif_redshift_age.png # Redshift and age analysis
```

### Complete Mode Output
```
results/
├── tutorial_analysis/
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
sage data/SN2018bif.fits --output-dir quick_results/
```

**Use case**: Initial screening, time-critical observations
**Output**: Basic classification, redshift, age estimate

### Example 2: Detailed Analysis
```bash
# Comprehensive analysis with all outputs
sage data/SN2018bif.fits \
  --output-dir detailed_results/ \
  --complete \
  --min-correlation 0.75
```

**Use case**: Publication-quality analysis, detailed investigation
**Output**: Full analysis suite with detailed plots and data

### Example 3: Known Redshift Analysis
```bash
# Use known redshift for better age determination
sage data/SN2018bif.fits \
  --forced-redshift 0.018 \
  --age-min -5 \
  --age-max 20 \
  --output-dir fixed_z_results/
```

**Use case**: When redshift is known from host galaxy
**Benefit**: More accurate age determination, faster analysis

### Example 4: Noisy Spectrum
```bash
# Handle low signal-to-noise spectrum
sage data/noisy_spectrum.dat \
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
sage data/ground_based.dat \
  --telluric-correction \
  --output-dir corrected_results/
```

**Use case**: Ground-based observations, visible wavelengths
**Effect**: Cleaner spectrum, better template matching

## Batch Processing

### Basic Batch Analysis
```bash
# Process all spectra in directory
sage batch "data/*.fits" --output-dir batch_results/
```

### Parallel Processing
```bash
# Use 4 parallel processes
sage batch "data/*.fits" --output-dir batch_results/ --parallel 4
```

### Filtered Batch Processing
```bash
# Process only Type II candidates with known redshifts
sage batch "data/ii_candidates/*.fits" \
  --type-filter II \
  --max-redshift 0.1 \
  --output-dir ii_results/
```

## Best Practices

### 1. Start Simple
```bash
# Begin with basic analysis
sage spectrum.dat --output-dir results/
```

### 2. Use Known Information
```bash
# Leverage known redshift when available
sage spectrum.dat --forced-redshift 0.018
```

### 3. Handle Data Quality
```bash
# Adjust parameters for poor quality data
sage noisy.dat --smooth-window 7 --min-correlation 0.6
```

### 4. Organize Outputs
```bash
# Use descriptive output directories
sage spectrum.dat --output-dir results/2024_spectra/SN2018bif/
```

### 5. Document Parameters
```bash
# Save analysis parameters for reproducibility
sage spectrum.dat --complete --output-dir results/
# Check analysis_parameters.txt in output
```

## Troubleshooting

### Common Issues

**"No templates found"**
```bash
# Check template installation
sage templates list

# Verify template directory
sage config get paths.templates_dir
```

**"Analysis failed"**
```bash
# Check data format
head -5 spectrum.dat

# Try with preprocessing
sage spectrum.dat --smooth-window 5
```

**"Poor correlation scores"**
```bash
# Lower correlation threshold
sage spectrum.dat --min-correlation 0.5

# Apply smoothing
sage spectrum.dat --smooth-window 7
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
