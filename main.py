"""
main.py
=======
Main entry point for the geometry project.

Demonstrates the usage of the 9 sampling methods defined in square_points.py
by running each one for a configurable number of iterations and printing
per-method statistics and a comparative report.
"""

import sys
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


def print_points(p1, p2):
    """Pretty-print two perimeter points."""
    print(f"  Point 1: ({p1[0]:.4f}, {p1[1]:.4f})")
    print(f"  Point 2: ({p2[0]:.4f}, {p2[1]:.4f})")


def verify_on_perimeter(point, L, tolerance=1e-9):
    """Return True if the point lies on the perimeter of [0,L]×[0,L]."""
    x, y = point
    on_bottom = abs(y) < tolerance and 0 <= x <= L
    on_top    = abs(y - L) < tolerance and 0 <= x <= L
    on_left   = abs(x) < tolerance and 0 <= y <= L
    on_right  = abs(x - L) < tolerance and 0 <= y <= L
    return on_bottom or on_top or on_left or on_right


def test_method(method, method_name, L=10, iterations=5):
    """Run one method for `iterations` steps and print results and statistics."""
    print(f"\n{'='*60}")
    print(f"{method_name}")
    print(f"{'='*60}")

    all_points = []
    edge_count = {"bottom": 0, "top": 0, "left": 0, "right": 0}
    all_valid = True

    for i in range(iterations):
        try:
            p1, p2 = method(L)
            all_points.extend([p1, p2])

            valid_p1 = verify_on_perimeter(p1, L)
            valid_p2 = verify_on_perimeter(p2, L)
            distinct = abs(p1[0] - p2[0]) > 1e-9 or abs(p1[1] - p2[1]) > 1e-9

            # Categorise points by edge (horizontal edges take priority at corners)
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

            status = "[OK]" if (valid_p1 and valid_p2 and distinct) else "[!]"
            if i == 0:
                print(f"{status} Iteration {i+1}:")
                print_points(p1, p2)
            elif i == 1:
                print(f"... ({iterations - 2} more iterations)")

        except Exception as e:
            print(f"[!] Iteration {i+1}: ERROR - {e}")
            all_valid = False

    # Statistics
    print(f"\n--- Statistics ({iterations} iterations, {iterations*2} total points) ---")
    total_points = iterations * 2
    print("Edge distribution:")
    for edge, count in edge_count.items():
        pct = (count / total_points * 100) if total_points > 0 else 0
        bar = "#" * int(pct / 5)
        print(f"  {edge:>6}: {count:2d} points ({pct:5.1f}%) {bar}")

    if all_points:
        x_coords = [p[0] for p in all_points]
        y_coords = [p[1] for p in all_points]
        print("Coordinate ranges:")
        print(f"  X: [{min(x_coords):.4f}, {max(x_coords):.4f}]")
        print(f"  Y: [{min(y_coords):.4f}, {max(y_coords):.4f}]")

    return all_valid, edge_count, total_points


