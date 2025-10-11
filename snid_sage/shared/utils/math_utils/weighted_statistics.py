"""
Statistically rigorous weighted calculations for redshift and age estimation in SNID SAGE.

This module implements best-metric weighted estimation methods (preferring RLAP-CCC) for optimal redshift 
and age estimation with full covariance analysis.
"""

import numpy as np
from typing import Union, List, Tuple, Optional
import logging

# Get logger for this module
logger = logging.getLogger(__name__)


def compute_cluster_weights(
    rlap_ccc_values: Union[np.ndarray, List[float]],
    redshift_errors: Union[np.ndarray, List[float]]
) -> np.ndarray:
    """
    Compute canonical cluster weights: w_i = (rlapccc_i)^2 / sigma_z_i^2.

    This is a thin wrapper around calculate_combined_weights for clarity.
    """
    return calculate_combined_weights(rlap_ccc_values, redshift_errors)


def _weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    """Compute weighted mean with basic validation; returns NaN if no valid data."""
    if values.size == 0 or weights.size == 0:
        return float('nan')
    sum_w = float(np.sum(weights))
    if sum_w <= 0 or not np.isfinite(sum_w):
        return float('nan')
    return float(np.sum(weights * values) / sum_w)


def _weighted_sample_sd(values: np.ndarray, weights: np.ndarray) -> float:
    """
    Bias-corrected weighted sample standard deviation over cluster values.

    - Population variance: var_pop = Σ w_i (x_i - μ)^2 / Σ w_i
    - N_eff = (Σ w_i)^2 / Σ (w_i^2)
    - Sample variance: var_sample = var_pop × N_eff/(N_eff - 1)
    - SD = sqrt(var_sample); return NaN if N_eff ≤ 1
    """
    if values.size == 0 or weights.size == 0:
        return float('nan')
    valid_mask = (np.isfinite(values) & np.isfinite(weights) & (weights > 0))
    if not np.any(valid_mask):
        return float('nan')
    v = values[valid_mask]
    w = weights[valid_mask]
    sum_w = float(np.sum(w))
    if sum_w <= 0 or not np.isfinite(sum_w):
        return float('nan')
    mean = float(np.sum(w * v) / sum_w)
    dev = v - mean
    var_pop = float(np.sum(w * (dev ** 2)) / sum_w)
    sum_w_sq = float(np.sum(w ** 2))
    if sum_w_sq <= 0:
        return float('nan')
    n_eff = (sum_w ** 2) / sum_w_sq
    if n_eff <= 1:
        return float('nan')
    var_sample = var_pop * (n_eff / (n_eff - 1.0))
    return float(np.sqrt(var_sample))


def estimate_weighted_redshift(
    redshifts: Union[np.ndarray, List[float]],
    redshift_errors: Union[np.ndarray, List[float]],
    rlap_ccc_values: Union[np.ndarray, List[float]]
) -> float:
    """
    Weighted mean redshift using weights w = (rlapccc)^2 / sigma_z^2.
    """
    z = np.asarray(redshifts, dtype=float)
    sigma = np.asarray(redshift_errors, dtype=float)
    r = np.asarray(rlap_ccc_values, dtype=float)
    if not (len(z) == len(sigma) == len(r)):
        logger.error("Mismatched input lengths for estimate_weighted_redshift")
        return float('nan')
    valid = (np.isfinite(z) & np.isfinite(sigma) & np.isfinite(r) & (sigma > 0))
    if not np.any(valid):
        return float('nan')
    w = compute_cluster_weights(r[valid], sigma[valid])
    return _weighted_mean(z[valid], w)


def estimate_weighted_epoch(
    ages: Union[np.ndarray, List[float]],
    redshift_errors: Union[np.ndarray, List[float]],
    rlap_ccc_values: Union[np.ndarray, List[float]]
) -> float:
    """
    Weighted mean epoch (age) using the same cluster weights as redshift:
    w = (rlapccc)^2 / sigma_z^2.
    """
    t = np.asarray(ages, dtype=float)
    sigma = np.asarray(redshift_errors, dtype=float)
    r = np.asarray(rlap_ccc_values, dtype=float)
    if not (len(t) == len(sigma) == len(r)):
        logger.error("Mismatched input lengths for estimate_weighted_epoch")
        return float('nan')
    valid = (np.isfinite(t) & np.isfinite(sigma) & np.isfinite(r) & (sigma > 0))
    if not np.any(valid):
        return float('nan')
    w = compute_cluster_weights(r[valid], sigma[valid])
    return _weighted_mean(t[valid], w)


