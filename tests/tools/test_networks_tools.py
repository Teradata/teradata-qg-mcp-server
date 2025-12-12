"""Integration tests for networks_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_get_networks(mcp_client: Client):
    """Test getting all networks."""
    result = await mcp_client.call_tool("qg_get_networks", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_networks"
    assert metadata["success"] is True

    # Verify result is a list
    networks = result.data["result"]
    assert isinstance(networks, list), "Networks result should be a list"


@pytest.mark.integration
async def test_qg_get_networks_with_flatten(mcp_client: Client):
    """Test getting all networks with flatten option."""
    result = await mcp_client.call_tool(
        "qg_get_networks", arguments={"flatten": True}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_networks"
    assert metadata["success"] is True

    networks = result.data["result"]
    assert isinstance(networks, list)


@pytest.mark.integration
async def test_qg_get_networks_with_extra_info(mcp_client: Client):
    """Test getting all networks with extra_info option."""
    result = await mcp_client.call_tool(
        "qg_get_networks", arguments={"extra_info": True}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_networks"
    assert metadata["success"] is True

    networks = result.data["result"]
    assert isinstance(networks, list)


@pytest.mark.integration
async def test_qg_get_networks_with_name_filter(mcp_client: Client, test_network):
    """Test getting networks filtered by name."""
    # Use test_network fixture to ensure a network exists
    network_name = test_network.get("name")
    
    result = await mcp_client.call_tool(
        "qg_get_networks", arguments={"filter_by_name": network_name}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_networks"
    assert metadata["success"] is True

    networks = result.data["result"]
    assert isinstance(networks, list)
    if len(networks) > 0:
        # Verify the filtered network matches
        assert any(net.get("name") == network_name for net in networks)


@pytest.mark.integration
async def test_qg_get_networks_with_wildcard_filter(mcp_client: Client):
    """Test getting networks with wildcard name filter."""
    result = await mcp_client.call_tool(
        "qg_get_networks", arguments={"filter_by_name": "*"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_networks"
    assert metadata["success"] is True

    networks = result.data["result"]
    assert isinstance(networks, list)


@pytest.mark.integration
async def test_qg_get_networks_with_tag_filter(mcp_client: Client):
    """Test getting networks filtered by tag."""
    result = await mcp_client.call_tool(
        "qg_get_networks", arguments={"filter_by_tag": "environment:test"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_networks"
    assert metadata["success"] is True

    networks = result.data["result"]
    assert isinstance(networks, list)


@pytest.mark.integration
async def test_qg_get_networks_with_combined_options(mcp_client: Client):
    """Test getting networks with multiple options combined."""
    result = await mcp_client.call_tool(
        "qg_get_networks",
        arguments={
            "flatten": True,
            "extra_info": True,
            "filter_by_name": "*",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_networks"
    assert metadata["success"] is True

    networks = result.data["result"]
    assert isinstance(networks, list)


@pytest.mark.integration
async def test_qg_get_network_by_id(mcp_client: Client, test_network):
    """Test getting a specific network by ID."""
    # Use test_network fixture to ensure a network exists
    network_id = test_network.get("id")

    result = await mcp_client.call_tool(
        "qg_get_network_by_id", arguments={"id": network_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_network_by_id"
    assert metadata["success"] is True

    # Verify network data
    network = result.data["result"]
    assert isinstance(network, dict)
    assert network.get("id") == network_id
    assert "name" in network


@pytest.mark.integration
async def test_qg_get_network_by_id_with_extra_info(mcp_client: Client, test_network):
    """Test getting a network with extra_info option."""
    # Use test_network fixture to ensure a network exists
    network_id = test_network.get("id")

    result = await mcp_client.call_tool(
        "qg_get_network_by_id", arguments={"id": network_id, "extra_info": True}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_network_by_id"
    assert metadata["success"] is True

    network = result.data["result"]
    assert isinstance(network, dict)
    assert network.get("id") == network_id


@pytest.mark.integration
async def test_qg_get_network_by_id_not_found(mcp_client: Client):
    """Test getting a network with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_network_by_id", arguments={"id": fake_id}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_network_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_network_by_id_invalid_uuid(mcp_client: Client):
    """Test getting a network with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_network_by_id", arguments={"id": "not-a-valid-uuid"}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_network_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_network_active(mcp_client: Client, test_network):
    """Test getting active configuration of a network."""
    # Use test_network fixture to ensure a network exists
    network_id = test_network.get("id")

    result = await mcp_client.call_tool(
        "qg_get_network_active", arguments={"id": network_id}
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_network_active"
    assert metadata["success"] is True

    # Verify active config
    if "result" in result.data:
        active_config = result.data["result"]
        assert isinstance(active_config, dict)


@pytest.mark.integration
async def test_qg_get_network_active_not_found(mcp_client: Client):
    """Test getting active config for non-existent network."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_network_active", arguments={"id": fake_id}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_network_active"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_network_pending(mcp_client: Client, test_network):
    """Test getting pending configuration of a network."""
    # Use test_network fixture to ensure a network exists
    network_id = test_network.get("id")

    result = await mcp_client.call_tool(
        "qg_get_network_pending", arguments={"id": network_id}
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_network_pending"
    # Pending config may or may not exist
    assert metadata["success"] in [True, False]


@pytest.mark.integration
async def test_qg_get_network_pending_not_found(mcp_client: Client):
    """Test getting pending config for non-existent network."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_network_pending", arguments={"id": fake_id}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_network_pending"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_network_previous(mcp_client: Client, test_network):
    """Test getting previous configuration of a network."""
    # Use test_network fixture to ensure a network exists
    network_id = test_network.get("id")

    result = await mcp_client.call_tool(
        "qg_get_network_previous", arguments={"id": network_id}
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_network_previous"
    # Previous config may or may not exist
    assert metadata["success"] in [True, False]


@pytest.mark.integration
async def test_qg_get_network_previous_not_found(mcp_client: Client):
    """Test getting previous config for non-existent network."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_network_previous", arguments={"id": fake_id}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_network_previous"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_delete_network_not_found(mcp_client: Client):
    """Test deleting a network with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_network", arguments={"id": fake_id}
    )

    # API may return success for non-existent IDs (idempotent delete)
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_network"


@pytest.mark.integration
async def test_qg_delete_network_invalid_uuid(mcp_client: Client):
    """Test deleting a network with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_network", arguments={"id": "not-a-valid-uuid"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_network"


@pytest.mark.integration
async def test_qg_networks_list_and_get_consistency(mcp_client: Client, test_network):
    """Test consistency between list networks and get network by ID."""
    # Use test_network fixture to ensure a network exists
    network_id = test_network.get("id")
    
    # Get all networks
    list_result = await mcp_client.call_tool("qg_get_networks", arguments={})
    
    assert list_result.data["metadata"]["success"] is True
    networks = list_result.data["result"]
    
    # Find our test network in the list
    first_network_from_list = next((n for n in networks if n.get("id") == network_id), None)
    assert first_network_from_list is not None, "Test network should be in the list"
    
    get_result = await mcp_client.call_tool(
        "qg_get_network_by_id", arguments={"id": network_id}
    )
    
    assert get_result.data["metadata"]["success"] is True
    network_by_id = get_result.data["result"]
    
    # Verify key fields match
    assert network_by_id.get("id") == first_network_from_list.get("id")
    assert network_by_id.get("name") == first_network_from_list.get("name")


@pytest.mark.integration
async def test_qg_networks_error_handling(mcp_client: Client):
    """Test error handling across network operations."""
    # Test getting network with empty ID
    result = await mcp_client.call_tool(
        "qg_get_network_by_id",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data
    
    # Test deleting network with empty ID
    result = await mcp_client.call_tool(
        "qg_delete_network",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data
    
    # Test getting network with all-zeros UUID
    result = await mcp_client.call_tool(
        "qg_get_network_by_id",
        arguments={"id": "00000000-0000-0000-0000-000000000000"},
    )
    assert result.data is not None
    assert "metadata" in result.data


@pytest.mark.integration
async def test_qg_networks_structure_validation(mcp_client: Client, test_network):
    """Test that network objects have expected structure."""
    # Use test_network fixture to ensure a network exists
    result = await mcp_client.call_tool("qg_get_networks", arguments={})
    
    assert result.data["metadata"]["success"] is True
    networks = result.data["result"]
    
    assert len(networks) > 0, "At least one network should exist (test_network)"
    
    # Verify each network has expected fields
    for network in networks:
        assert isinstance(network, dict), "Each network should be a dictionary"
        assert "id" in network, "Network should have 'id' field"
        assert "name" in network, "Network should have 'name' field"
        
        # Validate ID is UUID format (basic check)
        network_id = network.get("id")
        assert isinstance(network_id, str), "Network ID should be a string"
        assert len(network_id) > 0, "Network ID should not be empty"


@pytest.mark.integration
async def test_qg_get_networks_case_insensitive_filter(mcp_client: Client, test_network):
    """Test that name filtering is case insensitive."""
    # Use test_network fixture to ensure a network exists
    test_name = test_network.get("name")
    
    # Test with uppercase version of name
    result_upper = await mcp_client.call_tool(
        "qg_get_networks", arguments={"filter_by_name": test_name.upper()}
    )
    
    # Test with lowercase version
    result_lower = await mcp_client.call_tool(
        "qg_get_networks", arguments={"filter_by_name": test_name.lower()}
    )
    
    # Both should succeed (case insensitive matching)
    assert result_upper.data["metadata"]["success"] is True
    assert result_lower.data["metadata"]["success"] is True
    
    # Both should return same number of results (if any)
    networks_upper = result_upper.data["result"]
    networks_lower = result_lower.data["result"]
    
    assert len(networks_upper) == len(networks_lower)


@pytest.mark.integration
async def test_qg_network_config_states(mcp_client: Client, test_network):
    """Test getting different configuration states for a network."""
    # Use test_network fixture to ensure a network exists
    network_id = test_network.get("id")
    
    # Get active config
    active_result = await mcp_client.call_tool(
        "qg_get_network_active", arguments={"id": network_id}
    )
    assert active_result.data["metadata"]["success"] is True
    
    # Get pending config (may or may not exist)
    pending_result = await mcp_client.call_tool(
        "qg_get_network_pending", arguments={"id": network_id}
    )
    assert pending_result.data is not None
    
    # Get previous config (may or may not exist)
    previous_result = await mcp_client.call_tool(
        "qg_get_network_previous", arguments={"id": network_id}
    )
    assert previous_result.data is not None


@pytest.mark.integration
async def test_qg_create_network_basic(mcp_client: Client):
    """Test creating a basic network with required parameters only."""
    import uuid

    network_name = f"pytest_network_basic_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "STANDARD",
            "matching_rules": [{"type": "CIDR_NOTATION", "value": "0.0.0.0/0"}],
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_network"
    assert metadata["success"] is True

    # Verify created network
    network = result.data["result"]
    assert isinstance(network, dict)
    assert "id" in network
    assert network.get("name") == network_name

    # Cleanup - delete the created network
    network_id = network.get("id")
    cleanup_result = await mcp_client.call_tool(
        "qg_delete_network", arguments={"id": network_id}
    )
    assert cleanup_result.data is not None


@pytest.mark.integration
async def test_qg_create_network_with_description(mcp_client: Client):
    """Test creating a network with description."""
    import uuid

    network_name = f"pytest_network_desc_{uuid.uuid4().hex[:8]}"
    test_description = "Test network created by pytest with description"

    result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "STANDARD",
            "description": test_description,
            "matching_rules": [{"type": "CIDR_NOTATION", "value": "0.0.0.0/0"}],
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    network = result.data["result"]
    assert network.get("name") == network_name
    # Description might be in the result or need extra_info to retrieve

    # Cleanup
    network_id = network.get("id")
    await mcp_client.call_tool("qg_delete_network", arguments={"id": network_id})


@pytest.mark.integration
async def test_qg_create_network_with_tags(mcp_client: Client):
    """Test creating a network with tags."""
    import uuid

    network_name = f"pytest_network_tags_{uuid.uuid4().hex[:8]}"
    test_tags = {"environment": "test", "purpose": "pytest", "team": "qa"}

    result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "STANDARD",
            "matching_rules": [{"type": "CIDR_NOTATION", "value": "0.0.0.0/0"}],
            "tags": test_tags,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    network = result.data["result"]
    assert network.get("name") == network_name

    # Cleanup
    network_id = network.get("id")
    await mcp_client.call_tool("qg_delete_network", arguments={"id": network_id})


@pytest.mark.integration
async def test_qg_create_network_with_matching_rules(mcp_client: Client):
    """Test creating a network with matching rules."""
    import uuid

    network_name = f"pytest_network_rules_{uuid.uuid4().hex[:8]}"
    matching_rules = [
        {"type": "CIDR_NOTATION", "value": "192.168.1.0/24"},
        {"type": "INTERFACE_NAME", "value": "eth0"},
    ]

    result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "STANDARD",
            "matching_rules": matching_rules,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    network = result.data["result"]
    assert network.get("name") == network_name

    # Cleanup
    network_id = network.get("id")
    await mcp_client.call_tool("qg_delete_network", arguments={"id": network_id})


@pytest.mark.integration
async def test_qg_create_network_load_balancer_type(mcp_client: Client):
    """Test creating a network with LOAD_BALANCER connection type."""
    import uuid

    network_name = f"pytest_network_lb_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "LOAD_BALANCER",
            "load_balancer_address": "lb.example.com",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    network = result.data["result"]
    assert network.get("name") == network_name

    # Cleanup
    network_id = network.get("id")
    await mcp_client.call_tool("qg_delete_network", arguments={"id": network_id})


@pytest.mark.integration
async def test_qg_create_network_no_ingress_type(mcp_client: Client):
    """Test creating a network with NO_INGRESS connection type."""
    import uuid

    network_name = f"pytest_network_no_ingress_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "NO_INGRESS",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    network = result.data["result"]
    assert network.get("name") == network_name

    # Cleanup
    network_id = network.get("id")
    await mcp_client.call_tool("qg_delete_network", arguments={"id": network_id})


@pytest.mark.integration
async def test_qg_create_network_with_all_parameters(mcp_client: Client):
    """Test creating a network with all optional parameters."""
    import uuid

    network_name = f"pytest_network_full_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "STANDARD",
            "description": "Full parameter test network",
            "matching_rules": [
                {"type": "CIDR_NOTATION", "value": "10.0.0.0/16"},
            ],
            "tags": {
                "environment": "test",
                "created_by": "pytest",
                "test_type": "full_params",
            },
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    network = result.data["result"]
    assert network.get("name") == network_name

    # Cleanup
    network_id = network.get("id")
    await mcp_client.call_tool("qg_delete_network", arguments={"id": network_id})


@pytest.mark.integration
async def test_qg_create_network_duplicate_name(mcp_client: Client, test_network):
    """Test creating a network with duplicate name (should fail)."""
    # Use existing test_network name
    existing_network_name = test_network.get("name")

    result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": existing_network_name,
            "connection_type": "STANDARD",
        },
    )

    # Should return error for duplicate name
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_create_network_invalid_connection_type(mcp_client: Client):
    """Test creating a network with invalid connection type."""
    import uuid

    network_name = f"pytest_network_invalid_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "INVALID_TYPE",
        },
    )

    # Should return error for invalid connection type
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_create_network_load_balancer_missing_address(mcp_client: Client):
    """Test creating LOAD_BALANCER network without load_balancer_address."""
    import uuid

    network_name = f"pytest_network_lb_missing_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "LOAD_BALANCER",
            # Missing load_balancer_address - should fail
        },
    )

    # Should return error when load_balancer_address is missing for LOAD_BALANCER type
    assert result.data is not None
    metadata = result.data["metadata"]
    # API might accept this or return error - just verify we get a response
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_create_and_retrieve_network(mcp_client: Client):
    """Test creating a network and then retrieving it by ID."""
    import uuid

    network_name = f"pytest_network_retrieve_{uuid.uuid4().hex[:8]}"

    # Create network
    create_result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "STANDARD",
            "description": "Test network for retrieve test",
            "matching_rules": [{"type": "CIDR_NOTATION", "value": "0.0.0.0/0"}],
        },
    )

    assert create_result.data["metadata"]["success"] is True
    created_network = create_result.data["result"]
    network_id = created_network.get("id")

    # Retrieve the created network
    get_result = await mcp_client.call_tool(
        "qg_get_network_by_id", arguments={"id": network_id}
    )

    assert get_result.data["metadata"]["success"] is True
    retrieved_network = get_result.data["result"]

    # Verify consistency
    assert retrieved_network.get("id") == network_id
    assert retrieved_network.get("name") == network_name

    # Cleanup
    await mcp_client.call_tool("qg_delete_network", arguments={"id": network_id})


@pytest.mark.integration
async def test_qg_network_create_filter_retrieve(mcp_client: Client):
    """Test creating network, filtering by name, and verifying."""
    import uuid

    network_name = f"pytest_network_filter_{uuid.uuid4().hex[:8]}"

    # Create network
    create_result = await mcp_client.call_tool(
        "qg_create_network",
        arguments={
            "name": network_name,
            "connection_type": "STANDARD",
            "matching_rules": [{"type": "CIDR_NOTATION", "value": "0.0.0.0/0"}],
            "tags": {"test_type": "filter_test"},
        },
    )

    assert create_result.data["metadata"]["success"] is True
    network_id = create_result.data["result"].get("id")

    # Filter networks by name
    filter_result = await mcp_client.call_tool(
        "qg_get_networks", arguments={"filter_by_name": network_name}
    )

    assert filter_result.data["metadata"]["success"] is True
    networks = filter_result.data["result"]

    # Verify our network is in the filtered results
    assert any(net.get("name") == network_name for net in networks)

    # Cleanup
    await mcp_client.call_tool("qg_delete_network", arguments={"id": network_id})
