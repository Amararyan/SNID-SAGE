"""
Mathematical utility functions for SNID SAGE.

This module provides statistically rigorous weighted calculations for
redshift and age estimation using template quality metrics.
"""

from .weighted_statistics import (
    calculate_combined_weights,
    apply_exponential_weighting,
    compute_cluster_weights,
    estimate_weighted_redshift,
    estimate_weighted_epoch,
    weighted_redshift_sd,
    weighted_epoch_sd,
    calculate_weighted_median,
    validate_joint_result,
    validate_weighted_calculation
)

from .similarity_metrics import (
    concordance_correlation_coefficient,
    compute_rlap_ccc_metric,
    compute_locality_metric,
    compute_chi_square_metric,
    get_best_metric_value,
    get_best_metric_name,
    get_metric_name_for_match,
    get_metric_display_values
)

__all__ = [
    # Weighted statistics
    'calculate_combined_weights',
    'apply_exponential_weighting',
    'compute_cluster_weights',
    'estimate_weighted_redshift',
    'estimate_weighted_epoch',
    'weighted_redshift_sd',
    'weighted_epoch_sd',
    'calculate_weighted_median',
    'validate_joint_result',
    'validate_weighted_calculation',
    # Similarity metrics
    'concordance_correlation_coefficient',
    'compute_rlap_ccc_metric',
    'compute_locality_metric',
    'compute_chi_square_metric',
    'get_best_metric_value',
    'get_best_metric_name',
    'get_metric_name_for_match',
    'get_metric_display_values'
]