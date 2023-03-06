test:
	pytest -vv

format:
	isort --profile=black .
	black .

lint:
	isort --profile=black --check .
	black --check .
	flake8 --max-line-length=120 .
	mypy --strict forbid
