# API Reference

Complete API reference for SNID SAGE's programmatic interface, including all classes, methods, and functions.

## Overview

SNID SAGE provides a Python API for:
- **Spectrum analysis** and classification
- **Template management** and matching
- **Data preprocessing** and validation
- **Result processing** and export
- **Workflow automation** and customization

## First Analysis

### **Basic Usage**
```python
from snid.snid import run_snid, preprocess_spectrum, run_snid_analysis
from snid.io import read_spectrum

# Method 1: Full pipeline
result, trace = run_snid(
    spectrum_path="spectrum.dat",
    templates_dir="templates/",
    output_dir="results/"
)

# Method 2: Step-by-step
# Preprocess spectrum
processed_spectrum, trace = preprocess_spectrum(
    spectrum_path="spectrum.dat",
    aband_remove=True,
    skyclip=True
)

# Run analysis
result, analysis_trace = run_snid_analysis(
    processed_spectrum,
    templates_dir="templates/",
    zmin=-0.01,
    zmax=1.0
)

# Access results
print(f"Type: {result.consensus_type}")
print(f"Redshift: {result.redshift}")
print(f"Confidence: {result.rlap}")
```

---

## Core Functions

### **run_snid()**

Main function for complete SNID analysis pipeline.

```python
def run_snid(
    spectrum_path: str,
    templates_dir: str,
    *,
    # Preprocessing options
    preprocessed_spectrum: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    skip_preprocessing_steps: Optional[List[str]] = None,
    savgol_window: int = 0,
    savgol_fwhm: float = 0.0,
    savgol_order: int = 3,
    aband_remove: bool = False,
    skyclip: bool = False,
    emclip_z: float = -1.0,
    emwidth: float = 40.0,
    wavelength_masks: Optional[List[Tuple[float, float]]] = None,
    apodize_percent: float = 10.0,
    # Analysis parameters
    zmin: float = -0.01,
    zmax: float = 1.0,
    age_range: Optional[Tuple[float, float]] = None,
    type_filter: Optional[List[str]] = None,
    template_filter: Optional[List[str]] = None,
    forced_redshift: Optional[float] = None,
    peak_window_size: int = 10,
    lapmin: float = 0.3,
    rlapmin: float = 5,
    # Output options
    output_dir: Optional[str] = None,
    output_main: bool = False,
    output_fluxed: bool = False,
    output_flattened: bool = False,
    output_correlation: bool = False,
    output_plots: bool = False,
    plot_types: Optional[List[str]] = None,
    max_output_templates: int = 5,
    max_plot_templates: int = 20,
    plot_figsize: Tuple[int, int] = (10, 8),
    plot_dpi: int = 150,
    verbose: bool = False,
    # Plotting options
    show_plots: bool = True,
    save_plots: bool = False,
    plot_dir: Optional[str] = None
) -> Tuple[SNIDResult, Dict[str, Any]]
```

**Parameters:**
- `spectrum_path` (str): Path to input spectrum file
- `templates_dir` (str): Path to template library directory
- `preprocessed_spectrum` (tuple, optional): Pre-processed (wave, flux) arrays
- `skip_preprocessing_steps` (list, optional): Steps to skip in preprocessing
- `savgol_window` (int): Savitzky-Golay filter window size (0 = no filtering)
- `savgol_fwhm` (float): Savitzky-Golay filter FWHM in Angstroms
- `savgol_order` (int): Savitzky-Golay filter polynomial order
- `aband_remove` (bool): Remove telluric A-band
- `skyclip` (bool): Clip sky emission lines
- `emclip_z` (float): Redshift for emission line clipping (-1 to disable)
- `emwidth` (float): Width for emission line clipping
- `wavelength_masks` (list): Wavelength ranges to mask
- `apodize_percent` (float): Percentage of spectrum ends to apodize
- `zmin` (float): Minimum redshift to search
- `zmax` (float): Maximum redshift to search
- `age_range` (tuple, optional): Age range filter for templates
- `type_filter` (list, optional): Supernova types to include
- `template_filter` (list, optional): Specific templates to use
- `forced_redshift` (float, optional): Force analysis at specific redshift
- `peak_window_size` (int): Window size for peak detection
- `lapmin` (float): Minimum overlap fraction
- `rlapmin` (float): Minimum rlap value
- `output_dir` (str, optional): Directory for output files
- `output_main` (bool): Generate main output file
- `output_fluxed` (bool): Generate fluxed spectrum file
- `output_flattened` (bool): Generate flattened spectrum file
- `output_correlation` (bool): Generate correlation files
- `output_plots` (bool): Generate plots
- `plot_types` (list, optional): Types of plots to generate
- `max_output_templates` (int): Maximum templates in output
- `max_plot_templates` (int): Maximum templates to plot
- `plot_figsize` (tuple): Figure size for plots
- `plot_dpi` (int): DPI for saved plots
- `verbose` (bool): Print detailed information
- `show_plots` (bool): Display plots
- `save_plots` (bool): Save plots to files
- `plot_dir` (str, optional): Directory for saved plots

