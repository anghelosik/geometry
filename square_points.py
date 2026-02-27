"""
square_points.py
================
Collection of 5 methods (+3 variants) for sampling two distinct random points
on the perimeter of a square with side length L.

Bug fixes compared to the original version
-------------------------------------------
- sample_by_side (original: metodo2): forced the two points onto *different sides*
  using:
      while side1 == side2: ...
  This systematically excluded valid point pairs that fall on the same side
  (approximately 25% of all pairs), introducing a significant bias.
  The correct check is whether the resulting POINTS are distinct,
  not whether the sides are different.

Note on sample_side_pos (original: metodo5)
--------------------------------------------
The condition `while side1 == side2 and abs(s1 - s2) < 1e-12` is
logically correct (the points are identical iff same side AND same
position), but uses a very tight threshold (1e-12). In practice,
with `random.uniform` an exact collision is virtually impossible,
so the loop almost never retries. The condition has been kept unchanged
but is documented here.
"""

import random
import math
from typing import Tuple

Point = Tuple[float, float]


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def _perimeter_to_xy(t: float, L: float) -> Point:
    """Convert a parameter t ∈ [0, 4L) to (x, y) coordinates on the boundary.

    The perimeter is traversed counter-clockwise starting from the
    bottom-left corner:
      [0,   L)  → bottom side  (y=0, x increasing)
      [L,  2L)  → right side   (x=L, y increasing)
      [2L, 3L)  → top side     (y=L, x decreasing)
      [3L, 4L)  → left side    (x=0, y decreasing)
    """
    t = t % (4 * L)
    if t < L:
        return (t, 0.0)
    elif t < 2 * L:
        return (L, t - L)
    elif t < 3 * L:
        return (L - (t - 2 * L), L)
    else:
        return (0.0, L - (t - 3 * L))


def _is_distinct(p1: Point, p2: Point, tol: float = 1e-12) -> bool:
    """Return True if the two points are geometrically distinct."""
    return abs(p1[0] - p2[0]) > tol or abs(p1[1] - p2[1]) > tol


# ─────────────────────────────────────────────────────────────────────────────
# ORIGINAL METHODS (1-5)
# ─────────────────────────────────────────────────────────────────────────────

def sample_parametric(L: float) -> Tuple[Point, Point]:
    """Linear parametrization of the perimeter.

    Unrolls the perimeter into [0, 4L) and samples two distinct values t,
    then converts them to (x, y) coordinates.
    Distribution: uniform on the perimeter.
    """
    def point(t: float) -> Point:
        if t < L:        return (t, 0.0)          # bottom side
        elif t < 2 * L:  return (L, t - L)         # right side
        elif t < 3 * L:  return (3 * L - t, L)     # top side
        else:            return (0.0, 4 * L - t)   # left side

    t1 = random.uniform(0, 4 * L)
    t2 = random.uniform(0, 4 * L)
    while abs(t1 - t2) < 1e-12:
        t2 = random.uniform(0, 4 * L)
    return point(t1), point(t2)


def sample_by_side(L: float) -> Tuple[Point, Point]:
    """Side selection + uniform position on the chosen side.

    For each point: picks one of the 4 sides at random, then a uniform
    position s ∈ [0, L] on that side. Retries until the two points are
    distinct (they may land on the same side).
    Distribution: uniform on the perimeter.

    FIX: the original version used `while side1 == side2` (forcing different
    sides), which excluded 25% of valid pairs. The condition now correctly
    checks the geometric distinctness of the resulting points.
    """
    SIDES = ["bottom", "top", "left", "right"]

    def choose_point(side: str) -> Point:
        s = random.uniform(0, L)
        if side == "bottom": return (s, 0.0)
        if side == "top":    return (s, L)
        if side == "left":   return (0.0, s)
        return (L, s)   # right

    p1 = choose_point(random.choice(SIDES))
    p2 = choose_point(random.choice(SIDES))
    while not _is_distinct(p1, p2):
        p2 = choose_point(random.choice(SIDES))
    return p1, p2


def sample_by_edge_label(L: float) -> Tuple[Point, Point]:
    """Edge labels (x0, xL, y0, yL).

    Each point is identified by an edge label ("x0", "xL", "y0", "yL") and
    a uniform position on that edge. Retries until the resulting points
    are distinct.
    Distribution: uniform on the perimeter.
    """
    EDGES = ["x0", "xL", "y0", "yL"]

    def point(edge: str) -> Point:
        s = random.uniform(0, L)
        if edge == "x0": return (0.0, s)
        if edge == "xL": return (L, s)
        if edge == "y0": return (s, 0.0)
        return (s, L)   # yL

    p1 = point(random.choice(EDGES))
    p2 = point(random.choice(EDGES))
    while not _is_distinct(p1, p2):
        p2 = point(random.choice(EDGES))
    return p1, p2


def sample_polar_ray(L: float) -> Tuple[Point, Point]:
    """Ray intersections from the center of the square.

    Samples two angles θ ∈ [0, 2π) and traces a ray from the center
    (L/2, L/2) to the boundary for each, computing the exact intersection
    with each of the four walls.
    Distribution: uniform over angles (not over the perimeter).
    """
    cx, cy = L / 2, L / 2

    def intersection(theta: float) -> Point:
        dx, dy = math.cos(theta), math.sin(theta)
        candidates = []

        if dx != 0:
            for xw in (0.0, L):
                t = (xw - cx) / dx
                y = cy + t * dy
                if t > 0 and 0 <= y <= L:
                    candidates.append((t, (xw, y)))
        if dy != 0:
            for yw in (0.0, L):
                t = (yw - cy) / dy
                x = cx + t * dx
                if t > 0 and 0 <= x <= L:
                    candidates.append((t, (x, yw)))

        if not candidates:
            # Degenerate case (should never occur with random angles)
            return (cx, 0.0)
        return min(candidates)[1]

    t1 = random.uniform(0, 2 * math.pi)
    t2 = random.uniform(0, 2 * math.pi)
    while abs(t1 - t2) < 1e-12:
        t2 = random.uniform(0, 2 * math.pi)
    return intersection(t1), intersection(t2)


