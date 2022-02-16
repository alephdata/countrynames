
all: clean

test:
	pip install -q -e ".[dev]"
	pytest

clean:
	rm -rf dist build
