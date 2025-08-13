# Publication-Ready Plots Tutorial

Complete guide to creating professional, publication-quality plots and figures in SNID SAGE.

## What Makes a Plot Publication-Ready?

Publication-ready plots require:
- **High resolution** (300+ DPI for print)
- **Clear typography** (readable fonts and sizes)
- **Proper formatting** (consistent style and layout)
- **Complete labeling** (axes, titles, legends)
- **Color accessibility** (colorblind-friendly schemes)
- **Vector formats** (scalable for any size)

## Prerequisites

### **Setup Requirements**
- SNID SAGE installed and configured
- Sample spectrum data for plotting
- Understanding of basic plotting concepts
- Target journal requirements (if applicable)

### **Sample Data**
We'll use these spectra for the tutorial:
- **`sn2003jo.dat`** - High-quality Type Ia supernova
- **`tns_2019muj.ascii`** - Modern transient discovery
- **`ATLAS25egg_MagE.txt`** - High-resolution spectrum

---

## Part 1: Basic Publication Plotting

### **Step 1: Generate Analysis Results**

First, let's create analysis results to plot:

```bash
# Run analysis with plotting
python run_snid_cli.py identify data/sn2003jo.dat \
    --output-dir publication_plots/ \
    --complete \
    --plot-all
```

### **Step 2: Create Basic Publication Plot**

#### **CLI Method**
```bash
# Generate publication-ready plot
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum \
    --format pdf \
    --dpi 300 \
    --size 10x6 \
    --publication-style

# With custom parameters
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum \
    --format pdf \
    --dpi 300 \
    --size 8x6 \
    --font-size 12 \
    --line-width 1.5 \
    --output publication_spectrum.pdf
```

#### **GUI Method**
1. Load spectrum and run analysis
2. Open **"Plot Manager"** dialog
3. Select **"Publication Style"** theme
4. Configure plot parameters
5. Export in high-resolution format

### **Step 3: Understanding Plot Parameters**

#### **Essential Parameters**
```yaml
Format Options:
  - PDF: Vector format, best for publications
  - SVG: Vector format, good for web
  - PNG: Raster format, high DPI for print
  - EPS: Vector format, traditional journals

Resolution Settings:
  - 300 DPI: Standard for print publications
  - 600 DPI: High-quality print
  - 150 DPI: Web/display use

Size Options:
  - 8x6 inches: Standard single-column
  - 10x6 inches: Wide format
  - 6x4 inches: Small format
  - Custom: User-defined dimensions
```

---

## Part 2: Advanced Plot Styling

### **Step 1: Custom Plot Themes**

#### **Journal-Specific Themes**
```bash
# ApJ style
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --theme apj \
    --format pdf \
    --dpi 300

# MNRAS style
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --theme mnras \
    --format pdf \
    --dpi 300

# A&A style
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --theme aa \
    --format pdf \
    --dpi 300

# Custom theme
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --theme custom \
    --theme-file my_theme.yaml \
    --format pdf \
    --dpi 300
```

#### **Custom Theme Configuration**
```yaml
# my_theme.yaml
theme:
  name: "Custom Publication Theme"
  
  # Typography
  font_family: "Times New Roman"
  font_size: 12
  font_weight: "normal"
  
  # Colors
  color_scheme: "colorblind_friendly"
  primary_color: "#1f77b4"
  secondary_color: "#ff7f0e"
  background_color: "white"
  
  # Lines
  line_width: 1.5
  line_style: "solid"
  
  # Axes
  axis_line_width: 1.0
  grid_line_width: 0.5
  grid_alpha: 0.3
  
  # Margins
  margin_left: 0.12
  margin_right: 0.05
  margin_top: 0.05
  margin_bottom: 0.12
```

### **Step 2: Multi-Panel Plots**

#### **Spectrum + Correlation Plot**
```bash
# Create multi-panel plot
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type multi-panel \
    --panels spectrum correlation \
    --layout 2x1 \
    --format pdf \
    --dpi 300 \
    --size 10x8 \
    --output multi_panel_plot.pdf
```

