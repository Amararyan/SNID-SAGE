# AI-Assisted Analysis Tutorial

Complete tutorial for using AI-powered analysis features in SNID SAGE to enhance your supernova spectrum analysis.

## What is AI-Assisted Analysis?

AI-assisted analysis in SNID SAGE provides:
- **Intelligent interpretation** of classification results
- **Automated feature identification** and analysis
- **Scientific context** and literature comparison
- **Publication-ready descriptions** and insights
- **Interactive chat** about your spectra

## Prerequisites

### **Setup Requirements**
- SNID SAGE installed and configured
- OpenRouter API key set up (see [OpenRouter Setup](../ai/openrouter-setup.md))
- Sample spectrum data for analysis
- Basic understanding of supernova types

### **Sample Data**
We'll use these spectra for the tutorial:
- **`sn2003jo.dat`** - High-quality Type Ia supernova
- **`tns_2019muj.ascii`** - Modern transient discovery
- **`ATLAS25egg_MagE.txt`** - High-resolution spectrum

---

## Part 1: Quick AI Analysis

### **Step 1: Basic Spectrum Analysis**

First, let's run a standard SNID analysis:

```bash
# Run basic analysis
python run_snid_cli.py identify data/sn2003jo.dat \
    --output-dir ai_tutorial_results/ \
    --complete
```

### **Step 2: Generate Quick AI Summary**

#### **CLI Method**
```bash
# Generate quick summary
python run_snid_cli.py ai analyze ai_tutorial_results/sn2003jo_results.json \
    --type quick

# With specific model
python run_snid_cli.py ai analyze ai_tutorial_results/sn2003jo_results.json \
    --type quick \
    --model "openai/gpt-3.5-turbo"
```

#### **GUI Method**
1. Load spectrum and run analysis
2. Click **"AI Analysis"** button
3. Select **"Quick Summary"** tab
4. Click **"Generate Summary"**

### **Step 3: Understanding the Output**

#### **Expected Quick Summary**
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

---

## Part 2: Detailed AI Analysis

### **Step 1: Generate Detailed Analysis**

#### **CLI Method**
```bash
# Generate detailed analysis
python run_snid_cli.py ai analyze ai_tutorial_results/sn2003jo_results.json \
    --type detailed \
    --model "anthropic/claude-3-opus"

# Save to file
python run_snid_cli.py ai analyze ai_tutorial_results/sn2003jo_results.json \
    --type detailed \
    --output detailed_analysis.txt
```

#### **GUI Method**
1. Open **"AI Analysis"** dialog
2. Select **"Detailed Analysis"** tab
3. Choose analysis parameters
4. Click **"Generate Analysis"**

### **Step 2: Understanding Detailed Output**

#### **Detailed Analysis Structure**
```yaml
Output Sections:
  - Executive Summary: High-level overview
  - Spectral Feature Analysis: Detailed line analysis
  - Physical Parameters: Redshift, age, velocity
  - Quality Assessment: Data quality metrics
  - Scientific Implications: Physical interpretation
  - Recommendations: Follow-up suggestions
```

#### **Example Detailed Analysis**
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

---

## Part 3: Scientific Context Analysis

### **Step 1: Generate Scientific Context**

#### **CLI Method**
```bash
# Generate scientific context
python run_snid_cli.py ai analyze ai_tutorial_results/sn2003jo_results.json \
    --type scientific_context \
    --model "openai/gpt-4-turbo"

# Focus on specific aspects
python run_snid_cli.py ai analyze ai_tutorial_results/sn2003jo_results.json \
    --type scientific_context \
    --focus literature
```

#### **GUI Method**
1. Open **"AI Analysis"** dialog
2. Select **"Scientific Context"** tab
3. Choose focus areas (literature, implications, etc.)
4. Generate context analysis

### **Step 2: Understanding Scientific Context**

#### **Scientific Context Structure**
```yaml
Output Sections:
  - Research Context: Broader scientific significance
  - Literature Comparison: Similar objects in literature
  - Current Research Questions: Active research areas
  - Broader Implications: Scientific impact
  - Future Research Directions: Recommended studies
```

#### **Example Scientific Context**
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

---

## Part 4: Publication Notes Analysis

### **Step 1: Generate Publication Notes**

#### **CLI Method**
```bash
# Generate publication notes
python run_snid_cli.py ai analyze ai_tutorial_results/sn2003jo_results.json \
    --type publication_notes \
    --model "anthropic/claude-3-opus"

# With specific journal style
python run_snid_cli.py ai analyze ai_tutorial_results/sn2003jo_results.json \
    --type publication_notes \
    --journal ApJ

# Include figure captions
python run_snid_cli.py ai analyze ai_tutorial_results/sn2003jo_results.json \
    --type publication_notes \
    --include-figures
```

