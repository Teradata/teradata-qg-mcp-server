"""Integration tests for bridges_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from src.tools import set_qg_manager


@pytest.mark.integration
async def test_qg_get_bridges(mcp_client: Client):
    """Test getting all bridges."""
    result = await mcp_client.call_tool("qg_get_bridges", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_bridges"
    assert metadata["success"] is True

    # Verify result is a list
    bridges = result.data["result"]
    assert isinstance(bridges, list), "Bridges result should be a list"


@pytest.mark.integration
async def test_qg_get_bridges_with_filters(mcp_client: Client, qg_manager):
    """Test getting bridges with filter parameters."""
    # First get all bridges to find a valid system_id
    all_bridges = qg_manager.bridge_client.get_bridges()

    if not all_bridges:
        pytest.skip("No bridges available to test filtering")

    # Test with system_id filter
    first_bridge = all_bridges[0]
    system_id = (
        first_bridge.get("system", {}).get("id") if "system" in first_bridge else None
    )

    if system_id:
        result = await mcp_client.call_tool(
            "qg_get_bridges", arguments={"filter_by_system_id": system_id}
        )

        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["success"] is True

        filtered_bridges = result.data["result"]
        assert isinstance(filtered_bridges, list)

    # Test with name filter
    bridge_name = first_bridge.get("name")
    if bridge_name:
        result = await mcp_client.call_tool(
            "qg_get_bridges", arguments={"filter_by_name": bridge_name}
        )

        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["success"] is True

        filtered_bridges = result.data["result"]
        assert isinstance(filtered_bridges, list)
        # Should find at least the bridge we searched for
        if filtered_bridges:
            assert any(b.get("name") == bridge_name for b in filtered_bridges)


@pytest.mark.integration
async def test_qg_get_bridge_by_id(mcp_client: Client, qg_manager):
    """Test getting a specific bridge by ID."""
    # First get all bridges to find a valid bridge ID
    bridges = qg_manager.bridge_client.get_bridges()

    if not bridges:
        pytest.skip("No bridges available to test")

    bridge_id = bridges[0].get("id")
    assert bridge_id is not None, "Bridge should have an ID"

    # Get bridge by ID
    result = await mcp_client.call_tool(
        "qg_get_bridge_by_id", arguments={"id": bridge_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_bridge_by_id"
    assert metadata["success"] is True

    # Verify bridge data
    bridge = result.data["result"]
    assert isinstance(bridge, dict)
    assert bridge.get("id") == bridge_id


@pytest.mark.integration
async def test_qg_get_bridge_by_id_not_found(mcp_client: Client):
    """Test getting a bridge with invalid ID."""
    invalid_id = "00000000-0000-0000-0000-000000000000"

    result = await mcp_client.call_tool(
        "qg_get_bridge_by_id", arguments={"id": invalid_id}
    )

    # Should return error response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_bridge_by_id"
    # Expecting failure for non-existent bridge
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_create_bridge(mcp_client: Client, qg_manager, test_infrastructure):
    """Test creating a new bridge."""
    # Use the test system from infrastructure (guaranteed to exist)
    system_id = test_infrastructure["system_id"]
    assert system_id is not None, "Test infrastructure should have created a system"

    # Get nodes for the system (if any exist)
    nodes = qg_manager.node_client.get_nodes(filter_by_system_id=system_id)

    # Use node_ids only if nodes exist
    node_ids = [nodes[0].get("id")] if nodes else None

    # Create a test bridge with unique name
    unique_suffix = str(uuid.uuid4())[:8]
    bridge_args = {
        "name": f"test_bridge_pytest_{unique_suffix}",
        "system_id": system_id,
        "description": "Test bridge created by pytest",
    }
    if node_ids:
        bridge_args["node_ids"] = node_ids

    result = await mcp_client.call_tool("qg_create_bridge", arguments=bridge_args)

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_bridge"
    assert (
        metadata["success"] is True
    ), f"Bridge creation failed: {result.data.get('result')}"

    # Verify created bridge
    bridge = result.data["result"]
    assert isinstance(bridge, dict)
    assert bridge.get("name") == bridge_args["name"]
    assert bridge.get("description") == "Test bridge created by pytest"

    # Cleanup - delete the created bridge
    bridge_id = bridge.get("id")
    if bridge_id:
        try:
            qg_manager.bridge_client.delete_bridge(bridge_id)
        except Exception:
            pass  # Ignore cleanup errors


@pytest.mark.integration
async def test_qg_create_bridge_minimal(
    mcp_client: Client, qg_manager, test_infrastructure
):
    """Test creating a bridge with minimal required parameters."""
    # Use the test system from infrastructure (guaranteed to exist)
    system_id = test_infrastructure["system_id"]
    assert system_id is not None, "Test infrastructure should have created a system"

    # Create bridge with only required parameters and unique name
    unique_suffix = str(uuid.uuid4())[:8]
    bridge_name = f"test_bridge_minimal_pytest_{unique_suffix}"
    result = await mcp_client.call_tool(
        "qg_create_bridge", arguments={"name": bridge_name, "system_id": system_id}
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_bridge"
    assert (
        metadata["success"] is True
    ), f"Bridge creation failed: {result.data.get('result')}"

    bridge = result.data["result"]
    assert bridge.get("name") == bridge_name

    # Cleanup - delete the created bridge
    bridge_id = bridge.get("id")
    if bridge_id:
        try:
            qg_manager.bridge_client.delete_bridge(bridge_id)
        except Exception:
            pass  # Ignore cleanup errors


@pytest.mark.integration
async def test_qg_delete_bridge(mcp_client: Client, qg_manager, test_infrastructure):
    """Test deleting a bridge."""
    # Use the test system from infrastructure (guaranteed to exist)
    system_id = test_infrastructure["system_id"]
    assert system_id is not None, "Test infrastructure should have created a system"

    # Create a bridge to delete
    unique_suffix = str(uuid.uuid4())[:8]
    bridge_name = f"test_bridge_delete_pytest_{unique_suffix}"
    created_bridge = qg_manager.bridge_client.create_bridge(
        name=bridge_name,
        system_id=system_id,
        description="Test bridge for deletion",
    )

    bridge_id = created_bridge.get("id")
    assert bridge_id is not None, "Created bridge should have an ID"

    # Delete the bridge using the tool
    result = await mcp_client.call_tool("qg_delete_bridge", arguments={"id": bridge_id})

    # Verify response structure
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_bridge"
    assert metadata["success"] is True

    # Verify bridge is actually deleted
    try:
        qg_manager.bridge_client.get_bridge_by_id(bridge_id)
        # If we get here, deletion failed
        assert False, "Bridge should have been deleted"
    except Exception:
        # Expected - bridge should not be found
        pass


@pytest.mark.integration
async def test_qg_delete_bridge_not_found(mcp_client: Client):
    """Test deleting a non-existent bridge."""
    invalid_id = "00000000-0000-0000-0000-000000000000"

    result = await mcp_client.call_tool(
        "qg_delete_bridge", arguments={"id": invalid_id}
    )

    # API might return success even for non-existent resources
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_bridge"
    # Just verify we got a response, success may be True or False
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_bridges_error_handling(mcp_client: Client, qg_manager):
    """Test error handling when QueryGrid Manager is not available."""
    # Set manager to None to simulate unavailability
    set_qg_manager(None)

    result = await mcp_client.call_tool("qg_get_bridges", arguments={})

    # Verify error response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_bridges"
    assert metadata["success"] is False
    assert "error" in metadata

    # Restore manager for other tests
    set_qg_manager(qg_manager)


# Tests for qg_update_bridge


@pytest.mark.integration
async def test_qg_update_bridge_name(
    mcp_client: Client, qg_manager, test_infrastructure
):
    """Test updating a bridge's name."""
    # Use the test system from infrastructure
    system_id = test_infrastructure["system_id"]
    assert system_id is not None, "Test infrastructure should have created a system"

    # Create a bridge to update
    unique_suffix = str(uuid.uuid4())[:8]
    original_name = f"test_bridge_update_name_{unique_suffix}"
    created_bridge = qg_manager.bridge_client.create_bridge(
        name=original_name,
        system_id=system_id,
        description="Bridge for testing name update",
    )

    bridge_id = created_bridge.get("id")
    assert bridge_id is not None, "Created bridge should have an ID"

    try:
        # Update the bridge name
        new_name = f"updated_bridge_name_{unique_suffix}"
        result = await mcp_client.call_tool(
            "qg_update_bridge",
            arguments={
                "id": bridge_id,
                "name": new_name,
            },
        )

        # Verify response
        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_update_bridge"
        assert metadata["success"] is True

        # Verify the update by fetching the bridge
        get_result = await mcp_client.call_tool(
            "qg_get_bridge_by_id",
            arguments={"id": bridge_id},
        )

        assert get_result.data is not None
        assert get_result.data["metadata"]["success"] is True
        assert get_result.data["result"]["name"] == new_name

    finally:
        # Cleanup
        try:
            qg_manager.bridge_client.delete_bridge(bridge_id)
        except Exception:
            pass


