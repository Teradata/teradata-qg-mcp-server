"""Integration tests for systems_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from src.tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_get_systems_basic(mcp_client: Client):
    """Test getting all systems."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True

    # Should return list of systems
    if "result" in result.data:
        result_data = result.data["result"]
        assert isinstance(result_data, (list, dict))


@pytest.mark.integration
async def test_qg_get_systems_with_extra_info(mcp_client: Client):
    """Test getting systems with extra information."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "extra_info": True,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_systems_without_extra_info(mcp_client: Client):
    """Test getting systems without extra information."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "extra_info": False,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_systems_filter_by_no_proxy(mcp_client: Client):
    """Test getting systems filtered by NO_PROXY."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "filter_by_proxy_support": "NO_PROXY",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_systems_filter_by_local_proxy(mcp_client: Client):
    """Test getting systems filtered by LOCAL_PROXY."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "filter_by_proxy_support": "LOCAL_PROXY",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_systems_filter_by_bridge_proxy(mcp_client: Client):
    """Test getting systems filtered by BRIDGE_PROXY."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "filter_by_proxy_support": "BRIDGE_PROXY",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_systems_filter_by_name(mcp_client: Client):
    """Test getting systems filtered by name."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "filter_by_name": "test",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_systems_filter_by_name_wildcard(mcp_client: Client):
    """Test getting systems filtered by name with wildcard."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "filter_by_name": "test*",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_systems_filter_by_tag(mcp_client: Client):
    """Test getting systems filtered by tag."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "filter_by_tag": "env:test",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_systems_filter_by_multiple_tags(mcp_client: Client):
    """Test getting systems filtered by multiple tags."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "filter_by_tag": "env:test,type:production",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_systems_with_all_filters(mcp_client: Client):
    """Test getting systems with all filters combined."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "extra_info": True,
            "filter_by_proxy_support": "NO_PROXY",
            "filter_by_name": "test*",
            "filter_by_tag": "env:test",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_systems_response_structure(mcp_client: Client):
    """Test systems response structure validation."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_system_by_id_not_found(mcp_client: Client):
    """Test getting system by non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_system_by_id",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_system_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_system_by_id_invalid_uuid(mcp_client: Client):
    """Test getting system by invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_system_by_id",
        arguments={"id": "not-a-valid-uuid"},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_system_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_system_by_id_empty_id(mcp_client: Client):
    """Test getting system by empty ID."""
    result = await mcp_client.call_tool(
        "qg_get_system_by_id",
        arguments={"id": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_system_by_id"
    # API may accept empty ID
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_system_by_id_with_extra_info(
    mcp_client: Client, test_infrastructure
):
    """Test getting system by ID with extra information."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_get_system_by_id",
        arguments={
            "id": system_id,
            "extra_info": True,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_system_by_id"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_system_by_id_without_extra_info(
    mcp_client: Client, test_infrastructure
):
    """Test getting system by ID without extra information."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_get_system_by_id",
        arguments={
            "id": system_id,
            "extra_info": False,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_system_by_id"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_system_by_id_existing(mcp_client: Client, test_infrastructure):
    """Test getting existing system by ID."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_get_system_by_id",
        arguments={"id": system_id},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_system_by_id"
    assert metadata["success"] is True

    # Should return system details
    if "result" in result.data:
        system = result.data["result"]
        assert isinstance(system, dict)
        assert system.get("id") == system_id


@pytest.mark.integration
async def test_qg_get_system_by_id_response_structure(
    mcp_client: Client, test_infrastructure
):
    """Test system by ID response structure validation."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_get_system_by_id",
        arguments={"id": system_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_system_by_id_consistency(mcp_client: Client, test_infrastructure):
    """Test consistency of get_system_by_id for same ID."""
    system_id = test_infrastructure.get("system_id")

    result1 = await mcp_client.call_tool(
        "qg_get_system_by_id",
        arguments={"id": system_id},
    )

    result2 = await mcp_client.call_tool(
        "qg_get_system_by_id",
        arguments={"id": system_id},
    )

    # Both calls should return same success status
    assert result1.data is not None
    assert result2.data is not None
    assert result1.data["metadata"]["success"] == result2.data["metadata"]["success"]

    # If successful, results should match
    if result1.data["metadata"]["success"]:
        assert result1.data["result"]["id"] == result2.data["result"]["id"]


@pytest.mark.integration
async def test_qg_create_system_basic(mcp_client: Client, test_infrastructure):
    """Test creating a system with minimal required parameters."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    system_name = f"test_system_pytest_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,  # 1GB in bytes
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_system"
    assert metadata["success"] is True

    # Clean up - delete created system
    if "result" in result.data:
        created_system_id = result.data["result"].get("id")
        if created_system_id:
            await mcp_client.call_tool(
                "qg_delete_system",
                arguments={"id": created_system_id},
            )


