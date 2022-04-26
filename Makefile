
all: clean

compile:
	python countrynames/compile.py

typecheck:
	mypy --strict countrynames

test: compile typecheck
	pip install -q -e ".[dev]"
	pytest

clean:
	rm -rf dist build
