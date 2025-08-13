# AI Analysis Types Guide

SNID SAGE offers 4 specialized AI analysis types, each designed for different aspects of supernova spectrum analysis. This guide explains each type, when to use it, and what to expect.

## Overview of Analysis Types

| Analysis Type | Purpose | Best For | Output Length | Typical Cost |
|---------------|---------|----------|---------------|--------------|
| **Quick Summary** | Rapid understanding | Initial assessment | 100-200 words | $0.001-0.005 |
| **Detailed Analysis** | Comprehensive examination | Deep investigation | 500-1000 words | $0.005-0.02 |
| **Scientific Context** | Literature comparison | Research context | 300-600 words | $0.01-0.05 |
| **Publication Notes** | Manuscript preparation | Publication writing | 400-800 words | $0.02-0.08 |

---

## 1. Quick Summary Analysis

### **Purpose**
Provide rapid, high-level understanding of classification results and key spectral features.

### **When to Use**
- **Initial assessment** of new spectra
- **Quick verification** of classification results
- **Teaching and education** - simple explanations
- **Batch processing** - rapid screening of multiple spectra
- **Real-time analysis** - immediate feedback during observations

### **What You Get**
```yaml
Output Structure:
  - Classification summary (1-2 sentences)
  - Key spectral features (3-5 bullet points)
  - Confidence assessment
  - Notable characteristics
  - Brief physical interpretation
```

### **Example Output**
```
QUICK ANALYSIS SUMMARY
======================
This spectrum shows clear characteristics of a Type Ia supernova, 
specifically matching SN 1994D around +2 days from maximum light. 
The prominent Si II λ6355 absorption and lack of hydrogen features 
confirm the thermonuclear explosion classification.

Key Features:
• Strong Si II λ6355 absorption (Type Ia signature)
• Ca II H&K lines present (intermediate-mass elements)
• No Balmer series lines (confirms lack of hydrogen)
• Broad spectral features (high expansion velocity ~12,000 km/s)

Confidence: High (8.7/10)
Classification: Type Ia-norm
```

### **Usage Examples**

#### **CLI Usage**
```bash
# Basic quick summary
python run_snid_cli.py ai analyze results.json --type quick

# With specific model
python run_snid_cli.py ai analyze results.json --type quick --model "openai/gpt-3.5-turbo"

# Batch processing
python run_snid_cli.py ai analyze-batch results/ --type quick --output summaries/
```

#### **GUI Usage**
1. Load spectrum and run analysis
2. Click **"AI Analysis"** button
3. Select **"Quick Summary"** tab
4. Click **"Generate Summary"**

---

## 2. Detailed Analysis

### **Purpose**
Comprehensive examination of spectral features, physical parameters, and detailed interpretation.

### **When to Use**
- **Deep investigation** of interesting spectra
- **Research analysis** - detailed feature examination
- **Quality assessment** - thorough evaluation of results
- **Teaching advanced concepts** - detailed explanations
- **Publication preparation** - comprehensive documentation

### **What You Get**
```yaml
Output Structure:
  - Executive summary (2-3 sentences)
  - Spectral feature analysis (detailed examination)
  - Physical parameter interpretation
  - Comparison with templates
  - Quality assessment
  - Scientific implications
  - Recommendations for follow-up
```

