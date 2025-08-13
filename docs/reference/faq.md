# Frequently Asked Questions (FAQ)

This FAQ covers the most common questions about SNID SAGE installation, usage, and troubleshooting.

## Installation & Setup

### Q: What are the system requirements for SNID SAGE?
**A:** Minimum requirements:
- Python 3.8 or higher
- 4GB RAM (8GB recommended)
- 2GB storage space
- Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

For AI features, you'll also need an internet connection and an OpenRouter API key.

### Q: How do I install SNID SAGE?
**A:** The recommended method:
```powershell
python -m pip install --upgrade pip
python -m pip install snid-sage
```

For detailed instructions, see our [Installation Guide](../installation/installation.md).

### Q: Do I need an internet connection?
**A:** No, for basic spectrum analysis. Internet is only required for:
- AI-powered analysis features
- Downloading updates
- Installing from TestPyPI

### Q: Can I use SNID SAGE offline?
**A:** Yes! All core functionality works offline once installed. AI features require internet connection for OpenRouter API access.

---

## Data & File Formats

### Q: What file formats does SNID SAGE support?
**A:** SNID SAGE supports multiple formats:

**Input Spectra:**
- ASCII/text files (.dat, .txt, .ascii)
- FITS files (.fits, .fit) 
- Two-column format: wavelength, flux
- Space or tab separated values

### Q: How should my spectrum file be formatted?
**A:** The simplest format is two columns (space or tab separated):
```
# This is a comment line
# Wavelength(Å)  Flux(arbitrary)
3500.0          1.023
3501.0          1.045
3502.0          1.012
...
```

FITS files are automatically handled with header parsing.

### Q: My spectrum file won't load. What's wrong?
**A:** Common issues:
1. **Wrong format**: Ensure two-column (wavelength, flux)
2. **File permissions**: Check read permissions
3. **Special characters**: Use UTF-8 encoding
4. **Headers**: Comments should start with `#`

Try: `head -20 your_file.dat` to check format.

### Q: Can I use spectra from different instruments?
**A:** Yes! SNID SAGE handles spectra from various sources:
- Ground-based spectrographs
- HST/STIS, HST/COS
- ESO pipeline products
- Amateur spectra (with good wavelength calibration)

---

## Analysis & Classification

### Q: How accurate is classification?
**A:** Depends on data quality and coverage. Always review confidence and alternatives.

### Q: What does the confidence score mean?
**A:** 0–10 scale; higher is better. Treat <6 as low and inspect manually.

### Q: Why is my spectrum misclassified?
**A:** Possible reasons:
1. **Poor wavelength calibration**: Check rest-frame wavelengths
2. **Wrong redshift**: Try manual redshift input
3. **Host galaxy contamination**: Strong emission lines from host
4. **Observation phase**: Very early/late phases can be ambiguous
5. **Low S/N**: Noise masking key features

### Q: How do I interpret the age determination?
**A:** Ages are relative to maximum light:
- **Negative**: Before maximum (rising phase)
- **Zero**: At maximum light
- **Positive**: After maximum (declining phase)

Typical ranges: -20 to +100 days for most types.

### Q: Can it identify non-supernova objects?
**A:** No. It’s optimized for supernovae.

---

## AI Features

### Q: Do I need to pay for AI features?
**A:** It depends on provider/model. Check current pricing on the provider’s site and ensure your account has credit if required.