def sample_side_pos(L: float) -> Tuple[Point, Point]:
    """Side selection + position, with distinctness check.

    Similar to sample_by_side but the (side, position) pair is generated
    in a single step. The while loop retries only when both the side and
    the position are practically identical (the points coincide).
    Distribution: uniform on the perimeter.

    Note: `while side1 == side2 and abs(s1 - s2) < 1e-12` is logically
    equivalent to checking that the points are not identical, but uses a
    very tight threshold; it works correctly in floating point because two
    independent `random.uniform` calls rarely produce the same value.
    """
    SIDES = ["bottom", "top", "left", "right"]

    def point(side: str, s: float) -> Point:
        if side == "bottom": return (s, 0.0)
        if side == "top":    return (s, L)
        if side == "left":   return (0.0, s)
        return (L, s)   # right

    side1 = random.choice(SIDES)
    side2 = random.choice(SIDES)
    s1 = random.uniform(0, L)
    s2 = random.uniform(0, L)

    while side1 == side2 and abs(s1 - s2) < 1e-12:
        side2 = random.choice(SIDES)
        s2 = random.uniform(0, L)

    return point(side1, s1), point(side2, s2)


# ─────────────────────────────────────────────────────────────────────────────
# VARIANTS / IMPROVED VERSIONS
# ─────────────────────────────────────────────────────────────────────────────

def sample_parametric_modular(L: float) -> Tuple[Point, Point]:
    """Linear parametrization of the perimeter (modular version).

    Identical to sample_parametric but uses the helper function
    _perimeter_to_xy for better readability and reuse.
    Distribution: uniform on the perimeter.
    """
    t1 = random.uniform(0, 4 * L)
    t2 = random.uniform(0, 4 * L)
    while abs(t1 - t2) < 1e-12:
        t2 = random.uniform(0, 4 * L)
    return _perimeter_to_xy(t1, L), _perimeter_to_xy(t2, L)


def sample_cartesian(L: float) -> Tuple[Point, Point]:
    """Cartesian coordinates with boundary constraint.

    For each point: randomly decides whether to fix x or y, then fixes
    that coordinate to 0 or L and samples the other uniformly in [0, L].
    Distribution: quasi-uniform (slight over-representation of sides
    compared to corners).
    """
    def pick_point() -> Point:
        if random.random() < 0.5:
            return (random.choice([0.0, L]), random.uniform(0, L))  # fix x
        else:
            return (random.uniform(0, L), random.choice([0.0, L]))  # fix y

    p1 = pick_point()
    p2 = pick_point()
    while not _is_distinct(p1, p2):
        p2 = pick_point()
    return p1, p2


def sample_polar_angle(L: float) -> Tuple[Point, Point]:
    """Polar angle from the center (simplified and robust version).

    Samples two angles θ ∈ [0, 2π) and computes the boundary point using
    the ratio between |cos θ| and |sin θ|, without explicitly searching
    for intersections with all four walls.
    Distribution: uniform over angles (not over the perimeter).
    """
    def angle_to_point(theta: float) -> Point:
        cx, cy = L / 2, L / 2
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        half = L / 2
        # Determine which pair of walls is intersected first
        if abs(cos_t) >= abs(sin_t):
            scale = half / abs(cos_t)
        else:
            scale = half / abs(sin_t)
        x = max(0.0, min(L, cx + cos_t * scale))
        y = max(0.0, min(L, cy + sin_t * scale))
        return (x, y)

    theta1 = random.uniform(0, 2 * math.pi)
    theta2 = random.uniform(0, 2 * math.pi)
    while abs(theta1 - theta2) < 1e-12:
        theta2 = random.uniform(0, 2 * math.pi)
    return angle_to_point(theta1), angle_to_point(theta2)


def sample_interior_projection(L: float) -> Tuple[Point, Point]:
    """Rejection sampling + projection onto the nearest boundary side.

    Samples a random point in the interior [0, L]² and projects it onto
    the nearest side of the square. Retries until the two resulting points
    are distinct.
    Distribution: NOT uniform — the midpoints of each side receive a
    disproportionate number of projections (most interior points project
    there). Corners are under-represented.
    """
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
    while not _is_distinct(p1, p2):
        p2 = pick_point()
    return p1, p2


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    L = 5.0
    methods = [
        ("1  - Parametric (linear)            ", sample_parametric),
        ("2  - Side selection (FIX)           ", sample_by_side),
        ("3  - Edge label                     ", sample_by_edge_label),
        ("4  - Polar ray from center          ", sample_polar_ray),
        ("5  - Side + position                ", sample_side_pos),
        ("6  - Parametric (modular)           ", sample_parametric_modular),
        ("7  - Cartesian boundary             ", sample_cartesian),
        ("8  - Polar angle (simplified)       ", sample_polar_angle),
        ("9  - Interior projection            ", sample_interior_projection),
    ]

    print(f"Square with side L = {L}\n")
    for name, fn in methods:
        p1, p2 = fn(L)
        print(f"Method {name}  P1=({p1[0]:.4f},{p1[1]:.4f})  P2=({p2[0]:.4f},{p2[1]:.4f})")
