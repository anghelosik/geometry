"""
tests/unit/test_shapes.py
==========================
Unit tests for models/shapes.py and utils/helpers.py.
"""

import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from models.shapes import Square
from utils.helpers import is_on_perimeter, side_of, euclidean, are_distinct, clamp


# ── Square model ──────────────────────────────────────────────────────────────

class TestSquareInit:

    def test_valid_side(self):
        sq = Square(10.0)
        assert sq.L == 10.0

    def test_zero_side_raises(self):
        with pytest.raises(ValueError):
            Square(0)

    def test_negative_side_raises(self):
        with pytest.raises(ValueError):
            Square(-5)


class TestSquareProperties:

    def test_perimeter(self):
        assert Square(10).perimeter == 40.0

    def test_area(self):
        assert Square(5).area == 25.0

    def test_diagonal(self):
        sq = Square(10)
        assert math.isclose(sq.diagonal, 10 * math.sqrt(2))

    def test_center(self):
        assert Square(10).center == (5.0, 5.0)

    def test_equality(self):
        assert Square(10) == Square(10)
        assert Square(10) != Square(5)


class TestSquareOnPerimeter:

    def test_corners_on_perimeter(self):
        sq = Square(10)
        assert sq.on_perimeter((0, 0))
        assert sq.on_perimeter((10, 0))
        assert sq.on_perimeter((10, 10))
        assert sq.on_perimeter((0, 10))

    def test_midpoints_on_perimeter(self):
        sq = Square(10)
        assert sq.on_perimeter((5, 0))    # bottom midpoint
        assert sq.on_perimeter((10, 5))   # right midpoint
        assert sq.on_perimeter((5, 10))   # top midpoint
        assert sq.on_perimeter((0, 5))    # left midpoint

    def test_interior_not_on_perimeter(self):
        sq = Square(10)
        assert not sq.on_perimeter((5, 5))
        assert not sq.on_perimeter((3, 4))

    def test_outside_not_on_perimeter(self):
        sq = Square(10)
        assert not sq.on_perimeter((11, 5))
        assert not sq.on_perimeter((5, -1))


class TestSquareContains:

    def test_interior_contained(self):
        sq = Square(10)
        assert sq.contains((5, 5))

    def test_boundary_contained(self):
        sq = Square(10)
        assert sq.contains((0, 0))
        assert sq.contains((10, 10))

    def test_outside_not_contained(self):
        sq = Square(10)
        assert not sq.contains((11, 5))
        assert not sq.contains((-1, 5))


class TestSquareDistance:

    def test_origin_to_corner(self):
        assert math.isclose(Square.distance((0, 0), (10, 10)), 10 * math.sqrt(2))

    def test_same_point(self):
        assert Square.distance((3, 4), (3, 4)) == 0.0

    def test_horizontal(self):
        assert math.isclose(Square.distance((0, 5), (10, 5)), 10.0)


# ── Helper functions ──────────────────────────────────────────────────────────

class TestIsOnPerimeter:

    def test_bottom_side(self):
        assert is_on_perimeter((5, 0), 10)

    def test_top_side(self):
        assert is_on_perimeter((5, 10), 10)

    def test_left_side(self):
        assert is_on_perimeter((0, 5), 10)

    def test_right_side(self):
        assert is_on_perimeter((10, 5), 10)

    def test_interior(self):
        assert not is_on_perimeter((5, 5), 10)

    def test_outside(self):
        assert not is_on_perimeter((12, 5), 10)


class TestSideOf:

    def test_bottom(self):
        assert side_of((5, 0), 10) == "bottom"

    def test_top(self):
        assert side_of((5, 10), 10) == "top"

    def test_left(self):
        assert side_of((0, 5), 10) == "left"

    def test_right(self):
        assert side_of((10, 5), 10) == "right"

    def test_corner(self):
        assert side_of((0, 0), 10) == "corner"
        assert side_of((10, 10), 10) == "corner"

    def test_off(self):
        assert side_of((5, 5), 10) == "off"


class TestEuclidean:

    def test_pythagorean(self):
        assert math.isclose(euclidean((0, 0), (3, 4)), 5.0)

    def test_zero(self):
        assert euclidean((2, 3), (2, 3)) == 0.0


class TestAreDistinct:

    def test_distinct(self):
        assert are_distinct((0, 0), (1, 0))

    def test_identical(self):
        assert not are_distinct((5, 5), (5, 5))

    def test_within_tolerance(self):
        assert not are_distinct((0, 0), (1e-13, 0))


class TestClamp:

    def test_within_range(self):
        assert clamp(5, 0, 10) == 5

    def test_below_range(self):
        assert clamp(-1, 0, 10) == 0

    def test_above_range(self):
        assert clamp(15, 0, 10) == 10
