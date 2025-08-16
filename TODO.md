# TODO List

## Current Issues to Address

### 1. Template Matching Issue
- **Problem**: Galaxy templates should not be included in the matching process
- **Status**: Pending
- **Priority**: High
- **Notes**: Need to investigate where galaxy templates are being included and exclude them from the matching algorithm

### 2. Cluster Detection Error
- **Problem**: When no cluster is found but results are still being returned
- **Status**: Pending  
- **Priority**: High
- **Notes**: 
  - Check spectrum from `data/` directory
  - Investigate why results are returned even when no cluster is detected
  - May need to add validation to prevent false positive results

### 3. Transient IXF Failure Issue
- **Problem**: Transient IXF seems to fail frequently
- **Status**: Pending
- **Priority**: High
- **Notes**: 
  - Investigate why transient IXF processing is failing often
  - Check for common failure patterns or edge cases
  - May need to improve error handling or validation for IXF processing
  - Consider adding retry logic or fallback mechanisms

### 4. Analysis Quality Score Cleanup
- **Problem**: Analysis quality quantitative scores like "RLAP-CCC (analysis quality): 1.74" need to be converted to categories
- **Status**: Pending
- **Priority**: Medium
- **Notes**: 
  - Current quantitative scores (e.g., 1.74) should be converted to categorical values
  - Define clear categories for analysis quality (e.g., "Poor", "Fair", "Good", "Excellent")
  - Update all analysis quality metrics to use categorical instead of numerical values
  - May need to update UI displays and result formatting
  - Consider what threshold values to use for each category

### 5. Plot Save Keyboard Shortcuts
- **Problem**: Need keyboard shortcuts for saving plots
- **Status**: Pending
- **Priority**: Medium
- **Notes**: 
  - Add Ctrl+S shortcut to save plot (same functionality as save button)
  - Add Ctrl+Shift+S shortcut to save plot as SVG
  - Implement in plot widgets/dialogs where plots are displayed
  - May need to update event handlers and keyboard shortcuts management
  - Consider adding visual feedback or tooltips to inform users about available shortcuts

## Additional Notes
- Both issues appear to be related to the core analysis functionality
- May need to review the clustering algorithm and template selection logic
- Consider adding more robust error handling and validation

---
*Last updated: $(Get-Date)*
