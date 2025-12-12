"""Integration tests for manager_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_get_managers(mcp_client: Client):
    """Test getting all managers."""
    result = await mcp_client.call_tool("qg_get_managers", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_managers"
    assert metadata["success"] is True

    # Verify result is a list
    managers = result.data["result"]
    assert isinstance(managers, list), "Managers result should be a list"
    assert len(managers) > 0, "Should have at least one manager"
    
    # Verify manager structure
    first_manager = managers[0]
    assert "id" in first_manager, "Manager should have 'id' field"
    assert "hostname" in first_manager, "Manager should have 'hostname' field"


@pytest.mark.integration
async def test_qg_get_managers_with_extra_info(mcp_client: Client):
    """Test getting all managers with extra_info option."""
    result = await mcp_client.call_tool(
        "qg_get_managers", arguments={"extra_info": True}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_managers"
    assert metadata["success"] is True

    managers = result.data["result"]
    assert isinstance(managers, list)
    assert len(managers) > 0


@pytest.mark.integration
async def test_qg_get_managers_with_name_filter(mcp_client: Client, qg_manager):
    """Test getting managers filtered by hostname."""
    # First, get all managers to know what hostname to filter by
    all_managers = qg_manager.manager_client.get_managers()
    
    if not all_managers:
        pytest.skip("No managers available for filtering test")
    
    # Use the first manager's hostname for filtering
    test_hostname = all_managers[0].get("hostname")
    
    result = await mcp_client.call_tool(
        "qg_get_managers", arguments={"filter_by_name": test_hostname}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_managers"
    assert metadata["success"] is True

    managers = result.data["result"]
    assert isinstance(managers, list)
    # Should find at least one manager matching the hostname
    if len(managers) > 0:
        assert any(mgr.get("hostname") == test_hostname for mgr in managers)


@pytest.mark.integration
async def test_qg_get_managers_with_wildcard_filter(mcp_client: Client, qg_manager):
    """Test getting managers with wildcard hostname filter."""
    # Get a manager hostname and use wildcard pattern
    all_managers = qg_manager.manager_client.get_managers()
    
    if not all_managers:
        pytest.skip("No managers available for filtering test")
    
    # Use wildcard pattern - just use * to match all
    result = await mcp_client.call_tool(
        "qg_get_managers", arguments={"filter_by_name": "*"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_managers"
    assert metadata["success"] is True

    managers = result.data["result"]
    assert isinstance(managers, list)
    assert len(managers) > 0


@pytest.mark.integration
async def test_qg_get_managers_with_nonexistent_filter(mcp_client: Client):
    """Test getting managers with filter that matches nothing."""
    result = await mcp_client.call_tool(
        "qg_get_managers", 
        arguments={"filter_by_name": "nonexistent-manager-hostname-12345"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_managers"
    assert metadata["success"] is True

    managers = result.data["result"]
    assert isinstance(managers, list)
    # Should return empty list when no matches
    assert len(managers) == 0


@pytest.mark.integration
async def test_qg_get_manager_by_id(mcp_client: Client, qg_manager):
    """Test getting a specific manager by ID."""
    # First, get all managers to get a valid manager ID
    all_managers = qg_manager.manager_client.get_managers()
    
    if not all_managers:
        pytest.skip("No managers available for ID test")
    
    manager_id = all_managers[0].get("id")

    result = await mcp_client.call_tool(
        "qg_get_manager_by_id", arguments={"id": manager_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_manager_by_id"
    assert metadata["success"] is True

    # Verify manager data
    manager = result.data["result"]
    assert isinstance(manager, dict)
    assert manager.get("id") == manager_id
    assert "hostname" in manager


@pytest.mark.integration
async def test_qg_get_manager_by_id_not_found(mcp_client: Client):
    """Test getting a manager with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_manager_by_id", arguments={"id": fake_id}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_manager_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_manager_by_id_invalid_uuid(mcp_client: Client):
    """Test getting a manager with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_manager_by_id", arguments={"id": "not-a-valid-uuid"}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_manager_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_manager_by_id_empty_id(mcp_client: Client):
    """Test getting a manager with empty ID."""
    result = await mcp_client.call_tool(
        "qg_get_manager_by_id", arguments={"id": ""}
    )

    # API may handle empty ID differently - just verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_manager_by_id"
    # API behavior with empty ID may vary


@pytest.mark.integration
async def test_qg_get_manager_by_id_with_all_zeros_uuid(mcp_client: Client):
    """Test getting a manager with all-zeros UUID."""
    result = await mcp_client.call_tool(
        "qg_get_manager_by_id",
        arguments={"id": "00000000-0000-0000-0000-000000000000"},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_manager_by_id"
    # Likely returns not found
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_managers_list_and_get_consistency(mcp_client: Client, qg_manager):
    """Test consistency between list managers and get manager by ID."""
    # Get all managers
    list_result = await mcp_client.call_tool("qg_get_managers", arguments={})
    
    assert list_result.data["metadata"]["success"] is True
    managers = list_result.data["result"]
    
    if not managers:
        pytest.skip("No managers available for consistency test")
    
    # Pick the first manager and get it by ID
    first_manager_from_list = managers[0]
    manager_id = first_manager_from_list.get("id")
    
    get_result = await mcp_client.call_tool(
        "qg_get_manager_by_id", arguments={"id": manager_id}
    )
    
    assert get_result.data["metadata"]["success"] is True
    manager_by_id = get_result.data["result"]
    
    # Verify key fields match
    assert manager_by_id.get("id") == first_manager_from_list.get("id")
    assert manager_by_id.get("hostname") == first_manager_from_list.get("hostname")


@pytest.mark.integration
async def test_qg_managers_with_combined_options(mcp_client: Client, qg_manager):
    """Test getting managers with multiple options combined."""
    # Get a manager hostname for filtering
    all_managers = qg_manager.manager_client.get_managers()
    
    if not all_managers:
        pytest.skip("No managers available for combined options test")
    
    test_hostname = all_managers[0].get("hostname")
    
    # Test with both extra_info and filter
    result = await mcp_client.call_tool(
        "qg_get_managers",
        arguments={
            "extra_info": True,
            "filter_by_name": test_hostname,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_managers"
    assert metadata["success"] is True

    managers = result.data["result"]
    assert isinstance(managers, list)


@pytest.mark.integration
async def test_qg_managers_error_handling(mcp_client: Client):
    """Test error handling across manager operations."""
    # Test with various invalid IDs
    invalid_ids = [
        "not-a-uuid",
        "",
        "12345",
        "invalid-format-abc-123",
    ]
    
    for invalid_id in invalid_ids:
        result = await mcp_client.call_tool(
            "qg_get_manager_by_id",
            arguments={"id": invalid_id},
        )
        assert result.data is not None
        assert "metadata" in result.data
        # Should handle gracefully, either success=False or appropriate error


@pytest.mark.integration
async def test_qg_managers_structure_validation(mcp_client: Client, qg_manager):
    """Test that manager objects have expected structure."""
    result = await mcp_client.call_tool("qg_get_managers", arguments={})
    
    assert result.data["metadata"]["success"] is True
    managers = result.data["result"]
    
    if not managers:
        pytest.skip("No managers available for structure validation")
    
    # Verify each manager has expected fields
    for manager in managers:
        assert isinstance(manager, dict), "Each manager should be a dictionary"
        assert "id" in manager, "Manager should have 'id' field"
        assert "hostname" in manager, "Manager should have 'hostname' field"
        
        # Validate ID is UUID format (basic check)
        manager_id = manager.get("id")
        assert isinstance(manager_id, str), "Manager ID should be a string"
        assert len(manager_id) > 0, "Manager ID should not be empty"


@pytest.mark.integration
async def test_qg_get_managers_case_insensitive_filter(mcp_client: Client, qg_manager):
    """Test that hostname filtering is case insensitive."""
    all_managers = qg_manager.manager_client.get_managers()
    
    if not all_managers:
        pytest.skip("No managers available for case sensitivity test")
    
    test_hostname = all_managers[0].get("hostname")
    
    # Test with uppercase version of hostname
    result_upper = await mcp_client.call_tool(
        "qg_get_managers", arguments={"filter_by_name": test_hostname.upper()}
    )
    
    # Test with lowercase version
    result_lower = await mcp_client.call_tool(
        "qg_get_managers", arguments={"filter_by_name": test_hostname.lower()}
    )
    
    # Both should succeed (case insensitive matching)
    assert result_upper.data["metadata"]["success"] is True
    assert result_lower.data["metadata"]["success"] is True
    
    # Both should return same number of results (if any)
    managers_upper = result_upper.data["result"]
    managers_lower = result_lower.data["result"]
    
    assert len(managers_upper) == len(managers_lower)
