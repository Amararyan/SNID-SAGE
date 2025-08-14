# Basic Analysis (Short)

Goal: run one spectrum through the GUI or CLI and interpret the result.

## Prerequisites

- SNID SAGE installed and running
- Sample data files (included with installation)
- Basic understanding of supernova types

Sample data: `data/sn2003jo.dat` (or your own spectrum)

---

## Part 1: Your First Analysis

!!! tip "At a glance"
    GUI: Load → Preprocess → Analyze → Review → AI (optional)
    
    CLI: `snid identify <file> --output-dir results/`

### Step 1: Launch

#### GUI Method
```powershell
# If installed via pip
snid-sage

# If running from source
python snid_sage/interfaces/gui/sage_gui.py
```

#### CLI Method
```powershell
# Check available commands
snid --help
```

### Step 2: Load spectrum

#### In GUI:
1. Click **"Load Spectrum"** button (grey)
2. Navigate to `data/` folder
3. Select `sn2003jo.dat`
4. Observe the spectrum preview

#### In CLI:
```powershell
# Preview the data (PowerShell)
Get-Content -TotalCount 20 data/sn2003jo.dat

# Basic identification
snid identify data/sn2003jo.dat --output-dir results/ --verbose
```

### Step 3: Inspect

The loaded spectrum shows:
- **Wavelength range**: ~3500-9000 Å
- **Spectral features**: Broad absorption lines
- **Signal-to-noise**: Good quality (>10)
- **Continuum**: Relatively smooth

### Step 4: Analyze

#### GUI Method:
1. Click **"Preprocessing"** (amber button)
2. Select **"Quick SNID Preprocessing"**
3. Click **"SNID Analysis"** (magenta button)
4. Watch progress bar (~30 seconds)

#### CLI Method:
```powershell
snid identify data/sn2003jo.dat --output-dir tutorial_results/ --complete
```

### Step 5: Review

Typical output includes: type, confidence, redshift, age, and top template.

#### Key Quality Metrics:
- **Correlation coefficient**: 0.87 (excellent)
- **Wavelength coverage**: 85% (good)
- **Template quality**: 9.2/10 (high)

---

## Part 2: Understanding Classification Results

### Classification hierarchy

```
Main Type: Ia          # Thermonuclear explosion
├── Subtype: norm      # Normal brightness/spectrum  
├── Subtype: 91bg      # Faint, peculiar
├── Subtype: 91T       # Bright, peculiar
└── Subtype: 02cx      # Very peculiar
```

### Key features

#### Type Ia Characteristics:
- **Si II λ6355**: Strong absorption feature
- **Ca II H&K**: Intermediate-mass elements
- **No hydrogen**: Lack of Balmer lines
- **Expansion velocity**: ~10,000-15,000 km/s

#### Age Determination:
- **Negative ages**: Pre-maximum light
- **Age = 0**: Maximum light
- **Positive ages**: Post-maximum light
- **Typical range**: -20 to +100 days

### Confidence

| Confidence | Interpretation | Action |
|------------|----------------|---------|
| 9-10 | Excellent match | Trust classification |
| 7-8 | Good match | Verify key features |
| 5-6 | Fair match | Check alternatives |
| <5 | Poor match | Manual inspection needed |

---

## Plots

### GUI Plotting Features

#### Interactive Plot Tools:
1. **Zoom**: Mouse wheel or selection box
2. **Pan**: Click and drag
3. **Line ID**: Hover over features
4. **Measure**: Click two points for wavelength/flux

#### Multi-Panel View:
- **Top panel**: Input spectrum vs. template
- **Middle panel**: Correlation function
- **Bottom panel**: Residuals (difference)

### CLI Plotting

```powershell
# Generate all plots
snid identify data/sn2003jo.dat --output-dir plots/ --complete

# The --complete flag generates:
# - snid_comparison.png
# - snid_3d_clustering.png
# - snid_subtype_analysis.png
# - snid_clustering_statistics.png
# - snid_redshift_age.png
```