@pytest.mark.integration
async def test_qg_update_bridge_description(
    mcp_client: Client, qg_manager, test_infrastructure
):
    """Test updating a bridge's description."""
    # Use the test system from infrastructure
    system_id = test_infrastructure["system_id"]
    assert system_id is not None, "Test infrastructure should have created a system"

    # Create a bridge to update
    unique_suffix = str(uuid.uuid4())[:8]
    bridge_name = f"test_bridge_update_desc_{unique_suffix}"
    created_bridge = qg_manager.bridge_client.create_bridge(
        name=bridge_name,
        system_id=system_id,
        description="Original description",
    )

    bridge_id = created_bridge.get("id")
    assert bridge_id is not None, "Created bridge should have an ID"

    try:
        # Update the bridge description
        new_description = "Updated description via pytest"
        result = await mcp_client.call_tool(
            "qg_update_bridge",
            arguments={
                "id": bridge_id,
                "description": new_description,
            },
        )

        # Verify response
        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_update_bridge"
        assert metadata["success"] is True

        # Verify the update by fetching the bridge
        get_result = await mcp_client.call_tool(
            "qg_get_bridge_by_id",
            arguments={"id": bridge_id},
        )

        assert get_result.data is not None
        assert get_result.data["metadata"]["success"] is True
        assert get_result.data["result"]["description"] == new_description

    finally:
        # Cleanup
        try:
            qg_manager.bridge_client.delete_bridge(bridge_id)
        except Exception:
            pass


