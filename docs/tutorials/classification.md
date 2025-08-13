# Supernova Classification Guide

Complete guide to understanding supernova classification methods, types, and interpretation in SNID SAGE.

## What is Supernova Classification?

Supernova classification involves:
- **Identifying explosion type** based on spectral features
- **Determining physical properties** from spectral analysis
- **Understanding progenitor systems** from classification
- **Predicting light curve behavior** based on type
- **Informing follow-up strategies** for observations

## Prerequisites

### **Basic Knowledge**
- Understanding of stellar evolution
- Familiarity with spectral features
- Basic astronomical terminology
- Knowledge of SNID SAGE interface

### **Sample Data**
We'll use these examples throughout:
- **Type Ia**: `sn2003jo.dat` - Thermonuclear explosion
- **Type II**: `tns_2019muj.ascii` - Core collapse
- **Type Ib/c**: Various examples - Stripped envelope

---

## Part 1: Supernova Types Overview

### **Type Ia Supernovae**

#### **Characteristics**
```yaml
Progenitor: White dwarf in binary system
Explosion: Thermonuclear runaway
Key Features:
  - No hydrogen lines
  - Strong Si II λ6355 absorption
  - Ca II H&K lines
  - Fe II line complexes
  - Broad spectral features

Subtypes:
  - Ia-norm: Normal Type Ia
  - Ia-91bg: Sub-luminous
  - Ia-91T: Super-luminous
  - Ia-02cx: Peculiar
```

#### **Spectral Evolution**
```yaml
Early Phase (-10 to 0 days):
  - Strong Si II λ6355
  - Ca II H&K prominent
  - High expansion velocities

Peak Phase (0 to +10 days):
  - Maximum Si II absorption
  - Fe II lines develop
  - Velocity begins to decline

Late Phase (+10 to +50 days):
  - Si II weakens
  - Fe II dominates
  - Co II appears
```

### **Type II Supernovae**

#### **Characteristics**
```yaml
Progenitor: Massive star (>8 M☉)
Explosion: Core collapse
Key Features:
  - Strong hydrogen lines (Balmer series)
  - P-Cygni profiles
  - Ca II lines
  - Fe II lines
  - Variable expansion velocities

Subtypes:
  - II-P: Plateau light curve
  - II-L: Linear light curve
  - II-n: Narrow lines
  - II-b: Transitional to Ib
```

#### **Spectral Evolution**
```yaml
Early Phase (-10 to 0 days):
  - Strong Hα, Hβ, Hγ
  - P-Cygni profiles
  - High expansion velocities

Peak Phase (0 to +20 days):
  - Maximum hydrogen absorption
  - Ca II develops
  - Velocity plateaus

Late Phase (+20 to +100 days):
  - Hydrogen weakens
  - Ca II strengthens
  - Fe II appears
```

### **Type Ib/c Supernovae**

#### **Characteristics**
```yaml
Progenitor: Stripped massive star
Explosion: Core collapse
Key Features:
  - No hydrogen lines
  - He I lines (Ib) or no He I (Ic)
  - O I λ7774 (Ic)
  - Ca II lines
  - High expansion velocities

Subtypes:
  - Ib: Helium present
  - Ic: No helium
  - Ic-BL: Broad-lined Ic
```

#### **Spectral Evolution**
```yaml
Early Phase (-10 to 0 days):
  - He I lines (Ib)
  - O I λ7774 (Ic)
  - High expansion velocities

Peak Phase (0 to +15 days):
  - Maximum line strengths
  - Ca II develops
  - Velocity begins decline

Late Phase (+15 to +50 days):
  - Lines weaken
  - Fe II dominates
  - Co II appears
```

---

## Part 2: Classification Methods

### **Template Matching**

#### **Cross-Correlation Analysis**
```yaml
Method: FFT-based cross-correlation
Process:
  1. Load input spectrum
  2. Compare with template library
  3. Calculate correlation function
  4. Find correlation peak
  5. Determine redshift and type

Quality Metrics:
  - Correlation coefficient (r-value)
  - Peak height and width
  - Secondary peaks
  - Template quality score
```

