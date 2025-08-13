# OpenRouter Setup Guide

Complete guide to setting up OpenRouter for AI-powered spectrum analysis in SNID SAGE.

## What is OpenRouter?

OpenRouter provides access to 15+ state-of-the-art AI models through a single API, including:
- **GPT-4 Turbo** (OpenAI) - Most capable reasoning
- **Claude 3 Opus** (Anthropic) - Excellent scientific analysis  
- **Gemini Pro** (Google) - Strong multilingual support
- **Llama 2** (Meta) - Open source alternative
- **Command R+** (Cohere) - Strong summarization

## Quick Setup (5 minutes)

### Step 1: Get Your API Key
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Click **"Sign Up"** or **"Get Started"**
3. Create account (email + password)
4. Navigate to **"API Keys"** in dashboard
5. Click **"Create Key"**
6. Copy your key (starts with `sk-or-...`)

### Step 2: Configure SNID SAGE

#### Method A: Environment Variable (Recommended)
```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# macOS/Linux Terminal
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# Make permanent (Linux/macOS)
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Method B: Configuration File
```bash
# Using SNID SAGE CLI
python run_snid_cli.py config set ai.openrouter_api_key "sk-or-v1-your-key-here"

# Or edit config file directly
echo "openrouter_api_key: sk-or-v1-your-key-here" >> config/user_config.yaml
```

#### Method C: API Key File
```bash
# Create API key file in project root
echo "sk-or-v1-your-key-here" > openrouter_api_key.txt

# SNID SAGE will automatically detect and use this file
```

### Step 3: Test Connection
1. Launch SNID SAGE GUI
2. Click **Settings** → **Configure AI**
3. Enter your API key and test connection
4. Select your preferred model from the dropdown

---

## Model Selection Guide

### **Top Models for Scientific Analysis**

#### Best Overall: GPT-4 Turbo
```yaml
Model: "openai/gpt-4-turbo"
Cost: $0.01-0.03 per request
Speed: Fast
Strengths: 
  - Best reasoning capabilities
  - Excellent scientific understanding
  - Strong context handling
  - Reliable performance
```

#### Scientific Specialist: Claude 3 Opus
```yaml
Model: "anthropic/claude-3-opus"
Cost: $0.015-0.075 per request  
Speed: Medium
Strengths:
  - Exceptional scientific analysis
  - Strong literature knowledge
  - Detailed explanations
  - Publication-quality output
```

#### Fast & Efficient: GPT-3.5 Turbo
```yaml
Model: "openai/gpt-3.5-turbo"
Cost: $0.0005-0.002 per request
Speed: Very Fast
Strengths:
  - Cost-effective
  - Quick responses
  - Good general knowledge
  - Reliable availability
```

#### Multilingual: Gemini Pro
```yaml
Model: "google/gemini-pro"
Cost: $0.0005-0.002 per request
Speed: Fast
Strengths:
  - Excellent multilingual support
  - Strong code understanding
  - Good scientific knowledge
  - Cost-effective
