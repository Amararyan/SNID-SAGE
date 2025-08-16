# Basic Analysis Tutorial

This tutorial walks you through your first complete analysis using SNID SAGE, from opening the GUI to interpreting results. Follow along step-by-step to learn the essential workflow.

## Prerequisites

- SNID SAGE installed (see [Installation Guide](../installation/installation.md))
- A spectrum file to analyze (FITS, ASCII, or other supported formats)

## Step 1: Launching the GUI

Start SNID SAGE by running one of these commands in your terminal:

```bash
# Launch the main GUI
snid-sage

# Or use the Python module
python -m snid_sage
```

![Initial Screen](../images/0.InitialScreen.png)

The main window opens with a clean interface ready for analysis. The toolbar at the top provides quick access to essential functions.

## Step 2: Loading Your Spectrum

### Method 1: Drag and Drop
Simply drag your spectrum file from your file explorer directly onto the main window.

### Method 2: File Menu
1. Click **File** → **Load Spectrum**
2. Navigate to your spectrum file
3. Select the file and click **Open**

### Method 3: Toolbar Button
Click the folder icon in the toolbar to open the file dialog.

![Loaded Spectrum](../images/1.LoadedSpectrum.png)

Once loaded, your spectrum appears in the main plot area. The interface shows:
- **Raw spectrum** in the main plot
- **File information** in the status bar
- **Available actions** become enabled

## Step 3: Quick Preprocessing

Before analysis, you'll want to preprocess your spectrum to improve results.

### Opening Preprocessing
- Click **Preprocessing** in the menu bar, or
- Use the toolbar preprocessing button, or
- **Right-click** on the plot and select **Quick Preprocessing**

### Preprocessing Options

#### Flux View
![Quick Preprocessing - Flux](../images/2.QuickPreprocessing_Flux.png)

The flux view shows your spectrum with preprocessing options:
- **Filtering**: Remove noise and artifacts
- **Rebinning**: Adjust spectral resolution
- **Continuum removal**: Normalize the spectrum
- **Apodization**: Smooth spectral edges

#### Flattened View
![Quick Preprocessing - Flattened](../images/2.QuickPreprocessing_Flattened.png)

The flattened view shows the continuum-removed spectrum, making absorption and emission features more prominent.

### Quick Preprocessing Shortcuts
- **Ctrl+Enter** (Windows/Linux) or **Cmd+Enter** (macOS): Apply current preprocessing settings
- **Shift+Click**: Apply preprocessing and immediately start analysis
- **Right-click** on preprocessing controls: Access advanced options

## Step 4: Starting Analysis

### Method 1: Quick Analysis
- Click **Analysis** → **Quick Analysis**, or
- Use the toolbar analysis button, or
- **Right-click** on the plot and select **Quick Analysis**

### Method 2: Full Analysis
- Click **Analysis** → **Full Analysis** for more control over parameters

### Analysis Progress
![Analysis Progress 1](../images/3.AnalysisProgress1.png)
![Analysis Progress 2](../images/3.AnalysisProgress2.png)

The analysis dialog shows:
- **Progress bar**: Current analysis stage
- **Status messages**: What's happening
- **Cancel button**: Stop analysis if needed

## Step 5: Clustering Results

After analysis completes, SNID SAGE groups similar templates into clusters.

![Clustering](../images/4.Clustering.png)

The clustering view displays:
- **Template matches** grouped by similarity
- **Match scores** for each template
- **Spectral types** and subtypes
- **Redshift estimates**

### Clustering Interactions
- **Click** on a cluster to expand/collapse
- **Right-click** on templates for detailed information
- **Double-click** to view template comparison

## Step 6: Template Matching

### Flux Comparison
![Match Template Flux](../images/5.MatchTemplateFlux.png)

This view shows your spectrum overlaid with the best-matching template:
- **Your spectrum** (blue line)
- **Best template** (red line)
- **Match quality** indicators
- **Redshift information**

### Match Summary
![Match Summary](../images/6.MatchSummary.png)

The summary provides:
- **Top matches** with scores
- **Spectral classification**
- **Redshift estimates**
- **Confidence levels**

## Step 7: Redshift and Age Analysis

### Redshift vs Age Plot
![Redshift vs Age](../images/7.RedshiftVsAge.png)

This plot shows:
- **Redshift distribution** across templates
- **Age estimates** for different redshifts
- **Confidence regions**
- **Best-fit parameters**

### Subtype Analysis
![Subtypes](../images/8.Subtypes.png)

The subtype analysis reveals:
- **Detailed classifications**
- **Subtype proportions**
- **Template contributions**
- **Classification confidence**

## Essential Keyboard Shortcuts

### General Shortcuts
- **Ctrl+O** (Windows/Linux) / **Cmd+O** (macOS): Open spectrum file
- **Ctrl+S** / **Cmd+S**: Save results
- **Ctrl+Q** / **Cmd+Q**: Quit application
- **F1**: Open help documentation

### Analysis Shortcuts
- **Ctrl+Enter** / **Cmd+Enter**: Apply preprocessing and start analysis
- **Shift+Enter**: Quick analysis with default settings
- **Ctrl+A** / **Cmd+A**: Start full analysis
- **Escape**: Cancel current operation

### Navigation Shortcuts
- **Ctrl+Z** / **Cmd+Z**: Undo last action
- **Ctrl+Y** / **Cmd+Y**: Redo action
- **Ctrl+F** / **Cmd+F**: Find in results
- **Ctrl+P** / **Cmd+P**: Print or export plot

### Right-Click Context Menus
- **Right-click on plot**: Access quick preprocessing, analysis, and export options
- **Right-click on results**: Copy, export, or get detailed information
- **Right-click on templates**: View template details and comparisons

## Interpreting Your Results

### Match Scores
- **Score > 10**: Excellent match
- **Score 5-10**: Good match
- **Score 1-5**: Fair match
- **Score < 1**: Poor match

### Redshift Confidence
- **High confidence**: Multiple templates agree on redshift
- **Medium confidence**: Some disagreement between templates
- **Low confidence**: Wide range of redshift estimates

### Spectral Classification
- **Primary type**: Most likely classification
- **Subtypes**: Detailed classification within the primary type
- **Confidence**: How certain the classification is

## Next Steps

1. **Save your results**: Use File → Save Results to preserve your analysis
2. **Export plots**: Right-click on plots to save as images
3. **Try different preprocessing**: Experiment with different settings
4. **Compare multiple spectra**: Load additional files for comparison
5. **Advanced analysis**: Explore the full analysis options for more control

## Troubleshooting

### Common Issues
- **No templates found**: Check that template libraries are installed
- **Poor matches**: Try different preprocessing settings
- **Slow analysis**: Reduce the number of templates or use quick analysis
- **GUI not responding**: Wait for analysis to complete or restart the application

### Getting Help
- **Documentation**: Check the [Reference Guide](../reference/api-reference.md)
- **Configuration**: See [Configuration Guide](../reference/configuration-guide.md)
- **Troubleshooting**: Visit [Troubleshooting Guide](../reference/troubleshooting.md)

## Related Tutorials

- [Advanced Analysis](advanced-analysis.md): Learn advanced techniques and customization
- [AI-Assisted Analysis](ai-assisted-analysis.md): Use AI to enhance your analysis
- [Template Management](template-management.md): Manage and customize template libraries
- [Plotting and Visualization](plotting-visualization.md): Create publication-ready plots