### **Example Output**
```
DETAILED SPECTRAL ANALYSIS
==========================

EXECUTIVE SUMMARY
This spectrum represents a well-observed Type Ia supernova at +2.1 ± 0.3 days 
from maximum light, with excellent signal-to-noise ratio (S/N ≈ 15) and 
comprehensive wavelength coverage (3500-9000 Å). The classification as Type Ia-norm 
is highly confident (8.7/10) based on strong correlation with SN 1994D template.

SPECTRAL FEATURE ANALYSIS

Primary Classification Features:
• Si II λ6355: Strong absorption at 6355.2 Å with equivalent width EW = 45 ± 3 Å
  - Characteristic of Type Ia supernovae
  - Expansion velocity: 11,800 ± 200 km/s
  - Profile shows slight asymmetry suggesting ejecta structure

• Ca II H&K: Doublet absorption at 3933.7 and 3968.5 Å
  - EW(H) = 12 ± 1 Å, EW(K) = 8 ± 1 Å
  - Velocity: 12,200 ± 300 km/s
  - Indicates intermediate-mass element synthesis

• Fe II lines: Multiple absorption features 4000-5000 Å
  - Complex blend structure typical of Type Ia
  - Velocity consistent with Si II features
  - Suggests efficient iron-group element production

Absence of Hydrogen:
• No detectable Balmer series lines (Hα, Hβ, Hγ)
• Confirms thermonuclear explosion mechanism
• Rules out Type II and Type IIn classifications

PHYSICAL PARAMETERS

Redshift: z = 0.0017 ± 0.0002
- Determined from cross-correlation with templates
- Consistent with nearby galaxy environment
- Low uncertainty due to high-quality spectrum

Age: +2.1 ± 0.3 days from maximum light
- Based on spectral evolution comparison
- Typical for well-sampled Type Ia light curves
- Suggests early discovery and follow-up

Expansion Velocity: 11,800 ± 200 km/s
- Measured from Si II λ6355 absorption minimum
- Normal for Type Ia supernovae at this phase
- Consistent with standard explosion models

QUALITY ASSESSMENT

Signal-to-Noise: S/N ≈ 15 (excellent)
- Sufficient for detailed line analysis
- Allows reliable velocity measurements
- Supports high-confidence classification

Wavelength Coverage: 85% of usable range
- Comprehensive coverage of key features
- Includes both blue and red spectral regions
- Enables robust template matching

Template Quality: 9.2/10
- SN 1994D template is well-calibrated
- Excellent phase match (+2 days)
- High-quality reference spectrum

SCIENTIFIC IMPLICATIONS

This spectrum provides strong evidence for a normal Type Ia supernova 
explosion, likely from a white dwarf exceeding the Chandrasekhar mass 
limit. The spectral features indicate efficient synthesis of 
intermediate-mass elements (Si, Ca) and iron-group elements, 
consistent with standard thermonuclear explosion models.

RECOMMENDATIONS

1. Continue spectroscopic monitoring to track spectral evolution
2. Obtain photometric data for light curve analysis
3. Consider host galaxy observations for environmental context
4. Monitor for potential late-time features or peculiarities
```

### **Usage Examples**

#### **CLI Usage**
```bash
# Detailed analysis with best model
python run_snid_cli.py ai analyze results.json --type detailed --model "anthropic/claude-3-opus"

# With custom parameters
python run_snid_cli.py ai analyze results.json --type detailed --max-length 1000 --include-uncertainties

# Export to file
python run_snid_cli.py ai analyze results.json --type detailed --output detailed_analysis.txt
```

#### **GUI Usage**
1. Run spectrum analysis
2. Open **"AI Analysis"** dialog
3. Select **"Detailed Analysis"** tab
4. Configure analysis parameters
5. Click **"Generate Analysis"**

---

## 3. Scientific Context Analysis

### **Purpose**
Provide research context, literature comparison, and scientific background for the observed spectrum.

### **When to Use**
- **Research planning** - understand current state of field
- **Literature review** - compare with similar objects
- **Grant proposals** - justify scientific importance
- **Collaboration discussions** - provide context for colleagues
- **Educational purposes** - understand broader implications

### **What You Get**
```yaml
Output Structure:
  - Research context and significance
  - Literature comparison
  - Similar objects in literature
  - Current research questions
  - Broader scientific implications
  - Future research directions
```

