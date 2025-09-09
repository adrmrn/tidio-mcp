.PHONY: lint test install run clean fix help debug test-coverage test-coverage-html build

# Default target
help:
	@echo "Available commands:"
	@echo "  make lint               - Format and check code with ruff"
	@echo "  make fix                - Auto-fix ruff errors where possible"
	@echo "  make test               - Run all pytest tests"
	@echo "  make test-coverage      - Run tests with coverage report"
	@echo "  make test-coverage-html - Run tests with HTML coverage report"
	@echo "  make install            - Install dependencies with uv"
	@echo "  make run                - Run the MCP server"
	@echo "  make debug              - Run MCP inspector for debugging"
	@echo "  make build              - Build Docker image"
	@echo "  make clean              - Clean up cache files"

# Check code formatting and linting (no changes)
lint:
	uv run ruff format --check
	uv run ruff check

# Auto-fix ruff errors and format code
fix:
	uv run ruff format
	uv run ruff check --fix

# Run all tests
test:
	uv run pytest

# Run all tests with coverage report
test-coverage:
	uv run pytest --cov

# Run all tests with HTML coverage report
test-coverage-html:
	uv run pytest --cov --cov-report=html

# Install dependencies
install:
	uv sync

# Run the MCP server
run:
	uv run server.py

# Clean up cache files
clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name .pytest_cache -delete

# Run MCP inspector for debugging
debug:
	npx @modelcontextprotocol/inspector uv run server.py

# Build Docker image
build:
	docker build -t tidio-mcp .