#### **Template Selection**
```bash
# Use specific template types
python run_snid_cli.py identify spectrum.dat \
    --types Ia,Ib,Ic,II

# Exclude certain types
python run_snid_cli.py identify spectrum.dat \
    --exclude-types II-n

# Use high-quality templates only
python run_snid_cli.py identify spectrum.dat \
    --min-quality 8.0
```

### **Feature-Based Classification**

#### **Key Spectral Features**
```yaml
Type Ia Features:
  - Si II λ6355: Primary identifier
  - Ca II H&K: Intermediate-mass elements
  - Fe II complexes: Iron-group elements
  - No hydrogen: Confirms thermonuclear

Type II Features:
  - Hα, Hβ, Hγ: Hydrogen confirmation
  - P-Cygni profiles: Expansion signature
  - Ca II lines: Intermediate elements
  - Variable velocities: Ejecta structure

Type Ib Features:
  - He I lines: Helium confirmation
  - No hydrogen: Stripped envelope
  - O I λ7774: Oxygen signature
  - High velocities: Massive progenitor

Type Ic Features:
  - O I λ7774: Primary identifier
  - No hydrogen or helium: Fully stripped
  - Ca II lines: Intermediate elements
  - High velocities: Massive progenitor
```

#### **Feature Analysis**
```bash
# Analyze specific features
python run_snid_cli.py analyze-features spectrum.dat \
    --features "Si II 6355" "Ca II H&K" "H-alpha"

# Feature strength measurement
python run_snid_cli.py measure-features spectrum.dat \
    --features "Si II 6355" \
    --output feature_measurements.txt
```

---

## Part 3: Classification Confidence

### **Confidence Assessment**

#### **Confidence Metrics**
```yaml
Correlation Coefficient (r-value):
  - 0.9-1.0: Excellent (95%+ confidence)
  - 0.8-0.9: Very Good (85-95% confidence)
  - 0.7-0.8: Good (75-85% confidence)
  - 0.6-0.7: Fair (65-75% confidence)
  - <0.6: Poor (<65% confidence)

Template Quality:
  - 9-10: Excellent template
  - 7-8: Good template
  - 5-6: Fair template
  - <5: Poor template

Data Quality:
  - S/N > 20: Excellent data
  - S/N 15-20: Good data
  - S/N 10-15: Fair data
  - S/N < 10: Poor data
```

#### **Confidence Calculation**
```bash
# Calculate classification confidence
python run_snid_cli.py confidence spectrum.dat \
    --output confidence_report.txt

# Detailed confidence analysis
python run_snid_cli.py confidence spectrum.dat \
    --detailed \
    --output detailed_confidence.txt
```

### **Uncertainty Quantification**

#### **Statistical Uncertainties**
```yaml
Redshift Uncertainty:
  - High correlation: ±0.0001
  - Good correlation: ±0.0005
  - Fair correlation: ±0.001
  - Poor correlation: ±0.005

Type Uncertainty:
  - Clear features: 95%+ confidence
  - Mixed features: 75-95% confidence
  - Weak features: 50-75% confidence
  - No clear features: <50% confidence

Phase Uncertainty:
  - Good template match: ±1 day
  - Fair template match: ±3 days
  - Poor template match: ±7 days
```

#### **Systematic Uncertainties**
```yaml
Template Bias:
  - Template library completeness
  - Template quality variations
  - Phase coverage gaps
  - Redshift range limitations

Data Quality:
  - Calibration uncertainties
  - Telluric contamination
  - Instrumental effects
  - Atmospheric conditions
```

---

## Part 4: Classification Interpretation

### **Physical Interpretation**

#### **Type Ia Interpretation**
```yaml
Progenitor System:
  - White dwarf in binary
  - Mass transfer or merger
  - Chandrasekhar mass limit
  - Carbon-oxygen composition

Explosion Mechanism:
  - Thermonuclear runaway
  - Deflagration to detonation
  - Carbon fusion ignition
  - Complete disruption

Observable Features:
  - Silicon synthesis
  - Iron-group production
  - High expansion velocities
  - Uniform light curves
```

