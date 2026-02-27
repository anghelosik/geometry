"""
altri_square_points.py
=======================
Alternative / early implementations of the five core sampling strategies.

These were the original prototypes written before square_points.py was
refactored. They are kept here for reference and comparison.
The canonical, fully-documented versions live in square_points.py.
"""

import random
import math
from typing import Tuple

Point = Tuple[float, float]


def _perimeter_to_xy(t: float, L: float) -> Point:
    """Convert a parameter t ∈ [0, 4L) to (x, y) coordinates on the boundary."""
    t = t % (4 * L)
    if t < L:
        return (t, 0.0)
    elif t < 2 * L:
        return (L, t - L)
    elif t < 3 * L:
        return (L - (t - 2 * L), L)
    else:
        return (0.0, L - (t - 3 * L))


# ── Method 1: Linear parametrization ─────────────────────────────────────────

def sample_parametric_v0(L: float) -> Tuple[Point, Point]:
    """Unroll the perimeter into [0, 4L) and sample two distinct values t."""
    t1 = random.uniform(0, 4 * L)
    t2 = random.uniform(0, 4 * L)
    while t1 == t2:   # near-impossible in floating point, but correct
        t2 = random.uniform(0, 4 * L)
    return _perimeter_to_xy(t1, L), _perimeter_to_xy(t2, L)


# ── Method 2: Side index + position ──────────────────────────────────────────

def sample_by_side_v0(L: float) -> Tuple[Point, Point]:
    """Pick a random side (0=bottom, 1=right, 2=top, 3=left), then a position s ∈ [0, L].

    Note: uses integer side indices instead of string labels.
    """
    def pick_point() -> Point:
        side = random.randint(0, 3)
        s = random.uniform(0, L)
        if side == 0: return (s, 0.0)
        if side == 1: return (L, s)
        if side == 2: return (s, L)
        return (0.0, s)

    p1 = pick_point()
    p2 = pick_point()
    while p1 == p2:
        p2 = pick_point()
    return p1, p2


# ── Method 3: Cartesian boundary ─────────────────────────────────────────────

def sample_cartesian_v0(L: float) -> Tuple[Point, Point]:
    """Fix x or y to 0 or L, sample the other coordinate uniformly in [0, L]."""
    def pick_point() -> Point:
        if random.random() < 0.5:        # fix x
            x = random.choice([0.0, L])
            y = random.uniform(0, L)
            return (x, y)
        else:                             # fix y
            y = random.choice([0.0, L])
            x = random.uniform(0, L)
            return (x, y)

    p1 = pick_point()
    p2 = pick_point()
    while p1 == p2:
        p2 = pick_point()
    return p1, p2


# ── Method 4: Polar angle from center ────────────────────────────────────────

def sample_polar_angle_v0(L: float) -> Tuple[Point, Point]:
    """Sample two angles θ ∈ [0, 2π) and cast rays from the center to the boundary."""
    def angle_to_point(theta: float) -> Point:
        cx, cy = L / 2, L / 2
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        half = L / 2
        if abs(cos_t) > abs(sin_t):   # ray hits left or right wall first
            scale = half / abs(cos_t)
        else:                          # ray hits bottom or top wall first
            scale = half / abs(sin_t)
        x = max(0.0, min(L, cx + cos_t * scale))
        y = max(0.0, min(L, cy + sin_t * scale))
        return (x, y)

    theta1 = random.uniform(0, 2 * math.pi)
    theta2 = random.uniform(0, 2 * math.pi)
    while abs(theta1 - theta2) < 1e-12:
        theta2 = random.uniform(0, 2 * math.pi)
    return angle_to_point(theta1), angle_to_point(theta2)


# ── Method 5: Interior projection ────────────────────────────────────────────

def sample_interior_projection_v0(L: float) -> Tuple[Point, Point]:
    """Sample a random interior point and project it onto the nearest side."""
    def project_to_border(x: float, y: float) -> Point:
        d = {"bottom": y, "top": L - y, "left": x, "right": L - x}
        nearest = min(d, key=d.get)
        if nearest == "bottom": return (x, 0.0)
        if nearest == "top":    return (x, L)
        if nearest == "left":   return (0.0, y)
        return (L, y)

    def pick_point() -> Point:
        return project_to_border(random.uniform(0, L), random.uniform(0, L))

    p1 = pick_point()
    p2 = pick_point()
    while p1 == p2:
        p2 = pick_point()
    return p1, p2


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    L = 5.0
    methods = [
        ("1 - Parametric (v0)         ", sample_parametric_v0),
        ("2 - Side index + pos (v0)   ", sample_by_side_v0),
        ("3 - Cartesian (v0)          ", sample_cartesian_v0),
        ("4 - Polar angle (v0)        ", sample_polar_angle_v0),
        ("5 - Interior projection (v0)", sample_interior_projection_v0),
    ]

    print(f"Square side L = {L}\n")
    for name, fn in methods:
        p1, p2 = fn(L)
        print(f"Method {name}  P1=({p1[0]:.4f},{p1[1]:.4f})  P2=({p2[0]:.4f},{p2[1]:.4f})")