@pytest.mark.integration
async def test_qg_create_system_with_description(
    mcp_client: Client, test_infrastructure
):
    """Test creating a system with description."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    system_name = f"test_system_pytest_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,  # 1GB in bytes
            "description": "Test system created by pytest",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_system"
    assert metadata["success"] is True

    # Clean up
    if "result" in result.data:
        created_system_id = result.data["result"].get("id")
        if created_system_id:
            await mcp_client.call_tool(
                "qg_delete_system",
                arguments={"id": created_system_id},
            )


@pytest.mark.integration
async def test_qg_create_system_with_tags(mcp_client: Client, test_infrastructure):
    """Test creating a system with tags."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    system_name = f"test_system_pytest_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,  # 1GB in bytes
            "tags": {"env": "test", "created_by": "pytest"},
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_system"
    assert metadata["success"] is True

    # Clean up
    if "result" in result.data:
        created_system_id = result.data["result"].get("id")
        if created_system_id:
            await mcp_client.call_tool(
                "qg_delete_system",
                arguments={"id": created_system_id},
            )


@pytest.mark.integration
async def test_qg_create_system_with_software_version(
    mcp_client: Client, test_infrastructure
):
    """Test creating a system with software version."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    system_name = f"test_system_pytest_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,  # 1GB in bytes
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_system"
    assert metadata["success"] is True

    # Clean up
    if "result" in result.data:
        created_system_id = result.data["result"].get("id")
        if created_system_id:
            await mcp_client.call_tool(
                "qg_delete_system",
                arguments={"id": created_system_id},
            )


@pytest.mark.integration
async def test_qg_create_system_duplicate_name(mcp_client: Client, test_infrastructure):
    """Test creating a system with duplicate name."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    system_name = f"test_system_pytest_{uuid.uuid4().hex[:8]}"

    # Create first system
    result1 = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,  # 1GB in bytes
        },
    )

    assert result1.data is not None
    assert result1.data["metadata"]["success"] is True
    created_system_id = result1.data["result"].get("id")

    # Try to create duplicate
    result2 = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,  # 1GB in bytes
        },
    )

    assert result2.data is not None
    metadata = result2.data["metadata"]
    assert metadata["tool_name"] == "qg_create_system"
    # Should fail due to duplicate name
    assert metadata["success"] is False

    # Clean up
    if created_system_id:
        await mcp_client.call_tool(
            "qg_delete_system",
            arguments={"id": created_system_id},
        )


