"""
Analisi delle distanze fra i due punti restituiti dalle 9 funzioni in `square_points.py`.
Ad ogni iterazione vengono eseguiti tutti i metodi; la tabella riporta per ciascuno:
conteggio e percentuale distanza > L, media, deviazione standard, minimo, massimo,
e quante volte quel metodo ha prodotto la distanza più piccola / più grande fra tutti i metodi.

Usage:
    .venv\\Scripts\\python.exe distance_analysis.py --iterations 100 --L 10

"""
import math
import argparse
import csv
from typing import Callable, Dict, List, Optional, Tuple

from square_points import (
    metodo1, metodo2, metodo3, metodo4, metodo5,
    metodo1_alt, metodo3_alt, metodo4_alt, metodo6_proiezione
)

METHODS: List[Tuple[str, Callable]] = [
    ("1. Parametrization",       metodo1),
    ("2. Side Selection",        metodo2),
    ("3. Edge Labels",           metodo3),
    ("4. Ray from Center",       metodo4),
    ("5. Side + Parameters",     metodo5),
    ("6. Parametrization (Alt)", metodo1_alt),
    ("7. Edge Labels (Alt)",     metodo3_alt),
    ("8. Ray (Alt)",             metodo4_alt),
    ("9. Projection",            metodo6_proiezione),
]

N = len(METHODS)


def euclidean(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def run_all(L: float, iterations: int):
    """
    Ad ogni iterazione chiama tutti i metodi e confronta le distanze.
    Restituisce un dict con:
      - 'distances': lista di N liste di float (una per metodo, None se eccezione)
      - 'min_wins':  lista di N interi (quante volte il metodo ha dato la distanza minima)
      - 'max_wins':  lista di N interi (quante volte il metodo ha dato la distanza massima)
    In caso di parità (distanze identiche) tutti i metodi a pari merito vengono contati.
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
    """Calcola le statistiche per ogni metodo dal risultato di run_all."""
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
    Esegue l'analisi delle distanze.

    Args:
        iterations: int o lista di int. Se None, usa argparse (default 100).
        L:          lato del quadrato (default 10.0)
        csv_path:   percorso file CSV di output (opzionale)
    """
    if iterations is None:
        parser = argparse.ArgumentParser(
            description="Distance > L analysis for square point methods"
        )
        parser.add_argument(
            "--iterations", "-n", type=int, nargs="+", default=[100],
            help="Numero di iterazioni (default 100)"
        )
        parser.add_argument("--L", type=float, default=10.0, help="Lato L (default 10)")
        parser.add_argument("--csv", type=str, default=None, help="Percorso file CSV output")
        args = parser.parse_args()
        iteration_values = args.iterations
        L = args.L
        csv_path = args.csv
    else:
        iteration_values = [iterations] if isinstance(iterations, int) else list(iterations)

    # Larghezze colonne
    CM = 35; CC = 6; CA = 8; CP = 7; CME = 8; CS = 8; CMI = 8; CMA = 8; CMINW = 9; CMAXW = 8

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
            print(f"Impossibile aprire '{csv_path}': {e}")
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
                print(f"Errore scrittura CSV: {e}")

    if csv_file:
        csv_file.close()
        print(f"\nRisultati scritti in '{csv_path}'")


if __name__ == "__main__":
    main(iterations=1000000, L=1000.0)   