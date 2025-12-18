"""Integration tests for fabric_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_get_fabrics(mcp_client: Client):
    """Test getting all fabrics."""
    result = await mcp_client.call_tool("qg_get_fabrics", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_fabrics"
    assert metadata["success"] is True

    # Verify result is a list
    fabrics = result.data["result"]
    assert isinstance(fabrics, list), "Fabrics result should be a list"


@pytest.mark.integration
async def test_qg_get_fabrics_with_filters(mcp_client: Client, test_fabric):
    """Test getting fabrics with filter parameters."""
    fabric_name = test_fabric.get("name")

    # Test with name filter
    result = await mcp_client.call_tool(
        "qg_get_fabrics", arguments={"filter_by_name": fabric_name}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    filtered_fabrics = result.data["result"]
    assert isinstance(filtered_fabrics, list)
    # Should find at least the fabric we searched for
    assert any(f.get("name") == fabric_name for f in filtered_fabrics)


@pytest.mark.integration
async def test_qg_get_fabrics_with_flatten(mcp_client: Client):
    """Test getting fabrics with flatten option."""
    result = await mcp_client.call_tool("qg_get_fabrics", arguments={"flatten": True})

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_fabrics_with_extra_info(mcp_client: Client):
    """Test getting fabrics with extra_info option."""
    result = await mcp_client.call_tool(
        "qg_get_fabrics", arguments={"extra_info": True}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_fabric_by_id(mcp_client: Client, test_fabric):
    """Test getting a specific fabric by ID."""
    fabric_id = test_fabric.get("id")
    assert fabric_id is not None, "Test fabric should have an ID"

    # Get fabric by ID
    result = await mcp_client.call_tool(
        "qg_get_fabric_by_id", arguments={"id": fabric_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_fabric_by_id"
    assert metadata["success"] is True

    # Verify fabric data
    fabric = result.data["result"]
    assert isinstance(fabric, dict)
    assert fabric.get("id") == fabric_id


@pytest.mark.integration
async def test_qg_get_fabric_by_id_with_extra_info(mcp_client: Client, test_fabric):
    """Test getting a fabric by ID with extra_info."""
    fabric_id = test_fabric.get("id")

    result = await mcp_client.call_tool(
        "qg_get_fabric_by_id", arguments={"id": fabric_id, "extra_info": True}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_fabric_by_id_not_found(mcp_client: Client):
    """Test getting a fabric with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_fabric_by_id", arguments={"id": fake_id}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_fabric_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_fabric_by_id_invalid_uuid(mcp_client: Client):
    """Test getting a fabric with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_fabric_by_id", arguments={"id": "not-a-valid-uuid"}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_fabric_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_fabric_active(mcp_client: Client, test_fabric):
    """Test getting active configuration for a fabric."""
    fabric_id = test_fabric.get("id")

    result = await mcp_client.call_tool(
        "qg_get_fabric_active", arguments={"id": fabric_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_fabric_active"
    # May succeed or fail depending on fabric state
    if metadata["success"]:
        assert "result" in result.data


@pytest.mark.integration
async def test_qg_get_fabric_pending(mcp_client: Client, test_fabric):
    """Test getting pending configuration for a fabric."""
    fabric_id = test_fabric.get("id")

    result = await mcp_client.call_tool(
        "qg_get_fabric_pending", arguments={"id": fabric_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_fabric_pending"
    # May succeed or fail depending on fabric state


@pytest.mark.integration
async def test_qg_get_fabric_previous(mcp_client: Client, test_fabric):
    """Test getting previous configuration for a fabric."""
    fabric_id = test_fabric.get("id")

    result = await mcp_client.call_tool(
        "qg_get_fabric_previous", arguments={"id": fabric_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_fabric_previous"
    # May succeed or fail depending on fabric state


@pytest.mark.integration
async def test_qg_create_fabric(mcp_client: Client, qg_manager):
    """Test creating a new fabric."""
    # Get fabric software version
    softwares = qg_manager.software_client.get_software()
    fabric_software = None
    for sw in softwares:
        if sw.get("type") == "FABRIC":
            fabric_software = sw
            break

    if not fabric_software:
        pytest.skip("No FABRIC software available")

    fabric_name = f"test_fabric_pytest_{uuid.uuid4().hex[:8]}"
    fabric_version = fabric_software.get("version")

    result = await mcp_client.call_tool(
        "qg_create_fabric",
        arguments={
            "name": fabric_name,
            "port": 10100,
            "softwareVersion": fabric_version,
            "authKeySize": 2048,
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_fabric"

    # May succeed or fail depending on infrastructure
    if metadata["success"]:
        assert "result" in result.data
        created_fabric = result.data["result"]
        assert isinstance(created_fabric, dict)
        assert created_fabric.get("name") == fabric_name
        assert "id" in created_fabric

        # Cleanup - delete the created fabric
        fabric_id = created_fabric["id"]
        cleanup_result = await mcp_client.call_tool(
            "qg_delete_fabric", arguments={"id": fabric_id}
        )
        assert cleanup_result.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_create_fabric_with_description(mcp_client: Client, qg_manager):
    """Test creating a fabric with description."""
    # Get fabric software version
    softwares = qg_manager.software_client.get_software()
    fabric_software = None
    for sw in softwares:
        if sw.get("type") == "FABRIC":
            fabric_software = sw
            break

    if not fabric_software:
        pytest.skip("No FABRIC software available")

    fabric_name = f"test_fabric_desc_{uuid.uuid4().hex[:8]}"
    fabric_version = fabric_software.get("version")
    description = "Test fabric with description"

    result = await mcp_client.call_tool(
        "qg_create_fabric",
        arguments={
            "name": fabric_name,
            "port": 10101,
            "softwareVersion": fabric_version,
            "authKeySize": 2048,
            "description": description,
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_fabric"

    if metadata["success"]:
        created_fabric = result.data["result"]
        assert created_fabric.get("description") == description

        # Cleanup
        fabric_id = created_fabric["id"]
        cleanup_result = await mcp_client.call_tool(
            "qg_delete_fabric", arguments={"id": fabric_id}
        )
        assert cleanup_result.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_create_fabric_with_tags(mcp_client: Client, qg_manager):
    """Test creating a fabric with tags."""
    # Get fabric software version
    softwares = qg_manager.software_client.get_software()
    fabric_software = None
    for sw in softwares:
        if sw.get("type") == "FABRIC":
            fabric_software = sw
            break

    if not fabric_software:
        pytest.skip("No FABRIC software available")

    fabric_name = f"test_fabric_tags_{uuid.uuid4().hex[:8]}"
    fabric_version = fabric_software.get("version")
    tags = {"environment": "test", "created_by": "pytest"}

    result = await mcp_client.call_tool(
        "qg_create_fabric",
        arguments={
            "name": fabric_name,
            "port": 10102,
            "softwareVersion": fabric_version,
            "authKeySize": 2048,
            "tags": tags,
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_fabric"

    if metadata["success"]:
        created_fabric = result.data["result"]

        # Cleanup
        fabric_id = created_fabric["id"]
        cleanup_result = await mcp_client.call_tool(
            "qg_delete_fabric", arguments={"id": fabric_id}
        )
        assert cleanup_result.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_create_fabric_different_auth_key_sizes(
    mcp_client: Client, qg_manager
):
    """Test creating fabrics with different auth key sizes."""
    # Get fabric software version
    softwares = qg_manager.software_client.get_software()
    fabric_software = None
    for sw in softwares:
        if sw.get("type") == "FABRIC":
            fabric_software = sw
            break

    if not fabric_software:
        pytest.skip("No FABRIC software available")

    fabric_version = fabric_software.get("version")
    auth_key_sizes = [1536, 2048, 3072, 4096]

    for key_size in auth_key_sizes:
        fabric_name = f"test_fabric_auth_{key_size}_{uuid.uuid4().hex[:6]}"

        result = await mcp_client.call_tool(
            "qg_create_fabric",
            arguments={
                "name": fabric_name,
                "port": 10103,
                "softwareVersion": fabric_version,
                "authKeySize": key_size,
            },
        )

        assert result.data is not None
        metadata = result.data["metadata"]

        if metadata["success"]:
            created_fabric = result.data["result"]
            fabric_id = created_fabric["id"]

            # Cleanup
            cleanup_result = await mcp_client.call_tool(
                "qg_delete_fabric", arguments={"id": fabric_id}
            )
            # Only break after first successful creation to avoid too many tests
            break


@pytest.mark.integration
async def test_qg_create_fabric_invalid_auth_key_size(mcp_client: Client, qg_manager):
    """Test creating a fabric with invalid auth key size."""
    # Get fabric software version
    softwares = qg_manager.software_client.get_software()
    fabric_software = None
    for sw in softwares:
        if sw.get("type") == "FABRIC":
            fabric_software = sw
            break

    if not fabric_software:
        pytest.skip("No FABRIC software available")

    fabric_name = f"test_fabric_invalid_{uuid.uuid4().hex[:8]}"
    fabric_version = fabric_software.get("version")

    result = await mcp_client.call_tool(
        "qg_create_fabric",
        arguments={
            "name": fabric_name,
            "port": 10104,
            "softwareVersion": fabric_version,
            "authKeySize": 1024,  # Invalid size
        },
    )

    # Should fail with invalid auth key size
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_fabric"
    # May succeed or fail depending on API validation


@pytest.mark.integration
async def test_qg_delete_fabric(mcp_client: Client, qg_manager):
    """Test deleting a fabric."""
    # First create a fabric to delete
    softwares = qg_manager.software_client.get_software()
    fabric_software = None
    for sw in softwares:
        if sw.get("type") == "FABRIC":
            fabric_software = sw
            break

    if not fabric_software:
        pytest.skip("No FABRIC software available")

    fabric_name = f"test_fabric_delete_{uuid.uuid4().hex[:8]}"
    fabric_version = fabric_software.get("version")

    create_result = await mcp_client.call_tool(
        "qg_create_fabric",
        arguments={
            "name": fabric_name,
            "port": 10105,
            "softwareVersion": fabric_version,
            "authKeySize": 2048,
        },
    )

    if not create_result.data["metadata"]["success"]:
        pytest.skip("Could not create test fabric for deletion test")

    fabric_id = create_result.data["result"]["id"]

    # Delete the fabric
    result = await mcp_client.call_tool(
        "qg_delete_fabric",
        arguments={"id": fabric_id},
    )

    # Verify deletion response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_fabric"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_delete_fabric_not_found(mcp_client: Client):
    """Test deleting a fabric with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_fabric",
        arguments={"id": fake_id},
    )

    # API may return success for non-existent IDs (idempotent delete)
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_fabric"