**Returns:**
- `SNIDResult`: Analysis results object
- `trace` (dict): Processing trace for debugging

### **preprocess_spectrum()**

Preprocess a spectrum for SNID analysis.

```python
def preprocess_spectrum(
    spectrum_path: Optional[str] = None,
    input_spectrum: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    *,
    savgol_window: int = 0,
    savgol_fwhm: float = 0.0,
    savgol_order: int = 3,
    aband_remove: bool = False,
    skyclip: bool = False,
    emclip_z: float = -1.0,
    emwidth: float = 40.0,
    wavelength_masks: Optional[List[Tuple[float, float]]] = None,
    apodize_percent: float = 10.0,
    skip_steps: Optional[List[str]] = None,
    verbose: bool = False
) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]
```

**Parameters:**
- `spectrum_path` (str, optional): Path to spectrum file
- `input_spectrum` (tuple, optional): (wavelength, flux) arrays
- `savgol_window` (int): Savitzky-Golay filter window size
- `savgol_fwhm` (float): Savitzky-Golay filter FWHM
- `savgol_order` (int): Savitzky-Golay filter order
- `aband_remove` (bool): Remove telluric A-band
- `skyclip` (bool): Clip sky emission lines
- `emclip_z` (float): Redshift for emission line clipping
- `emwidth` (float): Width for emission line clipping
- `wavelength_masks` (list): Wavelength ranges to mask
- `apodize_percent` (float): Percentage to apodize
- `skip_steps` (list, optional): Steps to skip
- `verbose` (bool): Print detailed information

**Returns:**
- `processed_spectrum` (dict): Processed spectrum data
  - `'input_spectrum'`: Original input
  - `'log_wave'`: Log-rebinned wavelength
  - `'log_flux'`: Log-rebinned flux
  - `'flat_flux'`: Flattened flux
  - `'tapered_flux'`: Apodized flux
  - `'continuum'`: Fitted continuum
  - `'nonzero_mask'`: Valid data region
  - `'left_edge'`: Left edge index
  - `'right_edge'`: Right edge index
  - `'grid_params'`: Grid parameters
- `trace` (dict): Processing trace

### **run_snid_analysis()**

Run SNID analysis on preprocessed spectrum.

```python
def run_snid_analysis(
    processed_spectrum: Dict[str, np.ndarray],
    templates_dir: str,
    *,
    zmin: float = -0.01,
    zmax: float = 1.0,
    age_range: Optional[Tuple[float, float]] = None,
    type_filter: Optional[List[str]] = None,
    template_filter: Optional[List[str]] = None,
    exclude_templates: Optional[List[str]] = None,
    forced_redshift: Optional[float] = None,
    peak_window_size: int = 10,
    lapmin: float = 0.3,
    rlapmin: float = 5,
    max_output_templates: int = 5,
    verbose: bool = False,
    show_plots: bool = True,
    save_plots: bool = False,
    plot_dir: Optional[str] = None,
    progress_callback: Optional[Callable[[str, float], None]] = None
) -> Tuple[SNIDResult, Dict[str, Any]]
```

**Parameters:**
- `processed_spectrum` (dict): Preprocessed spectrum from `preprocess_spectrum()`
- `templates_dir` (str): Path to template library
- `zmin` (float): Minimum redshift
- `zmax` (float): Maximum redshift
- `age_range` (tuple, optional): Age range filter
- `type_filter` (list, optional): Type filter
- `template_filter` (list, optional): Template name filter
- `exclude_templates` (list, optional): Templates to exclude
- `forced_redshift` (float, optional): Force specific redshift
- `peak_window_size` (int): Peak detection window
- `lapmin` (float): Minimum overlap
- `rlapmin` (float): Minimum rlap
- `max_output_templates` (int): Maximum output templates
- `verbose` (bool): Verbose output
- `show_plots` (bool): Show plots
- `save_plots` (bool): Save plots
- `plot_dir` (str, optional): Plot directory
- `progress_callback` (callable, optional): Progress callback

**Returns:**
- `SNIDResult`: Analysis results
- `trace` (dict): Analysis trace

