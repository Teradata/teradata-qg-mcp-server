# Testing Guide

This document explains the testing setup and how to run tests for the Teradata QueryGrid MCP Server.

## ⚠️ Important: Test Execution Warning

**Integration tests will CREATE, MODIFY, and DELETE entities** in your configured QueryGrid Manager instance. 

Before running tests, you will be prompted to confirm execution. The prompt displays:
- Your QueryGrid Manager connection details (host, port, username)
- Information about test entities that will be created
- Cleanup behavior information

### Confirmation Prompt

When you run tests without the `--force` flag, you'll see:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                           ⚠️  TEST EXECUTION WARNING                        ║
╚════════════════════════════════════════════════════════════════════════════╝

Running these tests will CREATE, MODIFY, and DELETE entities in the QueryGrid
Manager instance configured in your environment.

QueryGrid Manager Configuration:
  • URL:      https://your-host:9443
  • Host:     your-host
  • Port:     9443
  • Username: your-username

Test entities (datacenters, systems, connectors, bridges, fabrics, policies,
user mappings, etc.) will be created with names prefixed with 'test_' or
'pytest_'. These entities are automatically cleaned up after test execution.

To skip this prompt in future runs, use: pytest --force

Do you want to continue? [y/N]:
```

### Bypassing the Confirmation

To skip the confirmation prompt (useful for CI/CD pipelines or repeated test runs):

```bash
pytest -v --force
```

### Test Entity Cleanup

Tests automatically clean up created entities after execution. However:
- If tests are interrupted (Ctrl+C), some entities may remain
- If cleanup fails due to dependencies, entities may remain
- You may need to manually delete leftover test entities from QueryGrid Manager

## Test Structure

```
tests/
├── conftest.py                 # Pytest configuration and fixtures
├── test_health.py             # Unit tests for health endpoint
├── test_server_modes.py        # Integration tests for server startup modes
├── test_tools_loading.py      # Unit tests for tool loading
├── qgm/
│   ├── __init__.py
│   └── test_api_info.py       # Unit tests for API info client
└── tools/                     # Integration tests for MCP tools
    ├── __init__.py
    ├── test_api_info_tools.py      # API information tools
    ├── test_systems_tools.py  # System management tools
    ├── test_connectors_tools.py  # Connector tools
    ├── test_fabrics_tools.py  # Fabric tools
    ├── test_datacenters_tools.py  # Datacenter tools
    ├── test_users_tools.py    # User management tools
    └── ...                    # 20+ other tool test files
```

## Test Types

### Unit Tests
Unit tests do not require a running QueryGrid Manager instance and test individual components in isolation.

**Examples:**
- `tests/qgm/test_api_info.py` - Tests for the API info client
- `tests/test_health.py` - Tests for the health endpoint
- `tests/test_tools_loading.py` - Tests for tool loading mechanism

### Integration Tests
Integration tests connect to a live QueryGrid Manager instance and test the full workflow from tool calls to API responses.

**Examples:**
- `tests/tools/test_api_info_tools.py` - Tests for API info tools
- `tests/tools/test_systems_tools.py` - Tests for system management tools (25+ tests)
- `tests/tools/test_connectors_tools.py` - Tests for connector management
- `tests/tools/test_users_tools.py` - Tests for user management (21 tests)
- `tests/test_server_modes.py` - Tests for server startup in foreground/background modes

**Server Mode Tests:**

The `test_server_modes.py` file validates the MCP server can run in different modes:

1. **Background Mode** - Server starts as daemon process with PID file
2. **Foreground Mode** - Server runs in interactive mode (can be stopped with Ctrl+C)
3. **Reload Validation** - Ensures `--reload` requires `--foreground` flag

These tests ensure deployment flexibility across different operating environments.
- `tests/tools/test_systems_tools.py` - Tests for system management tools (25+ tests)
- `tests/tools/test_connectors_tools.py` - Tests for connector management
- `tests/tools/test_users_tools.py` - Tests for user management (21 tests)
- `tests/test_server_modes.py` - Tests for server startup in foreground/background modes

## Configuration

### Environment Variables

Integration tests require these environment variables to be set (typically in a `.env` file):

```env
QG_MANAGER_HOST=your-qg-host
QG_MANAGER_PORT=9443
QG_MANAGER_USERNAME=your-username
QG_MANAGER_PASSWORD=your-password
QG_MANAGER_VERIFY_SSL=false
```

The `conftest.py` file automatically loads the `.env` file from the project root.

### Virtual Environment Setup

**Important:** Always run tests and the server from within an activated virtual environment:

```bash
# Create virtual environment (one-time setup)
python -m venv venv

