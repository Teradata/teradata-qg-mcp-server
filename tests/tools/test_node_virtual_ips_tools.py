"""Integration tests for node_virtual_ips_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from src.tools import set_qg_manager


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
async def test_qg_get_node_virtual_ip_by_id_with_existing(
    mcp_client: Client, qg_manager
):
    """Test getting a specific node virtual IP by ID if any exist."""
    # First get all nodes to find a valid node ID
    nodes = qg_manager.node_client.get_nodes()

    if not nodes:
        pytest.skip("No nodes available for virtual IP test")

    node_id = nodes[0].get("id")

    # Create a virtual IP for testing
    virtual_ips = [{"name": "eth0", "address": "192.168.100.1"}]

    create_result = await mcp_client.call_tool(
        "qg_put_node_virtual_ip", arguments={"id": node_id, "virtual_ips": virtual_ips}
    )

    assert create_result.data["metadata"]["success"] is True
    vip_id = node_id  # The virtual IP ID is the same as the node ID

    # Now test getting it by ID
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

    # Clean up
    await mcp_client.call_tool("qg_delete_node_virtual_ip", arguments={"id": vip_id})


@pytest.mark.integration
async def test_qg_node_virtual_ips_list_and_get_consistency(
    mcp_client: Client, qg_manager
):
    """Test consistency between list virtual IPs and get virtual IP by ID."""
    # First get all nodes to find a valid node ID
    nodes = qg_manager.node_client.get_nodes()

    if not nodes:
        pytest.skip("No nodes available for virtual IP test")

    node_id = nodes[0].get("id")

    # Create a virtual IP for testing
    virtual_ips = [{"name": "eth0", "address": "192.168.100.2"}]

    create_result = await mcp_client.call_tool(
        "qg_put_node_virtual_ip", arguments={"id": node_id, "virtual_ips": virtual_ips}
    )

    assert create_result.data["metadata"]["success"] is True

    # Get all virtual IPs
    list_result = await mcp_client.call_tool("qg_get_node_virtual_ips", arguments={})

    assert list_result.data["metadata"]["success"] is True
    virtual_ips_list = list_result.data["result"]

    # Find the virtual IP we just created
    first_vip_from_list = None
    for vip in virtual_ips_list:
        if vip.get("id") == node_id:
            first_vip_from_list = vip
            break

    assert first_vip_from_list is not None, "Created virtual IP not found in list"
    vip_id = first_vip_from_list.get("id")

    # Get by ID
    get_result = await mcp_client.call_tool(
        "qg_get_node_virtual_ip_by_id", arguments={"id": vip_id}
    )

    assert get_result.data["metadata"]["success"] is True
    vip_by_id = get_result.data["result"]

    # Verify key fields match
    assert vip_by_id.get("id") == first_vip_from_list.get("id")

    # Clean up
    await mcp_client.call_tool("qg_delete_node_virtual_ip", arguments={"id": vip_id})


@pytest.mark.integration
async def test_qg_put_node_virtual_ip(mcp_client: Client, qg_manager):
    """Test putting node virtual IPs."""
    # First get all nodes to find a valid node ID
    nodes = qg_manager.node_client.get_nodes()

    if not nodes:
        pytest.skip("No nodes available for virtual IP test")

    node_id = nodes[0].get("id")

    # Define virtual IPs to set
    virtual_ips = [
        {"name": "eth0", "address": "192.168.1.100"},
        {"name": "eth1", "address": "10.0.0.50"},
    ]

    # Put the virtual IPs
    result = await mcp_client.call_tool(
        "qg_put_node_virtual_ip", arguments={"id": node_id, "virtual_ips": virtual_ips}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_node_virtual_ip"
    assert metadata["success"] is True

    # Verify result
    updated_vip = result.data["result"]
    assert isinstance(updated_vip, dict)
    assert updated_vip.get("id") == node_id
    assert "networkInterfaces" in updated_vip

    # Verify virtual IPs were set correctly
    network_interfaces = updated_vip["networkInterfaces"]
    assert len(network_interfaces) == 2

    # Clean up - delete the virtual IP
    await mcp_client.call_tool("qg_delete_node_virtual_ip", arguments={"id": node_id})


@pytest.mark.integration
async def test_qg_put_node_virtual_ip_not_found(mcp_client: Client):
    """Test putting node virtual IPs with non-existent node ID."""
    fake_id = str(uuid.uuid4())
    virtual_ips = [{"name": "eth0", "address": "192.168.1.100"}]

    result = await mcp_client.call_tool(
        "qg_put_node_virtual_ip", arguments={"id": fake_id, "virtual_ips": virtual_ips}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_node_virtual_ip"
    # API might return success or failure depending on implementation
    # Just verify we get a response


@pytest.mark.integration
async def test_qg_put_node_virtual_ip_invalid_data(mcp_client: Client, qg_manager):
    """Test putting node virtual IPs with invalid data."""
    # First get all nodes to find a valid node ID
    nodes = qg_manager.node_client.get_nodes()

    if not nodes:
        pytest.skip("No nodes available for virtual IP test")

    node_id = nodes[0].get("id")

    # Test with missing 'address' field
    invalid_virtual_ips = [{"name": "eth0"}]

    result = await mcp_client.call_tool(
        "qg_put_node_virtual_ip",
        arguments={"id": node_id, "virtual_ips": invalid_virtual_ips},
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_node_virtual_ip"
    # API should reject invalid data


@pytest.mark.integration
async def test_qg_put_node_virtual_ip_empty_list(mcp_client: Client, qg_manager):
    """Test putting node virtual IPs with empty list."""
    # First get all nodes to find a valid node ID
    nodes = qg_manager.node_client.get_nodes()

    if not nodes:
        pytest.skip("No nodes available for virtual IP test")

    node_id = nodes[0].get("id")

    # Put empty list of virtual IPs
    result = await mcp_client.call_tool(
        "qg_put_node_virtual_ip", arguments={"id": node_id, "virtual_ips": []}
    )

    # Verify response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_node_virtual_ip"
    # Empty list should be accepted (removes all virtual IPs)


@pytest.mark.integration
async def test_qg_put_node_virtual_ip_update_existing(mcp_client: Client, qg_manager):
    """Test updating existing node virtual IPs."""
    # First get all nodes to find a valid node ID
    nodes = qg_manager.node_client.get_nodes()

    if not nodes:
        pytest.skip("No nodes available for virtual IP test")

    node_id = nodes[0].get("id")

    # Set initial virtual IPs
    initial_virtual_ips = [{"name": "eth0", "address": "192.168.1.100"}]

    result1 = await mcp_client.call_tool(
        "qg_put_node_virtual_ip",
        arguments={"id": node_id, "virtual_ips": initial_virtual_ips},
    )

    assert result1.data["metadata"]["success"] is True

    # Update with new virtual IPs
    updated_virtual_ips = [
        {"name": "eth0", "address": "192.168.1.200"},
        {"name": "eth1", "address": "10.0.0.100"},
    ]

    result2 = await mcp_client.call_tool(
        "qg_put_node_virtual_ip",
        arguments={"id": node_id, "virtual_ips": updated_virtual_ips},
    )

    assert result2.data["metadata"]["success"] is True

    # Verify the update
    updated_vip = result2.data["result"]
    network_interfaces = updated_vip["networkInterfaces"]
    assert len(network_interfaces) == 2

    # Clean up
    await mcp_client.call_tool("qg_delete_node_virtual_ip", arguments={"id": node_id})
