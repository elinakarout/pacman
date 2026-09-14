.PHONY: install run debug clean lint lint-strict

PYTHON := python3
MAIN := pac-man.py
CONFIG := config.json

install:
	uv sync

run:
	uv run $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	uv run flake8 . --exclude .venv
	uv run mypy .

.PHONY: install run debug clean lint