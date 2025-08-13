# Plot Swapping System - Developer Documentation

## Overview

The SNID SAGE GUI has been enhanced with a comprehensive plot swapping system that ensures seamless transitions between different types of plots. This system properly handles the coordination between:

1. **Flux/Flat buttons** (spectrum view controls)
2. **Right panel analysis buttons** (GMM clustering, redshift vs age, etc.)
3. **Plot state management** (remembering previous states)

## Architecture

### Plot Controller (`interfaces/gui/controllers/plot_controller.py`)

The `PlotController` class now includes advanced state management:

```python
class PlotController:
    def __init__(self, gui_instance):
        # NEW: Plot state management
        self.current_plot_type = None     # Track current plot type
        self.last_spectrum_view = 'flux'  # Remember last spectrum view
        self.plot_stack = []              # Track plot history
```

### Plot Types

The system recognizes these plot types:

- **Spectrum plots**: `'spectrum_flux'`, `'spectrum_flat'`
- **Analysis plots**: `'gmm_clustering'`, `'redshift_age'`, `'subtype_proportions'`, `'cluster_summary'`

## Key Features

### 1. Automatic View Style Management

When switching between plot types:
- **To spectrum plots**: Flux/Flat buttons are activated and properly set
- **To analysis plots**: Flux/Flat buttons are deactivated (grayed out)
- **Back to spectrum**: Previous spectrum view (flux/flat) is restored

### 2. State Preservation

```python
def _set_plot_type(self, plot_type):
    """Set plot type and handle view state transitions"""
    # Store current spectrum view before switching to analysis plots
    if plot_type in ['gmm_clustering', 'redshift_age', 'subtype_proportions']:
        if self.gui.view_style.get() in ['Flux', 'Flat']:
            self.last_spectrum_view = self.gui.view_style.get().lower()
```

### 3. Proper Button Coordination

All plot buttons now coordinate through the plot controller:

```python
# Right panel buttons delegate to plot controller
def plot_gmm_clustering(self):
    if hasattr(self, 'plot_controller'):
        self.plot_controller.plot_gmm_clustering()

# Plot controller handles state management
def plot_gmm_clustering(self):
    self._set_plot_type('gmm_clustering')  # Deactivates Flux/Flat buttons
    # ... plot the GMM clustering
```

## Usage Examples

### Example 1: User clicks GMM Clustering while Flux view is active

1. **Before**: Flux button is active, showing spectrum in flux view
2. **User clicks**: "🔮 GMM Clustering" button
3. **System response**:
   - `_set_plot_type('gmm_clustering')` is called
   - Current flux view is saved to `last_spectrum_view`
   - Flux/Flat buttons are deactivated (view_style set to "")
   - GMM clustering plot is displayed
4. **Result**: GMM clustering plot shown, Flux/Flat buttons grayed out

### Example 2: User clicks Flat button while GMM Clustering is active

1. **Before**: GMM clustering plot active, Flux/Flat buttons grayed out
2. **User clicks**: "Flat" button
3. **System response**:
   - `_on_view_style_change()` detects switch from analysis plot
   - `plot_flat_view()` is called
   - `_set_plot_type('spectrum_flat')` is called
   - Flat button becomes active, Flux button inactive
   - Spectrum is displayed in flat view
4. **Result**: Flat spectrum view shown, Flat button active

### Example 3: User switches between analysis plots

1. **User clicks**: "📈 Redshift vs Age" while GMM clustering is shown
2. **System response**:
   - `_set_plot_type('redshift_age')` is called
   - Previous analysis plot type stored in plot_stack
   - Redshift vs age plot displayed
   - Flux/Flat buttons remain deactivated
3. **Result**: Smooth transition between analysis plots

## Implementation Details

### View Style Control Integration

The enhanced view controller properly handles state transitions:

```python
def _on_view_style_change(self, *args):
    style = self.gui.view_style.get()
    
    if style == "Flux":
        # Check if switching from analysis plot
        if self.gui.plot_controller.is_analysis_plot_active():
            _LOGGER.debug("🔄 Switching from analysis plot to flux view")
        self.gui.plot_controller.plot_flux_view()
    # ... similar for Flat
    elif style == "":
        # View style deactivated for analysis plots
        pass
```

### State Checking Methods

New utility methods for checking plot state:

```python
def is_analysis_plot_active(self):
    """Check if an analysis plot is currently active"""
    return self.current_plot_type in ['gmm_clustering', 'redshift_age', 
                                     'subtype_proportions', 'cluster_summary']

def is_spectrum_plot_active(self):
    """Check if a spectrum plot is currently active"""
    return self.current_plot_type in ['spectrum_flux', 'spectrum_flat']
```

## Testing the System

### Manual Test Cases

1. **Basic spectrum switching**:
   - Load spectrum → Click Flux → Click Flat → Verify smooth transition

2. **Spectrum to analysis**:
   - Show flux view → Click GMM clustering → Verify Flux/Flat buttons deactivated

3. **Analysis back to spectrum**:
   - Show GMM clustering → Click Flux → Verify return to flux view

4. **Analysis to analysis**:
   - Show GMM clustering → Click Redshift vs Age → Verify smooth transition

5. **State preservation**:
   - Show flat view → Click analysis plot → Click Flux → Should show flux, not flat
   - Show flat view → Click analysis plot → Click Flat → Should show flat view

## Benefits

1. **Consistent behavior**: All plot buttons behave predictably
2. **State preservation**: Users return to their previous spectrum view
3. **Clear visual feedback**: Button states clearly indicate current plot type
4. **Robust error handling**: Graceful fallbacks if components aren't available
5. **Developer friendly**: Clear separation of concerns and easy to extend

## Future Enhancements

Potential improvements to consider:

1. **Plot history navigation**: Back/forward buttons for plot history
2. **Plot thumbnails**: Quick preview of different plot types
3. **Custom plot layouts**: Side-by-side plot comparisons
4. **Plot bookmarks**: Save favorite plot configurations

## Troubleshooting

### Common Issues

1. **Buttons not updating**: Check that `_update_segmented_control_buttons()` is called
2. **Wrong spectrum view restored**: Verify `last_spectrum_view` is properly saved
3. **Analysis plots not deactivating Flux/Flat**: Ensure `_set_plot_type()` is called
4. **3D axis errors**: System automatically detects and fixes incompatible axis types
5. **Subplot layout issues**: System detects multiple axes and reinitializes for single plots

### Automatic Error Recovery

The system includes automatic recovery for common plot transition issues:

- **3D → 2D transitions**: Automatically detects `Axes3D` incompatibility and reinitializes
- **Multi-subplot → single plot**: Detects multiple axes and creates fresh single plot
- **Retry mechanism**: Attempts reinitialization once, with safeguards against infinite loops

### Debug Logging

The system includes extensive debug logging:

```
🔄 Plot type changed to: gmm_clustering
🔘 View style deactivated for analysis plot
🔄 Switching from analysis plot to flux view
🔄 Restored spectrum view to: Flat
🔧 Reinitializing matplotlib for transition: gmm_clustering → spectrum_flux
⚠️ Detected 3D/incompatible axis error - forcing plot reinitialization
✅ Matplotlib reinitialized successfully
```

Enable debug logging to trace plot state transitions. 