# Activate virtual environment (required before each session)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

All commands below assume the virtual environment is activated.

### Installing Test Dependencies

Tests require development dependencies:

```bash
# Install all development dependencies (includes testing tools)
pip install -r requirements-dev.txt
```

This installs:
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `mypy` - Type checking
- `ruff` - Linting and formatting
- All production dependencies

## Running the Server for Development

When developing or testing, you can run the server in different modes:

### Foreground Mode with Hot Reload (Recommended for Development)

```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py start --foreground --reload --log-level DEBUG
```

This mode:
- Shows logs in the console
- Automatically restarts when code changes
- Can be stopped with Ctrl+C
- Perfect for active development

### Foreground Mode (Debugging)

```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py start --foreground --log-level DEBUG
```

This mode:
- Shows logs in the console
- No automatic restart
- Can be stopped with Ctrl+C
- Useful when you want more control

### Background Mode (Testing Production Behavior)

```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py start --log-level DEBUG

# Check status
./scripts/td-qg-mcp-server.py status

# Stop server
./scripts/td-qg-mcp-server.py stop
```

This mode:
- Runs as detached background process
- Logs written to `logs/qg_server_YYYYMMDD.log`
- PID file created at `run/server.pid`
- Mimics production deployment

### Pytest Configuration

The `pyproject.toml` file contains pytest configuration:

```toml
[tool.pytest.ini_options]
markers = [
    "unit: marks tests as unit tests that don't require external services",
    "integration: marks tests as integration tests that require a live QueryGrid Manager (deselect with '-m \"not integration\"')",
]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## Running Tests

### Run All Tests (with confirmation)
```bash
pytest -v
```

### Run All Tests (skip confirmation)
```bash
pytest -v --force
```

### Run Only Unit Tests (no confirmation needed)
```bash
pytest -v -m unit
```

### Run Tests with Coverage

The project is configured to automatically generate coverage reports when running tests.

**Run tests with coverage (default):**
```bash
pytest
```

This will:
- Run all tests
- Generate coverage data for the `src/` directory
- Display coverage summary in terminal with missing lines
- Create HTML coverage report in `htmlcov/`
- Generate XML coverage report for CI/CD (coverage.xml)

**View HTML coverage report:**
```bash
# After running tests
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

**Run tests without coverage:**
```bash
pytest --no-cov
```

**Generate coverage for specific tests:**
```bash
# Coverage for unit tests only
pytest -m unit

# Coverage for specific test file
pytest tests/test_config_integration.py

# Coverage for specific module
pytest tests/tools/test_systems_tools.py
```

### Coverage Configuration

Coverage settings in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=html --cov-report=term-missing --cov-report=xml"

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
    "*/venv/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
]
show_missing = true
precision = 2
```

Coverage reports are automatically excluded from version control via `.gitignore`.

### Run Only Integration Tests (requires confirmation)
```bash
pytest -v -m integration
```

### Run Tests in a Specific Directory
```bash
pytest -v tests/tools/ --force
```

### Run a Specific Test File
```bash
pytest -v tests/tools/test_api_info_tools.py --force
```

### Run a Specific Test Function
```bash
pytest -v tests/tools/test_api_info_tools.py::test_qg_get_api_info --force
```

### Command Line Options

- `--force`: Skip the confirmation prompt and proceed with test execution
- `-v` or `--verbose`: Increase verbosity
- `-s`: Show print statements and disable output capture
- `-x`: Stop on first failure
- `--tb=short`: Short traceback format
- `-k EXPRESSION`: Run tests matching the given substring expression

## Fixtures

### `qg_manager` (Session-scoped)

The `qg_manager` fixture provides a QueryGrid Manager instance for integration tests.

**Usage:**
```python
@pytest.mark.integration
def test_my_feature(qg_manager):
    result = qg_manager.api_info_client.get_api_info()
    assert "appVersion" in result
```

**Features:**
- Session-scoped: created once per test session
- Automatically loads configuration from environment variables
- Skips tests if required environment variables are not set
- Automatically closes the session after all tests complete

### `mcp_client` (Function-scoped)

The `mcp_client` fixture provides a FastMCP Client for testing MCP tools via the MCP protocol.

**Usage:**
```python
from fastmcp.client import Client

