.PHONY: ruff-fix
ruff-fix:
	uv run ruff check --fix prepo; \
	uv run ruff format prepo


.PHONY: test
test:
	pytest tests/