# Plotting and Visualization Guide

*Master the advanced visualization capabilities of SNID SAGE*

---

## Overview

SNID SAGE features a sophisticated plotting and visualization system with **2500+ lines** of plotting code, offering everything from basic spectrum plots to advanced 3D clustering visualization and interactive analysis tools.

---

## Core Plotting Features

### Spectrum Visualization

#### **Basic Spectrum Plotting**
```bash
# Simple spectrum plot
snid-sage plot spectrum.fits

# With template overlay
snid-sage plot spectrum.fits --template sn1987A.lnw

# Multiple spectra comparison
snid-sage plot spectrum1.fits spectrum2.fits spectrum3.fits --overlay
```

#### **Advanced Spectrum Options**
```bash
# Customized spectrum plot
snid-sage plot spectrum.fits \
    --wavelength-range 4000:8000 \
    --flux-scale log \
    --smooth-factor 2.0 \
    --show-lines \
    --theme dark
```

### Cross-Correlation Plots

```bash
# Correlation function visualization
snid-sage plot correlation results.json \
    --show-peaks \
    --confidence-levels \
    --interactive
```

**Correlation Plot Features:**
- Peak Identification: Automatic correlation peak detection
- Confidence Intervals: Statistical significance visualization
- Template Matching: Best matches highlighted
- Interactive Zoom: Detailed peak examination

---

## Theming System

### Available Themes

SNID SAGE includes multiple professional themes:

| **Theme** | **Description** | **Best For** |
|-----------|-----------------|--------------|
| **Light** | Clean white background | Publications, presentations |
| **Dark** | Dark background, bright text | Late-night analysis sessions |
| **Watercolor** | Artistic gradient backgrounds | Conference posters |
| **Scientific** | High-contrast, minimal | Technical papers |
| **Colorblind** | Colorblind-friendly palette | Accessibility |

#### **Theme Selection**
```bash
# Set global theme
snid-sage config set theme dark

# Use theme for specific plot
snid-sage plot spectrum.fits --theme watercolor

# Interactive theme switcher in GUI
# Tools → Preferences → Appearance → Theme
```

### Custom Theme Creation

```python
# Create custom theme
from shared.utils.plotting.plot_theming import create_custom_theme

custom_theme = create_custom_theme(
    background_color='#1a1a1a',
    text_color='#ffffff',
    line_colors=['#ff6b6b', '#4ecdc4', '#45b7d1'],
    grid_color='#333333',
    accent_color='#ffd93d'
)

# Apply custom theme
snid-sage config set theme.custom custom_theme
```

---

## Interactive Plotting Tools

### GUI Interactive Features

#### **Spectrum Analysis Tools**
- Zoom and Pan: Mouse-controlled navigation
- Line Measurement: Click-and-drag line identification
- Peak Selection: Interactive peak picking
- Real-time FWHM: Live line width calculation
- Continuum Fitting: Interactive baseline adjustment

#### **Template Comparison**
- Template Switching: Dropdown template selection
- Overlay Controls: Transparency and scaling
- Color Coding: Automatic color assignment
- Difference Plots: Template-spectrum residuals

### CLI Interactive Mode

```bash
# Launch interactive plotting session
snid-sage plot spectrum.fits --interactive

# Interactive commands available:
# - zoom: Select zoom region
# - measure: Measure line properties
# - identify: Identify spectral features
# - save: Export current view
# - quit: Exit interactive mode
```

---

## 3D Visualization

### Clustering Visualization

SNID SAGE includes advanced 3D plotting capabilities for clustering analysis:

```bash
# Generate 3D cluster plot
snid-sage identify spectrum.fits \
    --clustering \
    --plot-3d \
    --interactive-3d \
    --save-3d results/cluster_3d.png
```

#### **3D Plot Features**
- Interactive Rotation: Mouse-controlled 3D navigation
- Cluster Highlighting: Color-coded type groups
- Confidence Ellipsoids: 3D uncertainty visualization
- Point Selection: Click to identify individual spectra
- Trajectory Plotting: Evolution paths through parameter space

### Advanced 3D Options

```python
# Access 3D plotting directly
from snid.plotting_3d import create_3d_cluster_plot

fig = create_3d_cluster_plot(
    clustering_results,
    color_by='type',
    size_by='confidence',
    alpha=0.7,
    show_ellipsoids=True,
    interactive=True
)
```