---

## Result Classes

### **SNIDResult**

Class containing SNID analysis results.

#### **Properties**
- `success` (bool): Whether analysis succeeded
- `spectrum_name` (str): Input spectrum name
- `template_name` (str): Best matching template
- `template_type` (str): Best template type
- `template_subtype` (str): Best template subtype
- `consensus_type` (str): Consensus classification
- `best_subtype` (str): Best subtype
- `redshift` (float): Determined redshift
- `redshift_error` (float): Redshift uncertainty
- `age` (float): Age from maximum light
- `age_error` (float): Age uncertainty
- `rlap` (float): Best rlap value
- `lap` (float): Best overlap fraction
- `runtime_sec` (float): Analysis runtime
- `best_matches` (list): List of best template matches
- `filtered_matches` (list): Filtered matches above threshold
- `all_correlations` (list): All correlation results
- `type_fractions` (dict): Fraction of each type
- `subtype_fractions` (dict): Fraction of each subtype
- `clustering_results` (dict): GMM clustering results
- `processed_spectrum` (dict): Processed spectrum data

#### **Methods**

##### **get_summary()**
Get a text summary of results.

```python
def get_summary(self) -> str
```

**Returns:**
- `str`: Human-readable summary

##### **to_dict()**
Convert results to dictionary.

```python
def to_dict(self) -> Dict[str, Any]
```

**Returns:**
- `dict`: Results as dictionary

---

## I/O Functions

### **read_spectrum()**

Read spectrum from file.

```python
def read_spectrum(filename: str) -> Tuple[np.ndarray, np.ndarray]
```

**Parameters:**
- `filename` (str): Path to spectrum file

**Returns:**
- `wavelength` (np.ndarray): Wavelength array
- `flux` (np.ndarray): Flux array

**Supported formats:**
- ASCII text files (.dat, .txt, .ascii)
- CSV files (.csv)
- FITS files (.fits, .fit)

### **load_templates()**

Load template library.

```python
def load_templates(
    template_dir: str,
    flatten: bool = True
) -> Tuple[List[Dict], Dict]
```

**Parameters:**
- `template_dir` (str): Template directory
- `flatten` (bool): Whether to flatten templates

**Returns:**
- `templates` (list): List of template dictionaries
- `metadata` (dict): Template metadata

### **write_result()**

Write analysis results to file.

```python
def write_result(
    filename: str,
    result: SNIDResult,
    format: str = 'json'
)
```

**Parameters:**
- `filename` (str): Output filename
- `result` (SNIDResult): Analysis results
- `format` (str): Output format ('json', 'txt')

---

## Plotting Functions

### **plot_correlation_function()**

Plot correlation function.

```python
def plot_correlation_function(
    correlation_data: Dict,
    output_file: Optional[str] = None,
    show: bool = True
)
```

**Parameters:**
- `correlation_data` (dict): Correlation data
- `output_file` (str, optional): Save to file
- `show` (bool): Display plot

### **plot_type_fractions()**

Plot type fraction pie chart.

```python
def plot_type_fractions(
    type_fractions: Dict[str, float],
    output_file: Optional[str] = None,
    show: bool = True
)
```

**Parameters:**
- `type_fractions` (dict): Type fractions
- `output_file` (str, optional): Save to file
- `show` (bool): Display plot

---

## Preprocessing Functions

### **log_rebin()**

Rebin spectrum to logarithmic wavelength grid.

```python
def log_rebin(
    wave: np.ndarray,
    flux: np.ndarray,
    num_points: int = 1024
) -> Tuple[np.ndarray, np.ndarray]
```

**Parameters:**
- `wave` (np.ndarray): Input wavelength
- `flux` (np.ndarray): Input flux
- `num_points` (int): Number of output points

**Returns:**
- `log_wave` (np.ndarray): Log-rebinned wavelength
- `log_flux` (np.ndarray): Log-rebinned flux

### **fit_continuum()**

Fit and remove continuum.

```python
def fit_continuum(
    flux: np.ndarray,
    method: str = "spline",
    sigma: float = 50
) -> Tuple[np.ndarray, np.ndarray]
```

**Parameters:**
- `flux` (np.ndarray): Input flux
- `method` (str): Fitting method
- `sigma` (float): Smoothing parameter

**Returns:**
- `flat_flux` (np.ndarray): Flattened flux
- `continuum` (np.ndarray): Fitted continuum

### **apodize()**

Apply apodization to spectrum ends.

```python
def apodize(
    flux: np.ndarray,
    left_edge: int,
    right_edge: int,
    percent: float = 10.0
) -> np.ndarray
```