#### **Type II Interpretation**
```yaml
Progenitor System:
  - Massive star (>8 M☉)
  - Hydrogen-rich envelope
  - Iron core collapse
  - Supergiant evolution

Explosion Mechanism:
  - Core collapse
  - Neutrino-driven explosion
  - Shock wave propagation
  - Fallback possible

Observable Features:
  - Hydrogen retention
  - Variable expansion
  - Plateau light curves
  - Complex ejecta structure
```

#### **Type Ib/c Interpretation**
```yaml
Progenitor System:
  - Stripped massive star
  - Binary interaction
  - Wolf-Rayet evolution
  - Helium or CO core

Explosion Mechanism:
  - Core collapse
  - Neutrino-driven explosion
  - Compact progenitor
  - High explosion energy

Observable Features:
  - No hydrogen
  - Helium lines (Ib)
  - Oxygen lines (Ic)
  - High velocities
```

### **Environmental Context**

#### **Host Galaxy Information**
```yaml
Type Ia Hosts:
  - All galaxy types
  - Old stellar populations
  - Low star formation
  - Metallicity correlation

Type II Hosts:
  - Star-forming galaxies
  - Young stellar populations
  - High star formation
  - Metallicity correlation

Type Ib/c Hosts:
  - Star-forming regions
  - Young stellar populations
  - High metallicity
  - Binary fraction correlation
```

#### **Redshift Evolution**
```yaml
Cosmological Effects:
  - Time dilation
  - Redshift stretching
  - K-corrections
  - Malmquist bias

Evolutionary Effects:
  - Metallicity evolution
  - Star formation history
  - Progenitor evolution
  - Environment changes
```

---

## Part 5: Advanced Classification

### **Peculiar Supernovae**

#### **Type Ia Peculiarities**
```yaml
Ia-91bg (Sub-luminous):
  - Lower peak luminosity
  - Faster light curve
  - Different spectral features
  - Sub-Chandrasekhar mass

Ia-91T (Super-luminous):
  - Higher peak luminosity
  - Slower light curve
  - Enhanced Fe III
  - Super-Chandrasekhar mass

Ia-02cx (Peculiar):
  - Intermediate properties
  - Unusual spectral evolution
  - Variable light curves
  - Uncertain mechanism
```

#### **Type II Peculiarities**
```yaml
II-n (Narrow lines):
  - Circumstellar interaction
  - Narrow emission lines
  - Variable light curves
  - Complex evolution

II-b (Transitional):
  - Hydrogen to helium transition
  - Binary interaction
  - Stripped envelope
  - Intermediate properties
```

### **Classification Challenges**

#### **Ambiguous Cases**
```yaml
Mixed Features:
  - Hydrogen + silicon
  - Weak helium lines
  - Unusual line ratios
  - Complex evolution

Low Quality Data:
  - Poor signal-to-noise
  - Limited wavelength coverage
  - Calibration issues
  - Telluric contamination

Rare Types:
  - Insufficient templates
  - Unknown features
  - Complex evolution
  - Limited understanding
```

#### **Classification Strategies**
```bash
# Use multiple methods
python run_snid_cli.py identify spectrum.dat \
    --methods template feature statistical

# Compare multiple templates
python run_snid_cli.py identify spectrum.dat \
    --top-matches 10

# Feature-based analysis
python run_snid_cli.py analyze-features spectrum.dat \
    --all-features
```

---

## Part 6: Classification Validation

### **Validation Methods**

#### **Cross-Validation**
```bash
# Cross-validate classification
python run_snid_cli.py validate-classification spectrum.dat \
    --output validation_report.txt

# Multiple validation methods
python run_snid_cli.py validate-classification spectrum.dat \
    --methods template feature statistical \
    --output comprehensive_validation.txt
```

#### **Blind Testing**
```bash
# Blind classification test
python run_snid_cli.py blind-test test_spectra/ \
    --output blind_test_results.txt

# Performance assessment
python run_snid_cli.py assess-performance test_results/ \
    --output performance_report.txt
```

