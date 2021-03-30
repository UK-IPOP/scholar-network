
format:
	isort .
	black .

lint:
	flake8 .

test:
	pytest tests

test-cov:
	pytest --cov tests