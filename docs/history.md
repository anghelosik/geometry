# Geometry Project — Change History

This document records bugs found and fixed, refactoring decisions, and other
notable changes made during the development of the project.

---

## Bug fix: `sample_by_side` — same-side pairs excluded

**Introduced in:** original version (`metodo2`)  
**Fixed in:** refactoring to `sample_by_side`

### Problem

The original implementation used the condition:

```python
while side1 == side2:
    ...
```

This forced the two points onto *different sides*, systematically excluding
approximately **25% of valid pairs** — those where both points fall on the same
side — introducing a significant bias in the distribution.

### Effect

The method answered a subtly different question from all the other methods.
The bias was not immediately obvious because P(d > L) still came out around
30–35%, within the plausible range.

### Empirical verification

With 10 000 iterations, the original method produced **0 same-side pairs**
(0.0%); the expected value for a truly uniform distribution is ~25%.

### Fix

The constraint was removed entirely. The two points are now sampled
independently, and rejection occurs only if the resulting points are
geometrically coincident (checked via `_is_distinct`).

### Test added

`TestSampleBySideFix.test_same_side_allowed` in `tests/test_square_points.py`
was added specifically to catch this bug. It would have detected the issue
immediately had it existed from the start.

---

## Bug fix: SyntaxWarning in `distance_analysis.py`

The docstring of `distance_analysis.py` contained the Windows path fragment
`\Scripts`, where `\S` was interpreted by Python as an invalid escape sequence,
producing a `SyntaxWarning` at import time.

**Fix:** the backslash was doubled — `\\Scripts` — making it a valid literal
backslash in the string.

---

## Refactoring: Italian → English identifiers

The original codebase was written with Italian-style function names. All public
functions were renamed to descriptive English identifiers to make the project
accessible and consistent with standard Python conventions.

| Original name | Current name |
|---|---|
| `metodo1` | `sample_parametric` |
| `metodo2` | `sample_by_side` |
| `metodo3` | `sample_by_edge_label` |
| `metodo4` | `sample_polar_ray` |
| `metodo5` | `sample_side_pos` |
| `metodo1_alt` | `sample_parametric_modular` |
| `metodo3_alt` | `sample_cartesian` |
| `metodo4_alt` | `sample_polar_angle` |
| `metodo6_proiezione` | `sample_interior_projection` |

Internal variable names that were in Italian (`lato`, `bordo`, `punto`, etc.)
were also renamed to their English equivalents at the same time.
