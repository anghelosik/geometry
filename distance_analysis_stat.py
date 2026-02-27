"""
Analisi delle distanze fra i due punti restituiti dalle 9 funzioni in `square_points.py`.
Per ogni metodo esegue `n` iterazioni (default=100) e conta quante volte la distanza
fra i due punti è > L. Stampa una tabella con conteggio, percentuale, media, deviazione
standard, minimo e massimo delle distanze.

Usage:
    .venv\\Scripts\\python.exe distance_analysis.py --iterations 100 --L 10

"""
import math
import argparse
import csv
from typing import Callable, List, Tuple

from square_points import (
    metodo1, metodo2, metodo3, metodo4, metodo5,
    metodo1_alt, metodo3_alt, metodo4_alt, metodo6_proiezione
)

METHODS: List[Tuple[str, Callable]] = [
    ("1. Parametrization", metodo1),
    ("2. Side Selection", metodo2),
    ("3. Edge Labels", metodo3),
    ("4. Ray from Center", metodo4),
    ("5. Side + Parameters", metodo5),
    ("6. Parametrization (Alt)", metodo1_alt),
    ("7. Edge Labels (Alt)", metodo3_alt),
    ("8. Ray (Alt)", metodo4_alt),
    ("9. Projection", metodo6_proiezione),
]


def euclidean(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def analyze(method_fn: Callable, L: float, iterations: int):
    """Restituisce (count_gt_L, attempts, mean, std, min, max).
    Le eccezioni vengono ignorate e non contate come attempts.
    """
    distances = []
    for _ in range(iterations):
        try:
            p1, p2 = method_fn(L)
            distances.append(euclidean(p1, p2))
        except Exception:
            continue

    if not distances:
        return 0, 0, 0.0, 0.0, 0.0, 0.0

    attempts = len(distances)
    count_gt_L = sum(1 for d in distances if d > L)
    mean = sum(distances) / attempts
    variance = sum((d - mean) ** 2 for d in distances) / attempts
    std = math.sqrt(variance)
    d_min = min(distances)
    d_max = max(distances)

    return count_gt_L, attempts, mean, std, d_min, d_max


def main(iterations=None, L=10.0, csv_path=None):
    """
    Esegue l'analisi delle distanze.

    Args:
        iterations: int o lista di int. Se None, usa argparse (default 100).
        L: lato del quadrato (default 10.0)
        csv_path: percorso file CSV di output (opzionale)
    """
    if iterations is None:
        parser = argparse.ArgumentParser(
            description="Distance > L analysis for square point methods"
        )
        parser.add_argument(
            "--iterations", "-n", type=int, nargs="+", default=[100],
            help="Numero di iterazioni per metodo (default 100)"
        )
        parser.add_argument("--L", type=float, default=10.0, help="Lato L (default 10)")
        parser.add_argument("--csv", type=str, default=None, help="Percorso file CSV di output")
        args = parser.parse_args()
        iteration_values = args.iterations
        L = args.L
        csv_path = args.csv
    else:
        iteration_values = [iterations] if isinstance(iterations, int) else iterations

    # Intestazioni colonne
    COL_METHOD  = 35
    COL_COUNT   =  6
    COL_ATT     =  8
    COL_PCT     =  7
    COL_MEAN    =  8
    COL_STD     =  8
    COL_MIN     =  8
    COL_MAX     =  8

    header = (
        f"{'Method':<{COL_METHOD}} | "
        f"{'Count':>{COL_COUNT}} | "
        f"{'Attempts':>{COL_ATT}} | "
        f"{'  >L %':>{COL_PCT}} | "
        f"{'Mean':>{COL_MEAN}} | "
        f"{'Std':>{COL_STD}} | "
        f"{'Min':>{COL_MIN}} | "
        f"{'Max':>{COL_MAX}}"
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
                "percent", "mean", "std", "min", "max"
            ])
        except Exception as e:
            print(f"Impossibile aprire '{csv_path}' per la scrittura: {e}")
            csv_file = None

    for iter_val in iteration_values:
        print(f"\nRunning analysis: iterations={iter_val}, L={L}\n")
        print(header)
        print(separator)

        results = []
        for name, fn in METHODS:
            count, attempts, mean, std, d_min, d_max = analyze(fn, L, iter_val)
            pct = (count / attempts * 100) if attempts > 0 else 0.0
            results.append((name, count, attempts, pct, mean, std, d_min, d_max))

            print(
                f"{name:<{COL_METHOD}} | "
                f"{count:{COL_COUNT}d} | "
                f"{attempts:{COL_ATT}d} | "
                f"{pct:{COL_PCT}.2f}% | "
                f"{mean:{COL_MEAN}.3f} | "
                f"{std:{COL_STD}.3f} | "
                f"{d_min:{COL_MIN}.3f} | "
                f"{d_max:{COL_MAX}.3f}"
            )

        if csv_file:
            try:
                for name, count, attempts, pct, mean, std, d_min, d_max in results:
                    csv_writer.writerow([
                        name, iter_val, count, attempts,
                        f"{pct:.3f}", f"{mean:.3f}", f"{std:.3f}",
                        f"{d_min:.3f}", f"{d_max:.3f}"
                    ])
            except Exception as e:
                print(f"Errore scrittura CSV per iterations={iter_val}: {e}")

    if csv_file:
        csv_file.close()
        print(f"\nRisultati scritti in {csv_path}")


if __name__ == "__main__":
    main(iterations=100000, L=1000.0)