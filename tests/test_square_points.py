"""
tests/test_square_points.py
============================
Test suite for square_points.py.

Changes compared to the original version
-----------------------------------------
- Added `test_same_side_allowed` which verifies that sample_by_side (and other
  methods with a uniform distribution) can return points on the same side —
  this test would have caught the original bug.
- Added `test_side_distribution_is_balanced` which checks the statistical
  distribution of sample_by_side.
- Uses `_is_distinct` from the library instead of duplicating the logic.
- Improved edge-case coverage for very small and very large values of L.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import math
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
    _is_distinct,
)

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


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def is_on_perimeter(point: tuple, L: float, tol: float = 1e-9) -> bool:
    """Return True if the point lies on the perimeter of the square [0,L]×[0,L]."""
    x, y = point
    on_bottom = abs(y) < tol and 0 <= x <= L
    on_top    = abs(y - L) < tol and 0 <= x <= L
    on_left   = abs(x) < tol and 0 <= y <= L
    on_right  = abs(x - L) < tol and 0 <= y <= L
    return on_bottom or on_top or on_left or on_right


def side_of(point: tuple, L: float, tol: float = 1e-9) -> str:
    """Return the side the point lies on ('bottom', 'top', 'left', 'right',
    or 'corner' for vertices)."""
    x, y = point
    sides = []
    if abs(y) < tol:       sides.append("bottom")
    if abs(y - L) < tol:   sides.append("top")
    if abs(x) < tol:       sides.append("left")
    if abs(x - L) < tol:   sides.append("right")
    if len(sides) > 1:     return "corner"
    return sides[0] if sides else "off"


# ─────────────────────────────────────────────────────────────────────────────
# PARAMETRIC TESTS — run on all methods
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("method", ALL_METHODS, ids=lambda m: m.__name__)
class TestAllMethods:

    def test_returns_two_tuples(self, method):
        p1, p2 = method(10)
        assert isinstance(p1, tuple) and len(p1) == 2
        assert isinstance(p2, tuple) and len(p2) == 2

    def test_points_on_perimeter(self, method):
        L = 10
        p1, p2 = method(L)
        assert is_on_perimeter(p1, L), f"P1={p1} is not on the perimeter"
        assert is_on_perimeter(p2, L), f"P2={p2} is not on the perimeter"

    def test_points_are_distinct(self, method):
        for _ in range(20):   # 20 calls to reduce false negatives
            p1, p2 = method(10)
            assert _is_distinct(p1, p2), f"Identical points: {p1}"

    @pytest.mark.parametrize("L", [0.1, 1.0, 5.0, 10.0, 100.0, 1000.0])
    def test_works_for_various_L(self, method, L):
        p1, p2 = method(L)
        assert is_on_perimeter(p1, L, tol=1e-7)
        assert is_on_perimeter(p2, L, tol=1e-7)
        assert _is_distinct(p1, p2)

    def test_coordinates_within_bounds(self, method):
        L = 10
        p1, p2 = method(L)
        for p in (p1, p2):
            assert 0 <= p[0] <= L, f"x={p[0]} out of [0,{L}]"
            assert 0 <= p[1] <= L, f"y={p[1]} out of [0,{L}]"


# ─────────────────────────────────────────────────────────────────────────────
# METHOD-SPECIFIC TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestSampleBySideFix:
    """
    Verify that sample_by_side does NOT force the two points onto different sides.

    This test would have caught the original bug:
        while side1 == side2: ...
    """

    def test_same_side_allowed(self):
        """In N samples, at least one pair must land on the same side."""
        L = 10
        N = 2000   # Probability of 0 successes in 2000 tries ≈ (3/4)^2000 ≈ 0
        found_same_side = False

        for _ in range(N):
            p1, p2 = sample_by_side(L)
            s1 = side_of(p1, L)
            s2 = side_of(p2, L)
            # Two points at a corner have side="corner" — skip them
            if s1 not in ("corner", "off") and s2 not in ("corner", "off"):
                if s1 == s2:
                    found_same_side = True
                    break

        assert found_same_side, (
            f"sample_by_side never returned two points on the same side "
            f"in {N} attempts. Possible bug: `while side1 == side2` "
            "forcing different sides."
        )

    def test_side_distribution_is_balanced(self):
        """The distribution across the 4 sides should be approximately uniform (25% each)."""
        L = 10
        N = 4000
        counts = {"bottom": 0, "top": 0, "left": 0, "right": 0}

        for _ in range(N):
            p1, p2 = sample_by_side(L)
            for p in (p1, p2):
                s = side_of(p, L)
                if s in counts:
                    counts[s] += 1

        total = sum(counts.values())
        for side, count in counts.items():
            pct = count / total
            assert 0.18 < pct < 0.32, (
                f"Side '{side}': {pct*100:.1f}% (expected ~25%). "
                "Distribution is too unbalanced."
            )


class TestSamplePolarRay:
    """Additional tests for the polar ray method."""

    def test_point_reachable_from_center(self):
        """Points must be at a positive distance from the center."""
        L = 10
        cx, cy = L / 2, L / 2
        p1, p2 = sample_polar_ray(L)
        for p in (p1, p2):
            dist = math.hypot(p[0] - cx, p[1] - cy)
            assert dist > 0, "Point coincides with the center"


class TestSampleInteriorProjection:
    """Additional tests for the interior projection method."""

    def test_runs_without_errors(self):
        """Verify the function runs correctly for many iterations without exceptions."""
        L = 10
        for _ in range(500):
            p1, p2 = sample_interior_projection(L)
            assert is_on_perimeter(p1, L)
            assert is_on_perimeter(p2, L)


class TestHelperPerimeterToXY:
    """Tests for the _perimeter_to_xy helper function."""

    def test_corners(self):
        from square_points import _perimeter_to_xy
        L = 10
        assert _perimeter_to_xy(0, L)      == (0.0, 0.0)   # bottom-left corner
        assert _perimeter_to_xy(L, L)      == (L, 0.0)     # bottom-right corner
        assert _perimeter_to_xy(2 * L, L)  == (L, L)       # top-right corner
        assert _perimeter_to_xy(3 * L, L)  == (0.0, L)     # top-left corner

    def test_midpoints(self):
        from square_points import _perimeter_to_xy
        L = 10
        assert _perimeter_to_xy(L / 2, L)       == (L / 2, 0.0)   # midpoint bottom side
        assert _perimeter_to_xy(1.5 * L, L)     == (L, L / 2)     # midpoint right side
        assert _perimeter_to_xy(2.5 * L, L)     == (L / 2, L)     # midpoint top side
        assert _perimeter_to_xy(3.5 * L, L)     == (0.0, L / 2)   # midpoint left side

    def test_wrapping(self):
        from square_points import _perimeter_to_xy
        L = 10
        # t = 4L should equal t = 0 (modulo)
        assert _perimeter_to_xy(4 * L, L) == _perimeter_to_xy(0, L)
        assert _perimeter_to_xy(5 * L, L) == _perimeter_to_xy(L, L)


# ─────────────────────────────────────────────────────────────────────────────
# COMPARATIVE STRESS TEST
# ─────────────────────────────────────────────────────────────────────────────

class TestComparative:

    def test_all_methods_valid_1000_iterations(self):
        """All methods must complete 1000 iterations without errors."""
        L = 10
        for method in ALL_METHODS:
            for _ in range(1000):
                p1, p2 = method(L)
                assert is_on_perimeter(p1, L), f"{method.__name__}: p1 off perimeter"
                assert is_on_perimeter(p2, L), f"{method.__name__}: p2 off perimeter"
                assert _is_distinct(p1, p2),   f"{method.__name__}: identical points"
