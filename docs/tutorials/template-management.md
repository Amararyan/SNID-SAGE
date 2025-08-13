# Template Management (Practical)

---

## Overview

SNID SAGE includes a comprehensive library of **500+ professional supernova templates** covering all major types and subtypes. This guide explains how to work with, manage, and extend this powerful template system.

---

## Template Library Structure

### Complete Template Categories

| **Category** | **Count** | **Subtypes** | **Key Features** |
|-------------|-----------|--------------|------------------|
| **Type Ia** | 150+ | Normal, 91bg-like, 91T-like, 02cx-like, Iax | Peak luminosity variations, silicon features |
| **Type Ib** | 60+ | Normal, peculiar, transitional | Helium features, no hydrogen |
| **Type Ic** | 60+ | Normal, broad-line (BL), hypernova | Neither hydrogen nor helium |
| **Type II-P** | 80+ | Plateau, peculiar | Hydrogen-rich, plateau light curves |
| **Type II-L** | 40+ | Linear decline, peculiar | Hydrogen-rich, linear decline |
| **Type IIn** | 45+ | Narrow lines, peculiar | Strong interaction signatures |
| **Type IIb** | 35+ | Transitional, peculiar | Hydrogen disappears over time |
| **LBV** | 25+ | Outbursts, transitions | Luminous Blue Variable events |
| **Kilonova** | 15+ | GRB afterglows, mergers | Neutron star merger events |
| **AGN/QSO** | 35+ | BAL, normal, variable | Active galactic nuclei |
| **Stellar** | 30+ | Carbon stars, M-type, variables | Various stellar classifications |

---

## Exploring the Template Library

### GUI Template Browser

1. **Open Template Manager**: `Tools` → `Template Library`
2. **Browse Categories**: Organized by supernova type
3. **Preview Templates**: Click to view spectrum and metadata
4. **Filter Options**:
   - By type/subtype
   - By date range
   - By quality metrics
   - By wavelength coverage

### CLI Template Exploration

```bash
# List all available templates
snid-sage template list

# List templates by type
snid-sage template list --type Ia
snid-sage template list --type "II-P"

# Get detailed template information
snid-sage template info sn1994D.lnw

# Search templates by name pattern
snid-sage template search "*2003*"
```

### Template metadata

Each template includes comprehensive metadata:

```bash
# View complete template metadata
snid-sage template metadata sn1987A.lnw
```

Common fields: discovery date, host galaxy, redshift, phase, quality, references, classification.

---

## Template Usage Strategies

### Optimal Template Selection

#### **Automatic Selection**
```bash
# Let SNID SAGE choose optimal templates
snid-sage identify spectrum.fits --auto-select-templates
```

#### **Manual Template Subset**
```bash
# Use only Type Ia templates
snid-sage identify spectrum.fits --template-types Ia

# Use specific phase range
snid-sage identify spectrum.fits --phase-range -10:+30

# Use high-quality templates only
snid-sage identify spectrum.fits --min-quality 0.8
```

### Template Matching Strategies

#### **1. Broad Search First**
```bash
# Initial broad classification
snid-sage identify spectrum.fits --all-types --top-matches 20
```

#### **2. Refined Type-Specific Search**
```bash
# Focus on best type from broad search
snid-sage identify spectrum.fits --type II-P --detailed-analysis
```

#### **3. Phase-Specific Matching**
```bash
# Match within specific phase window
snid-sage identify spectrum.fits --phase-window 5 --type Ia
```

---

## Custom Template Creation

### Preparing Your Spectrum

#### Required format
Templates must be in SNID `.lnw` format (log-wavelength):

```python
# Convert spectrum to log-wavelength format
import numpy as np

# Your linear wavelength spectrum
wavelength_linear = np.array([...])  # Angstroms
flux = np.array([...])               # Flux values

# Convert to log-wavelength
log_wavelength = np.log10(wavelength_linear)

# Save in SNID format
with open('my_template.lnw', 'w') as f:
    for lw, fl in zip(log_wavelength, flux):
        f.write(f"{lw:.6f} {fl:.6e}\n")
```

#### Quality requirements
- Wavelength range: 3500-9000 Å (min)
- Resolution: R > 100 preferred
- SNR > 10
- Proper wavelength/flux calibration

### Template Creation Workflow

#### **Step 1: Spectrum Preparation**
```bash
# Use SNID SAGE preprocessing tools
snid-sage preprocess raw_spectrum.fits \
    --output prepared_spectrum.fits \
    --wavelength-calibration \
    --flux-calibration \
    --noise-reduction
```

#### **Step 2: Convert to Template Format**
```bash
# Convert prepared spectrum to template
snid-sage template create prepared_spectrum.fits \
    --output my_sn2024abc.lnw \
    --type "II-P" \
    --phase +15 \
    --redshift 0.0234 \
    --quality-check
```

#### **Step 3: Add Metadata**
```bash
# Add comprehensive metadata
snid-sage template metadata my_sn2024abc.lnw \
    --discovery-date "2024-03-15" \
    --host-galaxy "NGC 1234" \
    --coordinates "12:34:56.7 +65:43:21" \
    --references "Smith et al. 2024, ApJ, 900, 123"
```

### Template Validation

```bash
# Validate template quality
snid-sage template validate my_sn2024abc.lnw

# Test template against known spectra
snid-sage template test my_sn2024abc.lnw \
    --test-against known_spectra/ \
    --correlation-threshold 0.7
```

---

## Template Library Management

### Installing Additional Templates

```bash
# Install templates from online repository
snid-sage template install --source online --category recent

# Install from local directory
snid-sage template install --source /path/to/templates/ --validate

# Install specific template sets
snid-sage template install --set "SNe2024_collection"
```

### Template Organization

