"""
utils/helpers.py
================
General utility functions shared across the project.
"""

import math
from typing import Tuple

Point = Tuple[float, float]


def is_on_perimeter(point: Point, L: float, tol: float = 1e-9) -> bool:
    """Return True if the point lies on the perimeter of [0, L] × [0, L]."""
    x, y = point
    on_bottom = abs(y) < tol       and 0 <= x <= L
    on_top    = abs(y - L) < tol   and 0 <= x <= L
    on_left   = abs(x) < tol       and 0 <= y <= L
    on_right  = abs(x - L) < tol   and 0 <= y <= L
    return on_bottom or on_top or on_left or on_right


def side_of(point: Point, L: float, tol: float = 1e-9) -> str:
    """Return the side label of a perimeter point.

    Returns one of: 'bottom', 'top', 'left', 'right', 'corner', 'off'.
    Corner points (vertices) that lie on two sides are labelled 'corner'.
    """
    x, y = point
    sides = []
    if abs(y) < tol:     sides.append("bottom")
    if abs(y - L) < tol: sides.append("top")
    if abs(x) < tol:     sides.append("left")
    if abs(x - L) < tol: sides.append("right")
    if len(sides) > 1:   return "corner"
    return sides[0] if sides else "off"


def euclidean(p1: Point, p2: Point) -> float:
    """Euclidean distance between two 2-D points."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def are_distinct(p1: Point, p2: Point, tol: float = 1e-12) -> bool:
    """Return True if the two points are geometrically distinct."""
    return abs(p1[0] - p2[0]) > tol or abs(p1[1] - p2[1]) > tol


def clamp(value: float, lo: float, hi: float) -> float:
    """Clamp a value to the range [lo, hi]."""
    return max(lo, min(hi, value))