---

## Multi-Panel Displays

### Comprehensive Analysis Plots

```bash
# Create multi-panel analysis figure
snid-sage plot comprehensive spectrum.fits \
    --panels "spectrum,correlation,residuals,3d" \
    --layout 2x2 \
    --output analysis_summary.pdf
```

#### **Available Panel Types**
- Spectrum: Main spectrum display
- Correlation: Cross-correlation function
- Residuals: Template-spectrum differences
- 3D Clustering: Cluster visualization
- Results Table: Classification summary
- Line Analysis: Detected line properties

### Custom Panel Layouts

```python
# Create custom multi-panel layout
from snid.plotting import MultiPanelPlotter

plotter = MultiPanelPlotter(
    layout=(3, 2),  # 3 rows, 2 columns
    panel_types=['spectrum', 'correlation', 'residuals', 
                 '3d', 'lines', 'summary'],
    shared_axes=['wavelength'],
    theme='scientific'
)

fig = plotter.create_figure(analysis_results)
```

---

## Advanced Visualization Features

### No-Title Plot Optimization

SNID SAGE includes space-efficient plotting with the **no-title plot manager**:

```python
# Access no-title optimization
from interfaces.gui.utils.no_title_plot_manager import NoTitlePlotManager

plot_manager = NoTitlePlotManager()
optimized_plot = plot_manager.optimize_plot_space(fig)
```

**Benefits:**
- Space Efficiency: Maximum plot area utilization
- Clean Appearance: Minimal visual clutter
- Better Data Visibility: Focus on scientific content
- Compact Exports: Smaller file sizes

### Interactive Line Tools

Advanced line analysis with real-time feedback:

```python
# Interactive line analysis
from interfaces.gui.components.analysis.interactive_line_tools import InteractiveLineAnalyzer

line_analyzer = InteractiveLineAnalyzer(spectrum_data)
line_analyzer.enable_manual_selection()
line_analyzer.show_real_time_feedback()
```

**Features:**
- 🎯 **Manual Line Selection**: Click to select spectral lines
- 📊 **Real-time FWHM**: Live calculation during selection
- 🌊 **Profile Fitting**: Multiple fitting methods
- 📈 **Quality Assessment**: Line strength and reliability metrics

---

## Publication-Quality Plots

### High-Resolution Export

```bash
# Export publication-ready figures
snid-sage plot spectrum.fits \
    --output publication_figure.pdf \
    --dpi 300 \
    --format pdf \
    --size 8x6 \
    --font-size 12 \
    --line-width 2.0
```

### LaTeX Integration

```bash
# Generate LaTeX-compatible plots
snid-sage plot spectrum.fits \
    --latex-fonts \
    --pgf-backend \
    --output figure.pgf
```

### Batch Figure Generation

```bash
# Generate figures for multiple spectra
snid-sage plot batch data_directory/ \
    --output figures/ \
    --format png \
    --template publication \
    --parallel-processing
```

---

## Plot Customization

### Styling Options

```bash
# Comprehensive styling
snid-sage plot spectrum.fits \
    --line-color "#ff6b6b" \
    --line-width 1.5 \
    --line-style solid \
    --marker-size 4 \
    --grid-alpha 0.3 \
    --background-color white \
    --text-color black
```

### Axis Configuration

```bash
# Advanced axis control
snid-sage plot spectrum.fits \
    --x-label "Wavelength (Å)" \
    --y-label "Flux (erg/s/cm²/Å)" \
    --x-scale linear \
    --y-scale log \
    --x-limits 3500:9500 \
    --y-limits auto
```

### Annotation Tools

```python
# Add custom annotations
from snid.plotting import add_annotations

annotations = [
    {'x': 6563, 'y': 1.2, 'text': 'Hα', 'arrow': True},
    {'x': 5876, 'y': 0.8, 'text': 'He I', 'arrow': True},
    {'x': 6150, 'y': 1.5, 'text': 'Si II', 'arrow': True}
]

add_annotations(fig, annotations)
```

---

## Specialized Plot Types

### P Cygni Profile Visualization

```bash
# Visualize P Cygni profiles
snid-sage plot pcygni spectrum.fits \
    --lines "H_alpha,He_I_5876" \
    --show-components \
    --velocity-scale
```

