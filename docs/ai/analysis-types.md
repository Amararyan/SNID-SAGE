# AI Analysis in SNID SAGE

SNID SAGE provides AI-powered analysis through two main features that help interpret your spectrum analysis results.

## Available AI Features

### 1. Generate Summary
**Purpose**: Create a comprehensive summary of your SNID analysis results.

**What it does**:
- Analyzes the SNID classification results
- Interprets the spectral features detected
- Provides context about the supernova type
- Summarizes the redshift and age estimates
- Explains the template matches and correlation scores

**When to use**:
- After completing SNID analysis
- When you want a quick overview of results
- For initial assessment of new spectra
- To get AI interpretation of complex results

**How to use**:
1. Complete SNID analysis in GUI
2. Click the AI Assistant button (enabled after analysis)
3. Go to the "Summary" tab
4. Fill in optional metadata (observer name, telescope, date, specific requests)
5. Click "Generate Summary"

### 2. Interactive Chat
**Purpose**: Have a conversation about your analysis results and ask specific questions.

**What it does**:
- Allows you to ask questions about your spectrum
- Provides detailed explanations of spectral features
- Helps interpret classification results
- Suggests follow-up observations or analysis
- Answers questions about supernova physics

**When to use**:
- When you have specific questions about results
- For deeper investigation of interesting features
- To understand the science behind classifications
- For educational purposes and learning

**How to use**:
1. Complete SNID analysis in GUI
2. Click the AI Assistant button
3. Go to the "Chat" tab
4. Type your questions in the chat input
5. Send messages and receive AI responses

## What the AI Receives

The AI has access to your complete SNID analysis results:

- **Classification**: Type, subtype, and confidence level
- **Redshift**: Determined redshift with uncertainty
- **Age**: Days from maximum light with uncertainty
- **Template matches**: Ranked list of best matching templates
- **Correlation scores**: RLAP-Cos scores and individual estimates
- **Spectral features**: Detected absorption and emission lines
- **User metadata**: Observer name, telescope, observation date, specific requests

## Configuration

### API Key Setup
1. Open AI Assistant dialog
2. Go to "Settings" tab
3. Enter your OpenRouter API key
4. Test the connection

### Model Selection
- Choose from available OpenRouter models
- Test different models for best results
- Models include GPT-4, Claude, Gemini, and others

## Best Practices

### Effective Usage
- **Start with Summary**: Get an overview before diving into details
- **Ask Specific Questions**: Use chat for targeted inquiries
- **Provide Context**: Include relevant metadata for better results
- **Verify Important Claims**: AI can make mistakes, cross-check critical information

### Research Workflow
1. Run SNID analysis
2. Generate AI summary for overview
3. Use chat for specific questions
4. Export results with AI insights
5. Incorporate into your research

## Limitations

- Requires internet connection for OpenRouter API
- Quality depends on the chosen AI model
- May not be available for all spectral types
- Results should be verified against literature

## Troubleshooting

### Common Issues
- **API Key Errors**: Check key format and account credits
- **Connection Issues**: Verify internet connection
- **Poor Results**: Try different models or rephrase questions
- **Timeout Errors**: Check OpenRouter service status

For setup instructions, see [OpenRouter Setup](openrouter-setup.md). 