#### **Custom Multi-Panel Layout**
```bash
# Custom panel arrangement
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type custom-multi \
    --panels spectrum correlation residuals \
    --layout 3x1 \
    --panel-sizes 0.6 0.2 0.2 \
    --format pdf \
    --dpi 300 \
    --size 10x10 \
    --output custom_multi_panel.pdf
```

### **Step 3: Advanced Styling Options**

#### **Color Schemes**
```bash
# Colorblind-friendly scheme
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --color-scheme colorblind_friendly \
    --format pdf \
    --dpi 300

# Journal-specific colors
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --color-scheme apj \
    --format pdf \
    --dpi 300

# Custom colors
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --colors "#1f77b4" "#ff7f0e" "#2ca02c" "#d62728" \
    --format pdf \
    --dpi 300
```

#### **Typography Options**
```bash
# Custom fonts
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --font-family "Times New Roman" \
    --font-size 12 \
    --font-weight normal \
    --format pdf \
    --dpi 300

# LaTeX rendering
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --latex-rendering \
    --format pdf \
    --dpi 300
```

---

## Part 3: Specialized Plot Types

### **Step 1: Spectrum Comparison Plots**

#### **Template Comparison**
```bash
# Spectrum vs template
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum-comparison \
    --show-template \
    --template-name "SN 1994D" \
    --format pdf \
    --dpi 300 \
    --size 10x6 \
    --output spectrum_comparison.pdf
```

#### **Multiple Template Comparison**
```bash
# Compare with multiple templates
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type multi-template \
    --templates "SN 1994D" "SN 2011fe" "SN 2014J" \
    --format pdf \
    --dpi 300 \
    --size 10x8 \
    --output multi_template_comparison.pdf
```

### **Step 2: Correlation Analysis Plots**

#### **Cross-Correlation Function**
```bash
# Correlation function plot
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type correlation \
    --show-peak \
    --show-confidence \
    --format pdf \
    --dpi 300 \
    --size 8x6 \
    --output correlation_function.pdf
```

#### **Correlation Matrix**
```bash
# Correlation matrix for multiple templates
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type correlation-matrix \
    --top-templates 10 \
    --format pdf \
    --dpi 300 \
    --size 8x8 \
    --output correlation_matrix.pdf
```

### **Step 3: Clustering and Classification Plots**

#### **3D Clustering Visualization**
```bash
# 3D clustering plot
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type clustering-3d \
    --show-clusters \
    --show-confidence \
    --format pdf \
    --dpi 300 \
    --size 10x8 \
    --output clustering_3d.pdf
```

#### **Classification Confidence Plot**
```bash
# Classification confidence
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type classification-confidence \
    --show-alternatives \
    --format pdf \
    --dpi 300 \
    --size 8x6 \
    --output classification_confidence.pdf
```

---

## Part 4: Interactive Plot Customization

### **Step 1: GUI Plot Editor**

#### **Launch Interactive Editor**
```bash
# Open interactive plot editor
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --interactive \
    --type spectrum
```

#### **Interactive Features**
```yaml
Available Tools:
  - Zoom: Mouse wheel or selection box
  - Pan: Click and drag
  - Line Selection: Click on spectral features
  - Annotation: Add text and arrows
  - Color Picker: Change colors interactively
  - Font Editor: Modify typography
  - Layout Adjuster: Resize panels
```

### **Step 2: Advanced Customization**

#### **Custom Annotations**
```bash
# Add custom annotations
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum \
    --annotations "Si II 6355" "Ca II H&K" "Fe II blend" \
    --annotation-positions 6355 3933 4500 \
    --format pdf \
    --dpi 300 \
    --output annotated_spectrum.pdf
```

#### **Custom Legends**
```bash
# Custom legend
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum \
    --legend-labels "Observed Spectrum" "SN 1994D Template" \
    --legend-position "upper right" \
    --format pdf \
    --dpi 300 \
    --output custom_legend.pdf
```

---

## Part 5: Journal-Specific Requirements

### **Step 1: ApJ (Astrophysical Journal)**

