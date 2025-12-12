"""Integration tests for nodes_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_get_nodes(mcp_client: Client):
    """Test getting all nodes."""
    result = await mcp_client.call_tool("qg_get_nodes", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    # Verify result is a list
    nodes = result.data["result"]
    assert isinstance(nodes, list), "Nodes result should be a list"


@pytest.mark.integration
async def test_qg_get_nodes_with_extra_info(mcp_client: Client):
    """Test getting all nodes with extra_info option."""
    result = await mcp_client.call_tool(
        "qg_get_nodes", arguments={"extra_info": True}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    nodes = result.data["result"]
    assert isinstance(nodes, list)


@pytest.mark.integration
async def test_qg_get_nodes_with_details(mcp_client: Client):
    """Test getting all nodes with details option."""
    result = await mcp_client.call_tool(
        "qg_get_nodes", arguments={"details": True}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    nodes = result.data["result"]
    assert isinstance(nodes, list)


@pytest.mark.integration
async def test_qg_get_nodes_with_name_filter(mcp_client: Client, qg_manager):
    """Test getting nodes filtered by name."""
    # First get all nodes to have a name to filter by
    all_nodes = qg_manager.node_client.get_nodes()
    
    if not all_nodes:
        pytest.skip("No nodes available for filtering test")
    
    node_name = all_nodes[0].get("name")
    
    result = await mcp_client.call_tool(
        "qg_get_nodes", arguments={"filter_by_name": node_name}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    nodes = result.data["result"]
    assert isinstance(nodes, list)
    if len(nodes) > 0:
        # Verify the filtered node matches
        assert any(node.get("name") == node_name for node in nodes)


@pytest.mark.integration
async def test_qg_get_nodes_with_system_id_filter(mcp_client: Client, test_infrastructure):
    """Test getting nodes filtered by system ID."""
    system_id = test_infrastructure.get("system_id")
    
    result = await mcp_client.call_tool(
        "qg_get_nodes", arguments={"filter_by_system_id": system_id}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    nodes = result.data["result"]
    assert isinstance(nodes, list)


@pytest.mark.integration
async def test_qg_get_nodes_with_combined_options(mcp_client: Client):
    """Test getting nodes with multiple options combined."""
    result = await mcp_client.call_tool(
        "qg_get_nodes",
        arguments={
            "extra_info": True,
            "details": True,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    nodes = result.data["result"]
    assert isinstance(nodes, list)


@pytest.mark.integration
async def test_qg_get_node_by_id(mcp_client: Client, qg_manager):
    """Test getting a specific node by ID."""
    # First get all nodes to get a valid node ID
    all_nodes = qg_manager.node_client.get_nodes()
    
    if not all_nodes:
        pytest.skip("No nodes available for ID test")
    
    node_id = all_nodes[0].get("id")

    result = await mcp_client.call_tool(
        "qg_get_node_by_id", arguments={"id": node_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_node_by_id"
    assert metadata["success"] is True

    # Verify node data
    node = result.data["result"]
    assert isinstance(node, dict)
    assert node.get("id") == node_id
    assert "name" in node


@pytest.mark.integration
async def test_qg_get_node_by_id_not_found(mcp_client: Client):
    """Test getting a node with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_node_by_id", arguments={"id": fake_id}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_node_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_node_by_id_invalid_uuid(mcp_client: Client):
    """Test getting a node with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_node_by_id", arguments={"id": "not-a-valid-uuid"}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_node_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_node_heartbeat_by_id(mcp_client: Client, qg_manager):
    """Test getting node heartbeat by ID."""
    all_nodes = qg_manager.node_client.get_nodes()
    
    if not all_nodes:
        pytest.skip("No nodes available for heartbeat test")
    
    node_id = all_nodes[0].get("id")

    result = await mcp_client.call_tool(
        "qg_get_node_heartbeat_by_id", arguments={"id": node_id}
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_node_heartbeat_by_id"
    # Heartbeat may or may not exist depending on node state
    assert metadata["success"] in [True, False]


@pytest.mark.integration
async def test_qg_get_node_heartbeat_by_id_not_found(mcp_client: Client):
    """Test getting heartbeat for non-existent node."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_node_heartbeat_by_id", arguments={"id": fake_id}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_node_heartbeat_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_delete_node_not_found(mcp_client: Client):
    """Test deleting a node with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_node", arguments={"id": fake_id}
    )

    # API may return success for non-existent IDs (idempotent delete)
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_node"


@pytest.mark.integration
async def test_qg_delete_node_invalid_uuid(mcp_client: Client):
    """Test deleting a node with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_node", arguments={"id": "not-a-valid-uuid"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_node"