def weighted_redshift_sd(
    redshifts: Union[np.ndarray, List[float]],
    redshift_errors: Union[np.ndarray, List[float]],
    rlap_ccc_values: Union[np.ndarray, List[float]]
) -> float:
    """
    Weighted sample SD of cluster redshifts using w = (rlapccc)^2 / sigma_z^2.
    Returns NaN if fewer than 2 effective samples.
    """
    z = np.asarray(redshifts, dtype=float)
    sigma = np.asarray(redshift_errors, dtype=float)
    r = np.asarray(rlap_ccc_values, dtype=float)
    if not (len(z) == len(sigma) == len(r)):
        logger.error("Mismatched input lengths for weighted_redshift_sd")
        return float('nan')
    valid = (np.isfinite(z) & np.isfinite(sigma) & np.isfinite(r) & (sigma > 0))
    if not np.any(valid):
        return float('nan')
    w = compute_cluster_weights(r[valid], sigma[valid])
    return _weighted_sample_sd(z[valid], w)


def weighted_epoch_sd(
    ages: Union[np.ndarray, List[float]],
    redshift_errors: Union[np.ndarray, List[float]],
    rlap_ccc_values: Union[np.ndarray, List[float]]
) -> float:
    """
    Weighted sample SD of cluster ages using w = (rlapccc)^2 / sigma_z^2.
    Returns NaN if fewer than 2 effective samples.
    """
    t = np.asarray(ages, dtype=float)
    sigma = np.asarray(redshift_errors, dtype=float)
    r = np.asarray(rlap_ccc_values, dtype=float)
    if not (len(t) == len(sigma) == len(r)):
        logger.error("Mismatched input lengths for weighted_epoch_sd")
        return float('nan')
    valid = (np.isfinite(t) & np.isfinite(sigma) & np.isfinite(r) & (sigma > 0))
    if not np.any(valid):
        return float('nan')
    w = compute_cluster_weights(r[valid], sigma[valid])
    return _weighted_sample_sd(t[valid], w)

def calculate_combined_weights(
    rlap_ccc_values: Union[np.ndarray, List[float]],
    uncertainties: Union[np.ndarray, List[float]]
) -> np.ndarray:
    """
    Calculate combined weights using both best-metric quality and individual uncertainties.
    
    This implements the statistically correct approach for weighted averaging when
    both quality indicators (best metric) and individual uncertainties are available.
    
    Parameters
    ----------
    rlap_ccc_values : array-like
        Best metric quality scores (prefer RLAP-CCC; fallback to RLAP)
    uncertainties : array-like
        Individual uncertainty estimates for each template (e.g., redshift errors)
        
    Returns
    -------
    np.ndarray
        Combined weights = (metric)² / σ²
        
    Notes
    -----
    Statistical Formulation:
    - Quality weight: q_i = (metric_i)²
    - Precision weight: p_i = 1/σ²_i
    - Combined weight: w_i = q_i × p_i = (metric_i)² / σ²_i
    
    This gives high-quality templates with low uncertainty the highest influence,
    which is statistically optimal for uncertainty propagation.
    """
    rlap_ccc_values = np.asarray(rlap_ccc_values, dtype=float)
    uncertainties = np.asarray(uncertainties, dtype=float)
    
    # Validate inputs
    if len(rlap_ccc_values) != len(uncertainties):
        raise ValueError("Metric values and uncertainties must have same length")
    
    if len(rlap_ccc_values) == 0:
        return np.array([])
    
    # Handle zero uncertainties (perfect measurements) by using a small floor value
    # This prevents infinite weights while preserving the relative ordering
    min_uncertainty = np.min(uncertainties[uncertainties > 0]) if np.any(uncertainties > 0) else 1e-6
    uncertainty_floor = min_uncertainty * 0.1
    safe_uncertainties = np.maximum(uncertainties, uncertainty_floor)
    
    # Calculate combined weights using squared best-metric values (RLAP-CCC preferred)
    quality_weights = rlap_ccc_values ** 2
    precision_weights = 1.0 / (safe_uncertainties ** 2)  # Inverse variance weighting
    combined_weights = quality_weights * precision_weights
    
    logger.debug(f"Combined weighting: Best-metric [{rlap_ccc_values.min():.2f}, {rlap_ccc_values.max():.2f}], "
                f"uncertainties [{uncertainties.min():.4f}, {uncertainties.max():.4f}], "
                f"weights [{combined_weights.min():.2e}, {combined_weights.max():.2e}]")
    
    return combined_weights


