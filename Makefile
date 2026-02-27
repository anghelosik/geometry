# ── geometry project Makefile ─────────────────────────────────────────────────
# Assumes the virtual environment is active.
# Windows: use   .venv\Scripts\activate.bat
# Linux:   use   source .venv/bin/activate

.PHONY: help install test test-verbose run analyse clean

help:
	@echo ""
	@echo "  make install       Install dependencies into the active venv"
	@echo "  make test          Run the full test suite (quiet)"
	@echo "  make test-verbose  Run the full test suite (verbose)"
	@echo "  make run           Run the interactive demo (main.py)"
	@echo "  make analyse       Run distance_analysis.py (100k iterations)"
	@echo "  make clean         Remove __pycache__, .pytest_cache, *.pyc"
	@echo ""

install:
	pip install -r requirements.txt

test:
	pytest tests/

test-verbose:
	pytest tests/ -v

run:
	python main.py

analyse:
	python distance_analysis.py --iterations 100000 --L 10

clean:
	find . -type d -name "__pycache__"  -not -path "./.venv/*" | xargs rm -rf
	find . -type d -name ".pytest_cache" -not -path "./.venv/*" | xargs rm -rf
	find . -type f -name "*.pyc"        -not -path "./.venv/*" -delete
	find . -type f -name "*.pyo"        -not -path "./.venv/*" -delete