#### **GUI Method**
1. Complete analysis workflow
2. Open **"AI Analysis"** dialog
3. Select **"Publication Notes"** tab
4. Choose output format and style
5. Generate publication-ready content

### **Step 2: Understanding Publication Notes**

#### **Publication Notes Structure**
```yaml
Output Sections:
  - Abstract Summary: Manuscript-ready abstract
  - Methods Description: Analysis methodology
  - Results Presentation: Key findings
  - Discussion Points: Scientific interpretation
  - Figure Captions: Plot descriptions
  - Key Findings: Main results
  - Publication Recommendations: Journal suggestions
```

#### **Example Publication Notes**
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

---

## Part 5: Interactive AI Chat

### **Step 1: Start AI Chat Session**

#### **CLI Method**
```bash
# Start interactive chat
python run_snid_cli.py ai chat

# Chat with specific model
python run_snid_cli.py ai chat --model "anthropic/claude-3-opus"

# Load analysis context
python run_snid_cli.py ai chat --context ai_tutorial_results/sn2003jo_results.json
```

#### **GUI Method**
1. Open **"AI Analysis"** dialog
2. Select **"Interactive Chat"** tab
3. Choose AI model and persona
4. Start conversation about your spectrum

### **Step 2: Example Chat Session**

#### **Sample Conversation**
```
User: What makes this spectrum typical of a Type Ia supernova?

AI: This spectrum shows several key characteristics typical of Type Ia supernovae:

1. **Si II λ6355 absorption**: This is the most distinctive feature of Type Ia supernovae. The strong absorption at 6355 Å indicates the presence of silicon, which is synthesized in thermonuclear explosions.

2. **Absence of hydrogen**: Unlike Type II supernovae, there are no Balmer series lines (Hα, Hβ, Hγ), confirming the lack of hydrogen in the progenitor system.

3. **Ca II H&K lines**: The presence of calcium lines at 3933.7 and 3968.5 Å indicates intermediate-mass element synthesis, typical of Type Ia explosions.

4. **Broad spectral features**: The lines show significant broadening due to high expansion velocities (~12,000 km/s), characteristic of Type Ia supernovae.

5. **Fe II line complexes**: Multiple iron absorption features in the 4000-5000 Å range indicate efficient iron-group element production.

The combination of these features, along with the excellent match to SN 1994D template, provides strong evidence for a normal Type Ia classification.

User: How does the expansion velocity compare to other Type Ia supernovae?

AI: The expansion velocity of 11,800 ± 200 km/s from Si II λ6355 is quite typical for normal Type Ia supernovae at this phase (+2.1 days from maximum light).

**Comparison with other Type Ia supernovae:**
- **SN 1994D**: ~11,500 km/s at similar phase
- **SN 2011fe**: ~11,200 km/s at maximum
- **SN 2014J**: ~12,100 km/s at +2 days

**Velocity ranges for normal Type Ia:**
- Early phase (-10 to 0 days): 10,000-13,000 km/s
- Peak phase (0 to +10 days): 9,000-12,000 km/s
- Late phase (+10 to +50 days): 8,000-11,000 km/s

Your object's velocity of 11,800 km/s falls right in the middle of the normal range, supporting the "normal" subtype classification. This velocity is consistent with standard Chandrasekhar-mass white dwarf explosions.

**Interesting note**: The velocity is slightly higher than SN 1994D (the best template match), which might indicate slightly different ejecta structure or viewing angle effects.

User: What follow-up observations would you recommend?

AI: Based on this high-quality spectrum, I'd recommend several follow-up observations:

**Immediate follow-up (next few days):**
1. **Continued spectroscopy**: Monitor spectral evolution, especially Si II velocity evolution
2. **Photometry**: Obtain light curve data to determine peak magnitude and light curve shape
3. **Multi-wavelength**: UV observations to probe the outer ejecta

**Short-term (next few weeks):**
1. **Host galaxy imaging**: Determine host galaxy type and environment
2. **Polarization**: Spectropolarimetry to probe ejecta asymmetry
3. **Near-IR**: IR spectroscopy to study iron-group elements

**Medium-term (next few months):**
1. **Late-time spectroscopy**: Monitor for nebular phase features
2. **Host galaxy spectroscopy**: Measure host metallicity and star formation rate
3. **Radio observations**: Search for circumstellar interaction

**Long-term considerations:**
1. **Hubble Space Telescope**: High-resolution imaging and spectroscopy
2. **JWST observations**: Mid-IR spectroscopy for dust and molecule formation
3. **X-ray observations**: Search for circumstellar material interaction

**Priority recommendations:**
- **Photometry** is highest priority for light curve analysis
- **Continued spectroscopy** for velocity evolution
- **Host galaxy** observations for environmental context

This object's high quality and normal Type Ia classification make it an excellent candidate for detailed follow-up studies.
```

