# Troubleshooting Guide

This guide helps you diagnose and fix common issues with SNID SAGE installation, setup, and usage.

## Emergency Quick Fixes

### GUI Won't Start
```bash
# Verify installation
pip show snid-sage

# Try CLI instead
snid --version
```

### Analysis Fails Immediately
```bash
# Check templates are installed
snid template list

# Test with sample data
snid identify data/sn2003jo.dat --output-dir test_results/
```

### No Results/Poor Classification
```bash
# Check input file format
head -10 your_spectrum.dat

# Try with preprocessing
snid identify spectrum.dat --output-dir results/ --savgol-window 11
```

---

## Installation Issues

### Problem: "Module not found" errors

#### Symptoms:
```
ImportError: No module named 'snid_sage'
ImportError: No module named 'numpy'
ModuleNotFoundError: No module named 'matplotlib'
```

#### Solutions:

**1. Verify Installation**
```bash
pip show snid-sage
# Should show package information
```

**2. Reinstall Package**
```powershell
python -m pip install --upgrade pip
python -m pip install --force-reinstall --no-cache-dir snid-sage
```

**3. Virtual Environment Issues**
```bash
# Ensure virtual environment is activated
which python  # Should point to venv/bin/python if using venv

# Recreate if needed
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows
python -m pip install --upgrade pip
python -m pip install snid-sage
```

### Problem: GUI doesn't start

#### Symptoms:
- Black screen or no window appears
- Qt-related errors
- Graphics/display issues

#### Solutions:

**1. Verify installation**
```bash
python -c "import snid_sage; print('SNID SAGE OK')"
```

**2. Display Issues (Linux)**
```bash
# Check DISPLAY variable
echo $DISPLAY

# If using SSH, enable X11 forwarding
ssh -X username@hostname

# Or use CLI interface instead
snid identify spectrum.dat --output-dir results/
```

**3. Windows Graphics Issues**
- Update graphics drivers
- Run as administrator
- Try different Python version (3.9 or 3.10)

---

## Data Loading Issues

### Problem: Spectrum won't load

#### Symptoms:
```
Error: Unable to read spectrum file
Error: Invalid file format
Error: No data found in file
```

#### Diagnosis:
```bash
# Check file format
head -20 your_spectrum.dat
file your_spectrum.dat  # Check file type

# Look for common issues
wc -l your_spectrum.dat  # Line count
grep -c "^#" your_spectrum.dat  # Comment lines
```

#### Solutions:

**1. Fix File Format**
```python
# Convert to proper format
import numpy as np
data = np.loadtxt('spectrum.dat', comments='#')
np.savetxt('spectrum_fixed.dat', data, fmt='%.6f %.6e')
```

**2. Handle Special Characters**
```bash
# Check encoding
file -bi your_spectrum.dat

# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 spectrum.dat > spectrum_utf8.dat
```

**3. FITS File Issues**
```python
from astropy.io import fits
hdul = fits.open('spectrum.fits')
hdul.info()
print(hdul[0].header)
```

### Problem: Wavelength calibration errors

#### Symptoms:
- Results don't match expected classification
- Wrong redshift determination
- Features at wrong wavelengths

#### Solutions:

**1. Check Wavelength Units**
```python
# Verify wavelength range
import numpy as np
data = np.loadtxt('spectrum.dat')
print(f"Wavelength range: {data[:,0].min():.1f} - {data[:,0].max():.1f}")
# Should be ~3000-10000 for Angstroms
```

**2. Convert Units if Needed**
```python
# Convert nm to Angstroms
data = np.loadtxt('spectrum.dat')
data[:,0] *= 10  # nm to Angstroms
np.savetxt('spectrum_angstroms.dat', data)
```

**3. Verify Rest Frame**
```bash
# Specify known redshift
snid identify spectrum.dat --output-dir results/ --forced-redshift 0.034
```

---

## Analysis Problems

### Problem: No good matches found

#### Symptoms:
```
Best match confidence: 2.1/10
No templates above quality threshold
Analysis completed with low confidence
```

#### Diagnosis:
```bash
# Check spectrum quality
snid identify spectrum.dat --output-dir results/ --verbose
```

#### Solutions:

**1. Improve Data Quality**
```bash
# Apply preprocessing
snid identify spectrum.dat --output-dir results/ \
    --savgol-window 15 --savgol-order 3
```

**2. Adjust Parameters**
```bash
# Broader search
snid identify spectrum.dat --output-dir results/ \
    --zmin 0.0 --zmax 0.1
```

**3. Check Template Selection**
```bash
# Use all templates
snid identify spectrum.dat --output-dir results/

# Try specific types
snid identify spectrum.dat --output-dir results/ --type-filter Ia Ib Ic
```

