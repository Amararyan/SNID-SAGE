# 📦 Installation Guide

This guide will walk you through installing SNID SAGE on your system. Choose the installation method that best fits your needs.

## 🔧 **System Requirements**

### **Minimum Requirements**
- **Python**: 3.8 or higher
- **RAM**: 4GB (8GB recommended for large datasets)
- **Storage**: 2GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

### **Recommended Requirements**
- **Python**: 3.9 or 3.10
- **RAM**: 16GB for optimal performance
- **Storage**: 5GB+ for templates and results
- **GPU**: CUDA-compatible for local LLM support (optional)

## 🚀 **Quick Installation (Recommended)**

### **Option 1: pip install from PyPI (Future Release)**
```bash
# This will be available in future releases
pip install snid-sage
```

### **Option 2: From Source (Current Method)**
```bash
# Clone the repository
git clone https://github.com/FiorenSt/SNID-SAGE.git
cd SNID_SAGE

# Install in development mode (recommended)
pip install -e .

# Or install directly
pip install .

# For all optional features
pip install -e ".[all]"

# Verify installation
python -c "import snid; print('SNID SAGE installed successfully!')"
```

---

## 🖥️ **Platform-Specific Installation**

### **Windows Installation**

#### **Method 1: Using Git and Python**
```powershell
# Install Git (if not already installed)
# Download from: https://git-scm.com/download/win

# Install Python 3.8+ (if not already installed)
# Download from: https://python.org/downloads/

# Clone and install
git clone https://github.com/FiorenSt/SNID-SAGE.git
cd SNID_SAGE
pip install -e .

# Launch GUI
python interfaces/gui/sage_gui.py
```

#### **Method 2: Download ZIP**
1. Download the ZIP file from GitHub
2. Extract to your desired location
3. Open PowerShell in the extracted folder
4. Run: `pip install -e .`

#### **Windows-Specific Notes**
- **PowerShell Execution Policy**: You may need to run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Path Issues**: Ensure Python and pip are in your PATH
- **Visual Studio Build Tools**: May be required for some dependencies

### **macOS Installation**

#### **Using Homebrew (Recommended)**
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Clone and install SNID SAGE
git clone https://github.com/FiorenSt/SNID-SAGE.git
cd SNID_SAGE
pip3 install -e .

# Launch GUI
python3 interfaces/gui/sage_gui.py
```

#### **macOS-Specific Notes**
- **Xcode Command Line Tools**: Required for some dependencies
  ```bash
  xcode-select --install
  ```
- **M1/M2 Macs**: All dependencies are compatible with Apple Silicon
- **Security**: You may need to allow the app in System Preferences > Security & Privacy

### **Linux Installation**

#### **Ubuntu/Debian**
```bash
# Update package manager
sudo apt update

# Install Python and dependencies
sudo apt install python3.10 python3-pip git

# Clone and install
git clone https://github.com/FiorenSt/SNID-SAGE.git
cd SNID_SAGE
pip3 install -e .

# Launch GUI (requires X11 or Wayland)
python3 interfaces/gui/sage_gui.py
```

#### **CentOS/RHEL/Fedora**
```bash
# Install Python and Git
sudo dnf install python3.10 python3-pip git  # Fedora
# sudo yum install python3 python3-pip git   # CentOS/RHEL

# Clone and install
git clone https://github.com/FiorenSt/SNID-SAGE.git
cd SNID_SAGE
pip3 install -e .
```

#### **Linux-Specific Notes**
- **GUI Dependencies**: Install tkinter if not included
  ```bash
  sudo apt install python3-tk  # Ubuntu/Debian
  sudo dnf install tkinter      # Fedora
  ```
- **Display Issues**: Ensure DISPLAY variable is set for GUI

---

## 🐍 **Virtual Environment Setup (Recommended)**

Using a virtual environment prevents dependency conflicts:

### **Using venv**
```bash
# Create virtual environment
python -m venv snid_env

# Activate (Windows)
snid_env\Scripts\activate

# Activate (macOS/Linux)
source snid_env/bin/activate

# Install SNID SAGE
cd SNID_SAGE
pip install -e .

# Deactivate when done
deactivate
```

### **Using conda**
```bash
# Create conda environment
conda create -n snid_sage python=3.10
conda activate snid_sage

