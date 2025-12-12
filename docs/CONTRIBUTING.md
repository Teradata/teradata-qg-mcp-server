# Contributing to Teradata QueryGrid MCP Server

Thank you for your interest in contributing to the Teradata QueryGrid MCP Server! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to professional standards of conduct. Please be respectful and constructive in all interactions.

## Getting Started

### Before You Start

**Important: Create a GitHub issue before starting work on a pull request.**

1. **Search existing issues** to see if your feature or bug has already been reported
2. **Create a new issue** if one doesn't exist:
   - Use a clear and descriptive title
   - For bug reports: include steps to reproduce, expected vs actual behavior
   - For feature requests: explain the use case and proposed solution
3. **Wait for feedback** from maintainers before investing significant time
4. **Reference the issue** in your pull request when ready

### Development Workflow

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or fix (reference the issue number: `feature/123-add-new-tool`)
4. Make your changes
5. Test your changes
6. Submit a pull request referencing the issue

## Development Setup

### Prerequisites

- Python 3.13 or higher
- pip and virtualenv
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Teradata/teradata-qg-mcp-server.git
   cd teradata-qg-mcp-server
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies (includes testing and linting tools):
   ```bash
   pip install -r requirements-dev.txt
   ```

## Code Style Guidelines

### Python Style

- Follow PEP 8 guidelines
- Use type annotations for all function parameters and return values
- Use `from __future__ import annotations` for forward references
- Maximum line length: 120 characters

### Type Annotations

- Use `str | None` instead of `Optional[str]`
- Use `dict[str, Any]` instead of `Dict[str, Any]`
- Always annotate function parameters and return types
- Ensure docstring types match function signature types

### Documentation

- All functions must have docstrings following Google style format
- Include:
  - Brief description
  - Args section with parameter names, types, and descriptions
  - Returns section with return type and description
  - Raises section if applicable

Example:
```python
def example_function(param1: str, param2: int | None = None) -> dict[str, Any]:
    """
    Brief description of the function.

    Args:
        param1 (str): Description of param1.
        param2 (int | None): Optional description of param2.

    Returns:
        dict[str, Any]: Description of return value.
    """
```

### Logging

- Use lazy logging format: `logger.debug("Message with %s", variable)`
- Do NOT use f-strings in logging calls
- Add debug logs at the start of tool functions: `logger.debug("Tool: function_name called")`
- For functions with parameters: `logger.debug("Tool: function_name called with param=%s", param)`

### Tool Development

When adding new tools:

1. Create tool functions in the appropriate file under `src/tools/`
2. Use the `@mcp.tool` decorator
3. Follow the standard pattern:
   ```python
   @mcp.tool
   def qg_operation_name(param: str) -> str:
       """
       Description of the operation.

       Args:
           param (str): Parameter description.

       Returns:
           ResponseType: formatted response with operation results + metadata
       """
       logger.debug("Tool: qg_operation_name called with param=%s", param)

       def _call():
           qg_manager = tools.get_qg_manager()
           if qg_manager is None:
               raise RuntimeError("QueryGridManager is not initialized")
           return qg_manager.client_name.operation(param)

       return run_tool("qg_operation_name", _call)
   ```

4. Import the new tool module in `src/tools/__init__.py`

### Type Checking

The project uses `mypy` for static type checking. All code must pass type checking:

```bash
# Run type checking
mypy src/ --ignore-missing-imports --show-error-codes

# Run with strict checking for untyped functions
mypy src/ --ignore-missing-imports --show-error-codes --check-untyped-defs
```

**Type checking requirements:**
- All functions must have type annotations for parameters and return values
- Use `dict[str, Any]` for dictionaries with mixed value types
- Use `str | None` for optional parameters (not `Optional[str]`)
- Ensure no type errors before submitting a pull request

### Testing

### Running Tests

The project has both unit tests and integration tests. For detailed testing information, see [TESTING.md](TESTING.md).

**Quick start:**
```bash
# Run all tests (requires confirmation for integration tests)
pytest -v

# Run all tests without confirmation
pytest -v --force

# Run only unit tests (no external dependencies)
pytest -v -m unit

# Run only integration tests
pytest -v -m integration

# Run with coverage
pytest --cov=src --cov-report=html
```

**Test structure:**
```
tests/
├── conftest.py              # Pytest configuration and shared fixtures
├── test_health.py          # Unit tests for health endpoint
├── test_server_modes.py    # Integration tests for server modes
├── test_tools_loading.py   # Unit tests for tool loading
├── qgm/                    # Unit tests for QGM API clients
│   └── test_api_info.py
└── tools/                  # Integration tests for MCP tools
    ├── test_api_info_tools.py
    ├── test_systems_tools.py
    ├── test_connectors_tools.py
    └── ...                 # 20+ tool test files
```

### Writing Tests

**Unit tests:**
- Mark with `@pytest.mark.unit`
- No external dependencies required
- Test individual components in isolation

**Integration tests:**
- Mark with `@pytest.mark.integration`
- Require QueryGrid Manager connection
- Test end-to-end functionality
- Use `qg_manager` or `mcp_client` fixtures

**Example:**

**Example:**
```python
from __future__ import annotations

import pytest
from fastmcp.client import Client

# Unit test
@pytest.mark.unit
def test_utility_function():
    """Test a utility function."""
    result = some_utility_function()
    assert result is not None

# Integration test
@pytest.mark.integration
async def test_mcp_tool(mcp_client: Client):
    """Test an MCP tool end-to-end."""
    result = await mcp_client.call_tool("qg_get_api_info", arguments={})
    
    assert result.data is not None
    assert "metadata" in result.data
    assert result.data["metadata"]["success"] is True
```

See [TESTING.md](TESTING.md) for comprehensive testing documentation.

## Submitting Changes

### Pull Request Process

1. **Ensure you have a corresponding GitHub issue** - Create one if it doesn't exist
2. Update documentation if needed
3. Ensure all tests pass
4. Verify type checking passes (no type errors)
5. Update the CHANGELOG if applicable
6. Create a pull request with a clear description of changes

### Pull Request Guidelines

- **Reference the issue number** in the PR title or description (e.g., "Fixes #123" or "Closes #456")
- Use a clear and descriptive title
- Include the purpose of the changes
- Provide context and reasoning for the changes
- Include screenshots for UI changes (if applicable)
- Link to the related issue using GitHub keywords (Fixes, Closes, Resolves)

### Commit Messages

- Use clear and meaningful commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Keep the first line under 72 characters
- Provide additional context in the commit body if needed
- Reference issue numbers where relevant

Example:
```
Add support for communication policies (#123)

- Implement qg_get_comm_policies tool
- Add comm_policies_tools module
- Update documentation

Fixes #123
```

## Documentation

### Code Documentation

- Keep docstrings up to date
- Document all public APIs
- Include examples where helpful

### README Updates

Update the README.md when:
- Adding new features
- Changing installation steps
- Modifying configuration options
- Adding new dependencies

## Questions?

If you have questions or need help, please:
- Check existing documentation
- Review closed issues for similar questions
- Open a new issue with your question

Thank you for contributing!
