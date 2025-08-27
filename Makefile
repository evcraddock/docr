.PHONY: install install-dev install-global uninstall-global upgrade-global test clean build upload

# Install package in development mode
install:
	uv sync
	uv pip install -e .

# Install with development dependencies
install-dev:
	uv sync --all-extras

# Install system-wide as a standalone tool
install-global:
	uv tool install .
	@echo "docr has been installed globally. You can now use 'docr' from anywhere."

# Uninstall global installation
uninstall-global:
	uv tool uninstall docr
	@echo "docr has been uninstalled from global tools."

# Upgrade global installation
upgrade-global:
	uv tool install --upgrade .

# Install system dependencies (Ubuntu/Debian)
install-system-deps:
	sudo apt update
	sudo apt install tesseract-ocr tesseract-ocr-eng libreoffice ghostscript fonts-dejavu unpaper

# Install system dependencies (macOS)
install-system-deps-mac:
	brew install tesseract libreoffice ghostscript

# Run tests
test:
	uv run pytest tests/ -v

# Run tests with coverage
test-coverage:
	uv run pytest --cov=docr --cov-report=html tests/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov/
	rm -rf .coverage

# Build package
build: clean
	uv build

# Upload to PyPI
upload: build
	uv publish

# Run docr with example
example:
	uv run docr --help

# Format code
format:
	uv run black docr/
	uv run ruff check --fix docr/

# Lint code
lint:
	uv run ruff check docr/
	uv run mypy docr/

# Run all checks (format, lint, test)
check: format lint test

# Create virtual environment if needed
venv:
	uv venv

# Update dependencies
update:
	uv lock --upgrade