"""Integration tests for api_info_tools."""

from __future__ import annotations

import pytest
from fastmcp.client import Client


@pytest.mark.integration
async def test_qg_get_api_info_via_tool(mcp_client: Client):
    """Test getting API information via the MCP tool wrapper."""
    result = await mcp_client.call_tool("qg_get_api_info", arguments={})

    # Verify response structure - result.data contains the actual response
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_api_info"
    assert metadata["success"] is True

    # Verify actual API info in result
    api_info = result.data["result"]
    assert isinstance(api_info, dict), "API info result should be a dictionary"
    assert "appVersion" in api_info, "API info should contain appVersion"


@pytest.mark.integration
async def test_qg_get_api_info_error_handling(mcp_client: Client, qg_manager):
    """Test error handling when QueryGrid Manager is not available."""
    from src import tools

    # Set manager to None to simulate unavailability
    tools.set_qg_manager(None)

    result = await mcp_client.call_tool("qg_get_api_info", arguments={})
    result = await mcp_client.call_tool("qg_get_api_info", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data even on error"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata indicates failure
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_api_info"
    assert metadata["success"] is False
    assert "error" in metadata

    # Verify error message in result
    error_result = result.data["result"]
    assert isinstance(error_result, str), "Error result should be a string"
    assert "Error" in error_result or "error" in error_result.lower()

    # Restore manager for other tests
    tools.set_qg_manager(qg_manager)