---

## Part 6: Batch AI Analysis

### **Step 1: Prepare Multiple Spectra**

```bash
# Analyze multiple spectra
python run_snid_cli.py identify-batch data/ \
    --output-dir batch_results/ \
    --complete
```

### **Step 2: Batch AI Analysis**

#### **Quick Summaries for All**
```bash
# Generate quick summaries for all results
python run_snid_cli.py ai analyze-batch batch_results/ \
    --type quick \
    --output ai_summaries/

# With specific model
python run_snid_cli.py ai analyze-batch batch_results/ \
    --type quick \
    --model "openai/gpt-3.5-turbo" \
    --output ai_summaries/
```

#### **Detailed Analysis for Selected**
```bash
# Detailed analysis for high-quality results
python run_snid_cli.py ai analyze-batch batch_results/ \
    --type detailed \
    --min-quality 8.0 \
    --model "anthropic/claude-3-opus" \
    --output detailed_analysis/
```

#### **Publication Notes for Best**
```bash
# Publication notes for best results
python run_snid_cli.py ai analyze-batch batch_results/ \
    --type publication_notes \
    --min-quality 9.0 \
    --model "anthropic/claude-3-opus" \
    --output publication_notes/
```

### **Step 3: Batch Results Management**

#### **Organize Results**
```bash
# Create organized output structure
mkdir -p ai_batch_results/{summaries,detailed,publication}

# Move results to organized structure
python run_snid_cli.py ai organize-batch-results \
    --input ai_summaries/ \
    --output ai_batch_results/summaries/

python run_snid_cli.py ai organize-batch-results \
    --input detailed_analysis/ \
    --output ai_batch_results/detailed/

python run_snid_cli.py ai organize-batch-results \
    --input publication_notes/ \
    --output ai_batch_results/publication/
```

#### **Generate Summary Report**
```bash
# Create batch summary report
python run_snid_cli.py ai batch-summary \
    --input ai_batch_results/ \
    --output batch_summary_report.txt
```

---

## Part 7: Advanced AI Configuration

### **Model Selection Strategy**

#### **Cost vs. Quality Optimization**
```bash
# Use cheaper models for screening
python run_snid_cli.py ai analyze-batch results/ \
    --type quick \
    --model "openai/gpt-3.5-turbo"

# Use best models for important analysis
python run_snid_cli.py ai analyze important.json \
    --type detailed \
    --model "anthropic/claude-3-opus"
```

#### **Analysis-Specific Models**
```bash
# Configure models for different analysis types
python run_snid_cli.py config set ai.models.quick_summary "openai/gpt-3.5-turbo"
python run_snid_cli.py config set ai.models.detailed_analysis "anthropic/claude-3-opus"
python run_snid_cli.py config set ai.models.scientific_context "openai/gpt-4-turbo"
python run_snid_cli.py config set ai.models.publication_notes "anthropic/claude-3-opus"
```

### **Performance Optimization**

#### **Caching Strategy**
```bash
# Enable caching for repeated analyses
python run_snid_cli.py config set ai.enable_caching true
python run_snid_cli.py config set ai.cache_duration 86400  # 24 hours

# Clear cache if needed
python run_snid_cli.py ai clear-cache
```

#### **Cost Management**
```bash
# Set spending limits
python run_snid_cli.py config set ai.daily_spending_limit 10.00
python run_snid_cli.py config set ai.max_cost_per_request 0.10

# Track usage
python run_snid_cli.py ai usage --provider openrouter
```

---

## Part 8: AI Analysis Workflows

### **Research Workflow**

#### **Discovery Workflow**
```bash
# 1. Quick screening
python run_snid_cli.py ai analyze-batch new_spectra/ \
    --type quick \
    --output screening/

# 2. Detailed analysis of interesting objects
python run_snid_cli.py ai analyze-batch interesting/ \
    --type detailed \
    --output detailed/

# 3. Scientific context for research planning
python run_snid_cli.py ai analyze-batch research_candidates/ \
    --type scientific_context \
    --output context/

# 4. Publication notes for best results
python run_snid_cli.py ai analyze-batch publication_candidates/ \
    --type publication_notes \
    --output publication/
```

