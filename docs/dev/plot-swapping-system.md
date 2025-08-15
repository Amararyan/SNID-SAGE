# Plot Swapping System

The SNID SAGE GUI has been enhanced with a comprehensive plot swapping system that ensures seamless transitions between different types of plots. This system properly handles the coordination between:

- **Matplotlib backend switching** (TkAgg ↔ Qt5Agg)
- **Plot type transitions** (spectrum → clustering → redshift-age)
- **Memory management** and cleanup
- **State preservation** during transitions

## Core Components

### Plot Controller
The `PlotController` class now includes advanced state management:

```python
class PlotController:
    def __init__(self):
        self.current_plot_type = None
        self.current_backend = None
        self.plot_objects = {}
        self.transition_history = []
```

### Backend Management
- **TkAgg**: Used for spectrum plots and basic analysis
- **Qt5Agg**: Used for interactive clustering and advanced plots
- **Automatic switching**: Based on plot type requirements

## Transition Workflow

### 1. User Interaction
1. **User clicks**: "Redshift vs Age" while GMM clustering is shown
2. **System detects**: Plot type change required
3. **Backend check**: Determines if backend switch needed

### 2. Backend Transition
```python
def switch_backend(self, target_backend):
    if self.current_backend != target_backend:
        # Save current state
        self.save_plot_state()
        
        # Switch backend
        matplotlib.use(target_backend)
        
        # Reinitialize plotting
        self.reinitialize_plotting()
```

### 3. Plot Recreation
- **State restoration**: Previous plot data preserved
- **New plot creation**: Target plot type generated
- **UI update**: Plot widget refreshed

## Memory Management

### Cleanup Procedures
```python
def cleanup_previous_plot(self):
    # Clear matplotlib figure
    plt.close('all')
    
    # Clear plot objects
    self.plot_objects.clear()
    
    # Garbage collection
    gc.collect()
```

### State Preservation
- **Plot data**: Saved before transition
- **User selections**: Preserved across transitions
- **Analysis results**: Maintained in memory

## Error Handling

### Transition Failures
```python
def handle_transition_error(self, error):
    # Log error details
    _LOGGER.error(f"Plot transition failed: {error}")
    
    # Fallback to previous state
    self.restore_previous_state()
    
    # Notify user
    self.show_error_message("Plot transition failed")
```

### Recovery Mechanisms
- **Automatic rollback**: Return to previous plot state
- **User notification**: Clear error messages
- **Logging**: Detailed error tracking

## Performance Optimization

### Transition Speed
- **Lazy loading**: Plot data loaded on demand
- **Caching**: Frequently used plots cached
- **Background processing**: Heavy computations in threads

### Memory Efficiency
- **Object pooling**: Reuse plot objects when possible
- **Selective cleanup**: Only clear necessary resources
- **Garbage collection**: Explicit cleanup calls

## Implementation Details

### Backend Detection
```python
def detect_required_backend(self, plot_type):
    if plot_type in ['gmm_clustering', 'redshift_age']:
        return 'Qt5Agg'
    else:
        return 'TkAgg'
```

### State Management
```python
def save_plot_state(self):
    self.plot_state = {
        'current_data': self.current_data,
        'user_selections': self.user_selections,
        'plot_settings': self.plot_settings
    }
```

## Testing

### Transition Tests
- **Backend switching**: Verify smooth transitions
- **State preservation**: Ensure data integrity
- **Error recovery**: Test failure scenarios
- **Performance**: Measure transition times

### Integration Tests
- **GUI integration**: Test with main interface
- **Memory usage**: Monitor resource consumption
- **User workflow**: End-to-end testing

## Future Enhancements

### Planned Improvements
- **Additional backends**: Support for more plotting backends
- **Enhanced caching**: More sophisticated plot caching
- **Async transitions**: Non-blocking plot changes
- **Custom transitions**: User-configurable transition effects

### Performance Goals
- **Transition time**: < 500ms for most transitions
- **Memory usage**: < 100MB additional overhead
- **Error rate**: < 1% transition failures

## Troubleshooting

### Common Issues

**Slow Transitions**
- Check available memory
- Verify backend installation
- Monitor system resources

**Transition Failures**
- Check matplotlib backend compatibility
- Verify plot data integrity
- Review error logs

**Memory Leaks**
- Monitor memory usage over time
- Check cleanup procedures
- Verify garbage collection

### Debug Information
```python
def get_debug_info(self):
    return {
        'current_backend': self.current_backend,
        'plot_objects_count': len(self.plot_objects),
        'memory_usage': self.get_memory_usage(),
        'transition_history': self.transition_history
    }
```

## Conclusion

The plot swapping system provides a robust foundation for seamless plot transitions in SNID SAGE. It handles complex backend switching while maintaining data integrity and providing a smooth user experience.

For more information, see:
- [GUI Interface Overview](../gui/interface-overview.md)
- [Plot Management](../gui/results-and-plots.md)
- [Troubleshooting](../reference/troubleshooting.md) 