#### **ApJ Requirements**
```yaml
Format Requirements:
  - Format: PDF or EPS
  - Resolution: 300 DPI minimum
  - Size: Single column (3.5 inches wide)
  - Font: Times New Roman or similar
  - Color: CMYK for print, RGB for online

Style Guidelines:
  - Clear, readable fonts
  - High contrast colors
  - Minimal grid lines
  - Complete axis labels
  - Figure captions in separate file
```

#### **ApJ Plot Generation**
```bash
# ApJ-compliant plot
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --theme apj \
    --format pdf \
    --dpi 300 \
    --size 3.5x2.5 \
    --font-family "Times New Roman" \
    --font-size 10 \
    --color-scheme cmyk \
    --output apj_spectrum.pdf
```

### **Step 2: MNRAS (Monthly Notices of the Royal Astronomical Society)**

#### **MNRAS Requirements**
```yaml
Format Requirements:
  - Format: PDF or EPS
  - Resolution: 300 DPI minimum
  - Size: Single column (3.3 inches wide)
  - Font: Arial or Helvetica
  - Color: Black and white preferred

Style Guidelines:
  - Simple, clean design
  - Clear line styles
  - Minimal decorations
  - Complete labeling
  - High contrast
```

#### **MNRAS Plot Generation**
```bash
# MNRAS-compliant plot
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --theme mnras \
    --format pdf \
    --dpi 300 \
    --size 3.3x2.4 \
    --font-family "Arial" \
    --font-size 9 \
    --color-scheme black_white \
    --output mnras_spectrum.pdf
```

### **Step 3: A&A (Astronomy & Astrophysics)**

#### **A&A Requirements**
```yaml
Format Requirements:
  - Format: PDF or EPS
  - Resolution: 300 DPI minimum
  - Size: Single column (3.5 inches wide)
  - Font: Times New Roman
  - Color: CMYK for print

Style Guidelines:
  - Professional appearance
  - Clear typography
  - Appropriate color schemes
  - Complete information
  - High quality
```

#### **A&A Plot Generation**
```bash
# A&A-compliant plot
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --theme aa \
    --format pdf \
    --dpi 300 \
    --size 3.5x2.5 \
    --font-family "Times New Roman" \
    --font-size 10 \
    --color-scheme cmyk \
    --output aa_spectrum.pdf
```

---

## 🎯 **Part 6: Figure Preparation**

### **Step 1: Figure Assembly**

#### **Multi-Panel Figure**
```bash
# Create complex multi-panel figure
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type figure-assembly \
    --panels spectrum correlation classification clustering \
    --layout 2x2 \
    --format pdf \
    --dpi 300 \
    --size 12x10 \
    --output complete_figure.pdf
```

#### **Figure with Insets**
```bash
# Figure with inset panels
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type figure-with-insets \
    --main-panel spectrum \
    --insets "Si II region" "Ca II region" \
    --inset-positions "upper right" "lower right" \
    --format pdf \
    --dpi 300 \
    --size 10x8 \
    --output figure_with_insets.pdf
```

### **Step 2: Figure Captions**

#### **Generate Figure Captions**
```bash
# Generate figure caption
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --generate-caption \
    --output figure_caption.txt

# Generate caption with specific style
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --generate-caption \
    --caption-style apj \
    --output apj_caption.txt
```

#### **Example Figure Caption**
```
Figure 1: Optical spectrum of Type Ia supernova SN 2023xyz at z = 0.0017, 
obtained +2.1 days from maximum light. The spectrum shows strong Si II λ6355 
absorption (v = 11,800 ± 200 km/s) and Ca II H&K lines, confirming 
classification as a normal Type Ia supernova. Template comparison (red dashed 
line) shows excellent agreement with SN 1994D at similar phase. The spectrum 
exhibits no detectable hydrogen features, confirming thermonuclear explosion 
mechanism. Key spectral features are labeled, including Si II λ6355 absorption 
and Ca II H&K lines. The high signal-to-noise ratio (S/N ≈ 15) and 
comprehensive wavelength coverage (3500-9000 Å) enable detailed spectral 
feature analysis and robust classification.
```

---

## Part 7: Batch Plot Generation

### **Step 1: Multiple Spectrum Plots**

