.PHONY: lint
lint:
	@tox -e lint

# Default python: 3.8
PY := py38


# prompt_example> make test PY=py38 OPTIONS="-- -s"
.PHONY: test
test:
	@tox -e $(PY) $(OPTIONS)

.PHONY: coverage
coverage:
	@tox -e coverage

.PHONY: install-dev
install-dev:
	@pip install -e .


##### Build #####

.PHONY: build-python-source
build-python-source:
	@python setup.py sdist

.PHONY: bumpversion
bumpversion:
	@tox -e bumpversion $(OPTIONS)