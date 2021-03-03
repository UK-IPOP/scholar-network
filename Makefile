
lint:
	flake8 src/scholar_network

test:
	pytest tests

test-cov:
	pytest --cov tests