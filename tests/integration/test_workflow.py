"""
tests/integration/test_workflow.py
====================================
End-to-end integration tests that exercise the full analysis workflow:
sampling → distance computation → statistical summary.
"""

import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from square_points import (
    sample_parametric,
    sample_by_side,
    sample_by_edge_label,
    sample_polar_ray,
    sample_side_pos,
    sample_parametric_modular,
    sample_cartesian,
    sample_polar_angle,
    sample_interior_projection,
)
from utils.helpers import is_on_perimeter, euclidean, are_distinct

ALL_METHODS = [
    sample_parametric,
    sample_by_side,
    sample_by_edge_label,
    sample_polar_ray,
    sample_side_pos,
    sample_parametric_modular,
    sample_cartesian,
    sample_polar_angle,
    sample_interior_projection,
]

UNIFORM_METHODS = [
    sample_parametric,
    sample_by_side,
    sample_by_edge_label,
    sample_side_pos,
    sample_parametric_modular,
    sample_cartesian,
]

THEORETICAL_P = 0.3573   # P(d > L) for uniform distribution on the perimeter


class TestFullWorkflow:
    """Test the complete sample → measure pipeline."""

    @pytest.mark.parametrize("method", ALL_METHODS, ids=lambda m: m.__name__)
    def test_sample_to_distance_pipeline(self, method):
        """Each method must produce valid points and a positive distance."""
        L = 10.0
        for _ in range(100):
            p1, p2 = method(L)
            assert is_on_perimeter(p1, L), f"{method.__name__}: p1 not on perimeter"
            assert is_on_perimeter(p2, L), f"{method.__name__}: p2 not on perimeter"
            assert are_distinct(p1, p2),   f"{method.__name__}: points are identical"
            d = euclidean(p1, p2)
            assert d > 0,                  f"{method.__name__}: zero distance"
            assert d <= math.sqrt(2) * L + 1e-9, f"{method.__name__}: distance exceeds diagonal"


class TestUniformMethodsConvergence:
    """Verify that the 6 uniform methods converge to the theoretical P(d > L)."""

    @pytest.mark.parametrize("method", UNIFORM_METHODS, ids=lambda m: m.__name__)
    def test_probability_within_tolerance(self, method):
        """P(d > L) should be within ±2 percentage points of 0.3573 for n=10 000."""
        L = 10.0
        n = 10_000
        hits = sum(1 for _ in range(n) if euclidean(*method(L)) > L)
        p_hat = hits / n
        assert abs(p_hat - THEORETICAL_P) < 0.02, (
            f"{method.__name__}: P(d>L) = {p_hat:.4f}, "
            f"expected {THEORETICAL_P} ± 0.02"
        )


class TestNonUniformMethodsBias:
    """Verify that the non-uniform methods produce a meaningfully lower P(d > L)."""

    @pytest.mark.parametrize("method,upper_bound", [
        (sample_polar_ray,           0.350),
        (sample_polar_angle,         0.350),
        (sample_interior_projection, 0.320),
    ], ids=lambda x: x.__name__ if callable(x) else str(x))
    def test_probability_below_uniform(self, method, upper_bound):
        """Non-uniform methods must produce P(d > L) strictly below the uniform value."""
        L = 10.0
        n = 10_000
        hits = sum(1 for _ in range(n) if euclidean(*method(L)) > L)
        p_hat = hits / n
        assert p_hat < upper_bound, (
            f"{method.__name__}: P(d>L) = {p_hat:.4f} is not below {upper_bound}"
        )


class TestConsistencyAcrossSideLengths:
    """P(d > L) / L should be scale-invariant (depends only on shape, not size)."""

    @pytest.mark.parametrize("L", [1.0, 10.0, 100.0])
    def test_scale_invariance(self, L):
        """The ratio P(d > L) should be the same regardless of L."""
        n = 5_000
        hits = sum(1 for _ in range(n) if euclidean(*sample_parametric(L)) > L)
        p_hat = hits / n
        assert abs(p_hat - THEORETICAL_P) < 0.03, (
            f"L={L}: P(d>L) = {p_hat:.4f}, expected ≈ {THEORETICAL_P}"
        )
