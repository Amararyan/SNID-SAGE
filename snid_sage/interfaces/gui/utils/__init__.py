"""
SNID SAGE GUI Utils Package
===========================

Utilities and helper functions for the SNID SAGE GUI.
Part of the SNID SAGE GUI restructuring.

NOTE: This package contains both Tkinter and PySide6 utilities.
Import specific modules as needed rather than using this package directly.
"""

# Cross-platform utilities (framework-agnostic)
from .import_manager import check_optional_features

# Tkinter-specific utilities (DEPRECATED - moved to OLD_* files)
TKINTER_UTILS_AVAILABLE = False

# PySide6-specific utilities
try:
    from .unified_pyside6_layout_manager import UnifiedPySide6LayoutManager, LayoutSettings
    from .pyside6_helpers import PySide6Helpers
    PYSIDE6_UTILS_AVAILABLE = True
except ImportError:
    PYSIDE6_UTILS_AVAILABLE = False

# Conditional exports based on what's available
__all__ = ['check_optional_features']

if PYSIDE6_UTILS_AVAILABLE:
    __all__.extend([
        'UnifiedPySide6LayoutManager',
        'LayoutSettings',
        'PySide6Helpers'
    ]) 
