# AI Analysis Types in SNID SAGE

SNID SAGE provides four AI analysis types to help interpret your spectrum analysis results. Each type serves different purposes in your workflow.

## Analysis Types Overview

| Type | Purpose | When to Use | Output |
|------|---------|-------------|--------|
| **Quick Summary** | Basic classification overview | Initial assessment | Brief summary |
| **Detailed Analysis** | Comprehensive feature examination | Deep investigation | Detailed report |
| **Scientific Context** | Research background | Literature review | Context information |
| **Publication Notes** | Manuscript preparation | Paper writing | Publication text |

## 1. Quick Summary

### Purpose
Get a rapid overview of your SNID analysis results.

### When to Use
- Initial assessment of new spectra
- Quick verification of classification
- Teaching and education
- Batch screening of multiple spectra

### What You Get
- Classification summary
- Key spectral features
- Confidence assessment
- Brief interpretation

### Usage
1. Complete SNID analysis in GUI
2. Click **AI Assistant** button
3. Select **Quick Summary** tab
4. Click **Generate Summary**

## 2. Detailed Analysis

### Purpose
Comprehensive examination of spectral features and physical parameters.

### When to Use
- Deep investigation of interesting spectra
- Research analysis
- Quality assessment
- Publication preparation

### What You Get
- Executive summary
- Detailed spectral feature analysis
- Physical parameter interpretation
- Template comparison
- Quality assessment
- Scientific implications
- Follow-up recommendations

### Usage
1. Run SNID analysis
2. Open **AI Assistant** dialog
3. Select **Detailed Analysis** tab
4. Configure analysis parameters
5. Generate analysis

## 3. Scientific Context

### Purpose
Provide research context and literature comparison.

### When to Use
- Research planning
- Literature review
- Grant proposals
- Collaboration discussions
- Educational purposes

### What You Get
- Research context and significance
- Literature comparison
- Similar objects in literature
- Current research questions
- Broader implications
- Future research directions

### Usage
1. Complete spectrum analysis
2. Open **AI Assistant** dialog
3. Select **Scientific Context** tab
4. Choose focus areas
5. Generate context analysis

## 4. Publication Notes

### Purpose
Generate manuscript-ready descriptions and analysis.

### When to Use
- Paper writing
- Abstract preparation
- Figure captions
- Methods sections
- Results interpretation

### What You Get
- Abstract-style summary
- Methods description
- Results presentation
- Discussion points
- Figure captions
- Key findings
- Publication recommendations

### Usage
1. Complete analysis workflow
2. Open **AI Assistant** dialog
3. Select **Publication Notes** tab
4. Choose output format
5. Generate publication content

## Configuration

### Model Selection
Configure preferred models for each analysis type:

```bash
# Set default models
python run_snid_cli.py config set ai.models.quick_summary "openai/gpt-3.5-turbo"
python run_snid_cli.py config set ai.models.detailed_analysis "anthropic/claude-3-opus"
python run_snid_cli.py config set ai.models.scientific_context "openai/gpt-4-turbo"
python run_snid_cli.py config set ai.models.publication_notes "anthropic/claude-3-opus"
```

### Output Customization
```bash
# Set output length limits
python run_snid_cli.py config set ai.output_length.quick_summary 200
python run_snid_cli.py config set ai.output_length.detailed_analysis 1000
python run_snid_cli.py config set ai.output_length.scientific_context 600
python run_snid_cli.py config set ai.output_length.publication_notes 800
```

## Workflow Integration

### Recommended Sequence

**For New Spectra:**
1. Quick Summary - Initial assessment
2. Detailed Analysis - If interesting or high quality
3. Scientific Context - For research planning
4. Publication Notes - If publishing

**For Research Projects:**
1. Scientific Context - Understand field
2. Detailed Analysis - Comprehensive study
3. Publication Notes - Manuscript preparation

**For Education:**
1. Quick Summary - Basic understanding
2. Detailed Analysis - Deep learning
3. Scientific Context - Broader implications

### Batch Processing
```bash
# Quick screening of multiple spectra
python run_snid_cli.py ai analyze-batch spectra/ --type quick --output screening/

# Detailed analysis of interesting objects
python run_snid_cli.py ai analyze-batch interesting/ --type detailed --output analysis/

# Publication preparation
python run_snid_cli.py ai analyze-batch results/ --type publication_notes --output papers/
```

## Performance Optimization

### Model Selection Strategy
```bash
# Use faster models for screening
python run_snid_cli.py ai analyze-batch spectra/ --type quick --model "openai/gpt-3.5-turbo"

# Use best models for important analysis
python run_snid_cli.py ai analyze important.json --type detailed --model "anthropic/claude-3-opus"
```

### Caching
```bash
# Enable caching for repeated analyses
python run_snid_cli.py config set ai.enable_caching true
python run_snid_cli.py config set ai.cache_duration 86400  # 24 hours
```

## Troubleshooting

### Common Issues

**Poor Quality Output**
- Check input data quality
- Try different model
- Adjust output length parameters

**Performance Issues**
- Use faster models for screening
- Enable caching
- Check internet connection

### Error Messages

| Error | Solution |
|-------|----------|
| `Analysis type not supported` | Use: quick, detailed, scientific_context, publication_notes |
| `Model not available` | Try alternative model or wait |
| `Input quality too low` | Improve data quality or use different analysis |
| `Output too long` | Reduce max_length parameter |

## Best Practices

### Effective Usage
1. **Start Simple**: Use Quick Summary first, then go deeper
2. **Ask Specific Questions**: Focus on particular features or aspects
3. **Cross-validate**: Use AI insights to guide further analysis
4. **Understand Limitations**: AI can make mistakes, verify important claims

### Research Workflow
1. **Run SNID Analysis**: Get initial classification
2. **Quick AI Summary**: Understand basic results
3. **Interactive Chat**: Explore specific questions
4. **Detailed Analysis**: Get comprehensive insights
5. **Export Results**: Save AI analysis with your data

## Next Steps

1. **Try Each Type**: Experiment with all 4 analysis types
2. **Optimize Workflow**: Develop efficient analysis sequences
3. **Customize Output**: Configure analysis parameters for your needs
4. **Batch Processing**: Set up automated workflows
5. **Integration**: Incorporate AI analysis into your research pipeline

For more information, see:
- [OpenRouter Setup](openrouter-setup.md) - Configure AI providers
- [AI Overview](overview.md) - Complete AI capabilities guide
- [AI Tutorial](../tutorials/ai-assisted-analysis.md) - Step-by-step workflow 