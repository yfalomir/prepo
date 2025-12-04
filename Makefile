.PHONY: ruff-fix
ruff-fix:
	uv run ruff check --fix .; \
	uv run ruff format .