@pytest.mark.integration
async def test_my_tool(mcp_client: Client):
    result = await mcp_client.call_tool("qg_get_api_info", arguments={})
    assert result.data is not None
```

**Features:**
- Function-scoped: created for each test function
- Automatically injects the QueryGrid Manager instance
- Provides async context for tool calls
- Cleans up after each test

### `test_infrastructure` (Session-scoped)

The `test_infrastructure` fixture sets up shared test resources (datacenter, system, software versions) for integration tests.

**Provides:**
- `datacenter_id`: ID of test datacenter
- `system_id`: ID of test system
- `node_version`: NODE software version
- `fabric_version`: FABRIC software version
- `connector_version`: CONNECTOR software version

## Writing New Tests

### Unit Tests

1. Create a new test file in `tests/` or a subdirectory
2. Mark tests with `@pytest.mark.unit`
3. Use standard pytest patterns

```python
from __future__ import annotations

import pytest

@pytest.mark.unit
def test_my_feature():
    """Test description."""
    # Your test code
    assert True
```

### Integration Tests

1. Create a new test file in `tests/tools/` or relevant subdirectory
2. Mark tests with `@pytest.mark.integration`
3. Use the `qg_manager` fixture

```python
from __future__ import annotations

import pytest

@pytest.mark.integration
def test_my_integration(qg_manager):
    """Test description."""
    result = qg_manager.some_client.some_method()
    assert result is not None
```

### Testing MCP Tools with FastMCP Client

To test MCP tools using the recommended FastMCP Client pattern (async):

```python
from __future__ import annotations

import pytest
from fastmcp.client import Client

from src.mcp_server import qg_mcp_server as mcp


@pytest.fixture
async def mcp_client(qg_manager):
    """Create an MCP client fixture for testing tools."""
    import tools

    # Inject the manager instance
    tools.set_qg_manager(qg_manager)

    async with Client(mcp) as client:
        yield client

    # Cleanup
    tools.set_qg_manager(None)


@pytest.mark.integration
async def test_qg_get_api_info(mcp_client: Client):
    """Test getting API information via MCP tool."""
    result = await mcp_client.call_tool("qg_get_api_info", arguments={})
    
    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data
    
    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_api_info"
    assert metadata["success"] is True
```

**Note:** Async tests require `pytest-asyncio` to be installed and `asyncio_mode = "auto"` configured in `pyproject.toml`.

### `test_infrastructure` (Session-scoped)

The `test_infrastructure` fixture sets up shared test resources (datacenter, system, software versions) for integration tests.

**Provides:**
- `datacenter_id`: ID of test datacenter
- `system_id`: ID of test system  
- `node_version`: NODE software version
- `fabric_version`: FABRIC software version
- `connector_version`: CONNECTOR software version

**Usage:**
```python
@pytest.mark.integration
async def test_create_system(mcp_client: Client, test_infrastructure):
    node_version = test_infrastructure.get("node_version")
    datacenter_id = test_infrastructure.get("datacenter_id")
    # Use these values in your test
```

## Test Coverage

To run tests with coverage:

```bash
pytest --cov=src --cov-report=html
```

This generates an HTML coverage report in `htmlcov/`.

## Continuous Integration

For CI/CD pipelines:

```bash
# Run unit tests only (no external dependencies)
pytest -v -m unit

# Run all tests (requires QueryGrid Manager)
pytest -v
```

## Troubleshooting

### Integration Tests Skipped

If integration tests are skipped with a message about missing configuration:
1. Ensure the `.env` file exists in the project root
2. Verify all required environment variables are set
3. Check that `python-dotenv` is installed: `pip install python-dotenv`

### Connection Errors

If integration tests fail with connection errors:
1. Verify the QueryGrid Manager is running and accessible
2. Check firewall settings
3. Verify credentials are correct
4. Set `QG_MANAGER_VERIFY_SSL=false` if using self-signed certificates

### SSL Warnings

The warnings about unverified HTTPS requests are expected when `QG_MANAGER_VERIFY_SSL=false`. To suppress them:
```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## Best Practices

1. **Keep tests focused**: Each test should verify one specific behavior
2. **Use descriptive names**: Test names should clearly indicate what is being tested
3. **Add docstrings**: Include a brief description of what the test does
4. **Mark integration tests**: Always use `@pytest.mark.integration` for tests that require external services
5. **Clean up resources**: Use fixtures for setup/teardown to ensure clean state
6. **Avoid test interdependencies**: Tests should be able to run in any order
7. **Use type annotations**: Include `from __future__ import annotations` in all test files
