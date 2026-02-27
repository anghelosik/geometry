# Distance Analysis Between Two Random Points on the Perimeter of a Square

**Project:** geometry  
**Reference files:** `square_points.py`, `distance_analysis.py`  
**Date:** February 2026

---

## Problem Statement

Given a square with side length L > 0, two distinct points are sampled on its
perimeter and we want to estimate the probability that their Euclidean distance
is greater than L.

The project implements 9 different methods to generate the pair of points.
The numerical analysis (100 000 and 1 000 000 iterations, L = 1000) allows a
comparison of the distributions produced by each method and an assessment of
their suitability for answering the original question.

---

## Methods Analysed

| # | Function | Algorithm description |
|---|----------|-----------------------|
| 1 | `sample_parametric` | Uniform parametrization of the perimeter (t ∈ [0, 4L)) |
| 2 | `sample_by_side` | Random side selection, then uniform coordinate on the side |
| 3 | `sample_by_edge_label` | Edge labelling with uniform sampling |
| 4 | `sample_polar_ray` | Ray from center with uniform polar angle |
| 5 | `sample_side_pos` | Side + parameter with rejection for identical points |
| 6 | `sample_parametric_modular` | Variant of the parametrization using `_perimeter_to_xy` |
| 7 | `sample_cartesian` | Cartesian boundary constraint |
| 8 | `sample_polar_angle` | Simplified polar angle from center |
| 9 | `sample_interior_projection` | Uniform interior point projected onto the nearest side |

---

## Results (1 000 000 iterations, L = 1000)

```
Method                         |  Count | Attempts |    >L % |     Mean |      Std |      Min |      Max | #Shortest | #Longest
1. Parametric                  | 356258 |  1000000 |   35.63% |  734.780 |  355.040 |    0.004 | 1413.962 |    108622 |   123696
2. Side Selection              | 356290 |  1000000 |   35.63% |  735.031 |  354.979 |    0.001 | 1413.008 |    109144 |   123181
3. Edge Label                  | 357695 |  1000000 |   35.77% |  735.128 |  355.413 |    0.000 | 1413.833 |    109223 |   124027
4. Polar Ray                   | 339344 |  1000000 |   33.93% |  718.561 |  346.394 |    0.003 | 1411.900 |    111007 |    99392
5. Side + Position             | 358182 |  1000000 |   35.82% |  735.873 |  355.374 |    0.003 | 1413.435 |    109030 |   124698
6. Parametric (Modular)        | 357246 |  1000000 |   35.72% |  735.051 |  355.335 |    0.001 | 1413.237 |    109492 |   123739
7. Cartesian                   | 357756 |  1000000 |   35.78% |  735.262 |  355.388 |    0.001 | 1412.885 |    108744 |   124104
8. Polar Angle                 | 339675 |  1000000 |   33.97% |  718.776 |  346.471 |    0.002 | 1413.820 |    110614 |   100121
9. Interior Projection         | 297943 |  1000000 |   29.79% |  686.887 |  334.416 |    0.000 | 1397.343 |    124124 |    57042
```

---

## Analysis of Results

### Group 1 — Methods with uniform distribution on the perimeter (1, 2, 3, 5, 6, 7)

The six methods — `sample_parametric`, `sample_by_side`, `sample_by_edge_label`,
`sample_side_pos`, `sample_parametric_modular`, `sample_cartesian` — converge to
statistically indistinguishable values:

- **P(d > L) ≈ 35.7%** (variation < 0.2 percentage points over 1M iterations)
- **Mean ≈ 735**, corresponding to approximately 0.735·L, the theoretical expected value
- **Max ≈ 1414 ≈ √2·L**, the square's diagonal, which is the maximum possible distance
- **#Shortest and #Longest** are balanced (~109 000 and ~124 000): no method is
  structurally "shorter" or "longer" than the others

These methods are different implementations of the same probabilistic process:
two points drawn from a uniform distribution on the perimeter. They are all
equivalent and all suitable for answering the original question.

### Group 2 — Methods with polar angle sampling (4 and 8)

`sample_polar_ray` and `sample_polar_angle` produce results that are consistent
with each other but systematically different from Group 1:

- **P(d > L) ≈ 33.9%**, roughly 1.7 percentage points below Group 1
- **Mean ≈ 719**, about 16 units below Group 1
- **#Longest ≈ 100 000**, noticeably lower than the ~124 000 of Group 1

The reason is geometric: sampling polar angles uniformly in [0, 2π) is not
equivalent to sampling points uniformly on the perimeter.
The square's corners subtend a larger angular interval than the midpoints of
the sides, and are therefore **over-represented**.
This distorts the distribution of distances relative to the uniform case.

These methods answer a different question from the original one and produce a
biased estimate of approximately −1.7 percentage points.

### Group 3 — Projection method (9)

`sample_interior_projection` shows the most pronounced deviations:

- **P(d > L) ≈ 29.8%**, approximately **−5.9 percentage points** compared to Group 1
- **Mean ≈ 687**, about 48 units below
- **Max = 1397**, the only method that never exceeds 1400: projection never populates
  the corners, which are the points that maximise the distance
- **#Shortest = 124 124**, the highest value of all: systematically tends to produce
  the shortest distance in each iteration
- **#Longest = 57 042**, less than half the value of the other methods

The cause is structural: interior points near the centre of the square all project
onto the midpoints of the sides, creating a strong **concentration** of points there.
The corners receive almost no projections and are heavily under-represented.

The systematic error of ~6 percentage points is not an implementation bug:
it is the direct consequence of a probability distribution that differs from the
uniform distribution on the perimeter. Increasing the number of iterations does
not reduce this error.

---

## Conclusions

The question "what is the probability that two randomly chosen points on the perimeter
of a square with side L have distance greater than L?" has a unique answer only if
one specifies what "randomly chosen" means. The three groups of methods answer three
different questions:

| Implicit distribution                        | P(d > L)    | Methods                                                                      |
|----------------------------------------------|-------------|------------------------------------------------------------------------------|
| Uniform on the perimeter                     | **≈ 35.7%** | `sample_parametric`, `sample_by_side`, `sample_by_edge_label`, `sample_side_pos`, `sample_parametric_modular`, `sample_cartesian` |
| Uniform over the polar angle from the centre | ≈ 33.9%     | `sample_polar_ray`, `sample_polar_angle`                                     |
| Projection of an interior point              | ≈ 29.8%     | `sample_interior_projection`                                                 |

**Only the methods in Group 1 answer the question in its standard and
mathematically most natural interpretation.**

The exact theoretical value for the uniform distribution on the perimeter is
P(d > L) ≈ 0.3573 (obtainable analytically by integration).
The numerical results with 1M iterations converge to this value with an error
below 0.2 percentage points, confirming the correctness of the implementations.