def print_comparative_report(results_data):
    """Print a comparative table and category analysis across all methods."""
    print("\n\n" + "="*80)
    print("COMPARATIVE ANALYSIS")
    print("="*80)

    print(f"\n{'Method':<45} | {'Bottom':<8} {'Top':<8} {'Left':<8} {'Right':<8}")
    print("-" * 80)

    for method_name, (_, edge_count, total_points) in results_data.items():
        bottom_pct = (edge_count["bottom"] / total_points * 100) if total_points > 0 else 0
        top_pct    = (edge_count["top"]    / total_points * 100) if total_points > 0 else 0
        left_pct   = (edge_count["left"]   / total_points * 100) if total_points > 0 else 0
        right_pct  = (edge_count["right"]  / total_points * 100) if total_points > 0 else 0
        print(f"{method_name:<45} | {bottom_pct:>6.1f}% {top_pct:>6.1f}% {left_pct:>6.1f}% {right_pct:>6.1f}%")

    print("\n" + "-" * 80)
    print(f"{'EXPECTED (uniform distribution)':<40} | {'25.0%':>7}  {'25.0%':>7}  {'25.0%':>7}  {'25.0%':>7}")

    # Category analysis
    print("\n" + "="*80)
    print("CATEGORY ANALYSIS")
    print("="*80)

    categories = {
        "Uniform on perimeter": [
            "1. Parametric",
            "2. Side Selection",
            "3. Edge Label",
            "5. Side + Position",
            "6. Parametric (Modular)",
            "7. Cartesian",
        ],
        "Uniform polar angle (non-uniform perimeter)": [
            "4. Polar Ray",
            "8. Polar Angle",
        ],
        "Interior projection (non-uniform)": [
            "9. Interior Projection",
        ],
    }

    for category, method_names in categories.items():
        print(f"\n[{category}]")
        print("-" * 80)

        total_bottom = total_top = total_left = total_right = count = 0

        for method_name, (_, edge_count, total_points) in results_data.items():
            if any(m in method_name for m in method_names):
                total_bottom += edge_count["bottom"] / total_points * 100
                total_top    += edge_count["top"]    / total_points * 100
                total_left   += edge_count["left"]   / total_points * 100
                total_right  += edge_count["right"]  / total_points * 100
                count += 1

        if count > 0:
            avg_b = total_bottom / count
            avg_t = total_top    / count
            avg_l = total_left   / count
            avg_r = total_right  / count

            print(f"Average distribution across {count} method(s):")
            print(f"  Bottom: {avg_b:6.1f}%  Top: {avg_t:6.1f}%  Left: {avg_l:6.1f}%  Right: {avg_r:6.1f}%")

            variance    = sum((v - 25.0) ** 2 for v in [avg_b, avg_t, avg_l, avg_r]) / 4
            uniformity  = 100 - (variance / 156.25) * 100

            if uniformity > 80:
                status = "GOOD (uniform)"
            elif uniformity > 50:
                status = "FAIR (some bias)"
            else:
                status = "POOR (significant bias)"

            print(f"  Uniformity: {uniformity:.1f}% — {status}")


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("GEOMETRY PROJECT: Square Perimeter Point Sampler")
    print("="*60)
    print("\nTesting 9 different methods for sampling random points")
    print("on the perimeter of a square [0,L]×[0,L]")

    L = 10
    iterations = 1000
    print(f"\nSquare side: L = {L}")
    print(f"Iterations per method: {iterations}")
    print(f"Total points per method: {iterations * 2}")

    method_descriptions = {
        "1. Parametric": (
            "Unrolls the perimeter into [0, 4L), samples a uniform parameter t.\n"
            "Distribution: uniform on the perimeter."
        ),
        "2. Side Selection": (
            "Randomly selects a side, then a uniform position on that side.\n"
            "Distribution: uniform on the perimeter.  [bug fixed: same-side pairs now allowed]"
        ),
        "3. Edge Label": (
            "Edge labelling approach (x0, xL, y0, yL).\n"
            "Distribution: uniform on the perimeter."
        ),
        "4. Polar Ray": (
            "Traces a ray from the center at a random polar angle to the boundary.\n"
            "Distribution: uniform over angles — NOT uniform on the perimeter."
        ),
        "5. Side + Position": (
            "Combines side selection with a scalar position on that side.\n"
            "Distribution: uniform on the perimeter."
        ),
        "6. Parametric (Modular)": (
            "Same as method 1 but uses the helper _perimeter_to_xy.\n"
            "Distribution: uniform on the perimeter."
        ),
        "7. Cartesian": (
            "Randomly fixes x or y to 0 or L, samples the other coordinate uniformly.\n"
            "Distribution: uniform on the perimeter."
        ),
        "8. Polar Angle": (
            "Simplified polar angle method using cos/sin ratio instead of ray casting.\n"
            "Distribution: uniform over angles — NOT uniform on the perimeter."
        ),
        "9. Interior Projection": (
            "Samples a random interior point and projects it onto the nearest side.\n"
            "Distribution: NOT uniform — side midpoints are over-represented."
        ),
    }

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

    results = {}
    results_data = {}

    for method, name in methods:
        if name in method_descriptions:
            print(f"\n{'-'*60}")
            print(f"Description: {method_descriptions[name]}")

        passed, edge_count, total_points = test_method(method, name, L=L, iterations=iterations)
        results[name] = passed
        results_data[name] = (passed, edge_count, total_points)

    # Summary
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)

    all_passed = True
    for method_name, passed in results.items():
        icon = "[OK]" if passed else "[!]"
        status = "PASSED" if passed else "FAILED"
        print(f"{icon} {method_name}: {status}")
        all_passed = all_passed and passed

    print_comparative_report(results_data)

    print("\n" + "="*60)
    if all_passed:
        print("\nAll methods working correctly!")
        return 0
    else:
        print("\nSome methods have issues. See details above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
