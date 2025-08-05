"""
Statistically rigorous weighted calculations for redshift and age estimation in SNID SAGE.

This module implements RLAP-Cos weighted estimation methods for optimal redshift 
and age estimation with full covariance analysis.
"""

import numpy as np
from typing import Union, List, Tuple, Optional
import logging

# Get logger for this module
logger = logging.getLogger(__name__)


def calculate_joint_weighted_estimates(
    redshifts: Union[np.ndarray, List[float]], 
    ages: Union[np.ndarray, List[float]],
    weights: Union[np.ndarray, List[float]]
) -> Tuple[float, float, float, float, float]:
    """
    Calculate joint weighted estimates for redshift and age with full covariance.
    
    This implements a statistically robust joint estimation approach that:
    1. Uses RLAP-Cos values as quality-based weights
    2. Computes weighted centroids in (redshift, age) space  
    3. Estimates the full 2×2 weighted covariance matrix
    4. Extracts marginal uncertainties and correlation from the covariance matrix
    
    Parameters
    ----------
    redshifts : array-like
        Redshift values from templates
    ages : array-like  
        Age values from templates (in days)
    weights : array-like
        RLAP-Cos quality weights for each template
        
    Returns
    -------
    Tuple[float, float, float, float, float]
        (weighted_redshift, weighted_age, redshift_uncertainty, age_uncertainty, redshift_age_covariance)
        
    Notes
    -----
    Statistical Method:
    - Weighted mean: μ = Σ(wᵢ xᵢ) / Σ(wᵢ)
    - Weighted covariance: Cov = Σ(wᵢ (xᵢ-μ)(yᵢ-ν)ᵀ) / Σ(wᵢ) × N_eff/(N_eff-1)
    - Effective sample size: N_eff = (Σwᵢ)² / Σ(wᵢ²)
    - Standard errors: σ_x = √(Var(x)/N_eff), σ_y = √(Var(y)/N_eff) 
    """
    redshifts = np.asarray(redshifts, dtype=float)
    ages = np.asarray(ages, dtype=float)
    weights = np.asarray(weights, dtype=float)
    
    # Validate inputs
    if len(redshifts) == 0 or len(ages) == 0 or len(weights) == 0:
        return np.nan, np.nan, np.nan, np.nan, np.nan
        
    if not (len(redshifts) == len(ages) == len(weights)):
        logger.error("Mismatched input lengths for joint estimation")
        return np.nan, np.nan, np.nan, np.nan, np.nan
    
    # Remove invalid data points
    valid_mask = (np.isfinite(redshifts) & np.isfinite(ages) & 
                  np.isfinite(weights) & (weights > 0))
    
    if not np.any(valid_mask):
        logger.warning("No valid (redshift, age, weight) triplets found")
        return np.nan, np.nan, np.nan, np.nan, np.nan
        
    valid_z = redshifts[valid_mask]
    valid_t = ages[valid_mask]
    valid_w = weights[valid_mask]
    N = len(valid_z)
    
    if N == 1:
        return float(valid_z[0]), float(valid_t[0]), 0.0, 0.0, 0.0
    
    # Calculate weighted means (centroids)
    sum_w = np.sum(valid_w)
    z_mean = np.sum(valid_w * valid_z) / sum_w
    t_mean = np.sum(valid_w * valid_t) / sum_w
    
    # Calculate effective sample size (handles clustering effects)
    sum_w_sq = np.sum(valid_w ** 2)
    N_eff = (sum_w ** 2) / sum_w_sq
    
    # Calculate weighted covariance matrix elements
    z_dev = valid_z - z_mean
    t_dev = valid_t - t_mean
    
    # Weighted variances and covariance (population estimates)
    var_z_pop = np.sum(valid_w * z_dev ** 2) / sum_w
    var_t_pop = np.sum(valid_w * t_dev ** 2) / sum_w  
    cov_zt_pop = np.sum(valid_w * z_dev * t_dev) / sum_w
    
    # Apply bias correction for finite sample size to get sample estimates
    if N_eff > 1:
        bias_correction = N_eff / (N_eff - 1)
        var_z_sample = var_z_pop * bias_correction
        var_t_sample = var_t_pop * bias_correction  
        cov_zt_sample = cov_zt_pop * bias_correction
    else:
        var_z_sample = var_z_pop
        var_t_sample = var_t_pop
        cov_zt_sample = cov_zt_pop
    
    # Standard errors of the weighted means (uncertainty in the means themselves)
    se_z = np.sqrt(var_z_sample / N_eff) if N_eff > 0 else np.inf
    se_t = np.sqrt(var_t_sample / N_eff) if N_eff > 0 else np.inf
    
    # Covariance of the means
    cov_means = cov_zt_sample / N_eff if N_eff > 0 else 0.0
    
    logger.info(f"Joint weighted estimates: "
                f"z={z_mean:.6f}±{se_z:.6f}, age={t_mean:.1f}±{se_t:.1f} days, "
                f"cov(z,t)={cov_means:.8f}, N_eff={N_eff:.1f}")
    
    result = (float(z_mean), float(t_mean), float(se_z), float(se_t), float(cov_means))
    return result


