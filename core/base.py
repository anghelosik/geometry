"""
core/base.py
============
Abstract base classes for the geometry project.
"""

from abc import ABC, abstractmethod
from typing import Tuple

Point = Tuple[float, float]
PointPair = Tuple[Point, Point]


class PerimeterSampler(ABC):
    """Abstract base class for all square-perimeter sampling strategies.

    Subclasses must implement `sample`, which returns two distinct points
    on the perimeter of a square with side length L.
    """

    def __init__(self, L: float) -> None:
        if L <= 0:
            raise ValueError(f"Side length L must be positive, got {L}")
        self.L = L

    @abstractmethod
    def sample(self) -> PointPair:
        """Return two distinct points on the perimeter of [0, L] × [0, L]."""

    def __call__(self) -> PointPair:
        """Allow the sampler to be called like a function."""
        return self.sample()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(L={self.L})"
