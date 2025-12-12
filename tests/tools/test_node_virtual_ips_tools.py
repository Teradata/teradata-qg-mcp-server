"""Integration tests for node_virtual_ips_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_get_node_virtual_ips(mcp_client: Client):
    """Test getting all node virtual IPs."""
    result = await mcp_client.call_tool("qg_get_node_virtual_ips", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_node_virtual_ips"
    assert metadata["success"] is True

    # Verify result is a list
    virtual_ips = result.data["result"]
    assert isinstance(virtual_ips, list), "Node virtual IPs result should be a list"


@pytest.mark.integration
async def test_qg_get_node_virtual_ip_by_id_not_found(mcp_client: Client):
    """Test getting a node virtual IP with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_node_virtual_ip_by_id", arguments={"id": fake_id}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_node_virtual_ip_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_node_virtual_ip_by_id_invalid_uuid(mcp_client: Client):
    """Test getting a node virtual IP with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_node_virtual_ip_by_id", arguments={"id": "not-a-valid-uuid"}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_node_virtual_ip_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_delete_node_virtual_ip_not_found(mcp_client: Client):
    """Test deleting a node virtual IP with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_node_virtual_ip", arguments={"id": fake_id}
    )

    # API may return success for non-existent IDs (idempotent delete)
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_node_virtual_ip"


@pytest.mark.integration
async def test_qg_delete_node_virtual_ip_invalid_uuid(mcp_client: Client):
    """Test deleting a node virtual IP with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_node_virtual_ip", arguments={"id": "not-a-valid-uuid"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_node_virtual_ip"


@pytest.mark.integration
async def test_qg_node_virtual_ips_error_handling(mcp_client: Client):
    """Test error handling across node virtual IP operations."""
    # Test getting virtual IP with empty ID
    result = await mcp_client.call_tool(
        "qg_get_node_virtual_ip_by_id",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data
    
    # Test deleting virtual IP with empty ID
    result = await mcp_client.call_tool(
        "qg_delete_node_virtual_ip",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data
    
    # Test getting virtual IP with all-zeros UUID
    result = await mcp_client.call_tool(
        "qg_get_node_virtual_ip_by_id",
        arguments={"id": "00000000-0000-0000-0000-000000000000"},
    )
    assert result.data is not None
    assert "metadata" in result.data


@pytest.mark.integration
async def test_qg_node_virtual_ips_structure_validation(mcp_client: Client):
    """Test that node virtual IP objects have expected structure."""
    result = await mcp_client.call_tool("qg_get_node_virtual_ips", arguments={})
    
    assert result.data["metadata"]["success"] is True
    virtual_ips = result.data["result"]
    
    # Virtual IPs may or may not exist depending on configuration
    if len(virtual_ips) > 0:
        # Verify each virtual IP has expected fields
        for vip in virtual_ips:
            assert isinstance(vip, dict), "Each virtual IP should be a dictionary"
            assert "id" in vip, "Virtual IP should have 'id' field"
            
            # Validate ID is UUID format (basic check)
            vip_id = vip.get("id")
            assert isinstance(vip_id, str), "Virtual IP ID should be a string"
            assert len(vip_id) > 0, "Virtual IP ID should not be empty"


@pytest.mark.integration
async def test_qg_get_node_virtual_ip_by_id_with_existing(mcp_client: Client, qg_manager):
    """Test getting a specific node virtual IP by ID if any exist."""
    # First get all virtual IPs to get a valid ID
    all_virtual_ips = qg_manager.node_virtual_ip_client.get_node_virtual_ips()
    
    if not all_virtual_ips:
        pytest.skip("No node virtual IPs available for ID test")
    
    vip_id = all_virtual_ips[0].get("id")

    result = await mcp_client.call_tool(
        "qg_get_node_virtual_ip_by_id", arguments={"id": vip_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_node_virtual_ip_by_id"
    assert metadata["success"] is True

    # Verify virtual IP data
    virtual_ip = result.data["result"]
    assert isinstance(virtual_ip, dict)
    assert virtual_ip.get("id") == vip_id


@pytest.mark.integration
async def test_qg_node_virtual_ips_list_and_get_consistency(mcp_client: Client, qg_manager):
    """Test consistency between list virtual IPs and get virtual IP by ID."""
    # Get all virtual IPs
    list_result = await mcp_client.call_tool("qg_get_node_virtual_ips", arguments={})
    
    assert list_result.data["metadata"]["success"] is True
    virtual_ips = list_result.data["result"]
    
    if not virtual_ips:
        pytest.skip("No node virtual IPs available for consistency test")
    
    # Pick the first virtual IP and get it by ID
    first_vip_from_list = virtual_ips[0]
    vip_id = first_vip_from_list.get("id")
    
    get_result = await mcp_client.call_tool(
        "qg_get_node_virtual_ip_by_id", arguments={"id": vip_id}
    )
    
    assert get_result.data["metadata"]["success"] is True
    vip_by_id = get_result.data["result"]
    
    # Verify key fields match
    assert vip_by_id.get("id") == first_vip_from_list.get("id")