### Problem: Wrong classification

#### Symptoms:
- Obvious Type Ia classified as Type II
- Classification conflicts with literature
- Unrealistic parameters

#### Diagnosis Steps:

**1. Visual Inspection**
```bash
# Generate plots
snid identify spectrum.dat --output-dir results/ --complete
# Examine snid_comparison.png
```

**2. Manual Redshift**
```bash
# Try known redshift
snid identify spectrum.dat --output-dir results/ --forced-redshift 0.0234
```

#### Common Causes & Solutions:

**Host Galaxy Contamination:**
```bash
# Strong emission lines can affect classification
# Try masking emission regions
snid identify spectrum.dat --output-dir results/ \
    --wavelength-masks 6550:6570 4850:4870
```

**Wrong Observational Phase:**
- Very early/late phases are challenging
- Check age range in results
- Compare with literature phases

**Poor S/N Ratio:**
```bash
# Increase smoothing
snid identify spectrum.dat --output-dir results/ --savgol-window 21
```

---

## AI Integration Issues

### Problem: AI analysis fails

#### Symptoms:
```
Error: OpenRouter API key not found
Error: Model not available
Timeout: Request timed out after 60s
```

#### Solutions:

**1. API Key Issues**
```bash
# Check environment variable
echo $OPENROUTER_API_KEY

# Set API key in GUI
# Settings → Configure AI → Enter API key
```

**2. Network Issues**
```bash
# Test internet connection
curl -I https://openrouter.ai

# Try different model in GUI AI Assistant
```

---

## Performance Issues

### Problem: Analysis too slow

#### Symptoms:
- Analysis takes >2 minutes
- GUI becomes unresponsive
- Memory usage keeps increasing

#### Solutions:

**1. Template Optimization**
```bash
# Limit templates
snid identify spectrum.dat --output-dir results/ \
    --type-filter Ia \
    --age-min -10 --age-max 30
```

**2. System Optimization**
- Check system resources (Task Manager/Activity Monitor)
- Close unnecessary applications
- Use SSD storage for templates

### Problem: High memory usage

#### Solutions:
```bash
# Use minimal mode
snid identify spectrum.dat --output-dir results/ --minimal

# Use CLI for batch processing
snid batch "data/*.dat" templates/ --output-dir results/
```

---

## Configuration Issues

### Problem: Settings not saved

#### Symptoms:
- Configuration changes don't persist
- Defaults reset after restart

#### Solutions:

**1. Check Config Files**
```bash
# Configuration is stored in user settings
# GUI: Settings → Configure Settings
# Changes should persist between sessions
```

**2. Reset Configuration**
- In GUI: Settings → Reset to Defaults
- Delete user configuration file if corrupted

---

## Error Messages & Solutions

### Common Error Messages:

#### "Template directory not found"
```bash
# Templates should be included with installation
# Verify installation:
snid template list
```

#### "Correlation failed"
- Check input spectrum format
- Verify wavelength calibration
- Try different preprocessing options

#### "Memory allocation failed"
```bash
# Reduce memory usage
snid identify spectrum.dat --output-dir results/ --minimal
```

#### "OpenRouter authentication failed"
- Check API key format (should start with sk-or-)
- Verify account has credits
- Try different model

---

## Getting Help

### Before Asking for Help:

1. **Check this guide** - Most issues are covered here
2. **Search documentation** - Use the navigation guide
3. **Try verbose mode** - `--verbose` provides detailed info
4. **Check system requirements** - Ensure compatibility

### When Reporting Issues:

**Include this information:**
```bash
# System info
python --version
pip show snid-sage

# Error message (full traceback)
# Steps to reproduce
# Sample data (if possible)
```

### Support Channels:

1. **GitHub Issues**: [Report bugs](https://github.com/FiorenSt/SNID-SAGE/issues)
2. **Discussions**: [Ask questions](https://github.com/FiorenSt/SNID-SAGE/discussions)
3. **Email**: fiorenzo.stoppa@physics.ox.ac.uk

---

## Common Workflows

### Basic Analysis Workflow
```bash
# 1. Load spectrum in GUI
snid-sage

# 2. Preprocessing (amber button)
# 3. SNID Analysis (magenta button)
# 4. Review results
# 5. Optional: AI Analysis (deep blue button)
```

### CLI Batch Processing
```bash
# Process all spectra in directory
snid batch "data/*.dat" templates/ --output-dir results/

# With specific parameters
snid batch "data/*.dat" templates/ --output-dir results/ \
    --type-filter Ia Ib Ic --complete
```

---

**Still having issues?** Don't hesitate to reach out through our support channels! 