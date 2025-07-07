"""
SNID SAGE CLI Interface
======================

Command-line interface for SNID SAGE spectrum analysis.

This module provides command-line tools for:
- Spectrum identification
- Template management
- Batch processing
- Configuration management
"""

__version__ = "1.0.0"

# Import main CLI components
try:
    from .main import main
except ImportError:
    main = None

try:
    # Import command modules
    from . import identify, template, batch, config
except ImportError:
    identify = template = batch = config = None

__all__ = ['main', 'identify', 'template', 'batch', 'config'] 