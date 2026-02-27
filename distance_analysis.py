"""
Distance analysis between the two points returned by the 9 functions in `square_points.py`.
At each iteration all methods are called; the table reports for each one:
count and percentage of distance > L, mean, standard deviation, min, max,
and how many times that method produced the shortest / longest distance among all methods.

Usage:
    .venv\\Scripts\\python.exe distance_analysis.py --iterations 100 --L 10

"""
import math
import argparse
import csv
from typing import Callable, Dict, List, Optional, Tuple

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

METHODS: List[Tuple[str, Callable]] = [
    ("1. Parametric",              sample_parametric),
    ("2. Side Selection",          sample_by_side),
    ("3. Edge Label",              sample_by_edge_label),
    ("4. Polar Ray",               sample_polar_ray),
    ("5. Side + Position",         sample_side_pos),
    ("6. Parametric (Modular)",    sample_parametric_modular),
    ("7. Cartesian",               sample_cartesian),
    ("8. Polar Angle",             sample_polar_angle),
    ("9. Interior Projection",     sample_interior_projection),
]

N = len(METHODS)


def euclidean(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def run_all(L: float, iterations: int) -> Dict:
    """
    Run `iterations` iterations. At each step all methods are called and
    their distances are collected. Returns a dict with:
      - 'distances': list of N lists of float (one per method, None on exception)
      - 'min_wins':  list of N ints (how many times the method produced the minimum distance)
      - 'max_wins':  list of N ints (how many times the method produced the maximum distance)
    In case of a tie (identical distances) all tied methods are counted.
    """
    distances: List[List[Optional[float]]] = [[] for _ in range(N)]
    min_wins = [0] * N
    max_wins = [0] * N

    for _ in range(iterations):
        row: List[Optional[float]] = []
        for _, fn in METHODS:
            try:
                p1, p2 = fn(L)
                row.append(euclidean(p1, p2))
            except Exception:
                row.append(None)

        valid = [(i, d) for i, d in enumerate(row) if d is not None]
        if valid:
            min_d = min(d for _, d in valid)
            max_d = max(d for _, d in valid)
            for i, d in valid:
                if math.isclose(d, min_d, rel_tol=1e-9):
                    min_wins[i] += 1
                if math.isclose(d, max_d, rel_tol=1e-9):
                    max_wins[i] += 1

        for i, d in enumerate(row):
            distances[i].append(d)

    return {"distances": distances, "min_wins": min_wins, "max_wins": max_wins}


def summarize(data: Dict, L: float) -> List[Tuple]:
    """Compute statistics for each method from the result of run_all."""
    results = []
    for i in range(N):
        dlist = [d for d in data["distances"][i] if d is not None]
        if not dlist:
            results.append((0, 0, 0.0, 0.0, 0.0, 0.0, 0, 0))
            continue
        attempts = len(dlist)
        count_gt_L = sum(1 for d in dlist if d > L)
        mean = sum(dlist) / attempts
        variance = sum((d - mean) ** 2 for d in dlist) / attempts
        std = math.sqrt(variance)
        d_min = min(dlist)
        d_max = max(dlist)
        results.append((
            count_gt_L, attempts, mean, std, d_min, d_max,
            data["min_wins"][i], data["max_wins"][i]
        ))
    return results


def main(iterations=None, L=10.0, csv_path=None):
    """
    Run the distance analysis.

    Args:
        iterations: int or list of int. If None, uses argparse (default 100).
        L:          square side length (default 10.0)
        csv_path:   path to CSV output file (optional)
    """
    if iterations is None:
        parser = argparse.ArgumentParser(
            description="Distance > L analysis for square point sampling methods"
        )
        parser.add_argument(
            "--iterations", "-n", type=int, nargs="+", default=[100],
            help="Number of iterations (default 100)"
        )
        parser.add_argument("--L", type=float, default=10.0, help="Side length L (default 10)")
        parser.add_argument("--csv", type=str, default=None, help="CSV output file path")
        args = parser.parse_args()
        iteration_values = args.iterations
        L = args.L
        csv_path = args.csv
    else:
        iteration_values = [iterations] if isinstance(iterations, int) else list(iterations)

    # Column widths
    CM = 30; CC = 6; CA = 8; CP = 7; CME = 8; CS = 8; CMI = 8; CMA = 8; CMINW = 9; CMAXW = 8

    header = (
        f"{'Method':<{CM}} | "
        f"{'Count':>{CC}} | "
        f"{'Attempts':>{CA}} | "
        f"{'  >L %':>{CP}} | "
        f"{'Mean':>{CME}} | "
        f"{'Std':>{CS}} | "
        f"{'Min':>{CMI}} | "
        f"{'Max':>{CMA}} | "
        f"{'#Shortest':>{CMINW}} | "
        f"{'#Longest':>{CMAXW}}"
    )
    separator = "-" * len(header)

    # CSV setup
    csv_file = None
    if csv_path:
        try:
            csv_file = open(csv_path, "w", newline="", encoding="utf-8")
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([
                "method", "iterations", "count_gt_L", "attempts",
                "percent", "mean", "std", "min", "max",
                "shortest_wins", "longest_wins"
            ])
        except Exception as e:
            print(f"Cannot open '{csv_path}': {e}")
            csv_file = None

    for iter_val in iteration_values:
        print(f"\nRunning analysis: iterations={iter_val}, L={L}\n")

        data = run_all(L, iter_val)
        stats = summarize(data, L)

        print(header)
        print(separator)

        for i, (name, _) in enumerate(METHODS):
            count, attempts, mean, std, d_min, d_max, min_wins, max_wins = stats[i]
            pct = (count / attempts * 100) if attempts > 0 else 0.0
            print(
                f"{name:<{CM}} | "
                f"{count:{CC}d} | "
                f"{attempts:{CA}d} | "
                f"{pct:{CP}.2f}% | "
                f"{mean:{CME}.3f} | "
                f"{std:{CS}.3f} | "
                f"{d_min:{CMI}.3f} | "
                f"{d_max:{CMA}.3f} | "
                f"{min_wins:{CMINW}d} | "
                f"{max_wins:{CMAXW}d}"
            )

        if csv_file:
            try:
                for i, (name, _) in enumerate(METHODS):
                    count, attempts, mean, std, d_min, d_max, min_wins, max_wins = stats[i]
                    pct = (count / attempts * 100) if attempts > 0 else 0.0
                    csv_writer.writerow([
                        name, iter_val, count, attempts,
                        f"{pct:.3f}", f"{mean:.3f}", f"{std:.3f}",
                        f"{d_min:.3f}", f"{d_max:.3f}",
                        min_wins, max_wins
                    ])
            except Exception as e:
                print(f"CSV write error: {e}")

    if csv_file:
        csv_file.close()
        print(f"\nResults written to '{csv_path}'")


if __name__ == "__main__":
    main(iterations=1000000, L=1000.0)
