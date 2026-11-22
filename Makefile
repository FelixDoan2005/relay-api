.PHONY: check run

check:
	ruff check --fix .
	ruff format .
	pytest

run:
	uvicorn app.main:app --reload