**Parameters:**
- `flux` (np.ndarray): Input flux
- `left_edge` (int): Left edge index
- `right_edge` (int): Right edge index
- `percent` (float): Percentage to apodize

**Returns:**
- `tapered_flux` (np.ndarray): Apodized flux

---

## Template Management

### **Template Structure**

Templates are stored as HDF5 files with the following structure:

```python
template = {
    'name': str,           # Template name
    'type': str,           # Supernova type
    'subtype': str,        # Subtype
    'age': float,          # Days from maximum
    'redshift': float,     # Template redshift
    'quality': float,      # Quality score
    'wave': np.ndarray,    # Wavelength array
    'flux': np.ndarray,    # Flux array
    'metadata': dict       # Additional metadata
}
```

### **Template Functions**

#### **add_template()**

Add template to library.

```python
def add_template(
    library_path: str,
    spectrum_file: str,
    template_info: Dict,
    force_rebin: bool = False
) -> str
```

**Parameters:**
- `library_path` (str): Template library path
- `spectrum_file` (str): Spectrum file to add
- `template_info` (dict): Template metadata
- `force_rebin` (bool): Force rebinning

**Returns:**
- `template_file` (str): Added template path

#### **get_template_info()**

Get template library information.

```python
def get_template_info(library_path: str) -> Dict
```

**Parameters:**
- `library_path` (str): Library path

**Returns:**
- `info` (dict): Library information

#### Merged index and user overrides (HDF5)

`get_template_info()` reads the unified storage index from `template_index.json` and, if present, merges it with the user index `User_templates/template_index.user.json`. If a per-type user HDF5 file exists (e.g., `User_templates/templates_Ia.user.hdf5`), templates for that type are taken exclusively from the user file and base entries for that type are ignored. This ensures that any user edits (add/rename/delete) for a type immediately take precedence across CLI and GUI without duplications.

---

## Usage Examples

### **Basic Analysis**
```python
from snid.snid import run_snid

# Simple analysis
result, trace = run_snid(
    "spectrum.dat",
    "templates/",
    output_dir="results/"
)

print(f"Classification: {result.consensus_type}")
print(f"Redshift: {result.redshift:.4f}")
print(f"Best template: {result.template_name}")
```

### **Advanced Analysis**
```python
from snid.snid import preprocess_spectrum, run_snid_analysis

# Custom preprocessing
processed, _ = preprocess_spectrum(
    "spectrum.dat",
    savgol_window=11,
    aband_remove=True,
    skyclip=True,
    wavelength_masks=[(6550, 6600), (7600, 7700)]
)

# Filtered analysis
result, _ = run_snid_analysis(
    processed,
    "templates/",
    type_filter=["Ia", "Ib", "Ic"],
    age_range=(-5, 20),
    zmin=0.0,
    zmax=0.1
)
```

### **Batch Processing**
```python
from snid.snid import run_snid
import glob

# Process multiple spectra
spectra = glob.glob("data/*.dat")
results = []

for spectrum in spectra:
    result, _ = run_snid(
        spectrum,
        "templates/",
        output_dir=f"results/{Path(spectrum).stem}/"
    )
    results.append(result)

# Summary statistics
types = [r.consensus_type for r in results if r.success]
print(f"Processed {len(results)} spectra")
print(f"Type distribution: {Counter(types)}")
```

### **Forced Redshift Analysis**
```python
# Known redshift from host galaxy
result, _ = run_snid(
    "spectrum.dat",
    "templates/",
    forced_redshift=0.0234,
    output_dir="results/"
)
```

---

## Error Handling

### **Common Exceptions**

- `FileNotFoundError`: Spectrum or template file not found
- `ValueError`: Invalid parameter values
- `RuntimeError`: Analysis failed
- `MemoryError`: Insufficient memory for templates

### **Error Handling Example**
```python
try:
    result, trace = run_snid("spectrum.dat", "templates/")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Invalid parameters: {e}")
except Exception as e:
    print(f"Analysis failed: {e}")
```

---

## Related Documentation

- **[CLI Reference](../cli/command-reference.md)** - Command-line interface
- **[GUI Manual](../gui/interface-overview.md)** - Graphical interface
- **[First Analysis](../quickstart/first-analysis.md)** - Step-by-step guide
- **[Template Guide](../data/template-library.md)** - Template management

---

**Note**: This API reference reflects the actual implementation of SNID SAGE v1.1.0. For the latest updates, check the [GitHub repository](https://github.com/FiorenSt/SNID-SAGE). 