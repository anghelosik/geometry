"""
models/shapes.py
================
Geometric models used throughout the project.
"""

import math
from typing import Tuple

Point = Tuple[float, float]


class Square:
    """Axis-aligned square [0, L] × [0, L].

    Attributes:
        L: side length (must be positive)
    """

    def __init__(self, L: float) -> None:
        if L <= 0:
            raise ValueError(f"Side length must be positive, got {L}")
        self.L = L

    # ── Geometry ──────────────────────────────────────────────────────────────

    @property
    def perimeter(self) -> float:
        """Total perimeter length."""
        return 4 * self.L

    @property
    def area(self) -> float:
        """Area of the square."""
        return self.L ** 2

    @property
    def diagonal(self) -> float:
        """Length of the diagonal (= maximum possible distance between two perimeter points)."""
        return self.L * math.sqrt(2)

    @property
    def center(self) -> Point:
        """Center point of the square."""
        return (self.L / 2, self.L / 2)

    # ── Predicates ────────────────────────────────────────────────────────────

    def contains(self, point: Point, tol: float = 1e-9) -> bool:
        """Return True if the point is inside or on the boundary of the square."""
        x, y = point
        return -tol <= x <= self.L + tol and -tol <= y <= self.L + tol

    def on_perimeter(self, point: Point, tol: float = 1e-9) -> bool:
        """Return True if the point lies on the perimeter of the square."""
        x, y = point
        on_bottom = abs(y) < tol       and 0 <= x <= self.L
        on_top    = abs(y - self.L) < tol and 0 <= x <= self.L
        on_left   = abs(x) < tol       and 0 <= y <= self.L
        on_right  = abs(x - self.L) < tol and 0 <= y <= self.L
        return on_bottom or on_top or on_left or on_right

    # ── Distance ──────────────────────────────────────────────────────────────

    @staticmethod
    def distance(p1: Point, p2: Point) -> float:
        """Euclidean distance between two points."""
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    # ── Dunder ────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"Square(L={self.L})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Square):
            return NotImplemented
        return math.isclose(self.L, other.L)