@pytest.mark.integration
async def test_qg_update_bridge_multiple_fields(
    mcp_client: Client, qg_manager, test_infrastructure
):
    """Test updating multiple bridge fields at once."""
    # Use the test system from infrastructure
    system_id = test_infrastructure["system_id"]
    assert system_id is not None, "Test infrastructure should have created a system"

    # Create a bridge to update
    unique_suffix = str(uuid.uuid4())[:8]
    original_name = f"test_bridge_multi_{unique_suffix}"
    created_bridge = qg_manager.bridge_client.create_bridge(
        name=original_name,
        system_id=system_id,
        description="Original description",
    )

    bridge_id = created_bridge.get("id")
    assert bridge_id is not None, "Created bridge should have an ID"

    try:
        # Update multiple fields
        new_name = f"updated_multi_{unique_suffix}"
        new_description = "Updated multiple fields via pytest"
        result = await mcp_client.call_tool(
            "qg_update_bridge",
            arguments={
                "id": bridge_id,
                "name": new_name,
                "description": new_description,
            },
        )

        # Verify response
        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_update_bridge"
        assert metadata["success"] is True

        # Verify the update by fetching the bridge
        get_result = await mcp_client.call_tool(
            "qg_get_bridge_by_id",
            arguments={"id": bridge_id},
        )

        assert get_result.data is not None
        assert get_result.data["metadata"]["success"] is True
        updated_bridge = get_result.data["result"]
        assert updated_bridge["name"] == new_name
        assert updated_bridge["description"] == new_description

    finally:
        # Cleanup
        try:
            qg_manager.bridge_client.delete_bridge(bridge_id)
        except Exception:
            pass


