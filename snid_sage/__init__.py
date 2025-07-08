"""
SNID SAGE - SuperNova IDentification with Spectrum Analysis and Guided Enhancement
================================================================================

A comprehensive Python package for supernova spectrum identification and analysis,
based on the original Fortran SNID by Stéphane Blondin & John L. Tonry.

Features:
- Spectrum identification and classification
- Template library management
- Batch processing capabilities
- Modern GUI interface
- Command-line interface
- LLM integration for enhanced analysis

Author: Fiorenzo Stoppa
Email: fiorenzo.stoppa@physics.ox.ac.uk
License: MIT
"""

__version__ = "1.2.0"
__author__ = "Fiorenzo Stoppa"
__email__ = "fiorenzo.stoppa@physics.ox.ac.uk"
__license__ = "MIT"

# Import main modules
try:
    from . import snid
except ImportError:
    snid = None

try:
    from . import interfaces
except ImportError:
    interfaces = None

try:
    from . import shared
except ImportError:
    shared = None

__all__ = ['snid', 'interfaces', 'shared'] 