#### **Publication Workflow**
```bash
# 1. Generate publication notes
python run_snid_cli.py ai analyze results.json \
    --type publication_notes \
    --journal ApJ

# 2. Interactive refinement
python run_snid_cli.py ai chat --context results.json

# 3. Final review and editing
# Manually review and edit AI-generated content
```

### **Educational Workflow**

#### **Learning Workflow**
```bash
# 1. Quick understanding
python run_snid_cli.py ai analyze spectrum.dat --type quick

# 2. Detailed learning
python run_snid_cli.py ai analyze spectrum.dat --type detailed

# 3. Interactive questions
python run_snid_cli.py ai chat --context results.json

# 4. Scientific context
python run_snid_cli.py ai analyze spectrum.dat --type scientific_context
```

---

## Part 9: Troubleshooting

### **Common Issues**

#### **API Key Problems**
```bash
# Check API key
echo $OPENROUTER_API_KEY

# Test connection
python run_snid_cli.py ai test --provider openrouter

# Regenerate key if needed
# Go to OpenRouter dashboard → API Keys → Create New Key
```

#### **Model Availability**
```bash
# Check available models
python run_snid_cli.py ai models --provider openrouter

# Try alternative model
python run_snid_cli.py ai analyze results.json \
    --model "openai/gpt-3.5-turbo"
```

#### **Cost Issues**
```bash
# Use cheaper models
python run_snid_cli.py ai analyze results.json \
    --type quick \
    --model "openai/gpt-3.5-turbo"

# Enable caching
python run_snid_cli.py config set ai.enable_caching true

# Set spending limits
python run_snid_cli.py config set ai.max_cost_per_request 0.05
```

### **Quality Issues**

#### **Poor AI Output**
```bash
# Try different model
python run_snid_cli.py ai analyze results.json \
    --type detailed \
    --model "anthropic/claude-3-opus"

# Adjust output length
python run_snid_cli.py ai analyze results.json \
    --type detailed \
    --max-length 1500

# Check input data quality
python run_snid_cli.py analyze spectrum.dat --verbose
```

---

## Part 10: Best Practices

### **AI Analysis Guidelines**

#### **Model Selection**
1. **Quick tasks** → GPT-3.5 Turbo (cheaper, faster)
2. **Complex analysis** → GPT-4 Turbo (better reasoning)
3. **Scientific work** → Claude 3 Opus (excellent for science)
4. **Publication** → Claude 3 Opus (high-quality output)

#### **Cost Optimization**
1. **Use appropriate models** for each task
2. **Enable caching** for repeated analyses
3. **Set spending limits** to control costs
4. **Compress context** for long analyses

#### **Quality Assurance**
1. **Review AI output** before using
2. **Cross-check results** with manual analysis
3. **Use multiple models** for important work
4. **Validate against known standards**

### **Workflow Optimization**

#### **Efficiency Tips**
1. **Batch process** similar analyses
2. **Use appropriate analysis types** for your needs
3. **Organize results** systematically
4. **Document AI usage** in your research

#### **Integration Tips**
1. **Incorporate AI analysis** into your workflow
2. **Use AI for initial screening** of large datasets
3. **Combine AI insights** with traditional analysis
4. **Validate AI results** with independent methods

---

## Support & Resources

### **Documentation**
- **[AI Overview](../ai/overview.md)** - Complete AI capabilities guide
- **[OpenRouter Setup](../ai/openrouter-setup.md)** - Setup instructions
- **[Analysis Types](../ai/analysis-types.md)** - Detailed analysis explanations

### **Tools & Utilities**
```bash
# AI analysis commands
python run_snid_cli.py ai --help

# Model management
python run_snid_cli.py ai models --help

# Usage tracking
python run_snid_cli.py ai usage --help
```

### **Community Support**
- **GitHub Issues**: Report AI analysis problems
- **Discussions**: AI-related questions
- **Contributions**: Submit AI improvements
- **Feedback**: AI feature suggestions

---

## References

### **Key Publications**
- **AI in Astronomy**: Various papers on AI applications in astronomy
- **Supernova Classification**: Standard classification methods
- **Machine Learning**: ML applications in spectral analysis

### **Resources**
- **OpenRouter Documentation**: [docs.openrouter.ai](https://docs.openrouter.ai/)
- **AI Model Papers**: Original papers for various AI models
- **Astronomical Data Standards**: Standard data formats and quality measures

For more information, see:
- **[AI Overview](../ai/overview.md)** - Complete AI capabilities guide
- **[OpenRouter Setup](../ai/openrouter-setup.md)** - Setup instructions
- **[Analysis Types](../ai/analysis-types.md)** - Detailed analysis explanations 