### Publication tips

#### Best Practices:
- **High DPI**: 300+ for publications
- **Vector formats**: PDF, SVG for scalability
- **Clear labels**: Wavelength (Å), Flux units
- **Color schemes**: Colorblind-friendly options

---

## Parameters (common)

### Redshift Considerations

#### Automatic Redshift (Default):
```powershell
# Let SNID determine redshift
snid identify spectrum.dat --output-dir results/
```

#### Fixed Redshift:
```powershell
# Known redshift from host galaxy
snid identify spectrum.dat --output-dir results/ --forced-redshift 0.0234
```

#### Redshift Range:
```powershell
# Search within specific range
snid identify spectrum.dat --output-dir results/ --zmin 0.01 --zmax 0.05
```

### Template Selection

#### Type Filtering:
```powershell
# Only Type Ia templates
snid identify spectrum.dat --output-dir results/ --type-filter Ia

# Multiple types
snid identify spectrum.dat --output-dir results/ --type-filter Ia Ib Ic
```

#### Quality Filtering:
```powershell
# Age constraints
snid identify spectrum.dat --output-dir results/ --age-min -5 --age-max 20
```

### Preprocessing

#### Noise Reduction:
```powershell
# Apply smoothing
snid identify spectrum.dat --output-dir results/ --savgol-window 11 --savgol-order 3
```

#### Wavelength Masking:
```powershell
# Remove telluric features
snid identify spectrum.dat --output-dir results/ --aband-remove --skyclip
```

---

## AI (optional)

### Quick AI Summary

#### GUI Method:
1. Complete spectrum analysis
2. Click **"AI Assistant"** button (deep blue)
3. Select **"Quick Summary"**
4. Review interpretation

### Detailed AI Analysis

In the GUI AI Assistant dialog:
1. Select **"Comprehensive Analysis"**
2. Choose your preferred model
3. Review detailed scientific interpretation

### Interactive AI Chat

**Example conversation:**
```
You: What makes you confident this is a Type Ia?

AI: The classification as Type Ia is supported by several key spectral features:

1. Strong Si II λ6355 absorption at ~12,000 km/s velocity
2. Ca II H&K complex showing intermediate-mass elements  
3. Complete absence of hydrogen Balmer lines
4. Overall spectral evolution matching SN 1994D template

The correlation coefficient of 0.87 indicates an excellent match.

You: Could the age determination be wrong?

AI: The +2.1 day age estimate appears reliable because:
- Strong correlation with SN 1994D at similar phase
- Si II velocity consistent with early post-maximum
- Lack of nebular features (would appear later)
- Template library has good coverage around maximum light

However, age uncertainty is ±1.2 days, so anything from maximum
to +3 days would be consistent with the data.
```

---

## Variants

### Analysis 2: Recent Discovery

```powershell
# Load and analyze recent transient
snid identify data/tns_2024ggi.dat --output-dir results_2024ggi/
```

**Expected challenges:**
- Lower signal-to-noise ratio
- Limited wavelength coverage
- Potential host galaxy contamination

**Troubleshooting:**
```bash
# Apply additional preprocessing
snid identify data/tns_2024ggi.dat --output-dir results_2024ggi/ \
  --savgol-window 15 --savgol-order 3 \
  --wavelength-masks 5550:5600 7550:7700
```

### Analysis 3: High-Quality Spectrum

```powershell
# High-quality analysis
snid identify data/tns_2025baq.dat --output-dir results_2025baq/ --complete
```

**Advantages of high quality data:**
- Detailed line profiles
- Velocity structure visible
- Better line identification
- Improved age determination

---

## Quality checks

### Quality Indicators

#### Excellent Classification (Confidence 8-10):
- High correlation coefficient (>0.8)
- Good wavelength coverage (>70%)
- Consistent with multiple templates
- Clear spectral features