### **Quality Assessment**

#### **Classification Quality**
```yaml
Accuracy Metrics:
  - True positive rate
  - False positive rate
  - Precision and recall
  - F1 score
  - Confusion matrix

Quality Factors:
  - Data quality
  - Template quality
  - Feature strength
  - Phase coverage
  - Redshift range
```

#### **Quality Improvement**
```bash
# Improve classification quality
python run_snid_cli.py improve-classification spectrum.dat \
    --methods preprocessing template_selection

# Quality optimization
python run_snid_cli.py optimize-classification spectrum.dat \
    --output optimized_results.json
```

---

## Part 7: Classification Workflows

### **Standard Classification Workflow**

#### **Step-by-Step Process**
```bash
# 1. Data preparation
python run_snid_cli.py preprocess spectrum.dat \
    --output prepared_spectrum.dat

# 2. Initial classification
python run_snid_cli.py identify prepared_spectrum.dat \
    --output initial_results.json

# 3. Confidence assessment
python run_snid_cli.py confidence initial_results.json \
    --output confidence_report.txt

# 4. Detailed analysis
python run_snid_cli.py analyze initial_results.json \
    --output detailed_analysis.txt

# 5. Validation
python run_snid_cli.py validate-classification initial_results.json \
    --output validation_report.txt
```

#### **Automated Workflow**
```bash
# Complete automated workflow
python run_snid_cli.py classify spectrum.dat \
    --workflow complete \
    --output complete_results/

# Custom workflow
python run_snid_cli.py classify spectrum.dat \
    --workflow-file custom_workflow.yaml \
    --output custom_results/
```

### **Specialized Workflows**

#### **Discovery Workflow**
```bash
# Discovery classification
python run_snid_cli.py classify spectrum.dat \
    --workflow discovery \
    --output discovery_results/
```

#### **Research Workflow**
```bash
# Research classification
python run_snid_cli.py classify spectrum.dat \
    --workflow research \
    --output research_results/
```

#### **Publication Workflow**
```bash
# Publication classification
python run_snid_cli.py classify spectrum.dat \
    --workflow publication \
    --output publication_results/
```

---

## Part 8: Classification Statistics

### **Statistical Analysis**

#### **Classification Statistics**
```bash
# Generate classification statistics
python run_snid_cli.py classification-stats results/ \
    --output classification_stats.txt

# Detailed statistics
python run_snid_cli.py classification-stats results/ \
    --detailed \
    --output detailed_stats.txt
```

#### **Performance Metrics**
```yaml
Accuracy Metrics:
  - Overall accuracy
  - Type-specific accuracy
  - Confusion matrix
  - Precision and recall

Quality Metrics:
  - Average confidence
  - Template quality
  - Data quality
  - Feature strength

Efficiency Metrics:
  - Processing time
  - Resource usage
  - Success rate
  - Error rate
```

### **Trend Analysis**

#### **Classification Trends**
```bash
# Analyze classification trends
python run_snid_cli.py analyze-trends results/ \
    --output trend_analysis.txt

# Temporal trends
python run_snid_cli.py analyze-trends results/ \
    --temporal \
    --output temporal_trends.txt
```

---

## Part 9: Troubleshooting

### **Common Classification Issues**

#### **Low Confidence Classifications**
```bash
# Diagnose low confidence
python run_snid_cli.py diagnose-confidence spectrum.dat \
    --output diagnosis_report.txt

# Improve confidence
python run_snid_cli.py improve-confidence spectrum.dat \
    --output improved_results.json
```

#### **Ambiguous Classifications**
```bash
# Resolve ambiguity
python run_snid_cli.py resolve-ambiguity spectrum.dat \
    --output resolved_results.json

# Multiple analysis methods
python run_snid_cli.py identify spectrum.dat \
    --methods template feature statistical
```

