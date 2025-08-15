# AI-Assisted Analysis Tutorial

This tutorial walks you through using AI features in SNID SAGE to enhance your spectrum analysis workflow.

## Prerequisites

- SNID SAGE installed and working
- OpenRouter API key configured
- Sample spectrum for analysis

## Setup

### 1. Configure AI Integration
1. Launch SNID SAGE GUI
2. **Load and analyze a spectrum** (AI Assistant button is enabled after analysis)
3. **Click AI Assistant button** (deep blue button - now enabled)
4. **Go to Settings tab** in the AI Assistant dialog
5. Enter your OpenRouter API key
6. Test connection
7. Select preferred model (GPT-3.5 Turbo recommended for testing)

### 2. Prepare Sample Data
For this tutorial, we'll use a Type Ia supernova spectrum:
- Download: [SN 2024ggi spectrum](https://www.wis-tns.org/object/2024ggi)
- Save as `data/sn2024ggi.dat`

## Tutorial Workflow

### Step 1: Basic SNID Analysis
1. **Load Spectrum**: Click **Load Spectrum** → select `sn2024ggi.dat`
2. **Preprocess**: Click **Preprocessing** → **Quick SNID Preprocessing**
3. **Analyze**: Click **SNID Analysis** → wait for completion
4. **Review Results**: Check classification, redshift, and age

### Step 2: Configure AI (After Analysis)
1. **Open AI Assistant**: Click the **AI Assistant** button (now enabled)
2. **Go to Settings**: Click the **Settings** tab
3. **Enter API Key**: Add your OpenRouter API key
4. **Test Connection**: Verify the connection works
5. **Select Model**: Choose your preferred model

### Step 3: Quick AI Summary
1. **Go to Summary Tab**: Click the **Summary** tab
2. **Add Metadata**: Enter observer name, telescope, date (optional)
3. **Generate**: Click **Generate Summary**
4. **Review**: Read the AI interpretation of your results

**Expected Output**: Brief overview of classification, key features, and confidence assessment.

### Step 4: Interactive Chat
1. **Start Chat**: Click **Chat** tab
2. **Ask Questions**: Try these examples:
   - "What makes this a Type Ia supernova?"
   - "How confident should I be in this classification?"
   - "What follow-up observations would be useful?"

## Advanced Features

### Model Comparison
Test different models for the same analysis:

1. **GPT-3.5 Turbo**: Fast, good for routine analysis
2. **GPT-4 Turbo**: Higher quality, better for complex cases
3. **Claude 3 Opus**: Excellent for scientific writing
4. **Gemini Pro**: Good for multilingual work

### Batch Analysis
For multiple spectra:
```bash
# Quick screening
python run_snid_cli.py ai analyze-batch spectra/ --type quick --output screening/

# Detailed analysis of interesting objects
python run_snid_cli.py ai analyze-batch interesting/ --type detailed --output analysis/
```

### Custom Configuration
```bash
# Set preferred models
python run_snid_cli.py config set ai.models.quick_summary "openai/gpt-3.5-turbo"
python run_snid_cli.py config set ai.models.detailed_analysis "anthropic/claude-3-opus"

# Enable caching
python run_snid_cli.py config set ai.enable_caching true
```

## Best Practices

### Effective AI Usage
1. **Complete SNID First**: Always run normal analysis before AI
2. **Start Simple**: Use Summary generation for initial assessment
3. **Ask Specific Questions**: Focus on particular features or aspects
4. **Cross-validate**: Use AI insights to guide further analysis
5. **Understand Limitations**: AI can make mistakes, verify important claims

### Research Workflow
1. **Initial Assessment**: SNID analysis + AI summary
2. **Deep Investigation**: Interactive chat for specific questions
3. **Context Building**: Use AI for research planning
4. **Publication Prep**: Export AI analysis for manuscript writing

### Quality Control
- **Check Input Quality**: Ensure good signal-to-noise ratio
- **Verify Results**: Cross-check AI interpretations with SNID results
- **Use Multiple Models**: Compare outputs from different AI models
- **Export and Save**: Keep AI analysis with your data

## Troubleshooting

### Common Issues

**AI Not Working**
- Check API key configuration in AI Assistant Settings tab
- Verify internet connection
- Test with different model

**Poor Quality Output**
- Ensure SNID analysis completed first
- Try different analysis type
- Check input data quality

**Slow Performance**
- Use faster models (GPT-3.5)
- Enable caching
- Check OpenRouter status

### Error Messages

| Error | Solution |
|-------|----------|
| `No analysis results` | Complete SNID analysis first |
| `API key not found` | Configure in AI Assistant Settings tab |
| `Model not available` | Try alternative model |
| `Request timeout` | Check internet connection |

## Next Steps

1. **Practice**: Try AI analysis on different spectrum types
2. **Customize**: Configure preferred models and settings
3. **Integrate**: Incorporate AI analysis into your research workflow
4. **Explore**: Try batch processing and advanced features

## Related Documentation

- [AI Overview](../ai/overview.md) - Complete AI capabilities guide
- [OpenRouter Setup](../ai/openrouter-setup.md) - Configuration guide
- [GUI Interface](../gui/interface-overview.md) - Using the GUI