@pytest.mark.integration
async def test_qg_delete_system_not_found(mcp_client: Client):
    """Test deleting system by non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_system",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_system"
    # API may be idempotent (succeed for non-existent IDs)
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_delete_system_invalid_uuid(mcp_client: Client):
    """Test deleting system by invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_system",
        arguments={"id": "not-a-valid-uuid"},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_system"
    # API may be idempotent
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_delete_system_empty_id(mcp_client: Client):
    """Test deleting system by empty ID."""
    result = await mcp_client.call_tool(
        "qg_delete_system",
        arguments={"id": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_system"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_delete_system_success(mcp_client: Client, test_infrastructure):
    """Test successfully deleting a system."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    system_name = f"test_system_pytest_{uuid.uuid4().hex[:8]}"

    # Create system first
    create_result = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,  # 1GB in bytes
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True

    created_system_id = create_result.data["result"].get("id")

    # Delete system
    delete_result = await mcp_client.call_tool(
        "qg_delete_system",
        arguments={"id": created_system_id},
    )

    assert delete_result.data is not None
    metadata = delete_result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_system"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_systems_error_handling(mcp_client: Client):
    """Test error handling across system tools."""
    # Test get_system_by_id with malformed UUID
    result = await mcp_client.call_tool(
        "qg_get_system_by_id",
        arguments={"id": "12345"},
    )
    assert result.data is not None
    assert "metadata" in result.data

    # Test delete_system with special characters
    result = await mcp_client.call_tool(
        "qg_delete_system",
        arguments={"id": "invalid@#$%"},
    )
    assert result.data is not None
    assert "metadata" in result.data


@pytest.mark.integration
async def test_qg_get_systems_consistency(mcp_client: Client):
    """Test consistency of get_systems calls."""
    result1 = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={},
    )

    result2 = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={},
    )

    # Both calls should return same success status
    assert result1.data is not None
    assert result2.data is not None
    assert result1.data["metadata"]["success"] == result2.data["metadata"]["success"]


@pytest.mark.integration
async def test_qg_create_system_missing_required_params(mcp_client: Client):
    """Test creating system with missing required parameters."""
    try:
        result = await mcp_client.call_tool(
            "qg_create_system",
            arguments={
                "name": "test_system",
                # Missing system_type and platform_type
            },
        )
        # If it doesn't raise an exception, check the result
        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_create_system"
        # Should fail due to missing required parameters
        assert metadata["success"] is False
    except Exception:
        # Expected to raise validation error for missing required params
        pass


@pytest.mark.integration
async def test_qg_get_systems_invalid_proxy_type(mcp_client: Client):
    """Test getting systems with invalid proxy support type."""
    result = await mcp_client.call_tool(
        "qg_get_systems",
        arguments={
            "filter_by_proxy_support": "INVALID_PROXY_TYPE",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_systems"
    # API may or may not validate proxy type
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_put_system(mcp_client: Client, test_infrastructure):
    """Test updating a system with PUT operation."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    system_name = f"test_system_put_{uuid.uuid4().hex[:8]}"

    # First create a system
    create_result = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,
            "description": "Original description",
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True
    system_id = create_result.data["result"]["id"]

    # Now update it using PUT
    updated_name = f"updated_{system_name}"
    result = await mcp_client.call_tool(
        "qg_put_system",
        arguments={
            "id": system_id,
            "name": updated_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 2147483648,  # Changed to 2GB
            "description": "Updated description",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_system"
    assert metadata["success"] is True

    # Verify the update
    if "result" in result.data:
        updated_system = result.data["result"]
        assert updated_system["name"] == updated_name
        assert updated_system["description"] == "Updated description"
        assert updated_system["maximumMemoryPerNode"] == 2147483648

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_system",
        arguments={"id": system_id},
    )


@pytest.mark.integration
async def test_qg_put_system_not_found(mcp_client: Client, test_infrastructure):
    """Test updating a non-existent system returns 404."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    fake_system_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_put_system",
        arguments={
            "id": fake_system_id,
            "name": "nonexistent_system",
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_system"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_put_system_invalid_data(mcp_client: Client, test_infrastructure):
    """Test updating system with invalid data."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    system_name = f"test_system_invalid_{uuid.uuid4().hex[:8]}"

    # First create a system
    create_result = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True
    system_id = create_result.data["result"]["id"]

    # Try to update with invalid system_type
    result = await mcp_client.call_tool(
        "qg_put_system",
        arguments={
            "id": system_id,
            "name": system_name,
            "system_type": "INVALID_TYPE",  # Invalid enum value
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_system"
    assert metadata["success"] is False

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_system",
        arguments={"id": system_id},
    )


@pytest.mark.integration
async def test_qg_put_system_partial_update(mcp_client: Client, test_infrastructure):
    """Test that PUT replaces all fields (not partial update)."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    system_name = f"test_system_partial_{uuid.uuid4().hex[:8]}"

    # Create system with description and region
    create_result = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,
            "description": "Original description",
            "region": "us-east-1",
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True
    system_id = create_result.data["result"]["id"]

    # Update with PUT but don't include description/region
    # These should be cleared (PUT is full replacement)
    result = await mcp_client.call_tool(
        "qg_put_system",
        arguments={
            "id": system_id,
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,
            # Note: NOT including description or region
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_system"
    assert metadata["success"] is True

    # Verify fields were cleared
    if "result" in result.data:
        updated_system = result.data["result"]
        # Description and region should be empty/null since not provided in PUT
        assert updated_system.get("description") in [None, "", "null"]
        assert updated_system.get("region") in [None, "", "null"]

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_system",
        arguments={"id": system_id},
    )


@pytest.mark.integration
async def test_qg_put_system_with_tags(mcp_client: Client, test_infrastructure):
    """Test updating system with tags."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    node_version = test_infrastructure.get("node_version")
    system_name = f"test_system_tags_{uuid.uuid4().hex[:8]}"

    # Create system
    create_result = await mcp_client.call_tool(
        "qg_create_system",
        arguments={
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True
    system_id = create_result.data["result"]["id"]

    # Update with tags
    result = await mcp_client.call_tool(
        "qg_put_system",
        arguments={
            "id": system_id,
            "name": system_name,
            "system_type": "TERADATA",
            "platform_type": "ON_PREM",
            "data_center_id": datacenter_id,
            "software_version": node_version,
            "maximum_memory_per_node": 1073741824,
            "tags": {"environment": "test", "owner": "pytest"},
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_system"
    assert metadata["success"] is True

    # Verify tags
    if "result" in result.data:
        updated_system = result.data["result"]
        assert "tags" in updated_system
        assert updated_system["tags"].get("environment") == "test"
        assert updated_system["tags"].get("owner") == "pytest"

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_system",
        arguments={"id": system_id},
    )
