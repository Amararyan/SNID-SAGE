# Contributing to SNID SAGE

Thank you for your interest in contributing to SNID SAGE! This guide will help you get started with development and contributions.

## Ways to Contribute

### **For Everyone**
- Report bugs and issues
- Suggest new features
- Improve documentation
- Test with different data
- Share analysis results

### **For Developers**
- Fix bugs and issues
- Implement new features
- Performance improvements
- Add test coverage
- Code refactoring

### **For Scientists**
- Contribute templates
- Scientific validation
- Publications and citations
- Educational content
- Feature requests from research

---

## Getting Started

### **Development Setup**

#### **1. Fork and Clone**
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/yourusername/SNID_SAGE.git
cd SNID_SAGE

# Add upstream remote
git remote add upstream https://github.com/FiorenSt/SNID-SAGE.git
```

#### **2. Set Up Development Environment**
```bash
# Create virtual environment
python -m venv venv_dev
source venv_dev/bin/activate  # Linux/macOS
# or venv_dev\Scripts\activate  # Windows

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt
```

#### **3. Verify Installation**
```bash
# Test CLI
sage --version

# Test GUI
snid-sage

# Run tests
python -m pytest tests/ -v
```

### **Development Dependencies**

```txt
# requirements-dev.txt (additional development tools)
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=1.0.0
sphinx>=5.0.0
pre-commit>=2.20.0
```

---

## Development Workflow

### **1. Create Feature Branch**
```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### **2. Make Changes**
- Follow coding standards
- Add tests for new features
- Update documentation
- Test thoroughly

### **3. Commit and Push**
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add: New feature description

- Detailed description of changes
- Any breaking changes noted
- References to issues if applicable"

# Push to your fork
git push origin feature/your-feature-name
```

### **4. Create Pull Request**
- Use clear title and description
- Reference related issues
- Include screenshots for UI changes
- Add tests and documentation

---

## Code Style Guide

### **Python Style**

#### **Follow PEP 8 with modifications:**
- Line length: 100 characters (not 79)
- Use `black` for automatic formatting
- Use `flake8` for linting

#### **Formatting**
```bash
# Auto-format code
black snid_sage/ interfaces/ shared/ tests/

# Check style
flake8 snid_sage/ interfaces/ shared/ tests/

# Type checking
mypy snid_sage/ interfaces/ shared/
```

#### **Naming Conventions**
```python
# Classes: PascalCase
class SpectrumAnalyzer:
    pass

# Functions/variables: snake_case
def analyze_spectrum(wavelength_data):
    pass

# Constants: UPPER_SNAKE_CASE
SPEED_OF_LIGHT = 299792458

# Private methods: _leading_underscore
def _internal_method(self):
    pass
```

### **Documentation Style**

#### **Docstrings (Google Style)**
```python
def analyze_spectrum(wavelength: np.ndarray, flux: np.ndarray) -> AnalysisResult:
    """Analyze a supernova spectrum using template matching.
    
    Args:
        wavelength: Wavelength array in Angstroms
        flux: Flux array in arbitrary units
        
    Returns:
        AnalysisResult containing classification and parameters
        
    Raises:
        ValueError: If wavelength and flux arrays have different lengths
        AnalysisError: If analysis fails due to poor data quality
        
    Example:
        >>> result = analyze_spectrum(wavelength, flux)
        >>> print(f"Type: {result.type}, Confidence: {result.confidence}")
    """
```

#### **Comments**
```python
# Use inline comments sparingly, prefer clear variable names
correlation_coefficient = 0.87  # Good match threshold

# Use block comments for complex algorithms
# Cross-correlation using FFT for efficiency:
# 1. Zero-pad both arrays to same length
# 2. Compute FFT of both arrays
# 3. Multiply FFT(a) * conj(FFT(b))
# 4. Inverse FFT to get correlation
```

---

## Project Architecture

### **Directory Structure**
```
SNID_SAGE/
├── snid_sage/               # Core algorithm
├── interfaces/              # User interfaces
│   ├── cli/                # Command-line interface
│   ├── gui/                # Graphical interface
│   └── llm/                # AI integration
├── shared/                  # Shared utilities
│   ├── constants/          # Physical constants
│   ├── exceptions/         # Custom exceptions
│   ├── types/              # Type definitions
│   └── utils/              # Utility functions
├── tests/                   # Test suite
├── docs/                    # Documentation
└── scripts/                 # Utility scripts
```

### **Design Principles**

#### **1. Separation of Concerns**
- Core algorithm independent of interfaces
- GUI/CLI as thin wrappers around core
- AI integration as optional enhancement

#### **2. Type Safety**
```python
from typing import Optional, List, Tuple
from shared.types import SpectrumData, AnalysisResult

def analyze(spectrum: SpectrumData, 
           templates: List[SpectrumData]) -> AnalysisResult:
    """Type-safe analysis function."""
```

#### **3. Error Handling**
```python
from shared.exceptions import SpectrumLoadError, AnalysisError

try:
    spectrum = load_spectrum(filename)
except SpectrumLoadError as e:
    logger.error(f"Failed to load {filename}: {e}")
    raise
```

#### **4. Configuration Management**
```python
from shared.utils.config import get_config

config = get_config()
correlation_method = config.analysis.correlation_method
```

---

## Testing Guidelines

### **Test Structure**
```
tests/
├── unit/                   # Unit tests
│   ├── test_snid_core.py  # Core algorithm tests  
│   ├── test_preprocessing.py
│   └── test_io.py
├── integration/            # Integration tests
│   ├── test_cli.py        # CLI functionality
│   └── test_gui.py        # GUI functionality
├── fixtures/               # Test data
│   ├── spectra/           # Sample spectra
│   └── templates/         # Test templates
└── conftest.py            # Pytest configuration
```

### **Writing Tests**

#### **Unit Tests**
```python
import pytest
import numpy as np
from snid_sage.snid.preprocessing import normalize_spectrum

