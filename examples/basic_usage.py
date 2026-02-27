"""
examples/basic_usage.py
========================
Basic usage examples for the square_points module.

Run from the project root:
    python examples/basic_usage.py
"""

import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

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
from utils.helpers import is_on_perimeter, euclidean, side_of
from models.shapes import Square


# ── Example 1: Generate a single pair of points ───────────────────────────────

def example_single_pair():
    print("=" * 50)
    print("Example 1: Single pair of points")
    print("=" * 50)

    L = 10.0
    p1, p2 = sample_parametric(L)

    print(f"Square side: L = {L}")
    print(f"Point 1: ({p1[0]:.4f}, {p1[1]:.4f})  side: {side_of(p1, L)}")
    print(f"Point 2: ({p2[0]:.4f}, {p2[1]:.4f})  side: {side_of(p2, L)}")
    print(f"Distance: {euclidean(p1, p2):.4f}  (> L: {euclidean(p1, p2) > L})")
    print(f"Both on perimeter: {is_on_perimeter(p1, L) and is_on_perimeter(p2, L)}")
    print(f"Distinct: {_is_distinct(p1, p2)}")


# ── Example 2: Compare all 9 methods ─────────────────────────────────────────

def example_compare_methods():
    print("\n" + "=" * 50)
    print("Example 2: One sample from each method")
    print("=" * 50)

    L = 10.0
    methods = [
        ("sample_parametric         ", sample_parametric),
        ("sample_by_side            ", sample_by_side),
        ("sample_by_edge_label      ", sample_by_edge_label),
        ("sample_polar_ray          ", sample_polar_ray),
        ("sample_side_pos           ", sample_side_pos),
        ("sample_parametric_modular ", sample_parametric_modular),
        ("sample_cartesian          ", sample_cartesian),
        ("sample_polar_angle        ", sample_polar_angle),
        ("sample_interior_projection", sample_interior_projection),
    ]

    print(f"{'Method':<30} {'P1':^22} {'P2':^22} {'Dist':>7}")
    print("-" * 85)
    for name, fn in methods:
        p1, p2 = fn(L)
        d = euclidean(p1, p2)
        print(f"{name}  ({p1[0]:6.3f},{p1[1]:6.3f})  ({p2[0]:6.3f},{p2[1]:6.3f})  {d:7.3f}")


# ── Example 3: Monte Carlo estimate of P(d > L) ───────────────────────────────

def example_monte_carlo(n: int = 50_000):
    print("\n" + "=" * 50)
    print(f"Example 3: Monte Carlo P(d > L)  [n={n:,}]")
    print("=" * 50)

    L = 10.0
    methods = [
        ("sample_parametric         ", sample_parametric),
        ("sample_polar_ray          ", sample_polar_ray),
        ("sample_interior_projection", sample_interior_projection),
    ]

    theoretical = 0.3573
    print(f"Theoretical value (uniform): {theoretical:.4f}\n")

    for name, fn in methods:
        hits = sum(1 for _ in range(n) if euclidean(*fn(L)) > L)
        pct = hits / n * 100
        print(f"  {name}  {pct:.2f}%")


# ── Example 4: Using the Square model class ───────────────────────────────────

def example_square_model():
    print("\n" + "=" * 50)
    print("Example 4: Square model class")
    print("=" * 50)

    sq = Square(L=10.0)
    print(f"Square:    {sq}")
    print(f"Perimeter: {sq.perimeter}")
    print(f"Area:      {sq.area}")
    print(f"Diagonal:  {sq.diagonal:.4f}  (= √2 · L)")
    print(f"Center:    {sq.center}")

    p1, p2 = sample_parametric(sq.L)
    print(f"\nSampled pair:")
    print(f"  P1 = {p1}  on_perimeter={sq.on_perimeter(p1)}")
    print(f"  P2 = {p2}  on_perimeter={sq.on_perimeter(p2)}")
    print(f"  distance = {sq.distance(p1, p2):.4f}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    example_single_pair()
    example_compare_methods()
    example_monte_carlo()
    example_square_model()
