"""
Vectorized Peak Finding for SNID Template Correlation

This module provides matrix-based peak finding operations that can process
multiple correlation functions simultaneously, providing significant speedup
over template-by-template processing.
"""

import numpy as np
from typing import List, Dict, Tuple, Any, Optional
from scipy.signal import find_peaks
import logging

_LOG = logging.getLogger(__name__)


class VectorizedPeakFinder:
    """
    Matrix-based peak finder for correlation functions.
    
    Processes multiple correlation functions simultaneously using vectorized
    operations for significant performance improvements.
    """
    
    def __init__(self, NW_grid: int, DWLOG_grid: float, 
                 lz1: int, lz2: int, k1: int, k2: int, k3: int, k4: int):
        """
        Initialize vectorized peak finder.
        
        Parameters
        ----------
        NW_grid : int
            Grid size (1024)
        DWLOG_grid : float
            Log wavelength step
        lz1, lz2 : int
            Redshift search range indices
        k1, k2, k3, k4 : int
            Bandpass filter parameters
        """
        self.NW_grid = NW_grid
        self.DWLOG_grid = DWLOG_grid
        self.lz1 = lz1
        self.lz2 = lz2
        self.k1, self.k2, self.k3, self.k4 = k1, k2, k3, k4
        self.mid = NW_grid // 2
        
    def find_peaks_batch(self, correlation_matrix: np.ndarray, 
                        template_names: List[str],
                        template_rms_array: np.ndarray,
                        spectrum_rms: float) -> Dict[str, Dict[str, Any]]:
        """
        Find peaks in multiple correlation functions simultaneously.
        
        Parameters
        ----------
        correlation_matrix : np.ndarray
            Shape (n_templates, NW_grid) - correlation functions for all templates
        template_names : List[str]
            Names corresponding to each row in correlation_matrix
        template_rms_array : np.ndarray
            RMS values for each template
        spectrum_rms : float
            Spectrum RMS value
            
        Returns
        -------
        Dict[str, Dict[str, Any]]
            Peak information for each template
        """
        # Normalize all correlation functions at once
        rms_products = spectrum_rms * template_rms_array
        valid_rms_mask = rms_products > 0
        
        results = {}
        if not np.any(valid_rms_mask):
            return results
            
        # Get valid templates and their data
        valid_indices = np.where(valid_rms_mask)[0]
        valid_correlations = correlation_matrix[valid_indices]
        valid_names = [template_names[i] for i in valid_indices]
        valid_rms = rms_products[valid_indices]
        
        # Normalize correlations (vectorized)
        rolled_correlations = np.roll(valid_correlations, self.mid, axis=1)
        normalized_correlations = rolled_correlations / (self.NW_grid * valid_rms[:, np.newaxis])
        
        # Process all correlation functions
        for i, (name, correlation) in enumerate(zip(valid_names, normalized_correlations)):
            # Find peaks in this correlation function
            peaks_indices, properties = find_peaks(
                correlation, 
                distance=3, 
                height=0.3
            )
            
            # Filter peaks to allowed redshift range
            valid_peaks = peaks_indices[(peaks_indices >= self.lz1) & (peaks_indices <= self.lz2)]
            
            if len(valid_peaks) > 0:
                results[name] = {
                    'peaks': valid_peaks,
                    'correlation': correlation,
                    'template_index': valid_indices[i],
                    'template_rms': template_rms_array[valid_indices[i]],
                    'properties': properties
                }
        
        return results
    

def create_vectorized_peak_finder(NW_grid: int, DWLOG_grid: float,
                                 lz1: int, lz2: int, 
                                 k1: int, k2: int, k3: int, k4: int) -> VectorizedPeakFinder:
    """
    Create a vectorized peak finder instance.
    
    Parameters
    ----------
    NW_grid : int
        Grid size
    DWLOG_grid : float
        Log wavelength step
    lz1, lz2 : int
        Redshift search range
    k1, k2, k3, k4 : int
        Bandpass filter parameters
        
    Returns
    -------
    VectorizedPeakFinder
        Configured peak finder instance
    """
    return VectorizedPeakFinder(NW_grid, DWLOG_grid, lz1, lz2, k1, k2, k3, k4) 