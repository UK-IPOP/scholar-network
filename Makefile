format:
	@isort .
	@black .

lint:
	@flake8 . --max-line-length=89

test:
	@pytest tests

test-cov:
	@pytest --cov tests

build:
	@poetry build

version:
	@poetry version patch

publish:
	@poetry publish

clean:
	@rm -rf dist