#### **Directory Structure**
```
templates/
├── type_Ia/
│   ├── normal/
│   ├── 91bg_like/
│   ├── 91T_like/
│   └── peculiar/
├── type_Ib/
├── type_Ic/
├── type_II/
│   ├── II_P/
│   ├── II_L/
│   ├── II_n/
│   └── IIb/
├── lbv/
├── kilonova/
├── agn/
└── stellar/
```

#### **Custom Collections**
```bash
# Create custom template collection
snid-sage template collection create "my_research_set" \
    --templates sn2024a.lnw,sn2024b.lnw,sn2024c.lnw \
    --description "Templates for 2024 research project"

# Use custom collection
snid-sage identify spectrum.fits --collection "my_research_set"
```

---

## Advanced Template Features

### Template Quality Metrics

```bash
# Analyze template quality
snid-sage template analyze my_template.lnw
```

**Quality Metrics:**
- 📊 **SNR Profile**: Signal-to-noise across wavelength
- 📏 **Wavelength Coverage**: Completeness assessment
- 🎯 **Feature Strength**: Key spectral line visibility
- 🔍 **Contamination**: Host galaxy or instrumental artifacts
- 📈 **Correlation Power**: Cross-correlation effectiveness

### Template Preprocessing

```bash
# Apply advanced preprocessing to templates
snid-sage template preprocess input_template.lnw \
    --output enhanced_template.lnw \
    --smooth-factor 1.5 \
    --remove-continuum \
    --normalize-flux \
    --mask-tellurics
```

### Template Comparison Tools

```bash
# Compare multiple templates
snid-sage template compare template1.lnw template2.lnw template3.lnw \
    --output comparison_report.pdf \
    --plot-differences \
    --correlation-matrix
```

---

## Template Best Practices

### Selection Guidelines

#### For Classification
1. **🎯 Use Broad Search First**: Start with all types
2. **📊 Consider Phase Range**: Match evolutionary phase
3. **🔍 Check Wavelength Overlap**: Ensure good coverage
4. **📈 Validate with Multiple Templates**: Don't rely on single match

#### For Research
1. **📚 Use High-Quality Templates**: SNR > 20 preferred
2. **🎯 Match Observational Setup**: Similar resolution/coverage
3. **🔬 Consider Host Contamination**: Clean templates preferred
4. **📊 Document Template Selection**: For reproducibility

### Common Template Issues

#### **❌ Problems to Avoid**
- **Low SNR Templates**: Can lead to false matches
- **Poor Wavelength Calibration**: Causes correlation issues
- **Host Galaxy Contamination**: Affects line measurements
- **Incorrect Phase Assignment**: Misleads evolutionary analysis
- **Inadequate Metadata**: Reduces scientific value

#### **✅ Solutions**
- **Quality Filtering**: Use `--min-quality` flags
- **Visual Inspection**: Always examine top matches
- **Cross-Validation**: Test with multiple approaches
- **Metadata Verification**: Check template documentation

---

## Template Utilities

### Batch Template Operations

```bash
# Process multiple templates
snid-sage template batch-process templates_directory/ \
    --operation validate \
    --output validation_report.txt

# Convert format for multiple templates
snid-sage template batch-convert *.fits \
    --output-format lnw \
    --output-directory converted_templates/
```

### Template Statistics

```bash
# Generate library statistics
snid-sage template stats --full-report

# Type distribution analysis
snid-sage template distribution --plot-histogram
```

### Template Maintenance

```bash
# Check for template updates
snid-sage template update --check-online

# Clean duplicate templates
snid-sage template clean --remove-duplicates --similarity-threshold 0.95

# Rebuild template index
snid-sage template reindex --optimize
```

---

## Template Performance Optimization

### Caching Strategies

```bash
# Configure template caching
snid-sage config set templates.cache_size 500
snid-sage config set templates.preload_common true
snid-sage config set templates.cache_strategy lru
```

### Memory Management

```bash
# Optimize memory usage for large template sets
snid-sage config set templates.fft_optimization true
snid-sage config set templates.max_memory_gb 4.0
```

---

## Template Creation Workshop

### Exercise 1: Basic Template Creation

1. **Obtain High-Quality Spectrum**
2. **Apply Preprocessing Pipeline**
3. **Convert to Template Format**
4. **Add Complete Metadata**
5. **Validate Against Known Spectra**

### Exercise 2: Template Collection

1. **Gather Related Spectra** (same object, different phases)
2. **Create Consistent Template Set**
3. **Build Custom Collection**
4. **Test Classification Performance**

---

## Template Resources

### Online Template Repositories

- SNID SAGE Central: Official template updates
- WISeREP: Weizmann Interactive Supernova Repository
- TNS: Transient Name Server spectra
- SUSPECT: SUperNova SPECTra database

### Contributing Templates

```bash
# Submit template to community repository
snid-sage template submit my_template.lnw \
    --repository community \
    --license "CC-BY-4.0" \
    --contact "researcher@university.edu"
```

---

## Template Troubleshooting

### Common Issues

#### **Template Not Loading**
```bash
# Check template format
snid-sage template validate problematic_template.lnw --verbose
```

#### **Poor Correlation Results**
```bash
# Analyze template quality
snid-sage template diagnose template.lnw --correlation-test
```

#### **Missing Metadata**
```bash
# Add missing information
snid-sage template metadata template.lnw --interactive-edit
```

---

## Template Support

- 📧 **Template Issues**: Report problems with specific templates
- 🎓 **Creation Help**: Assistance with custom template development
- 📚 **Best Practices**: Guidance on template selection strategies
- 🔬 **Research Collaboration**: Joint template development projects

---

<span style="color:#3b82f6">Master the template system to unlock the full classification power of SNID SAGE!</span>