def apply_exponential_weighting(rlap_ccc_values: Union[np.ndarray, List[float]]) -> np.ndarray:
    """
    Apply squared-metric weighting to RLAP-CCC/RLAP values for template prioritization.
    
    This helper now implements w = (metric)² to match the main pipeline's
    weighting policy when per-template σ is unavailable (quality-only case).
    
    Parameters
    ----------
    rlap_ccc_values : array-like
        Raw best-metric values from template matching
        
    Returns
    -------
    np.ndarray
        Squared metric weights
        
    Notes
    -----
    Transformation: w = (metric)²
    """
    rlap_ccc_values = np.asarray(rlap_ccc_values, dtype=float)
    
    # Handle empty input
    if len(rlap_ccc_values) == 0:
        return np.array([])
    
    # Apply squared weighting: w = x^2
    exponential_weights = rlap_ccc_values ** 2
    
    # Log the transformation for debugging
    if len(rlap_ccc_values) > 0:
        logger.debug(f"Squared weighting: Best-metric range [{rlap_ccc_values.min():.2f}, {rlap_ccc_values.max():.2f}] "
                    f"→ weight range [{exponential_weights.min():.2e}, {exponential_weights.max():.2e}]")
    
    return exponential_weights


def calculate_weighted_redshift_balanced(
    redshifts: Union[np.ndarray, List[float]], 
    redshift_errors: Union[np.ndarray, List[float]],
    rlap_ccc_values: Union[np.ndarray, List[float]]
) -> Tuple[float, float]:
    """
    Calculate weighted redshift estimate with balanced uncertainty propagation.
    
    This function implements a statistically sound approach that balances:
    1. Template quality weighting ((RLAP-CCC)²)
    2. Precision weighting (inverse variance) 
    3. Proper uncertainty propagation
    
    Parameters
    ----------
    redshifts : array-like
        Redshift values from templates
    redshift_errors : array-like
        Individual redshift uncertainties for each template
    rlap_ccc_values : array-like
        Best metric quality scores (prefer RLAP-CCC; fallback to RLAP)
        
    Returns
    -------
    Tuple[float, float]
        (weighted_redshift, final_uncertainty)
        
    Notes
    -----
    Statistical Method:
    - Combined weights: w_i = (metric_i)² / σ²_i
    - Weighted mean: z = Σ(w_i * z_i) / Σ(w_i)  
    - Final uncertainty: σ_final = √(Σ(w_i * σ_i²)) / Σ(w_i)
    
    This gives high-quality templates with low uncertainty the highest influence
    while properly propagating uncertainties using weighted RMS.
    """
    redshifts = np.asarray(redshifts, dtype=float)
    redshift_errors = np.asarray(redshift_errors, dtype=float)
    rlap_ccc_values = np.asarray(rlap_ccc_values, dtype=float)
    
    # Validate inputs
    if len(redshifts) == 0:
        return np.nan, np.nan
        
    if not (len(redshifts) == len(redshift_errors) == len(rlap_ccc_values)):
        logger.error("Mismatched input lengths for balanced redshift estimation")
        return np.nan, np.nan
    
    # Remove invalid data points
    valid_mask = (np.isfinite(redshifts) & np.isfinite(redshift_errors) & 
                  np.isfinite(rlap_ccc_values) & (redshift_errors > 0))
    
    if not np.any(valid_mask):
        logger.warning("No valid (redshift, error, metric) triplets found")
        return np.nan, np.nan
        
    valid_z = redshifts[valid_mask]
    valid_sigma = redshift_errors[valid_mask]
    valid_rlap = rlap_ccc_values[valid_mask]
    N = len(valid_z)
    
    if N == 1:
        return float(valid_z[0]), float(valid_sigma[0])
    
    # Calculate combined weights (quality × precision)
    combined_weights = calculate_combined_weights(valid_rlap, valid_sigma)

    # Weighted mean
    sum_w = np.sum(combined_weights)
    z_weighted = np.sum(combined_weights * valid_z) / sum_w

    # Correct standard error of a weighted mean with arbitrary weights:
    # σ_final = sqrt( Σ w_i^2 σ_i^2 ) / Σ w_i
    sigma_final = float(
        np.sqrt(np.sum((combined_weights ** 2) * (valid_sigma ** 2))) / sum_w
    )
    
    logger.info(f"Balanced redshift (RMS): {z_weighted:.6f}±{sigma_final:.6f}, N={N}")
    
    return float(z_weighted), float(sigma_final)