#### **Batch Plot Generation**
```bash
# Generate plots for multiple spectra
python run_snid_cli.py plot-batch results/ \
    --type spectrum \
    --format pdf \
    --dpi 300 \
    --size 10x6 \
    --output batch_plots/

# With consistent styling
python run_snid_cli.py plot-batch results/ \
    --type spectrum \
    --theme apj \
    --format pdf \
    --dpi 300 \
    --size 3.5x2.5 \
    --output apj_batch_plots/
```

#### **Batch with Custom Parameters**
```bash
# Custom batch parameters
python run_snid_cli.py plot-batch results/ \
    --type spectrum \
    --format pdf \
    --dpi 300 \
    --size 10x6 \
    --font-family "Times New Roman" \
    --font-size 12 \
    --color-scheme colorblind_friendly \
    --output custom_batch_plots/
```

### **Step 2: Plot Organization**

#### **Organize Generated Plots**
```bash
# Create organized directory structure
mkdir -p publication_figures/{spectra,correlations,classifications}

# Move plots to organized structure
python run_snid_cli.py plot organize-batch \
    --input batch_plots/ \
    --output publication_figures/ \
    --organize-by type
```

#### **Generate Plot Index**
```bash
# Create plot index
python run_snid_cli.py plot generate-index \
    --input publication_figures/ \
    --output plot_index.html
```

---

## Part 8: Advanced Plotting Features

### **Step 1: Custom Plot Types**

#### **Phase Evolution Plot**
```bash
# Phase evolution plot
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type phase-evolution \
    --phases -5 0 5 10 15 \
    --format pdf \
    --dpi 300 \
    --size 10x8 \
    --output phase_evolution.pdf
```

#### **Velocity Evolution Plot**
```bash
# Velocity evolution plot
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type velocity-evolution \
    --lines "Si II 6355" "Ca II H&K" \
    --format pdf \
    --dpi 300 \
    --size 8x6 \
    --output velocity_evolution.pdf
```

### **Step 2: Statistical Plots**

#### **Confidence Distribution**
```bash
# Classification confidence distribution
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type confidence-distribution \
    --show-histogram \
    --show-cumulative \
    --format pdf \
    --dpi 300 \
    --size 8x6 \
    --output confidence_distribution.pdf
```

#### **Correlation Statistics**
```bash
# Correlation statistics plot
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type correlation-stats \
    --show-top-matches 10 \
    --format pdf \
    --dpi 300 \
    --size 8x6 \
    --output correlation_stats.pdf
```

---

## Part 8: Plot Optimization

### **Step 1: File Size Optimization**

#### **Vector Format Optimization**
```bash
# Optimize PDF file size
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum \
    --format pdf \
    --optimize-size \
    --output optimized_spectrum.pdf

# Compress PDF
python run_snid_cli.py plot compress-pdf optimized_spectrum.pdf \
    --output compressed_spectrum.pdf
```

#### **Raster Format Optimization**
```bash
# Optimize PNG file size
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum \
    --format png \
    --dpi 300 \
    --optimize-size \
    --output optimized_spectrum.png
```

### **Step 2: Quality Assurance**

#### **Plot Validation**
```bash
# Validate plot quality
python run_snid_cli.py plot validate publication_spectrum.pdf \
    --output validation_report.txt

# Check resolution
python run_snid_cli.py plot check-resolution publication_spectrum.pdf

# Verify colors
python run_snid_cli.py plot check-colors publication_spectrum.pdf
```

#### **Print Preview**
```bash
# Generate print preview
python run_snid_cli.py plot print-preview publication_spectrum.pdf \
    --output print_preview.pdf

# Check print compatibility
python run_snid_cli.py plot check-print publication_spectrum.pdf
```

---

## Part 9: Troubleshooting

### **Common Issues**

#### **Resolution Problems**
```bash
# Check current resolution
python run_snid_cli.py plot check-resolution plot.pdf

# Increase resolution
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum \
    --format pdf \
    --dpi 600 \
    --output high_res_spectrum.pdf
```

#### **Font Issues**
```bash
# Check available fonts
python run_snid_cli.py plot list-fonts

# Use system fonts
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum \
    --font-family "Arial" \
    --format pdf \
    --dpi 300
```

