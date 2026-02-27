"""
test_dist_1000.py
=================
Quick sanity check: run 1000 iterations per method and print the
edge-distribution percentages. Useful for a fast visual check from the
command line before running the full pytest suite.

Run from the project root:
    python test_dist_1000.py
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

L = 10
ITERATIONS = 1000


def check_distribution(method, method_name: str):
    """Run the method and print the edge distribution."""
    edge_count = {"bottom": 0, "top": 0, "left": 0, "right": 0}

    for _ in range(ITERATIONS):
        try:
            p1, p2 = method(L)
            for p in [p1, p2]:
                x, y = p
                if abs(y) < 1e-9:
                    edge_count["bottom"] += 1
                elif abs(y - L) < 1e-9:
                    edge_count["top"] += 1
                elif abs(x) < 1e-9:
                    edge_count["left"] += 1
                elif abs(x - L) < 1e-9:
                    edge_count["right"] += 1
        except Exception as e:
            print(f"  ERROR: {e}")

    total = sum(edge_count.values())
    print(f"{method_name}:")
    for edge, count in edge_count.items():
        pct = count / total * 100 if total else 0
        bar = "#" * int(pct / 2)
        print(f"  {edge:>6}: {pct:5.1f}%  {bar}")


if __name__ == "__main__":
    print(f"Edge distribution check — {ITERATIONS} iterations, L={L}\n")
    print(f"Expected: ~25% per side for uniform methods\n")

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
        check_distribution(method, name)
        print()