def calculate_weighted_age_estimate(
    ages: Union[np.ndarray, List[float]],
    rlap_ccc_values: Union[np.ndarray, List[float]]
) -> float:
    """
    Calculate weighted age estimate using squared RLAP-CCC/RLAP weighting.
    
    Ages typically don't have well-defined individual uncertainties, so this
    function uses simple squared quality weighting without uncertainty propagation.
    
    Parameters
    ----------
    ages : array-like
        Age values from templates (in days)
    rlap_ccc_values : array-like
        Best metric quality scores (prefer RLAP-CCC; fallback to RLAP)
        
    Returns
    -------
    float
        Weighted age estimate
        
    Notes
    -----
    Statistical Method:
    - Weights: w_i = (metric_i)²
    - Weighted mean: age = Σ(w_i * age_i) / Σ(w_i)
    
    No uncertainty is computed since individual age uncertainties are 
    typically not available or well-defined in template libraries.
    """
    ages = np.asarray(ages, dtype=float)
    rlap_ccc_values = np.asarray(rlap_ccc_values, dtype=float)
    
    # Validate inputs
    if len(ages) == 0:
        return np.nan
        
    if len(ages) != len(rlap_ccc_values):
        logger.error("Mismatched input lengths for age estimation")
        return np.nan
    
    # Remove invalid data points
    # Note: Ages can be negative (before peak), so no age > 0 filter
    valid_mask = (np.isfinite(ages) & np.isfinite(rlap_ccc_values))
    
    if not np.any(valid_mask):
        logger.warning("No valid (age, metric) pairs found")
        return np.nan
        
    valid_ages = ages[valid_mask]
    valid_rlap = rlap_ccc_values[valid_mask]
    N = len(valid_ages)
    
    if N == 1:
        return float(valid_ages[0])
    
    # Calculate squared-quality weights
    weights = apply_exponential_weighting(valid_rlap)
    
    # Weighted mean
    sum_w = np.sum(weights)
    age_weighted = np.sum(weights * valid_ages) / sum_w
    
    logger.info(f"Weighted age: {age_weighted:.1f} days, N={N}")
    
    return float(age_weighted)




def calculate_joint_weighted_estimates(
    redshifts: Union[np.ndarray, List[float]], 
    ages: Union[np.ndarray, List[float]],
    weights: Union[np.ndarray, List[float]]
) -> Tuple[float, float, float, float, float]:
    """
    Calculate joint weighted estimates for redshift and age with full covariance.
    
    This implements a statistically robust joint estimation approach that:
    1. Uses squared RLAP-CCC/RLAP values as quality-based weights
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
        Quality weights for each template (should be exponentially transformed)
        
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
    
    Weight Transformation:
    - For optimal results, quality-only weights should be transformed as w = (metric)²
    - Use apply_exponential_weighting() (now squared) before calling this function
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
        Quality weights for each template (should be exponentially transformed)
        
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
        Quality weights for each template (should be exponentially transformed)
        
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
    'calculate_combined_weights',
    'apply_exponential_weighting',
    'compute_cluster_weights',
    'estimate_weighted_redshift',
    'estimate_weighted_epoch',
    'weighted_redshift_sd',
    'weighted_epoch_sd',
    'calculate_weighted_redshift_balanced', 
    'calculate_weighted_age_estimate',      
    'calculate_joint_weighted_estimates',
    'calculate_weighted_redshift', 
    'calculate_weighted_age',
    'calculate_weighted_median',
    'validate_joint_result',
    'validate_weighted_calculation'
]