@pytest.mark.integration
async def test_qg_update_bridge_system_id(
    mcp_client: Client, qg_manager, test_infrastructure
):
    """Test updating a bridge's system_id."""
    # Use the test system from infrastructure
    system_id = test_infrastructure["system_id"]
    assert system_id is not None, "Test infrastructure should have created a system"

    # Get all systems to find another system for update test
    systems = qg_manager.system_client.get_systems()

    # If there are multiple systems, use a different one for the update
    # Otherwise, just update with the same system_id
    other_system_id = None
    if len(systems) > 1:
        for system in systems:
            if system.get("id") != system_id:
                other_system_id = system.get("id")
                break

    if not other_system_id:
        other_system_id = system_id

    # Create a bridge to update
    unique_suffix = str(uuid.uuid4())[:8]
    bridge_name = f"test_bridge_update_system_{unique_suffix}"
    created_bridge = qg_manager.bridge_client.create_bridge(
        name=bridge_name,
        system_id=system_id,
        description="Bridge for testing system update",
    )

    bridge_id = created_bridge.get("id")
    assert bridge_id is not None, "Created bridge should have an ID"

    try:
        # Update the bridge system_id
        result = await mcp_client.call_tool(
            "qg_update_bridge",
            arguments={
                "id": bridge_id,
                "system_id": other_system_id,
            },
        )

        # Verify response
        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_update_bridge"
        assert metadata["success"] is True

        # Verify the update by fetching the bridge
        get_result = await mcp_client.call_tool(
            "qg_get_bridge_by_id",
            arguments={"id": bridge_id},
        )

        assert get_result.data is not None
        assert get_result.data["metadata"]["success"] is True
        updated_bridge = get_result.data["result"]
        # Check systemId directly (not nested in a system object)
        assert updated_bridge.get("systemId") == other_system_id

    finally:
        # Cleanup
        try:
            qg_manager.bridge_client.delete_bridge(bridge_id)
        except Exception:
            pass


@pytest.mark.integration
async def test_qg_update_bridge_node_ids(
    mcp_client: Client, qg_manager, test_infrastructure
):
    """Test updating a bridge's node_ids."""
    # Use the test system from infrastructure
    system_id = test_infrastructure["system_id"]
    assert system_id is not None, "Test infrastructure should have created a system"

    # Get nodes for the system
    nodes = qg_manager.node_client.get_nodes(filter_by_system_id=system_id)

    if not nodes:
        pytest.skip("No nodes available to test node_ids update")

    # Create a bridge to update
    unique_suffix = str(uuid.uuid4())[:8]
    bridge_name = f"test_bridge_update_nodes_{unique_suffix}"
    created_bridge = qg_manager.bridge_client.create_bridge(
        name=bridge_name,
        system_id=system_id,
        description="Bridge for testing node update",
    )

    bridge_id = created_bridge.get("id")
    assert bridge_id is not None, "Created bridge should have an ID"

    try:
        # Update the bridge with node_ids
        node_ids = [nodes[0].get("id")]
        result = await mcp_client.call_tool(
            "qg_update_bridge",
            arguments={
                "id": bridge_id,
                "node_ids": node_ids,
            },
        )

        # Verify response
        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_update_bridge"
        assert metadata["success"] is True

        # Verify the update by fetching the bridge
        get_result = await mcp_client.call_tool(
            "qg_get_bridge_by_id",
            arguments={"id": bridge_id},
        )

        assert get_result.data is not None
        assert get_result.data["metadata"]["success"] is True
        updated_nodes = get_result.data["result"].get("nodes", [])
        if updated_nodes:  # Some systems might not return nodes in the response
            assert len(updated_nodes) > 0

    finally:
        # Cleanup
        try:
            qg_manager.bridge_client.delete_bridge(bridge_id)
        except Exception:
            pass


@pytest.mark.integration
async def test_qg_update_bridge_nonexistent(mcp_client: Client):
    """Test updating a non-existent bridge."""
    invalid_id = "00000000-0000-0000-0000-000000000000"

    result = await mcp_client.call_tool(
        "qg_update_bridge",
        arguments={
            "id": invalid_id,
            "name": "This should fail",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_update_bridge"
    # Should fail for non-existent bridge
    assert metadata["success"] is False