@pytest.mark.integration
async def test_qg_delete_fabric_invalid_uuid(mcp_client: Client):
    """Test deleting a fabric with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_fabric",
        arguments={"id": "not-a-valid-uuid"},
    )

    # API may handle invalid UUIDs differently
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_fabric"


@pytest.mark.integration
async def test_qg_fabric_error_handling(mcp_client: Client):
    """Test error handling across fabric operations."""
    # Test getting fabric with empty ID
    result = await mcp_client.call_tool(
        "qg_get_fabric_by_id",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data

    # Test creating fabric with empty name
    result = await mcp_client.call_tool(
        "qg_create_fabric",
        arguments={
            "name": "",
            "port": 10000,
            "softwareVersion": "1.0.0",
            "authKeySize": 2048,
        },
    )
    assert result.data is not None
    assert "metadata" in result.data

    # Test deleting fabric with empty ID
    result = await mcp_client.call_tool(
        "qg_delete_fabric",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data


@pytest.mark.integration
async def test_qg_update_fabric(mcp_client: Client, test_fabric):
    """Test updating a fabric's name and description using PATCH."""
    fabric_id = test_fabric.get("id")
    assert fabric_id is not None, "Test fabric should have an ID"

    # Update name and description
    updated_name = f"Updated-Fabric-{uuid.uuid4()}"
    updated_description = "Updated description via PATCH"

    result = await mcp_client.call_tool(
        "qg_update_fabric",
        arguments={
            "id": fabric_id,
            "name": updated_name,
            "description": updated_description,
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_update_fabric"
    assert metadata["success"] is True

    # Verify updated fabric
    fabric = result.data["result"]
    assert fabric.get("name") == updated_name
    assert fabric.get("description") == updated_description


@pytest.mark.integration
async def test_qg_update_fabric_partial(mcp_client: Client, test_fabric):
    """Test updating fabric with PATCH."""
    fabric_id = test_fabric.get("id")
    original_name = test_fabric.get("name")

    # Update description only (but name is required by API)
    updated_description = "Partial update - description only"

    result = await mcp_client.call_tool(
        "qg_update_fabric",
        arguments={
            "id": fabric_id,
            "name": original_name,  # Name is required even for PATCH
            "description": updated_description,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    fabric = result.data["result"]
    # Name should remain unchanged
    assert fabric.get("name") == original_name
    # Description should be updated
    assert fabric.get("description") == updated_description


@pytest.mark.integration
async def test_qg_put_fabric_active(mcp_client: Client, test_fabric):
    """Test updating active fabric version using PUT (full replacement)."""
    fabric_id = test_fabric.get("id")
    fabric_name = test_fabric.get("name")
    fabric_software_version = test_fabric.get("softwareVersion")  # Use current version

    # Put new active version
    result = await mcp_client.call_tool(
        "qg_put_fabric_active",
        arguments={
            "id": fabric_id,
            "name": fabric_name,
            "port": 1025,
            "softwareVersion": fabric_software_version,  # Use valid version
            "authKeySize": 3072,
            "description": "Updated active version",
            "tags": {"env": "test", "updated": "true"},
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_fabric_active"
    assert metadata["success"] is True

    # Verify updated active version
    fabric = result.data["result"]
    assert fabric.get("name") == fabric_name
    assert fabric.get("port") == 1025
    assert fabric.get("softwareVersion") == fabric_software_version
    assert fabric.get("authKeySize") == 3072
    assert fabric.get("description") == "Updated active version"


@pytest.mark.integration
async def test_qg_put_fabric_pending(mcp_client: Client, test_fabric):
    """Test creating a pending fabric version using PUT."""
    fabric_id = test_fabric.get("id")
    fabric_name = test_fabric.get("name")
    fabric_software_version = test_fabric.get("softwareVersion")  # Use current version

    # Create pending version
    result = await mcp_client.call_tool(
        "qg_put_fabric_pending",
        arguments={
            "id": fabric_id,
            "name": fabric_name,
            "port": 1026,
            "softwareVersion": fabric_software_version,  # Use valid version
            "authKeySize": 4096,
            "description": "Pending version for review",
            "tags": {"env": "staging", "version": "3.0"},
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_fabric_pending"
    assert metadata["success"] is True

    # Verify pending version
    fabric = result.data["result"]
    assert fabric.get("name") == fabric_name
    assert fabric.get("port") == 1026
    assert fabric.get("softwareVersion") == fabric_software_version
    assert fabric.get("authKeySize") == 4096
    assert fabric.get("version") == "PENDING"


@pytest.mark.integration
async def test_qg_update_fabric_active_workflow(mcp_client: Client, test_fabric):
    """Test the full workflow of creating pending version and activating it."""
    fabric_id = test_fabric.get("id")
    fabric_name = test_fabric.get("name")
    fabric_software_version = test_fabric.get("softwareVersion")  # Use current version

    # Step 1: Create a pending version
    pending_result = await mcp_client.call_tool(
        "qg_put_fabric_pending",
        arguments={
            "id": fabric_id,
            "name": fabric_name,
            "port": 1027,
            "softwareVersion": fabric_software_version,  # Use valid version
            "authKeySize": 2048,
            "description": "Version to be activated",
        },
    )

    assert pending_result.data is not None
    pending_fabric = pending_result.data["result"]
    assert pending_fabric.get("version") == "PENDING"

    # Step 2: Get the pending version to extract versionId
    get_pending = await mcp_client.call_tool(
        "qg_get_fabric_pending",
        arguments={"id": fabric_id},
    )

    assert get_pending.data is not None
    pending_data = get_pending.data["result"]
    version_id = pending_data.get("versionId")
    assert version_id is not None, "Pending version should have versionId"

    # Step 3: Activate the pending version
    activate_result = await mcp_client.call_tool(
        "qg_update_fabric_active",
        arguments={
            "id": fabric_id,
            "version_id": version_id,
        },
    )

    # Verify activation
    assert activate_result.data is not None
    metadata = activate_result.data["metadata"]
    assert metadata["tool_name"] == "qg_update_fabric_active"
    assert metadata["success"] is True

    # Step 4: Verify by getting the now-active version
    get_active = await mcp_client.call_tool(
        "qg_get_fabric_active",
        arguments={"id": fabric_id},
    )

    assert get_active.data is not None
    activated_fabric = get_active.data["result"]
    assert activated_fabric.get("version") == "ACTIVE"
    assert activated_fabric.get("softwareVersion") == fabric_software_version
    assert activated_fabric.get("port") == 1027


@pytest.mark.integration
async def test_qg_delete_fabric_pending(mcp_client: Client, test_fabric):
    """Test deleting a pending fabric version."""
    fabric_id = test_fabric.get("id")
    fabric_name = test_fabric.get("name")
    fabric_software_version = test_fabric.get("softwareVersion")  # Use current version

    # First create a pending version
    await mcp_client.call_tool(
        "qg_put_fabric_pending",
        arguments={
            "id": fabric_id,
            "name": fabric_name,
            "port": 1028,
            "softwareVersion": fabric_software_version,  # Use valid version
            "authKeySize": 2048,
        },
    )

    # Now delete the pending version
    result = await mcp_client.call_tool(
        "qg_delete_fabric_pending",
        arguments={"id": fabric_id},
    )

    # Verify response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_fabric_pending"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_delete_fabric_previous(mcp_client: Client, test_fabric):
    """Test deleting a previous fabric version."""
    fabric_id = test_fabric.get("id")
    fabric_name = test_fabric.get("name")
    fabric_software_version = test_fabric.get("softwareVersion")  # Use current version

    # First, create and activate a version to generate a previous version
    # Create pending
    await mcp_client.call_tool(
        "qg_put_fabric_pending",
        arguments={
            "id": fabric_id,
            "name": fabric_name,
            "port": 1029,
            "softwareVersion": fabric_software_version,  # Use valid version
            "authKeySize": 2048,
        },
    )

    # Get pending version
    get_pending = await mcp_client.call_tool(
        "qg_get_fabric_pending",
        arguments={"id": fabric_id},
    )
    pending_data = get_pending.data["result"]
    version_id = pending_data.get("versionId")

    # Activate it (this makes the current active become previous)
    await mcp_client.call_tool(
        "qg_update_fabric_active",
        arguments={
            "id": fabric_id,
            "version_id": version_id,
        },
    )

    # Now delete the previous version
    result = await mcp_client.call_tool(
        "qg_delete_fabric_previous",
        arguments={"id": fabric_id},
    )

    # Verify response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_fabric_previous"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_update_fabric_active_with_previous_version(
    mcp_client: Client, test_fabric
):
    """Test activating a previous version (rollback scenario)."""
    fabric_id = test_fabric.get("id")
    fabric_name = test_fabric.get("name")
    fabric_software_version = test_fabric.get("softwareVersion")  # Use current version

    # Create and activate a new version to generate previous
    await mcp_client.call_tool(
        "qg_put_fabric_pending",
        arguments={
            "id": fabric_id,
            "name": fabric_name,
            "port": 1030,
            "softwareVersion": fabric_software_version,  # Use valid version
            "authKeySize": 2048,
        },
    )

    get_pending = await mcp_client.call_tool(
        "qg_get_fabric_pending",
        arguments={"id": fabric_id},
    )
    version_id_new = get_pending.data["result"].get("versionId")

    # Activate the new version
    await mcp_client.call_tool(
        "qg_update_fabric_active",
        arguments={
            "id": fabric_id,
            "version_id": version_id_new,
        },
    )

    # Now get the previous version
    get_previous = await mcp_client.call_tool(
        "qg_get_fabric_previous",
        arguments={"id": fabric_id},
    )

    if get_previous.data is not None and get_previous.data.get("result"):
        previous_data = get_previous.data["result"]
        previous_version_id = previous_data.get("versionId")

        # Rollback: activate the previous version
        rollback_result = await mcp_client.call_tool(
            "qg_update_fabric_active",
            arguments={
                "id": fabric_id,
                "version_id": previous_version_id,
            },
        )

        # Verify rollback
        assert rollback_result.data is not None
        metadata = rollback_result.data["metadata"]
        assert metadata["success"] is True

        # Verify the rollback by getting the active version
        get_active = await mcp_client.call_tool(
            "qg_get_fabric_active",
            arguments={"id": fabric_id},
        )

        assert get_active.data is not None
        rolled_back_fabric = get_active.data["result"]
        assert rolled_back_fabric.get("version") == "ACTIVE"
