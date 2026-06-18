## Project Overview

This is a Tidio MCP (Model Context Protocol) server that provides integration with the Tidio customer support platform. The server exposes Tidio API functionality as MCP tools for managing contacts, tickets, departments, and operators.

## Architecture

- **server.py**: Thin runnable entrypoint — imports the shared app and the domain tool modules (to register their tools), then runs the server
- **core.py**: Leaf module holding the shared `FastMCP("Tidio")` instance, the configured `TidioApiClient`, and the `_tool_call_succeed` response helper
- **tools/**: Per-domain tool modules that decorate the shared instance — `contacts.py` (also owns the contact validation/payload-shaping helpers), `tickets.py`, `directory.py` (operators + departments)
- **tidio_client.py**: TidioApiClient wrapper class for API communication
- **pyproject.toml**: Python project configuration with dependencies
- **Makefile**: Shortcuts for common development tasks
- **.mcp.json**: MCP server configuration for Claude Code
- **Dockerfile**: Docker containerization for easy deployment
- **DOCKER.md**: Complete Docker deployment guide

### Core Components

- **TidioApiClient**: Custom API client wrapper using `requests.Session` with base URL `https://api.tidio.com` and authentication headers
- **Single shared FastMCP instance**: One `FastMCP("Tidio")` lives in `core.py`; every domain module imports it and registers tools against it. (`mcp` 1.13.1 has no `mount`/`import_server` sub-app composition.)
- **Registration is a side effect of import**: A tool only registers when its module is imported and its `@mcp.tool` decorator runs. `server.py` must import every domain module before serving. A wiring test (`tests/test_wiring.py`) asserts all expected tool names are exposed, guarding against a domain silently failing to register.
- **MCP Tools**: Each API endpoint is exposed as a decorated `@mcp.tool()` function
- **Environment Variables**: Requires `TIDIO_CLIENT_ID` and `TIDIO_CLIENT_SECRET` from .env file
- **Error Handling**: Centralized error handling in TidioApiClient with automatic HTTP status checking

### Adding a new domain

1. Create `tools/<domain>.py`, import `mcp` (and any helpers) from `core`, and define the tools with `@mcp.tool(...)`.
2. Import the new module in `server.py` so its tools register on startup.
3. Add a `tests/test_<domain>.py` and update the expected tool-name set in `tests/test_wiring.py`.

## Development Commands

**Run the MCP server:**
```bash
uv run python server.py
```

**Install dependencies:**
```bash
uv sync
```

**Run code linting and formatting:**
```bash
uv run ruff check          # Check for linting issues
uv run ruff check --fix    # Auto-fix issues where possible
uv run ruff format         # Format code
```

**Run tests:**
```bash
uv run pytest             # Run all tests
uv run pytest -v          # Run tests with verbose output
uv run pytest --cov       # Run tests with coverage report
uv run pytest tests/test_tidio_client.py  # Run specific test file
```

**IMPORTANT**: After making any code changes, always run `uv run ruff check` and `uv run pytest` to ensure code quality and functionality. All code must pass ruff checks and tests before committing.

## Key Design Patterns

- **Centralized API Client**: TidioApiClient class handles all HTTP communication with consistent headers and error handling
- **Simplified Error Handling**: TidioApiClient automatically raises exceptions for HTTP errors, JSON decode errors, and network issues
- **Tool Return Values**: All tools return `{"status": "ok", "data": {...}}` via `_tool_call_succeed()`. Mutation/delete operations that have no response body return `{"status": "ok", "data": {}}`
- **Input Validation**: Update and create operations include comprehensive validation with descriptive ValueError messages
- **Message Types**: Ticket replies support both public responses and internal notes via `message_type` parameter
- **Session Management**: Uses `requests.Session` for connection pooling and consistent headers across requests
- **Documentation**: Do not add redundant docs - usually class name, method name, and code itself should be descriptive enough