#### **Color Problems**
```bash
# Check color scheme
python run_snid_cli.py plot check-colors plot.pdf

# Convert to grayscale
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum \
    --color-scheme grayscale \
    --format pdf \
    --dpi 300
```

### **Performance Issues**

#### **Large File Sizes**
```bash
# Optimize file size
python run_snid_cli.py plot optimize-size large_plot.pdf \
    --output optimized_plot.pdf

# Use vector formats
python run_snid_cli.py plot publication_plots/sn2003jo_results.json \
    --type spectrum \
    --format svg \
    --output vector_spectrum.svg
```

---

## Part 10: Best Practices

### **Plot Design Guidelines**

#### **General Principles**
1. **Clarity**: Make plots easy to understand
2. **Simplicity**: Avoid unnecessary decorations
3. **Consistency**: Use consistent styling
4. **Completeness**: Include all necessary information
5. **Accessibility**: Ensure colorblind-friendly schemes

#### **Typography Guidelines**
1. **Readable fonts**: Use clear, professional fonts
2. **Appropriate sizes**: Ensure text is readable
3. **Consistent styling**: Use consistent font families
4. **Proper labeling**: Include complete axis labels
5. **Clear legends**: Make legends easy to read

### **Technical Guidelines**

#### **Format Selection**
1. **PDF**: Best for publications and print
2. **SVG**: Good for web and vector editing
3. **PNG**: Use for web with high DPI
4. **EPS**: Traditional journal format

#### **Resolution Guidelines**
1. **300 DPI**: Minimum for print publications
2. **600 DPI**: High-quality print
3. **150 DPI**: Web/display use
4. **Vector formats**: Scalable to any size

### **Journal-Specific Guidelines**

#### **Common Requirements**
1. **Check journal guidelines**: Follow specific requirements
2. **Use appropriate formats**: PDF/EPS for most journals
3. **Follow size limits**: Respect column width limits
4. **Use proper fonts**: Times New Roman or Arial
5. **Ensure quality**: High resolution and clear appearance

---

## Future Developments

### **Planned Features**

#### **Advanced Plotting**
- **Interactive plots**: Web-based interactive figures
- **3D visualization**: Advanced 3D plotting capabilities
- **Animation support**: Time-series animations
- **Real-time plotting**: Live plot updates

#### **Enhanced Export**
- **Multiple formats**: Simultaneous export to multiple formats
- **Batch optimization**: Automated batch optimization
- **Quality checking**: Automated quality assessment
- **Journal templates**: Pre-configured journal templates

### **Community Development**

#### **Plot Sharing**
- **Plot galleries**: Community plot sharing
- **Template sharing**: Share custom plot templates
- **Style guides**: Community style guidelines
- **Best practices**: Community best practices

---

## Support & Resources

### **Documentation**
- **[Plotting Guide](../gui/interface-overview.md)** - GUI plotting features
- **[Configuration Guide](../reference/configuration-guide.md)** - Plot configuration options
- **[Advanced Analysis](advanced-analysis.md)** - Advanced plotting techniques

### **Tools & Utilities**
```bash
# Plotting commands
python run_snid_cli.py plot --help

# Theme management
python run_snid_cli.py plot themes --help

# Format conversion
python run_snid_cli.py plot convert --help
```

### **Community Support**
- **GitHub Issues**: Report plotting problems
- **Discussions**: Plot-related questions
- **Contributions**: Submit plot improvements
- **Feedback**: Plot feature suggestions

---

## References

### **Key Publications**
- **Journal Guidelines**: ApJ, MNRAS, A&A style guides
- **Plot Design**: Scientific visualization best practices
- **Typography**: Scientific typography guidelines

### **Resources**
- **Color Schemes**: Colorblind-friendly color schemes
- **Font Resources**: Scientific font recommendations
- **Plot Examples**: Example publication plots

For more information, see:
- **[Plotting Guide](../gui/interface-overview.md)** - GUI plotting features
- **[Configuration Guide](../reference/configuration-guide.md)** - Plot configuration options
- **[Advanced Analysis](advanced-analysis.md)** - Advanced plotting techniques