def test_normalize_spectrum():
    """Test spectrum normalization."""
    # Arrange
    wavelength = np.linspace(4000, 7000, 100)
    flux = np.random.normal(1.0, 0.1, 100)
    
    # Act
    normalized_flux = normalize_spectrum(wavelength, flux)
    
    # Assert
    assert np.isclose(np.median(normalized_flux), 1.0, rtol=0.1)
    assert len(normalized_flux) == len(flux)
    assert not np.any(np.isnan(normalized_flux))

def test_normalize_spectrum_empty():
    """Test normalization with empty input."""
    with pytest.raises(ValueError, match="Empty spectrum"):
        normalize_spectrum(np.array([]), np.array([]))
```

#### **Integration Tests**
```python
def test_cli_identify_command(tmpdir):
    """Test CLI identify command end-to-end."""
    import subprocess
    
    # Create test spectrum
    test_spectrum = tmpdir.join("test_spectrum.dat")
    test_spectrum.write("4000 1.0\n4001 1.1\n4002 0.9\n")
    
    # Run CLI command
    result = subprocess.run([
        "python", "run_snid_cli.py", "identify", str(test_spectrum)
    ], capture_output=True, text=True)
    
    # Check results
    assert result.returncode == 0
    assert "Type:" in result.stdout
```

### **Running Tests**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=snid_sage --cov=interfaces --cov=shared

# Run specific test file
pytest tests/unit/test_snid_sage_core.py -v

# Run tests matching pattern
pytest -k "test_normalize" -v
```

---

## Documentation Guidelines

### **Types of Documentation**

#### **1. Code Documentation**
- Docstrings for all public functions/classes
- Type hints for function signatures
- Inline comments for complex logic

#### **2. User Documentation**
- Installation guides
- Tutorials and examples
- API reference
- FAQ and troubleshooting

#### **3. Developer Documentation**
- Architecture overview
- Contributing guidelines
- Release notes
- Development setup

### **Documentation Tools**

#### **Markdown for Guides**
```markdown
# Use clear headings
## Subsections help navigation
### Examples with code blocks

```python
# Code examples should be runnable
result = analyze_spectrum(wavelength, flux)
```

**Bold** for emphasis, *italic* for variables.
```

#### **Sphinx for API Documentation**
```python
# Install Sphinx
pip install sphinx sphinx-autodoc-typehints

# Generate documentation
cd docs/
make html
```

---

## Bug Reports

### **Before Reporting**
1. Check existing issues
2. Try latest version
3. Verify it's reproducible
4. Check documentation

### **Good Bug Report Template**
```markdown
## Bug Description
Clear description of what went wrong.

## Steps to Reproduce
1. Load spectrum file `example.dat`
2. Run analysis with default parameters
3. Click "Export Results"
4. Error occurs

## Expected Behavior
Results should export to JSON file.

## Actual Behavior
Error message: "Unable to write file"

## Environment
- OS: Windows 10
- Python: 3.9.7
- SNID SAGE: v2.0.1
- Error log: [attach log file]

## Additional Context
- File permissions are correct
- Disk space available
- Works with other spectra
```

---

## Feature Requests

### **Good Feature Request Template**
```markdown
## Feature Description
Add support for multi-object spectra analysis.

## Use Case
When analyzing fiber spectra from SDSS, need to process
multiple objects simultaneously.

## Proposed Solution
Add batch processing mode that:
1. Reads multi-extension FITS files
2. Processes each spectrum independently  
3. Generates combined results report

## Alternatives Considered
- Manual processing (too slow)
- External scripts (complex)

## Additional Context
Would benefit astronomical surveys and large datasets.
```

---

## Release Process

### **Version Numbering**
- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes only

### **Release Checklist**
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] Changelog updated
- [ ] Create GitHub release
- [ ] Update package registries

---

## Community Guidelines

### **Code of Conduct**
- Be respectful and inclusive
- Focus on technical merit
- Help newcomers learn
- Credit contributors appropriately

### **Communication Channels**
- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, help
- **Pull Requests**: Code contributions
- **Email**: Sensitive security issues

### **Recognition**
Contributors are acknowledged in:
- README contributors section
- Release notes
- Academic publications (for significant contributions)
- Conference presentations

---

## Contribution Examples

### **Beginner-Friendly**
- Fix typos in documentation
- Add example spectrum files
- Improve error messages
- Add unit tests for existing functions

### **Intermediate**
- Implement new preprocessing options
- Add support for new file formats
- Improve GUI usability
- Optimize performance bottlenecks

### **Advanced**
- Add new correlation algorithms
- Implement machine learning features
- Extend AI integration capabilities
- Add support for new instrument types

---

## Getting Help

### **Development Questions**
- Check existing documentation
- Search GitHub issues/discussions
- Ask specific, focused questions
- Provide context and examples

### **Mentorship**
New contributors can request mentorship for:
- Understanding codebase
- Choosing appropriate issues
- Code review feedback
- Best practices guidance

---

**Ready to contribute?** Check out our [good first issues](https://github.com/FiorenSt/SNID-SAGE/labels/good%20first%20issue) or reach out on [GitHub Discussions](https://github.com/FiorenSt/SNID-SAGE/discussions)! 