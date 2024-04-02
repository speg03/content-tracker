.PHONY: all clean requirements dist lint test

all: dist
clean:
	rm -rf ./dist

requirements:
	uv pip compile -U pyproject.toml -o requirements.txt
lint:
	pre-commit run --all-files
test:
	pytest -v ./tests
dist:
	python3 -m build