def calculate_weighted_redshift(
    redshifts: Union[np.ndarray, List[float]], 
    weights: Union[np.ndarray, List[float]]
) -> Tuple[float, float]:
    """
    Calculate weighted redshift estimate.
    
    Parameters
    ----------
    redshifts : array-like
        Redshift values from templates
    weights : array-like
        RLAP-Cos quality weights for each template
        
    Returns
    -------
    Tuple[float, float]
        (weighted_redshift, redshift_uncertainty)
    """
    redshifts = np.asarray(redshifts, dtype=float)
    weights = np.asarray(weights, dtype=float)
    
    if len(redshifts) == 0 or len(weights) == 0:
        return np.nan, np.nan
        
    if len(redshifts) != len(weights):
        logger.error("Mismatched input lengths for redshift estimation")
        return np.nan, np.nan
    
    # Remove invalid data points  
    # Weights should be > 0 (RLAP, cosine similarity, or RLAP-cos are all positive metrics)
    valid_mask = (np.isfinite(redshifts) & np.isfinite(weights) & (weights > 0))
    
    if not np.any(valid_mask):
        logger.warning("No valid (redshift, weight) pairs found")
        return np.nan, np.nan
        
    valid_z = redshifts[valid_mask]
    valid_w = weights[valid_mask]
    N = len(valid_z)
    
    if N == 1:
        return float(valid_z[0]), 0.0
    
    # Calculate weighted mean
    sum_w = np.sum(valid_w)
    z_mean = np.sum(valid_w * valid_z) / sum_w
    
    # Calculate effective sample size and uncertainty
    sum_w_sq = np.sum(valid_w ** 2)
    N_eff = (sum_w ** 2) / sum_w_sq
    
    # Weighted variance with bias correction
    z_dev = valid_z - z_mean
    var_z = np.sum(valid_w * z_dev ** 2) / sum_w
    
    if N_eff > 1:
        bias_correction = N_eff / (N_eff - 1)
        var_z *= bias_correction
    
    # Standard error of the weighted mean
    se_z = np.sqrt(var_z / N_eff) if N_eff > 0 else np.inf
    
    logger.info(f"Weighted redshift: {z_mean:.6f}±{se_z:.6f}, N_eff={N_eff:.1f}")
    
    return float(z_mean), float(se_z)