### Q: How do I set up AI analysis?
**A:** For OpenRouter:
1. Get API key from [openrouter.ai](https://openrouter.ai)
2. In GUI: Settings → Configure AI → Enter API key
3. Or set environment variable: `export OPENROUTER_API_KEY="your_key"`

See our [AI Setup Guide](../ai/overview.md) for details.

### Q: Can AI make mistakes in analysis?
**A:** Yes! AI analysis should be used as a guide, not definitive truth:
- Cross-validate important claims
- Check against literature
- Use your scientific judgment
- AI is best for initial interpretation and insight generation

### Q: Which AI model should I use?
**A:** Use higher-end models for complex reasoning; mid-tier for quick summaries. Evaluate latency, cost, and accuracy for your task.

---

## Interface Usage

### Q: Should I use the GUI or CLI?
**A:** Choose based on your needs:

**GUI (Recommended for most users):**
- Interactive analysis
- Real-time plotting
- Easy parameter adjustment
- AI chat interface

**CLI (For automation):**
- Batch processing
- Scripting/automation
- Remote server use
- Reproducible workflows

### Q: How do I save my analysis results?
**A:** Multiple options:

**GUI:**
- Results are automatically displayed
- Use File menu to export
- Screenshots for plots

**CLI:**
```bash
snid identify spectrum.dat --output-dir results/
```

### Q: Can I batch process multiple spectra?
**A:** Yes! 

**CLI batch mode:**
```bash
snid batch "data/*.dat" templates/ --output-dir results/
```

**GUI:** Load and process spectra one by one.

---

## Performance & Optimization

### Q: Analysis is slow. How can I speed it up?
**A:** Limit templates by type/age; close other apps; use SSD for templates.

### Q: Memory usage is high. What can I do?
**A:** Limit template selection; use `--minimal`; close unused apps.

### Q: How long does analysis take?
**A:** Typically 10–30 s per spectrum (hardware dependent).

---

## Troubleshooting

### Q: GUI won't start. What's wrong?
**A:** Common issues:

**Check installation:**
```bash
snid-sage  # Should launch GUI
```

**Check Python/tkinter:**
```bash
python -c "import tkinter; tkinter.Tk()"
```

**Install tkinter (Linux):**
```bash
sudo apt install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

### Q: "Module not found" errors
**A:** Ensure proper installation:
```powershell
python -m pip install --upgrade pip
python -m pip install --force-reinstall snid-sage
```

### Q: Analysis fails with "No templates found"
**A:** Check templates directory:
- Templates should be in the configured directory
- Use `snid template list` to verify

### Q: Results seem wrong compared to literature
**A:** Debugging steps:
1. **Check input spectrum**: Wavelength calibration, units
2. **Verify redshift**: Manual vs. automatic
3. **Review preprocessing**: Try different smoothing
4. **Check alternatives**: Look at other matches
5. **Contact support**: With specific details

---

## Advanced Usage

### Q: Can I create custom templates?
**A:** Yes! See [Custom Templates Guide](../data/custom-templates.md) for detailed instructions.

### Q: How do I cite SNID SAGE in publications?
**A:** Suggested citation:
```
Spectral classification performed using SNID SAGE v1.2.1 
(Stoppa 2025), based on the SNID algorithm (Blondin & Tonry 2007).
```

**BibTeX:**
```bibtex
@software{snid_sage_2025,
  title={SNID SAGE: Advanced Supernova Spectral Analysis with AI Enhancement},
  author={Fiorenzo Stoppa},
  year={2025},
  url={https://github.com/FiorenSt/SNID-SAGE}
}
```

### Q: Can I integrate SNID SAGE into my own code?
**A:** Yes! Python API available:
```python
from snid_sage.snid import run_snid

# Basic analysis
results = run_snid('spectrum.dat', templates_dir='templates/')
```

### Q: How do I contribute to SNID SAGE development?
**A:** Contributions welcome!
1. Fork the repository
2. Create feature branch
3. Make improvements
4. Submit pull request

See [Contributing Guide](../dev/contributing.md).

---

## Getting More Help

### Q: My question isn't answered here. Where can I get help?
**A:** Multiple support channels:

1. **Documentation**: [Complete user guide](../index.md)
2. **Tutorials**: [Step-by-step guides](../tutorials/index.md)
3. **GitHub Issues**: [Report bugs/request features](https://github.com/FiorenSt/SNID-SAGE/issues)
4. **Discussions**: [Community Q&A](https://github.com/FiorenSt/SNID-SAGE/discussions)

### Q: How do I report a bug?
**A:** When reporting bugs, please include:
- Operating system and version
- Python version (`python --version`)
- SNID SAGE version
- Complete error message
- Steps to reproduce
- Sample data (if possible)

### Q: Can I request new features?
**A:** Absolutely! Feature requests are welcome:
- Check existing issues first
- Describe the use case
- Explain expected behavior
- Consider contributing code

### Q: Is commercial use allowed?
**A:** Yes, SNID SAGE is released under MIT license, allowing commercial use. Please see [LICENSE](https://github.com/FiorenSt/SNID-SAGE/blob/main/LICENSE) for full terms.

---

----

**Still have questions?** Check our [complete documentation](../index.md) or ask on [GitHub Discussions](https://github.com/FiorenSt/SNID-SAGE/discussions)! 