### **Example Output**
```
SCIENTIFIC CONTEXT ANALYSIS
===========================

RESEARCH CONTEXT

This Type Ia supernova (z = 0.0017) represents a valuable addition to the 
growing sample of nearby, well-observed thermonuclear supernovae. At this 
low redshift, it provides an excellent opportunity for detailed spectroscopic 
study with minimal cosmological effects.

SCIENTIFIC SIGNIFICANCE

Type Ia supernovae serve as critical tools for:
• Cosmological distance measurements (standard candles)
• Understanding stellar evolution and binary systems
• Probing nucleosynthesis in extreme environments
• Testing explosion physics and models

LITERATURE COMPARISON

Similar Objects:
• SN 1994D (z = 0.0015): Prototypical normal Type Ia, excellent template match
• SN 2011fe (z = 0.0008): Nearby, well-studied normal Type Ia
• SN 2014J (z = 0.0007): Extensively observed in M82

Key Differences:
• This object shows slightly higher expansion velocity than SN 1994D
• Spectral features appear more pronounced than typical normal Ia
• Age determination places it very close to maximum light

CURRENT RESEARCH QUESTIONS

This spectrum addresses several active research areas:

1. Type Ia Diversity: How much variation exists within "normal" Type Ia?
2. Progenitor Systems: What binary configurations produce normal Type Ia?
3. Explosion Physics: What mechanisms drive the explosion?
4. Cosmological Calibration: How do nearby objects inform distant measurements?

BROADER IMPLICATIONS

Understanding normal Type Ia supernovae is crucial for:
• Improving cosmological distance measurements
• Calibrating supernova-based dark energy studies
• Advancing stellar evolution theory
• Developing more accurate explosion models

FUTURE RESEARCH DIRECTIONS

Recommended follow-up studies:
1. Multi-wavelength observations (UV to IR)
2. Polarization measurements
3. Host galaxy characterization
4. Late-time spectroscopy
5. Comparison with explosion models
```

### **Usage Examples**

#### **CLI Usage**
```bash
# Scientific context analysis
python run_snid_cli.py ai analyze results.json --type scientific_context

# With literature focus
python run_snid_cli.py ai analyze results.json --type scientific_context --focus literature

# Include recent papers
python run_snid_cli.py ai analyze results.json --type scientific_context --include-recent
```

#### **GUI Usage**
1. Complete spectrum analysis
2. Open **"AI Analysis"** dialog
3. Select **"Scientific Context"** tab
4. Choose focus areas (literature, implications, etc.)
5. Generate context analysis

---

## 4. Publication Notes Analysis

### **Purpose**
Generate manuscript-ready descriptions and analysis suitable for publication.

### **When to Use**
- **Paper writing** - draft manuscript sections
- **Abstract preparation** - concise summaries
- **Figure captions** - detailed plot descriptions
- **Methods sections** - analysis descriptions
- **Results interpretation** - publication-quality analysis

### **What You Get**
```yaml
Output Structure:
  - Abstract-style summary
  - Methods description
  - Results presentation
  - Discussion points
  - Figure captions
  - Key findings
  - Publication recommendations
```

