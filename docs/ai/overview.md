# AI Integration Overview

SNID SAGE incorporates advanced AI capabilities to provide intelligent spectrum analysis, automated interpretation, and interactive assistance. This guide covers all AI features and how to use them effectively.

## AI Capabilities

### Comprehensive AI Analysis
- **Single Comprehensive Summary** - Complete spectral interpretation including classification, confidence assessment, and scientific context
- **Context-Aware Chat** - Interactive conversation about your spectrum analysis
- **Publication-Ready Descriptions** - Manuscript-quality scientific descriptions

### AI Provider
- **OpenRouter** - Cloud access to 15+ state-of-the-art models including GPT-4, Claude, and Gemini
- **Local LLM** - Future feature for offline analysis (not yet available)

### Interactive Features
- Interactive chat about spectra
- Context awareness (remembers results within the session)

## Quick Setup

### Option 1: OpenRouter (Recommended)
```bash
# 1. Get API key from https://openrouter.ai/
# 2. Set environment variable
export OPENROUTER_API_KEY="your_key_here"

# 3. Test connection in GUI
# Launch GUI and click Settings → Configure AI
```

### Option 2: Local LLM (Future Feature)
```bash
# Local LLM support will be available in future releases
# This will allow offline AI analysis without internet connection
```

## OpenRouter Setup

### Getting Your API Key
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Create an account
3. Navigate to **API Keys** section
4. Generate a new key
5. Copy the key (starts with `sk-or-...`)

### Configuration Methods

#### Method 1: GUI Configuration (Recommended)
1. Launch SNID SAGE GUI
2. Click **Settings** button
3. Select **Configure AI**
4. Enter your API key
5. Test connection

#### Method 2: Environment Variable
```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="your_key_here"

# macOS/Linux
export OPENROUTER_API_KEY="your_key_here"

# Make permanent (Linux/macOS)
echo 'export OPENROUTER_API_KEY="your_key_here"' >> ~/.bashrc
```

#### Method 3: Configuration File
```bash
# Edit configuration file directly
# ~/.snidanalyzer/openrouter_config.json
{
  "api_key": "your_key_here",
  "model_id": "openai/gpt-3.5-turbo"
}
```

### Available Models

#### Top Recommended Models
```yaml
# High Performance
"openai/gpt-4-turbo": "Most capable, best reasoning"
"anthropic/claude-3-opus": "Excellent scientific analysis"
"google/gemini-pro": "Strong multilingual support"

# Balanced Performance/Cost
"openai/gpt-3.5-turbo": "Fast, cost-effective"
"anthropic/claude-3-sonnet": "Good balance"
"meta-llama/llama-3-70b": "Open source alternative"

# Specialized
"cohere/command-r-plus": "Strong summarization"
"mistralai/mixtral-8x7b-instruct": "Fast reasoning"
```

## AI Analysis Features

### 1. Comprehensive Summary
**Best for:** Complete understanding of classification results

After running SNID analysis in the GUI:
1. Click **"AI Assistant"** button (deep blue)
2. Select **"Comprehensive Analysis"**
3. Choose your preferred model
4. Review the detailed analysis

Example outputs are displayed in the AI dialog; copy/export as needed.

### 2. Interactive Chat
**Best for:** Asking specific questions about your analysis

1. Complete spectrum analysis
2. Click **"AI Assistant"** button
3. Choose **"Interactive Chat"**
4. Select AI persona and model
5. Start conversing about your results

## Interactive Chat Interface

### AI Personas
Choose a style (scientist, educator, reviewer) to tailor tone.

### Chat Features

#### Context Awareness
```
You: "What makes you confident this is a Type Ia?"

AI: "Based on your analysis of SN 2003jo, I'm confident it's 
a Type Ia because of three key spectral signatures:

1. The strong Si II λ6355 absorption at ~12,000 km/s velocity
2. The Ca II H&K complex showing intermediate-mass elements
3. The overall spectral evolution matching SN 1994D at +2 days

Your correlation coefficient of 0.87 with the SN 1994D template 
is quite strong, and the redshift solution of z=0.0017 is 
consistent with the host galaxy properties."
```