# Install SNID SAGE
cd SNID_SAGE
pip install -e .
```

---

## 🔍 **Dependency Details**

### **Core Dependencies**
The following are automatically installed from `pyproject.toml`:
```txt
numpy>=1.20.0          # Numerical computing
scipy>=1.7.0           # Scientific computing
matplotlib>=3.5.0      # Plotting
astropy>=5.0.0         # Astronomical data handling
scikit-learn>=1.0.0    # Machine learning
requests>=2.25.0       # HTTP requests
ttkbootstrap>=1.10.0   # GUI framework
pyspeckit>=1.0.0       # Spectral analysis
h5py>=3.0.0            # HDF5 support
pandas>=1.3.0          # Data analysis
pillow>=8.0.0          # Image processing
```

### **Optional Dependencies**
Install with extras for additional features:
```bash
# AI Integration
pip install -e ".[llm]"
# Includes: openai>=1.0.0

# Astronomical Tools
pip install -e ".[astro]"
# Includes: astroquery>=0.4.0

# Development Tools
pip install -e ".[dev]"
# Includes: pytest, black, flake8, sphinx, etc.

# All features
pip install -e ".[all]"
```

---

## ✅ **Installation Verification**

### **Test Basic Installation**
```bash
# Test imports
python -c "
import snid
import numpy
import matplotlib
print('✅ All core modules imported successfully!')
"

# Test GUI launch
python interfaces/gui/sage_gui.py

# Test CLI
python run_snid_cli.py --version
```

### **Test with Sample Data**
```bash
# Run analysis on sample data
python run_snid_cli.py identify data/sn2003jo.dat templates/ --output-dir test_results/

# Expected output should show classification results
```

### **Test AI Integration (Optional)**
```bash
# Test AI imports
python -c "
from interfaces.llm.llm_integration import LLMIntegration
print('✅ AI components available!')
"
```

---

## 🛠️ **Troubleshooting Installation Issues**

### **Common Issues and Solutions**

#### **"Module not found" errors**
```bash
# Ensure you're in the correct directory
cd SNID_SAGE

# Reinstall in development mode
pip install -e . --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

#### **GUI doesn't launch**
```bash
# Test tkinter installation
python -c "import tkinter; tkinter.Tk()"

# Install tkinter (Linux)
sudo apt install python3-tk
```

#### **Permission errors (Windows)**
```powershell
# Run as administrator or use --user flag
pip install -e . --user
```

#### **SSL Certificate errors**
```bash
# Update certificates (macOS)
/Applications/Python\ 3.x/Install\ Certificates.command

# Use trusted hosts (temporary fix)
pip install -e . --trusted-host pypi.org --trusted-host pypi.python.org
```

### **Getting Help**

If you encounter issues not covered here:

1. **Check the [Troubleshooting Guide](../reference/troubleshooting.md)**
2. **Search [existing issues](https://github.com/FiorenSt/SNID-SAGE/issues)**
3. **Create a new issue** with:
   - Your operating system and version
   - Python version (`python --version`)
   - Complete error message
   - Steps to reproduce

---

## 🔄 **Updating SNID SAGE**

### **From Git Repository**
```bash
cd SNID_SAGE
git pull origin main
pip install -e . --upgrade
```

### **Check for Updates**
```bash
# Check git status for updates
git status
git log --oneline -5
```

---

## 🗑️ **Uninstallation**

### **Complete Removal**
```bash
# Uninstall package
pip uninstall snid-sage

# Remove the directory
rm -rf SNID_SAGE  # macOS/Linux
rmdir /s SNID_SAGE  # Windows

# Remove virtual environment (if used)
rm -rf snid_env  # or conda remove -n snid_sage --all
```

---

## ⚡ **Performance Optimization**

### **For Large Datasets**
- Allocate more RAM to Python processes
- Use SSD storage for templates and data
- Enable parallel processing in configuration

### **For AI Features**
- Install CUDA for GPU acceleration (local LLM)
- Configure OpenRouter API key for cloud models
- Optimize memory settings in `config.py`

---

## 📞 **Support**

- **Documentation**: [docs/](../)
- **Issues**: [GitHub Issues](https://github.com/FiorenSt/SNID-SAGE/issues)
- **Discussions**: [GitHub Discussions](https://github.com/FiorenSt/SNID-SAGE/discussions)

---

**Next Steps**: After installation, check out the [Quick Start Guide](../quickstart/first-analysis.md) to perform your first analysis! 