### **Example Output**
```
PUBLICATION NOTES
=================

ABSTRACT SUMMARY

We present spectroscopic observations of a Type Ia supernova at z = 0.0017, 
obtained +2.1 ± 0.3 days from maximum light. The spectrum shows strong 
Si II λ6355 absorption (EW = 45 ± 3 Å) and Ca II H&K features, confirming 
classification as a normal Type Ia supernova. Cross-correlation analysis 
yields a best match with SN 1994D template (correlation coefficient 0.87), 
with expansion velocity 11,800 ± 200 km/s. The high signal-to-noise ratio 
(S/N ≈ 15) and comprehensive wavelength coverage (3500-9000 Å) enable 
detailed spectral feature analysis and robust classification.

METHODS DESCRIPTION

Spectroscopic observations were obtained using [instrument] on [telescope] 
with [grating/grism] providing spectral resolution R ≈ [value]. Data 
reduction followed standard procedures including bias subtraction, flat 
fielding, wavelength calibration using arc lamps, and flux calibration 
using spectrophotometric standard stars. The spectrum was analyzed using 
SNID SAGE (v2.0), which employs FFT cross-correlation with a library of 
500+ template spectra. Classification confidence was assessed using 
correlation coefficients and template quality metrics.

RESULTS PRESENTATION

The spectrum exhibits characteristic Type Ia features including strong 
Si II λ6355 absorption (v = 11,800 ± 200 km/s) and Ca II H&K lines 
(v = 12,200 ± 300 km/s). No hydrogen features are detected, confirming 
the thermonuclear explosion mechanism. Cross-correlation analysis with 
SN 1994D template yields correlation coefficient 0.87, indicating 
excellent match quality. The spectrum shows no evidence of peculiar 
features or significant reddening.

DISCUSSION POINTS

1. Classification Reliability: The high correlation coefficient (0.87) 
   and absence of hydrogen features provide strong evidence for Type Ia 
   classification. The spectral features are consistent with normal 
   Type Ia supernovae at similar phases.

2. Physical Parameters: The expansion velocity (11,800 km/s) falls 
   within the normal range for Type Ia supernovae. The age determination 
   (+2.1 days) suggests early discovery and excellent temporal coverage.

3. Template Comparison: The excellent match with SN 1994D template 
   supports the "normal" subtype classification. This object appears 
   to follow standard Type Ia evolution patterns.

FIGURE CAPTIONS

Figure 1: Optical spectrum of Type Ia supernova at z = 0.0017, obtained 
+2.1 days from maximum light. Key spectral features are labeled, including 
Si II λ6355 absorption and Ca II H&K lines. The spectrum shows no 
detectable hydrogen features, confirming thermonuclear explosion mechanism. 
Template comparison (red dashed line) shows excellent agreement with 
SN 1994D at similar phase.

Figure 2: Cross-correlation function showing peak correlation coefficient 
0.87 with SN 1994D template. The narrow correlation peak indicates 
precise redshift determination and high-quality template match.

KEY FINDINGS

1. Confirmed Type Ia-norm classification with high confidence (8.7/10)
2. Expansion velocity 11,800 ± 200 km/s from Si II λ6355
3. No evidence for hydrogen or peculiar features
4. Excellent template match with SN 1994D
5. High-quality spectrum suitable for detailed analysis

PUBLICATION RECOMMENDATIONS

• Submit to ApJ, MNRAS, or A&A for publication
• Include in Type Ia supernova sample studies
• Consider for cosmological calibration work
• Valuable for template library development
• Suitable for explosion model testing
```

### **Usage Examples**

#### **CLI Usage**
```bash
# Generate publication notes
python run_snid_cli.py ai analyze results.json --type publication_notes

# With specific journal style
python run_snid_cli.py ai analyze results.json --type publication_notes --journal ApJ

# Include figure captions
python run_snid_cli.py ai analyze results.json --type publication_notes --include-figures
```

#### **GUI Usage**
1. Complete analysis workflow
2. Open **"AI Analysis"** dialog
3. Select **"Publication Notes"** tab
4. Choose output format and style
5. Generate publication-ready content

---

## Configuration Options

### **Analysis-Specific Settings**

#### **Configure Default Models**
```bash
# Set preferred models for each analysis type
python run_snid_cli.py config set ai.models.quick_summary "openai/gpt-3.5-turbo"
python run_snid_cli.py config set ai.models.detailed_analysis "anthropic/claude-3-opus"
python run_snid_cli.py config set ai.models.scientific_context "openai/gpt-4-turbo"
python run_snid_cli.py config set ai.models.publication_notes "anthropic/claude-3-opus"
```

#### **Output Customization**
```bash
# Set output length limits
python run_snid_cli.py config set ai.output_length.quick_summary 200
python run_snid_cli.py config set ai.output_length.detailed_analysis 1000
python run_snid_cli.py config set ai.output_length.scientific_context 600
python run_snid_cli.py config set ai.output_length.publication_notes 800

# Enable/disable specific sections
python run_snid_cli.py config set ai.sections.include_uncertainties true
python run_snid_cli.py config set ai.sections.include_recommendations true
python run_snid_cli.py config set ai.sections.include_literature true
```

### **Quality Control**

