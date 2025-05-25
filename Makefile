setup: # setup the environment with poetry
	pip install pipx
	pipx install poetry>=2
	poetry install
	poetry run pre-commit install
	poetry env activate

check: # run quality checking tools
	poetry check --lock
	poetry run pre-commit run -a
	poetry run mypy .

test: # test the code with pytest
	poetry run pytest tests/
