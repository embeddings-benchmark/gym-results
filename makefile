install:
	uv sync --group dev

test:
	uv run --no-sync pytest