#### Follow-up Questions
```
You: "Could this be a peculiar Type Ia instead?"

AI: "That's a good question. Looking at your spectrum, I don't 
see strong indicators of peculiarity:

- No unusually strong Ti II features (91bg-like)
- Si II velocity is normal (~12,000 km/s, not high-velocity)
- No prominent C II features (91T-like)
- Good match to normal Ia template

The confidence score and spectral features support a normal 
Type Ia classification rather than a peculiar subtype."
```

## Configuration and Customization

### Model Selection
In the GUI:
1. Click **Settings** → **Configure AI**
2. Select preferred model from dropdown
3. Test connection

### Analysis Customization
Available options in the AI dialog:
- **Analysis Depth**: Quick, Standard, or Comprehensive
- **Output Format**: Summary, Detailed, or Publication-ready
- **Focus Areas**: Classification, Features, or Context

## Privacy and Security

### Data Privacy
- **OpenRouter**: Analysis sent to cloud providers (OpenAI, Anthropic, Google, etc.)
- **No Storage**: SNID SAGE doesn't store your spectra on external servers
- **API Keys**: Stored locally, never transmitted except for authentication
- **Analysis Data**: Only spectrum analysis results are sent to AI models

### Best Practices
- Use dedicated API keys for SNID SAGE
- Monitor usage through OpenRouter dashboard
- Consider data sensitivity when using cloud AI

## Cost Management

### OpenRouter Pricing
- **GPT-4**: ~$0.03 per analysis
- **GPT-3.5**: ~$0.002 per analysis  
- **Claude**: ~$0.015 per analysis
- **Open Source Models**: Often free or very low cost

### Cost Optimization
- Use GPT-3.5 for routine analysis
- Reserve GPT-4 for complex cases
- Monitor usage at [OpenRouter Dashboard](https://openrouter.ai/keys)

## Troubleshooting

### Common Issues

#### API Key Problems
- **Check format**: Should start with `sk-or-`
- **Test in GUI**: Settings → Configure AI → Test Connection
- **Verify billing**: Ensure OpenRouter account has credits

#### Model Access Issues
- Some models require specific permissions
- Try alternative models if one fails
- Check OpenRouter status page for outages

#### Connection Problems
- Verify internet connection
- Check firewall settings
- Try different DNS servers

### Error Messages

#### "API key not found"
1. Set API key in GUI Settings
2. Or set environment variable
3. Restart SNID SAGE

#### "Model not available"
1. Check model name spelling
2. Verify model access with your API key
3. Try alternative model

#### "Request timeout"
1. Check internet connection
2. Try again with shorter input
3. Select faster model (GPT-3.5)

## Advanced Features

### Custom Analysis Prompts
Future versions will support custom prompts for specialized analysis needs.

### Batch AI Analysis
Currently, AI analysis is available through the GUI interface. Batch processing support is planned for future releases.

### API Integration
```python
# Python API for custom workflows (future feature)
from snid_sage.interfaces.llm import LLMIntegration

# Initialize with your results
llm = LLMIntegration()
analysis = llm.analyze_results(snid_results)
```

## Best Practices

### Effective AI Usage
1. **Start Simple**: Use Quick Summary first, then go deeper
2. **Ask Specific Questions**: "What about the Si II feature?" vs "Tell me about this"
3. **Cross-validate**: Use AI insights to guide further analysis
4. **Understand Limitations**: AI can make mistakes, verify important claims

### Research Workflow
1. **Run SNID Analysis**: Get initial classification
2. **Quick AI Summary**: Understand basic results
3. **Interactive Chat**: Explore specific questions
4. **Detailed Analysis**: Get comprehensive insights
5. **Export Results**: Save AI analysis with your data

## Related Documentation

- [OpenRouter Setup Guide](openrouter-setup.md) - Detailed OpenRouter configuration
- [Analysis Types](analysis-types.md) - Different AI analysis options
- [GUI Interface](../gui/interface-overview.md) - Using the GUI for AI features 