def calculate_weighted_age(
    ages: Union[np.ndarray, List[float]], 
    weights: Union[np.ndarray, List[float]]
) -> Tuple[float, float]:
    """
    Calculate weighted age estimate.
    
    Parameters
    ----------
    ages : array-like
        Age values in days
    weights : array-like
        RLAP-Cos quality weights for each template
        
    Returns
    -------
    Tuple[float, float]
        (weighted_age, age_uncertainty)
    """
    ages = np.asarray(ages, dtype=float)
    weights = np.asarray(weights, dtype=float)
    
    if len(ages) == 0 or len(weights) == 0:
        return np.nan, np.nan
        
    if len(ages) != len(weights):
        logger.error("Mismatched input lengths for age estimation")
        return np.nan, np.nan
    
    # Remove invalid data points
    # Note: Ages can be negative (before peak), so no age > 0 filter
    # Weights should be > 0 (RLAP, cosine similarity, or RLAP-cos are all positive metrics)
    valid_mask = (np.isfinite(ages) & np.isfinite(weights) & (weights > 0))
    
    if not np.any(valid_mask):
        # Count different types of invalid data for better diagnostics
        invalid_ages = np.sum(~np.isfinite(ages))  # Only non-finite ages are invalid
        invalid_weights = np.sum(~np.isfinite(weights) | (weights <= 0))  # Non-finite or non-positive weights
        total_pairs = len(ages)
        
        logger.warning(
            f"No valid (age, weight) pairs found from {total_pairs} templates. "
            f"Invalid ages: {invalid_ages} (non-finite), invalid weights: {invalid_weights} (≤0 or non-finite). "
            f"Note: Negative ages are valid (pre-peak). This typically means templates have low quality scores."
        )
        return np.nan, np.nan
        
    valid_t = ages[valid_mask]
    valid_w = weights[valid_mask]
    N = len(valid_t)
    
    if N == 1:
        return float(valid_t[0]), 0.0
    
    # Calculate weighted mean
    sum_w = np.sum(valid_w)
    t_mean = np.sum(valid_w * valid_t) / sum_w
    
    # Calculate effective sample size and uncertainty
    sum_w_sq = np.sum(valid_w ** 2)
    N_eff = (sum_w ** 2) / sum_w_sq
    
    # Weighted variance with bias correction
    t_dev = valid_t - t_mean
    var_t = np.sum(valid_w * t_dev ** 2) / sum_w
    
    if N_eff > 1:
        bias_correction = N_eff / (N_eff - 1)
        var_t *= bias_correction
    
    # Standard error of the weighted mean
    se_t = np.sqrt(var_t / N_eff) if N_eff > 0 else np.inf
    
    logger.info(f"Weighted age: {t_mean:.1f}±{se_t:.1f} days, N_eff={N_eff:.1f}")
    
    return float(t_mean), float(se_t)


def calculate_weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    """Calculate weighted median."""
    if len(values) == 0:
        return np.nan
        
    if len(values) == 1:
        return float(values[0])
    
    # Remove invalid data
    valid_mask = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    if not np.any(valid_mask):
        return np.nan
        
    valid_values = values[valid_mask]
    valid_weights = weights[valid_mask]
    
    if len(valid_values) == 1:
        return float(valid_values[0])
    
    # Sort by values
    sorted_indices = np.argsort(valid_values)
    sorted_values = valid_values[sorted_indices]
    sorted_weights = valid_weights[sorted_indices]
    
    # Calculate cumulative weights
    cumsum_weights = np.cumsum(sorted_weights)
    total_weight = cumsum_weights[-1]
    
    # Find median position
    median_weight = total_weight / 2.0
    
    # Find the value(s) at median position
    idx = np.searchsorted(cumsum_weights, median_weight)
    
    if idx == 0:
        return float(sorted_values[0])
    elif idx >= len(sorted_values):
        return float(sorted_values[-1])
    else:
        # Linear interpolation between adjacent values
        w1 = cumsum_weights[idx-1]
        w2 = cumsum_weights[idx]
        if w1 == median_weight:
            return float(sorted_values[idx-1])
        elif w2 == median_weight:
            return float((sorted_values[idx-1] + sorted_values[idx]) / 2.0)
        else:
            # Interpolate
            alpha = (median_weight - w1) / (w2 - w1)
            return float(sorted_values[idx-1] + alpha * (sorted_values[idx] - sorted_values[idx-1]))


