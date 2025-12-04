.PHONY: ruff-fix
ruff-fix:
	uv run ruff check --fix .; \
	uv run ruff format .


.PHONY: test
test:
	pytest tests/