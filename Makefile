SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	poetry run flake8 . --count --exit-zero --statistics

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check

.PHONY: test
test: lint package unit

patch_release:
	$(eval poetry_output=$(shell poetry version patch))
	@echo $(poetry_output)
	$(eval version_number=$(shell echo $(poetry_output) | cut -d' ' -f6))
	@git add .
	@git commit -m "New release $(version_number)"
	@git tag -a $(version_number) -m "Release $(version_number)"

minor_release:
	$(eval poetry_output=$(shell poetry version minor))
	@echo $(poetry_output)
	$(eval version_number=$(shell echo $(poetry_output) | cut -d' ' -f6))
	@git add .
	@git commit -m "New release $(version_number)"
	@git tag -a $(version_number) -m "Release $(version_number)"

major_release:
	$(eval poetry_output=$(shell poetry version major))
	@echo $(poetry_output)
	$(eval version_number=$(shell echo $(poetry_output) | cut -d' ' -f6))
	@git add .
	@git commit -m "New release $(version_number)"
	@git tag -a $(version_number) -m "Release $(version_number)"

clean:
	@rm -rf tests/output
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +
