# 🌟 SNID SAGE - Advanced Supernova Spectral Analysis

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

**SNID-SAGE** (SuperNova IDentification – Spectral Analysis and Guided Exploration) is a comprehensive spectrum analysis suite featuring an intuitive GUI and powerful cross-correlation techniques, enhanced with modern LLM-powered analysis capabilities.

## 🚀 **Quick Installation**

```bash
# Clone the repository
git clone https://github.com/FiorenSt/SNID-SAGE.git
cd SNID-SAGE

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install the package
pip install . --verbose

# Optional: Set up custom icons for better system integration
python scripts/generate_platform_icons.py
python scripts/setup_all_platform_icons.py
```
## 🎮 **Getting Started**

### **Launch the GUI** *(Recommended for most users)*
```bash
# Using installed entry point
snid-sage

# Or run directly from source
python run_snid_gui.py
```

### **Use the CLI** *(For batch processing and automation)*
```bash
# Single spectrum analysis
snid identify data/sn2003jo.dat --output-dir results/

# Batch processing
snid batch "data/*.dat" --output-dir results/ --quick

# Template management
snid-template list -v
```

### **Python API** *(For developers and custom workflows)*
```python
from snid import SNID
from interfaces.llm.analysis.llm_utils import SNIDLLMAnalyzer

# Traditional analysis
snid = SNID()
results = snid.identify_spectrum('data/sn2003jo.dat')

# AI-enhanced analysis
analyzer = SNIDLLMAnalyzer()
ai_summary = analyzer.analyze_results(results, analysis_type='comprehensive')
```

## 📚 **Documentation & Support**

- **[📖 Complete Documentation](docs/)** - Comprehensive guides and tutorials
- **[🎯 Quick Start Guide](docs/quickstart/first-analysis.md)** - Your first analysis in 5 minutes
- **[🖥️ GUI Manual](docs/gui/interface-overview.md)** - Complete interface guide
- **[💻 CLI Reference](docs/cli/command-reference.md)** - All commands and options
- **[🤖 AI Integration](docs/ai/overview.md)** - Setting up AI analysis
- **[🐛 Troubleshooting](docs/reference/troubleshooting.md)** - Common issues and solutions
- **[❓ FAQ](docs/reference/faq.md)** - Frequently asked questions

## 🗂️ **Supported Data Formats**

- **FITS files** (.fits, .fit)
- **ASCII tables** (.dat, .txt, .ascii)
- **Space-separated values** with flexible column detection
- **Custom formats** with configurable parsers

## 🏆 **Research & Citation**

If you use SNID SAGE in your research, please cite:

```bibtex
@software{snid_sage_2025,
  title={SNID-SAGE: A Modern Framework for Interactive Supernova
Classification and Spectral Analysis},
  author={F. Stoppa},
  year={In Prep, 2025},
  url={https://github.com/FiorenSt/SNID-SAGE}
}
```

## 🤝 **Community & Support**

- **[🐛 Report Bug](https://github.com/FiorenSt/SNID-SAGE/issues)** - Found a bug?
- **[✨ Request Feature](https://github.com/FiorenSt/SNID-SAGE/issues)** - Want a new feature?
- **[💬 Discussions](https://github.com/FiorenSt/SNID-SAGE/discussions)** - Questions and community chat
- **[📧 Email Support](mailto:fiorenzo.stoppa@physics.ox.ac.uk)** - Direct contact

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for the astronomical community**

[📖 Documentation](docs/) • [🐛 Report Bug](https://github.com/FiorenSt/SNID-SAGE/issues) • [✨ Request Feature](https://github.com/FiorenSt/SNID-SAGE/issues) • [💬 Discussions](https://github.com/FiorenSt/SNID-SAGE/discussions)

</div>
