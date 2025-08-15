# AI Integration in SNID SAGE

SNID SAGE includes optional AI-powered analysis to help interpret your spectrum classification results. This guide covers the AI features and how to use them.

## AI Features

### Analysis Types
- **Summary Generation**: Comprehensive analysis of your SNID results
- **Interactive Chat**: Ask questions about your spectrum analysis

### Integration
- **OpenRouter**: Cloud access to AI models (GPT-4, Claude, Gemini)
- **Context Awareness**: AI receives your complete SNID analysis results
- **User Metadata**: Include observer name, telescope, and observation date

## Setup

### OpenRouter Configuration
1. Get API key from [OpenRouter.ai](https://openrouter.ai/)
2. **Load and analyze a spectrum** in SNID SAGE
3. **Click AI Assistant button** (deep blue button - now enabled after analysis)
4. **Go to Settings tab** in the AI Assistant dialog
5. **Enter your API key** and test connection

## Available Models

### Recommended Models
- **GPT-3.5 Turbo**: Fast, reliable for most analysis
- **GPT-4 Turbo**: Best quality for complex cases
- **Claude 3 Opus**: Excellent for scientific writing
- **Gemini Pro**: Good multilingual support

### Model Selection
In the AI Assistant dialog:
1. **Settings tab** → **Model Selection**
2. **Fetch All Models** to see available options
3. **Select your preferred model** from the table
4. **Test the model** using "Test Selected" button

## Usage Workflow

### Basic AI Analysis
1. **Complete SNID Analysis**: Run normal spectrum analysis first
2. **Open AI Assistant**: Click the AI Assistant button (now enabled)
3. **Summary Tab**: Generate comprehensive analysis
4. **Review Results**: AI provides interpretation of your results

### Interactive Chat
1. Complete spectrum analysis
2. Click **AI Assistant** button (now enabled)
3. Choose **Chat tab**
4. Ask questions about your results

## What the AI Receives

The AI Assistant gets your complete SNID analysis results:

### Classification Data
- Supernova type and subtype
- Confidence scores
- Template matches and correlation coefficients
- Redshift and age estimates

### Spectral Information
- Key spectral features
- Line identifications
- Velocity measurements
- Quality metrics

### User Context
- Observer name and group
- Telescope information
- Observation date
- Specific analysis requests

## Example Chat Interaction

```
You: "What makes you confident this is a Type Ia?"

AI: "Based on your SNID analysis, I'm confident this is a Type Ia 
because of several key spectral signatures:

1. The strong Si II λ6355 absorption feature
2. The Ca II H&K complex showing intermediate-mass elements
3. The overall spectral evolution matching Type Ia templates
4. The absence of hydrogen features

Your correlation coefficients with Type Ia templates are strong, 
and the redshift solution is consistent with the host galaxy properties."
```

## Configuration

### Model Settings
In the AI Assistant dialog:
1. **Settings tab** → **Model Selection**
2. Select preferred model from the table
3. Test connection

### Analysis Options
Available in the AI dialog:
- **User Metadata**: Observer name, telescope, date
- **Specific Requests**: Custom questions or focus areas
- **Model Parameters**: Token limits and response settings

## Privacy and Security

### Data Handling
- **Spectrum Data**: Never sent to AI models
- **Analysis Results**: Only classification results sent to AI
- **API Keys**: Stored locally, encrypted transmission

### Best Practices
- Use dedicated API key for SNID SAGE
- Monitor usage through OpenRouter dashboard
- Consider data sensitivity for cloud AI

## Troubleshooting

### Common Issues

**API Key Problems**
- Check format (should start with `sk-or-`)
- Test in AI Assistant Settings tab
- Verify billing in OpenRouter dashboard

**Model Access Issues**
- Some models require specific permissions
- Try alternative models if one fails
- Check OpenRouter status page for outages

**Connection Problems**
- Verify internet connection
- Check firewall settings
- Try different DNS servers

### Error Messages

**"API key not found"**
1. Enter API key in AI Assistant Settings tab
2. Restart SNID SAGE

**"Model not available"**
1. Check model name spelling
2. Verify model access with your API key
3. Try alternative model

**"Request timeout"**
1. Check internet connection
2. Try again with shorter input
3. Select faster model (GPT-3.5)

## Best Practices

### Effective Usage
1. **Start Simple**: Use Summary generation first, then chat
2. **Ask Specific Questions**: Focus on particular features
3. **Cross-validate**: Use AI insights to guide further analysis
4. **Understand Limitations**: AI can make mistakes, verify important claims

### Research Workflow
1. **Run SNID Analysis**: Get initial classification
2. **Generate Summary**: Understand basic results
3. **Interactive Chat**: Explore specific questions
4. **Export Results**: Save AI analysis with your data

## Related Documentation

- [OpenRouter Setup](openrouter-setup.md) - Detailed OpenRouter configuration
- [Analysis Types](analysis-types.md) - Different AI analysis options
- [GUI Interface](../gui/interface-overview.md) - Using the GUI for AI features 