#### **Confidence Thresholds**
```bash
# Set minimum confidence for AI analysis
python run_snid_cli.py config set ai.min_confidence 7.0

# Require specific quality metrics
python run_snid_cli.py config set ai.require_snr 10.0
python run_snid_cli.py config set ai.require_coverage 0.8
```

---

## Workflow Integration

### **Recommended Analysis Sequence**

#### **For New Spectra**
1. **Quick Summary** - Initial assessment
2. **Detailed Analysis** - If interesting or high quality
3. **Scientific Context** - For research planning
4. **Publication Notes** - If publishing

#### **For Research Projects**
1. **Scientific Context** - Understand field
2. **Detailed Analysis** - Comprehensive study
3. **Publication Notes** - Manuscript preparation

#### **For Education**
1. **Quick Summary** - Basic understanding
2. **Detailed Analysis** - Deep learning
3. **Scientific Context** - Broader implications

### **Batch Processing Workflows**

#### **Screening Multiple Spectra**
```bash
# Quick screening of large sample
python run_snid_cli.py ai analyze-batch spectra/ --type quick --output screening/

# Detailed analysis of interesting objects
python run_snid_cli.py ai analyze-batch interesting/ --type detailed --output analysis/
```

#### **Publication Preparation**
```bash
# Generate publication notes for all results
python run_snid_cli.py ai analyze-batch results/ --type publication_notes --output papers/
```

---

## Performance Optimization

### **Cost Optimization**

#### **Model Selection Strategy**
```bash
# Use cheaper models for screening
python run_snid_cli.py ai analyze-batch spectra/ --type quick --model "openai/gpt-3.5-turbo"

# Use best models for important analysis
python run_snid_cli.py ai analyze important.json --type detailed --model "anthropic/claude-3-opus"
```

#### **Caching Strategy**
```bash
# Enable caching for repeated analyses
python run_snid_cli.py config set ai.enable_caching true
python run_snid_cli.py config set ai.cache_duration 86400  # 24 hours
```

### **Quality Optimization**

#### **Input Preparation**
- Ensure high signal-to-noise ratio (S/N > 10)
- Provide comprehensive wavelength coverage
- Include proper error estimates
- Use well-calibrated data

#### **Analysis Parameters**
- Set appropriate confidence thresholds
- Configure model-specific parameters
- Enable uncertainty propagation
- Use appropriate output length limits

---

## Troubleshooting

### **Common Issues**

#### **Poor Quality Output**
```bash
# Check input data quality
python run_snid_cli.py analyze spectrum.dat --verbose

# Try different model
python run_snid_cli.py ai analyze results.json --type detailed --model "openai/gpt-4-turbo"

# Adjust output length
python run_snid_cli.py ai analyze results.json --type detailed --max-length 1500
```

#### **Cost Issues**
```bash
# Use cheaper models for screening
python run_snid_cli.py ai analyze results.json --type quick --model "openai/gpt-3.5-turbo"

# Enable caching
python run_snid_cli.py config set ai.enable_caching true

# Set spending limits
python run_snid_cli.py config set ai.max_cost_per_request 0.05
```

### **Error Messages**

| Error | Cause | Solution |
|-------|-------|----------|
| `Analysis type not supported` | Invalid type specified | Use: quick, detailed, scientific_context, publication_notes |
| `Model not available` | Model temporarily down | Try alternative model or wait |
| `Input quality too low` | Poor spectrum quality | Improve data quality or use different analysis |
| `Output too long` | Exceeds model limits | Reduce max_length parameter |

---

## Next Steps

1. **Try Each Type**: Experiment with all 4 analysis types
2. **Optimize Workflow**: Develop efficient analysis sequences
3. **Customize Output**: Configure analysis parameters for your needs
4. **Batch Processing**: Set up automated workflows
5. **Integration**: Incorporate AI analysis into your research pipeline

For more information, see:
- **[OpenRouter Setup](openrouter-setup.md)** - Configure AI providers
- **[AI Overview](overview.md)** - Complete AI capabilities guide
- **[AI Tutorial](../tutorials/ai-assisted-analysis.md)** - Step-by-step workflow 