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
	uv run flake8 .
	uv run mypy .

compile:
	uv run pyinstaller --onefile --noconsole --add-data="pacraft_assets:." pac-man.py

.PHONY: install run debug clean lint