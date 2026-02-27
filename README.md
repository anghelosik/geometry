# geometry

A computational and probabilistic study of random point sampling on the
perimeter of a square.

## The problem

> Given a square with side length **L > 0**, what is the probability that two
> points chosen at random on its perimeter have Euclidean distance **greater than L**?

The answer depends entirely on what "chosen at random" means. This project
implements and compares **9 sampling methods**, showing that only those that
produce a uniform distribution on the perimeter converge to the correct
theoretical answer of **≈ 35.7%**.

## Quick start

```bash
git clone <repo-url>
cd geometry
python -m venv .venv

# Windows
.venv\Scripts\activate.bat
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt

# Run the demo
python main.py

# Run the statistical analysis
python distance_analysis.py --iterations 100000 --L 10

# Run the test suite
pytest tests/ -v
```

## Project layout

```
geometry/
├── square_points.py      # 9 sampling methods  (main module)
├── distance_analysis.py  # comparative statistical analysis
├── main.py               # interactive demo
├── tests/                # pytest test suite
├── docs/                 # full documentation
│   ├── index.md
│   └── distance_analysis_report.md
├── examples/             # usage examples
├── config/               # configuration (settings.yaml)
└── requirements.txt
```

## Sampling methods

| Function | Distribution | P(d > L) |
|---|---|---|
| `sample_parametric` | Uniform on perimeter | ≈ 35.7% |
| `sample_by_side` | Uniform on perimeter | ≈ 35.7% |
| `sample_by_edge_label` | Uniform on perimeter | ≈ 35.7% |
| `sample_side_pos` | Uniform on perimeter | ≈ 35.7% |
| `sample_parametric_modular` | Uniform on perimeter | ≈ 35.7% |
| `sample_cartesian` | Uniform on perimeter | ≈ 35.7% |
| `sample_polar_ray` | Uniform over angle | ≈ 33.9% |
| `sample_polar_angle` | Uniform over angle | ≈ 33.9% |
| `sample_interior_projection` | Non-uniform (biased) | ≈ 29.8% |

See [`docs/distance_analysis_report.md`](docs/distance_analysis_report.md) for
the full numerical analysis with 1 000 000 iterations.

## Requirements

- Python 3.8+
- pytest
- colorama

## License

MIT
