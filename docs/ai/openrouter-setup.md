# OpenRouter Setup for SNID SAGE

SNID SAGE uses OpenRouter to provide AI-powered spectrum analysis. This guide covers the essential setup steps.

## Setup Overview

SNID SAGE integrates with OpenRouter to offer:
- AI-powered spectrum interpretation
- Interactive analysis assistance
- Publication-ready descriptions

## Quick Setup

### 1. Get OpenRouter API Key
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Create an account
3. Go to **API Keys** section
4. Create a new key (starts with `sk-or-...`)

### 2. Configure in SNID SAGE
1. **Launch SNID SAGE GUI**
2. **Load and analyze a spectrum** (AI Assistant button is enabled after analysis)
3. **Click AI Assistant button** (deep blue button - now enabled)
4. **Go to Settings tab** in the AI Assistant dialog
5. **Enter your API key** in the "API Key" field
6. **Test connection** using the "Test Connection" button

## Model Selection

SNID SAGE works with these OpenRouter models:

### Recommended Models
- **GPT-3.5 Turbo**: Fast, reliable for most analysis
- **GPT-4 Turbo**: Best quality for complex cases
- **Claude 3 Opus**: Excellent for scientific writing
- **Gemini Pro**: Good multilingual support

### Model Configuration
In the AI Assistant dialog:
1. **Settings tab** → **Model Selection**
2. **Fetch All Models** to see available options
3. **Select your preferred model** from the table
4. **Test the model** using "Test Selected" button

## Usage in SNID SAGE

### AI Analysis Workflow
1. **Complete SNID Analysis**: Run normal spectrum analysis first
2. **Open AI Assistant**: Click the AI Assistant button (now enabled)
3. **Choose Analysis Type**:
   - **Summary tab**: Generate comprehensive analysis
   - **Chat tab**: Interactive questions about your results

### What the AI Receives
The AI Assistant gets your SNID analysis results including:
- Classification results (type, subtype, confidence)
- Redshift and age estimates
- Template matches and correlation scores
- Spectral features and measurements
- User metadata (observer name, telescope, date)

### Integration Features
- **Context Awareness**: AI remembers your analysis results
- **Interactive Chat**: Ask follow-up questions about your spectrum
- **Export Options**: Save AI analysis with your results

## Troubleshooting

### Common Issues

**API Key Not Working**
- Check key format (should start with `sk-or-`)
- Test connection in AI Assistant Settings tab
- Verify key in OpenRouter dashboard

**Model Not Available**
- Try alternative model from the model table
- Check OpenRouter status page
- Verify model access with your account

**Analysis Fails**
- Ensure SNID analysis completed first
- Check internet connection
- Try simpler analysis type

### Error Messages

| Error | Solution |
|-------|----------|
| `401 Unauthorized` | Check API key format and validity |
| `429 Too Many Requests` | Wait or upgrade OpenRouter plan |
| `503 Service Unavailable` | Try different model or wait |
| `No analysis results` | Complete SNID analysis first |

## Privacy and Security

### Data Handling
- **Spectrum Data**: Never sent to AI models
- **Analysis Results**: Only classification results sent to AI
- **API Keys**: Stored locally, encrypted transmission

### Best Practices
- Use dedicated API key for SNID SAGE
- Monitor usage through OpenRouter dashboard
- Consider data sensitivity for cloud AI

## Next Steps

1. **Test Setup**: Run AI analysis on a sample spectrum
2. **Explore Features**: Try different analysis types
3. **Customize**: Configure preferred models and settings
4. **Integration**: Incorporate AI analysis into your workflow

For detailed AI analysis options, see [Analysis Types](analysis-types.md). 