```

### **Model Comparison Table**

| Model | Cost/Request | Speed | Scientific Quality | Best For |
|-------|-------------|-------|-------------------|----------|
| GPT-4 Turbo | $0.01-0.03 | Fast | ⭐⭐⭐⭐⭐ | Complex analysis |
| Claude 3 Opus | $0.015-0.075 | Medium | ⭐⭐⭐⭐⭐ | Publication work |
| GPT-3.5 Turbo | $0.0005-0.002 | Very Fast | ⭐⭐⭐⭐ | Quick summaries |
| Gemini Pro | $0.0005-0.002 | Fast | ⭐⭐⭐⭐ | Multilingual work |
| Llama 2 70B | $0.0007-0.003 | Medium | ⭐⭐⭐⭐ | Open source option |

---

## Advanced Configuration

### GUI Configuration
All AI settings are configured through the SNID SAGE GUI:

1. **Launch GUI**: Run `snid-sage`
2. **Open Settings**: Click the **Settings** button
3. **Configure AI**: Select **Configure AI** option
4. **Model Selection**: Choose your preferred model from the dropdown
5. **Test Connection**: Verify your API key works

### Configuration File
Advanced users can edit the configuration file directly:
```bash
# Location: ~/.snidanalyzer/openrouter_config.json
{
  "api_key": "your-api-key-here",
  "model_id": "openai/gpt-3.5-turbo"
}
```

---

## Troubleshooting

### Common Issues

#### API Key Not Working
1. **Check Environment Variable**: Verify `$OPENROUTER_API_KEY` is set
2. **Test in GUI**: Settings → Configure AI → Test Connection
3. **Regenerate Key**: Go to OpenRouter dashboard → API Keys → Create New Key

#### Model Not Available
1. **Check Model List**: Settings → Configure AI → Browse available models
2. **Try Alternative**: Select a different model from the dropdown
3. **Check OpenRouter Status**: Visit [status.openrouter.ai](https://status.openrouter.ai/)

#### Rate Limiting
1. **Check Usage**: OpenRouter dashboard shows current usage
2. **Wait and Retry**: Rate limits reset automatically
3. **Upgrade Plan**: Consider upgrading for higher limits

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid API key | Check key format and validity |
| `429 Too Many Requests` | Rate limit exceeded | Wait or upgrade plan |
| `503 Service Unavailable` | Model temporarily down | Try alternative model |
| `400 Bad Request` | Invalid request format | Check input data |

---

## Cost Management

### **Understanding Costs**

#### **Cost Calculation**
```
Cost = (Input Tokens + Output Tokens) × Token Price
```

#### **Typical Costs per Analysis**
| Analysis Type | Input Tokens | Output Tokens | Cost Range |
|---------------|-------------|---------------|------------|
| Quick Summary | 500-1000 | 200-400 | $0.001-0.005 |
| Detailed Analysis | 1000-2000 | 500-1000 | $0.005-0.02 |
| Scientific Context | 1500-3000 | 800-1500 | $0.01-0.05 |
| Publication Notes | 2000-4000 | 1000-2000 | $0.02-0.08 |

### **Cost Optimization Tips**

#### **1. Choose Appropriate Models**
- **Quick tasks**: Use GPT-3.5 Turbo (cheaper, ~$0.002 per analysis)
- **Complex analysis**: Use GPT-4 Turbo (better quality, ~$0.03 per analysis)
- **Scientific work**: Use Claude 3 Opus (excellent quality, ~$0.015 per analysis)

#### **2. Monitor Usage**
- **OpenRouter Dashboard**: Track usage and costs in real-time
- **Set Budget Alerts**: Configure spending limits in OpenRouter dashboard
- **Review Regularly**: Check usage patterns to optimize costs

#### **3. Efficient Analysis**
- **Run SNID First**: Complete spectrum analysis before using AI
- **Use Specific Prompts**: Clear, focused questions reduce token usage
- **Batch Similar Questions**: Combine related queries when possible

---

## 🔒 **Security & Privacy**

### **API Key Security**

#### **Best Practices**
```bash
# Never commit keys to version control
echo "openrouter_api_key.txt" >> .gitignore
echo "*.key" >> .gitignore

# Use environment variables
export OPENROUTER_API_KEY="your-key-here"

# Rotate keys regularly
# OpenRouter dashboard → API Keys → Regenerate
```

#### **Data Privacy**
- **No data retention**: OpenRouter doesn't store your data
- **Encrypted transmission**: All API calls use HTTPS
- **GDPR compliant**: Full data protection compliance
- **Academic use**: Special pricing for research institutions

### **Network Security**

#### **Firewall Configuration**
```bash
# Allow OpenRouter API access
# Required domains: api.openrouter.ai, openrouter.ai

# Test connectivity
curl -I https://api.openrouter.ai/health
```

---

## 📊 **Usage Examples**

### **GUI-Based Analysis**
1. **Run SNID Analysis**: Load spectrum and run analysis in GUI
2. **Open AI Assistant**: Click the **AI Assistant** button (deep blue)
3. **Choose Analysis Type**: Select from available options
4. **Review Results**: AI provides comprehensive analysis

### **Interactive Chat**
1. **Complete Analysis**: Run SNID analysis first
2. **Start Chat**: Click **AI Assistant** → **Interactive Chat**
3. **Select Persona**: Choose Scientist, Educator, Reviewer, or Consultant
4. **Ask Questions**: Chat naturally about your results

---

## 🆘 **Support & Resources**

### **OpenRouter Support**
- **Documentation**: [docs.openrouter.ai](https://docs.openrouter.ai/)
- **Status Page**: [status.openrouter.ai](https://status.openrouter.ai/)
- **Discord**: [discord.gg/openrouter](https://discord.gg/openrouter)
- **Email**: support@openrouter.ai

### **SNID SAGE AI Support**
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: [AI Overview](overview.md)
- **Community**: GitHub Discussions

### **Academic Support**
- **Research Discounts**: Contact OpenRouter for academic pricing
- **Educational Resources**: Free tier available for students
- **Collaboration**: Open to research partnerships

---

## 📈 **Next Steps**

1. **Test Your Setup**: Run a quick analysis to verify everything works
2. **Explore Models**: Try different models for different use cases
3. **Optimize Costs**: Configure caching and model selection
4. **Advanced Features**: Learn about batch processing and custom prompts
5. **Integration**: Set up automated workflows with your analysis pipeline

For more advanced AI features, see:
- **[AI Overview](overview.md)** - Complete AI capabilities guide
- **[Analysis Types](analysis-types.md)** - Detailed analysis explanations
- **[AI Tutorial](../tutorials/ai-assisted-analysis.md)** - Step-by-step AI workflow 