
all: clean

test:
	pip install -q -e ".[dev]"
	nosetests

clean:
	rm -rf dist build