#### **Classification Errors**
```bash
# Debug classification errors
python run_snid_cli.py debug-classification spectrum.dat \
    --output debug_report.txt

# Error analysis
python run_snid_cli.py analyze-errors results/ \
    --output error_analysis.txt
```

### **Quality Issues**

#### **Data Quality Problems**
```bash
# Assess data quality
python run_snid_cli.py assess-quality spectrum.dat \
    --output quality_report.txt

# Improve data quality
python run_snid_cli.py improve-quality spectrum.dat \
    --output improved_spectrum.dat
```

#### **Template Quality Issues**
```bash
# Assess template quality
python run_snid_cli.py assess-templates \
    --output template_quality.txt

# Select better templates
python run_snid_cli.py select-templates spectrum.dat \
    --min-quality 8.0
```

---

## Part 10: Best Practices

### **Classification Guidelines**

#### **General Guidelines**
1. **Start with good data**: Ensure high-quality input spectra
2. **Use appropriate templates**: Select relevant template types
3. **Assess confidence**: Always check classification confidence
4. **Validate results**: Use multiple validation methods
5. **Document process**: Keep detailed classification records

#### **Quality Assurance**
1. **Check data quality**: Verify signal-to-noise and coverage
2. **Review template matches**: Examine best template matches
3. **Assess feature strength**: Verify key spectral features
4. **Consider context**: Use host galaxy and environment information
5. **Validate independently**: Use multiple classification methods

### **Workflow Optimization**

#### **Efficiency Tips**
1. **Use appropriate methods**: Choose methods based on data quality
2. **Optimize template selection**: Use relevant template subsets
3. **Batch process**: Process multiple spectra together
4. **Monitor performance**: Track classification accuracy
5. **Update regularly**: Keep template library current

#### **Accuracy Tips**
1. **Use high-quality templates**: Prefer high-quality template matches
2. **Consider phase information**: Use appropriate phase templates
3. **Check for peculiarities**: Look for unusual features
4. **Validate with features**: Confirm template matches with features
5. **Use multiple epochs**: Analyze temporal evolution when possible

---

## Future Developments

### **Planned Features**

#### **Advanced Classification**
- **Machine learning**: ML-based classification methods
- **Feature learning**: Automated feature identification
- **Real-time classification**: Live classification capabilities
- **Multi-wavelength**: Classification using multiple wavelengths

#### **Enhanced Validation**
- **Automated validation**: Automatic validation procedures
- **Quality assessment**: Advanced quality metrics
- **Performance monitoring**: Real-time performance tracking
- **Error analysis**: Comprehensive error analysis

### **Community Development**

#### **Classification Standards**
- **Standard procedures**: Community classification standards
- **Quality metrics**: Standardized quality measures
- **Validation protocols**: Standard validation methods
- **Performance benchmarks**: Community benchmarks

---

## Support & Resources

### **Documentation**
- **[Basic Analysis](basic-analysis.md)** - Basic analysis tutorial
- **[Advanced Analysis](advanced-analysis.md)** - Advanced analysis features
- **[Template Management](template-management.md)** - Template system guide

### **Tools & Utilities**
```bash
# Classification commands
python run_snid_cli.py identify --help

# Confidence assessment
python run_snid_cli.py confidence --help

# Validation tools
python run_snid_cli.py validate-classification --help
```

### **Community Support**
- **GitHub Issues**: Report classification problems
- **Discussions**: Classification-related questions
- **Contributions**: Submit classification improvements
- **Feedback**: Classification feature suggestions

---

## References

### **Key Publications**
- **SNID Paper**: Blondin & Tonry 2007, ApJ, 666, 1024
- **Supernova Classification**: Various classification schemes
- **Spectral Features**: Standard spectral feature identifications

### **Resources**
- **Template Libraries**: Various template collections
- **Classification Schemes**: Standard classification systems
- **Feature Catalogs**: Spectral feature databases

For more information, see:
- **[Basic Analysis](basic-analysis.md)** - Basic analysis tutorial
- **[Advanced Analysis](advanced-analysis.md)** - Advanced analysis features
- **[Template Management](template-management.md)** - Template system guide 