### Wind Velocity Plots

```bash
# Wind velocity analysis visualization
snid-sage plot wind-velocity spectrum.fits \
    --terminal-velocity \
    --expansion-profile \
    --comparison-templates
```

### Emission Line Overlays

```bash
# Comprehensive emission line identification
snid-sage plot emission-lines spectrum.fits \
    --line-database comprehensive \
    --show-identifications \
    --color-by-species
```

---

## Performance Optimization

### Large Dataset Visualization

```bash
# Optimize for large datasets
snid-sage plot large-dataset.fits \
    --fft-optimization \
    --memory-limit 4GB \
    --progressive-loading \
    --level-of-detail
```

### GPU Acceleration

```python
# Enable GPU acceleration for 3D plots
from snid.plotting_3d import enable_gpu_acceleration

enable_gpu_acceleration()  # Requires CUDA-compatible GPU
```

---

## Plotting Best Practices

### Scientific Visualization Guidelines

1. Clear Axis Labels: Always include units
2. Appropriate Scaling: Linear vs. logarithmic
3. Color Accessibility: Consider colorblind users
4. Consistent Styling: Maintain visual coherence
5. Error Representation: Show uncertainties when available

### Common Plotting Mistakes

#### **Avoid These Issues**
- **Overcrowded Plots**: Too much information in one figure
- **Poor Color Choices**: Low contrast or inaccessible colors
- **Missing Units**: Unlabeled axes
- **Inconsistent Scaling**: Mixed scales without justification
- **Low Resolution**: Pixelated exports

#### **Best Practices**
- **Focus on Key Information**: One main message per plot
- **Use High Contrast**: Ensure readability
- **Label Everything**: Axes, legends, annotations
- **Consistent Style**: Maintain visual coherence
- **High-Quality Exports**: Vector formats when possible

---

## Troubleshooting Plots

### Common Issues

#### **Plot Not Displaying**
```bash
# Check plotting backend
snid-sage config get plotting.backend

# Reset to default backend
snid-sage config set plotting.backend matplotlib
```

#### **Memory Issues with Large Plots**
```bash
# Enable memory optimization
snid-sage config set plotting.memory_efficient true
snid-sage config set plotting.max_points 10000
```

#### **Font Issues**
```bash
# Reset font cache
snid-sage plot --reset-font-cache

# Use system fonts
snid-sage config set plotting.use_system_fonts true
```

---

## Advanced Examples

### Complete Analysis Visualization

```python
# Comprehensive analysis plot
from snid.plotting import create_analysis_summary

summary_plot = create_analysis_summary(
    spectrum_file='sn2024abc.fits',
    template_matches=['sn1987A.lnw', 'sn1993J.lnw'],
    clustering_results=cluster_data,
    theme='scientific',
    output='analysis_summary.pdf'
)
```

### Interactive Dashboard

```python
# Create interactive analysis dashboard
from snid.plotting import InteractiveDashboard

dashboard = InteractiveDashboard()
dashboard.add_spectrum_panel(spectrum_data)
dashboard.add_correlation_panel(correlation_results)
dashboard.add_3d_cluster_panel(cluster_data)
dashboard.launch()
```

---

## Visualization Resources

### Color Palettes

- **🎨 Scientific**: High-contrast, colorblind-friendly
- **🌈 Qualitative**: Distinct colors for categories
- **📊 Sequential**: Gradual intensity changes
- **🔥 Diverging**: Two-color gradients from center

### Export Formats

| **Format** | **Use Case** | **Quality** | **Size** |
|------------|--------------|-------------|----------|
| **PNG** | Web, presentations | Good | Medium |
| **PDF** | Publications, vector | Excellent | Small |
| **SVG** | Web, scalable | Excellent | Small |
| **EPS** | LaTeX, print | Excellent | Medium |
| **PGF** | LaTeX integration | Excellent | Small |

---

## Visualization Support

- 🎨 **Custom Plotting**: Specialized visualization needs
- 📊 **Performance Issues**: Large dataset optimization
- 🎓 **Training**: Advanced plotting techniques
- 🔬 **Research Collaboration**: Publication-quality figures

---

*Transform your data into compelling visualizations with SNID SAGE's powerful plotting system!*