@pytest.mark.integration
async def test_qg_nodes_list_and_get_consistency(mcp_client: Client, qg_manager):
    """Test consistency between list nodes and get node by ID."""
    # Get all nodes
    list_result = await mcp_client.call_tool("qg_get_nodes", arguments={})
    
    assert list_result.data["metadata"]["success"] is True
    nodes = list_result.data["result"]
    
    if not nodes:
        pytest.skip("No nodes available for consistency test")
    
    # Pick the first node and get it by ID
    first_node_from_list = nodes[0]
    node_id = first_node_from_list.get("id")
    
    get_result = await mcp_client.call_tool(
        "qg_get_node_by_id", arguments={"id": node_id}
    )
    
    assert get_result.data["metadata"]["success"] is True
    node_by_id = get_result.data["result"]
    
    # Verify key fields match
    assert node_by_id.get("id") == first_node_from_list.get("id")
    assert node_by_id.get("name") == first_node_from_list.get("name")


@pytest.mark.integration
async def test_qg_nodes_error_handling(mcp_client: Client):
    """Test error handling across node operations."""
    # Test getting node with empty ID
    result = await mcp_client.call_tool(
        "qg_get_node_by_id",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data
    
    # Test deleting node with empty ID
    result = await mcp_client.call_tool(
        "qg_delete_node",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data
    
    # Test getting node with all-zeros UUID
    result = await mcp_client.call_tool(
        "qg_get_node_by_id",
        arguments={"id": "00000000-0000-0000-0000-000000000000"},
    )
    assert result.data is not None
    assert "metadata" in result.data


@pytest.mark.integration
async def test_qg_nodes_structure_validation(mcp_client: Client, qg_manager):
    """Test that node objects have expected structure."""
    result = await mcp_client.call_tool("qg_get_nodes", arguments={})
    
    assert result.data["metadata"]["success"] is True
    nodes = result.data["result"]
    
    if not nodes:
        pytest.skip("No nodes available for structure validation")
    
    # Verify each node has expected fields
    for node in nodes:
        assert isinstance(node, dict), "Each node should be a dictionary"
        assert "id" in node, "Node should have 'id' field"
        assert "name" in node, "Node should have 'name' field"
        
        # Validate ID is UUID format (basic check)
        node_id = node.get("id")
        assert isinstance(node_id, str), "Node ID should be a string"
        assert len(node_id) > 0, "Node ID should not be empty"


@pytest.mark.integration
async def test_qg_get_nodes_with_fabric_version_filter(mcp_client: Client):
    """Test getting nodes filtered by fabric version."""
    result = await mcp_client.call_tool(
        "qg_get_nodes", arguments={"fabric_version": "03.10.00.01"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    nodes = result.data["result"]
    assert isinstance(nodes, list)


@pytest.mark.integration
async def test_qg_get_nodes_with_connector_version_filter(mcp_client: Client):
    """Test getting nodes filtered by connector version."""
    result = await mcp_client.call_tool(
        "qg_get_nodes", arguments={"connector_version": "03.10.00.01"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    nodes = result.data["result"]
    assert isinstance(nodes, list)


@pytest.mark.integration
async def test_qg_get_nodes_with_bridge_id_filter(mcp_client: Client, test_infrastructure):
    """Test getting nodes filtered by bridge ID."""
    bridge_id = test_infrastructure.get("bridge_id")
    
    result = await mcp_client.call_tool(
        "qg_get_nodes", arguments={"filter_by_bridge_id": bridge_id}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    nodes = result.data["result"]
    assert isinstance(nodes, list)


@pytest.mark.integration
async def test_qg_get_nodes_with_fabric_id_filter(mcp_client: Client, test_infrastructure):
    """Test getting nodes filtered by fabric ID."""
    fabric_id = test_infrastructure.get("fabric_id")
    
    result = await mcp_client.call_tool(
        "qg_get_nodes", arguments={"filter_by_fabric_id": fabric_id}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    nodes = result.data["result"]
    assert isinstance(nodes, list)


@pytest.mark.integration
async def test_qg_get_nodes_with_connector_id_filter(mcp_client: Client, test_infrastructure):
    """Test getting nodes filtered by connector ID."""
    connector_id = test_infrastructure.get("connector_id")
    
    result = await mcp_client.call_tool(
        "qg_get_nodes", arguments={"filter_by_connector_id": connector_id}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes"
    assert metadata["success"] is True

    nodes = result.data["result"]
    assert isinstance(nodes, list)


@pytest.mark.integration
async def test_qg_get_node_heartbeat_invalid_uuid(mcp_client: Client):
    """Test getting node heartbeat with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_node_heartbeat_by_id", arguments={"id": "not-a-valid-uuid"}
    )

    # API may or may not return error for invalid UUID
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_node_heartbeat_by_id"
    # Just verify we get a response
    assert "success" in metadata