def validate_joint_result(
    redshifts: np.ndarray,
    ages: np.ndarray, 
    weights: np.ndarray,
    result: Tuple[float, float, float, float, float]
) -> bool:
    """
    Validate a joint weighted calculation result.
    
    Parameters
    ----------
    redshifts : np.ndarray
        Input redshift values
    ages : np.ndarray
        Input age values
    weights : np.ndarray
        Input weights
    result : Tuple[float, float, float, float, float]
        (z_mean, t_mean, z_uncertainty, t_uncertainty, zt_covariance)
        
    Returns
    -------
    bool
        True if result is valid, False otherwise
    """
    z_mean, t_mean, z_uncertainty, t_uncertainty, zt_covariance = result
    
    # Check for finite values
    if not all(np.isfinite([z_mean, t_mean, z_uncertainty, t_uncertainty, zt_covariance])):
        # Allow NaN if inputs are empty
        if len(redshifts) == 0 or len(ages) == 0:
            return all(np.isnan([z_mean, t_mean, z_uncertainty, t_uncertainty, zt_covariance]))
        return False
    
    # Empty input case
    if len(redshifts) == 0 or len(ages) == 0:
        return all(np.isnan([z_mean, t_mean, z_uncertainty, t_uncertainty, zt_covariance]))
    
    # Check if means are within input bounds
    min_z, max_z = np.min(redshifts), np.max(redshifts)
    min_t, max_t = np.min(ages), np.max(ages)
    
    if not (min_z <= z_mean <= max_z):
        return False
    if not (min_t <= t_mean <= max_t):
        return False
        
    # Check if uncertainties are positive and reasonable
    z_range = max_z - min_z if len(redshifts) > 1 else 1.0
    t_range = max_t - min_t if len(ages) > 1 else 1.0
    
    if z_uncertainty < 0 or z_uncertainty > z_range:
        return False
    if t_uncertainty < 0 or t_uncertainty > t_range:
        return False
    
    # Check for single-template case (uncertainties should be 0)
    if len(redshifts) == 1 or len(ages) == 1:
        return z_uncertainty == 0.0 and t_uncertainty == 0.0 and zt_covariance == 0.0
        
    # Check correlation coefficient constraint: |ρ| ≤ 1
    if z_uncertainty > 0 and t_uncertainty > 0:
        correlation = zt_covariance / (z_uncertainty * t_uncertainty)
        if abs(correlation) > 1.0 + 1e-10:  # Allow small numerical errors
            logger.debug(f"Invalid correlation coefficient: ρ={correlation:.3f}")
            return False
        
    # Check covariance matrix positive semidefinite constraint
    z_var = z_uncertainty**2
    t_var = t_uncertainty**2
    determinant = z_var * t_var - zt_covariance**2
    
    # Allow small numerical errors (relative to the matrix scale)
    tolerance = 1e-10 * max(z_var * t_var, 1e-20)
    if determinant < -tolerance:
        logger.debug(f"Covariance matrix not positive semidefinite")
        return False
        
    return True


def validate_weighted_calculation(
    values: np.ndarray, 
    weights: np.ndarray, 
    result: Tuple[float, float]
) -> bool:
    """Validate a weighted calculation result."""
    weighted_mean, uncertainty = result
    
    if not np.isfinite(weighted_mean) or not np.isfinite(uncertainty):
        return False
        
    if len(values) == 0:
        return np.isnan(weighted_mean) and np.isnan(uncertainty)
        
    # Check if result is within reasonable bounds
    min_val, max_val = np.min(values), np.max(values)
    if not (min_val <= weighted_mean <= max_val):
        return False
        
    # Check if uncertainty is positive and reasonable
    if uncertainty < 0 or uncertainty > (max_val - min_val):
        return False
        
    return True


# Exports
__all__ = [
    'calculate_joint_weighted_estimates',
    'calculate_weighted_redshift', 
    'calculate_weighted_age',
    'calculate_weighted_median',
    'validate_joint_result',
    'validate_weighted_calculation'
]