#### Good Classification (Confidence 6-8):
- Moderate correlation (0.6-0.8)
- Reasonable coverage (>50%)
- Some ambiguity in alternatives
- Most features identifiable

#### Poor Classification (Confidence <6):
- Low correlation (<0.6)
- Limited coverage (<50%)
- High uncertainty in parameters
- Requires manual inspection

### Validation Steps

#### 1. Check Alternative Matches:
In GUI: Review the results summary showing top matches
In CLI: Check the output file for alternative classifications

#### 2. Examine Key Features:
- Si II λ6355 for Type Ia
- He I lines for Type Ib
- H-alpha for Type II
- Ca II triplet for age

#### 3. Literature Comparison:
- Compare with published spectra
- Check host galaxy properties
- Verify discovery circumstances

### Common Issues and Solutions

#### Low Signal-to-Noise:
```bash
# Increase smoothing
snid identify spectrum.dat --output-dir results/ --savgol-window 21
```

#### Limited Wavelength Range:
```bash
# Focus on available range
snid identify spectrum.dat --output-dir results/ --wavelength-masks 3500:4000 8500:9000
```

---

## Save and report

### Saving Results

#### Complete Analysis Package:
```powershell
snid identify spectrum.dat --output-dir complete_analysis/ --complete
```

**Generated files:**
- `spectrum.output` - Main SNID results
- `spectrum.fluxed` - Fluxed spectrum
- `spectrum.flattened` - Flattened spectrum
- `snid_comparison.png` - Comparison plot
- `snid_3d_clustering.png` - Clustering visualization
- Additional analysis plots

### Publication Documentation

#### Methods Section Template:
```
Spectral classification was performed using SNID SAGE 
(Stoppa 2025), based on the SNID algorithm (Blondin & Tonry 2007). 
The spectrum was cross-correlated against a library of supernova 
templates spanning multiple types and subtypes. Classification 
employed FFT-based correlation with automatic redshift and age 
determination.
```

#### Results Section Template:
```
The spectrum shows characteristics consistent with a Type Ia 
supernova at +2.1 ± 1.2 days from maximum light (based on 
template matching with SN 1994D). The classification is 
supported by strong Si II λ6355 absorption at 12,000 km/s 
expansion velocity and the Ca II H&K complex typical of 
intermediate-mass elements. The correlation coefficient of 
0.87 indicates an excellent template match.
```

---

## Tutorial Summary

### What You've Learned:

- **Basic Analysis Workflow** - Load, analyze, interpret results  
- **Parameter Optimization** - Redshift, templates, preprocessing  
- **Quality Assessment** - Confidence metrics and validation  
- **Visualization** - Interactive plots and publication figures  
- **AI Integration** - Automated interpretation and insights  
- **Documentation** - Proper reporting and citation  

### Next Steps:

1. **Practice** with your own spectra
2. **Explore** advanced features (batch processing, custom templates)
3. **Learn** about specific supernova types
4. **Contribute** to the template library

### Advanced Tutorials:
- **[Batch Processing](advanced-workflows.md#batch-processing)** - Analyze multiple spectra
- **[Custom Templates](../data/custom-templates.md)** - Create your own templates  
- **[Publication Workflows](publication-ready-plots.md)** - Manuscript-ready figures
- **[AI-Assisted Analysis](ai-assisted-analysis.md)** - Advanced AI features

---

## Troubleshooting

### Common Issues:

#### "No good matches found"
- Check spectrum quality (S/N ratio)
- Verify wavelength calibration
- Try broader redshift range
- Consider preprocessing options

#### "Analysis takes too long"
- Reduce template library size with type filtering
- Use minimal mode for quick results
- Check system resources

#### "GUI buttons disabled"
- Follow the workflow order
- Ensure previous steps completed
- Check status bar for errors

### Getting Help:
- Check the [FAQ](../reference/faq.md)
- See [Troubleshooting Guide](../reference/troubleshooting.md)
- Visit [GitHub Issues](https://github.com/FiorenSt/SNID-SAGE/issues) 