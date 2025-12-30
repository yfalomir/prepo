.PHONY: ruff-fix
ruff-fix:
	uv run ruff check --fix prepo tests; \
	uv run ruff format prepo tests


.PHONY: test
test:
	pytest tests/


.PHONY: api-dev
api-dev:
	uv run fastapi dev prepo/api/api.py