"""
debug_methods.py
================
Debug script that shows detailed edge-distribution statistics for each
sampling method. Useful for spotting bias or off-perimeter points.

Run from the project root:
    python debug_methods.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

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
from utils.helpers import is_on_perimeter, side_of


def debug_method(method, method_name: str, L: float = 10, iterations: int = 100):
    """Run one method and print detailed edge-distribution statistics."""
    print(f"\n{'='*70}")
    print(f"Debugging: {method_name}")
    print(f"{'='*70}")

    edge_counts = {"bottom": 0, "top": 0, "left": 0, "right": 0,
                   "corner": 0, "off": 0}
    points_list = []

    for i in range(iterations):
        try:
            p1, p2 = method(L)
            points_list.extend([(p1, "p1"), (p2, "p2")])
            for p in [p1, p2]:
                label = side_of(p, L)
                if label in edge_counts:
                    edge_counts[label] += 1
                else:
                    edge_counts["off"] += 1
        except Exception as e:
            print(f"  ERROR in iteration {i}: {e}")
            edge_counts["off"] += 2

    total = iterations * 2
    print(f"\nDistribution of {total} points ({iterations} iterations):")
    for edge, count in edge_counts.items():
        if count > 0:
            pct = count / total * 100
            bar = "#" * int(pct / 2)
            print(f"  {edge:>8}: {count:4d}  ({pct:5.1f}%)  {bar}")

    # Show first 10 points
    print(f"\nFirst 10 points:")
    for p, label in points_list[:10]:
        edge = side_of(p, L)
        on = is_on_perimeter(p, L)
        print(f"  {label}: ({p[0]:7.4f}, {p[1]:7.4f})  side={edge:<8}  on_perimeter={on}")

    # Warn about off-perimeter points
    off = [(p, lab) for p, lab in points_list if not is_on_perimeter(p, L)]
    if off:
        print(f"\n  WARNING: {len(off)} points are OFF PERIMETER!")
        for p, lab in off[:5]:
            print(f"    {lab}: {p}")


def main():
    L = 10
    iterations = 200

    print("=" * 70)
    print("METHOD DEBUG ANALYSIS")
    print("=" * 70)

    methods = [
        (sample_parametric,          "1. Parametric"),
        (sample_by_side,             "2. Side Selection"),
        (sample_by_edge_label,       "3. Edge Label"),
        (sample_polar_ray,           "4. Polar Ray"),
        (sample_side_pos,            "5. Side + Position"),
        (sample_parametric_modular,  "6. Parametric (Modular)"),
        (sample_cartesian,           "7. Cartesian"),
        (sample_polar_angle,         "8. Polar Angle"),
        (sample_interior_projection, "9. Interior Projection"),
    ]

    for method, name in methods:
        debug_method(method, name, L, iterations)


if __name__ == "__main__":
    main()
