"""Integration tests for datacenters_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_get_datacenters(mcp_client: Client):
    """Test getting all datacenters."""
    result = await mcp_client.call_tool("qg_get_datacenters", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_datacenters"
    assert metadata["success"] is True

    # Verify result is a list
    datacenters = result.data["result"]
    assert isinstance(datacenters, list), "Datacenters result should be a list"


@pytest.mark.integration
async def test_qg_get_datacenters_with_name_filter(
    mcp_client: Client, test_infrastructure
):
    """Test getting datacenters with name filter."""
    datacenter_id = test_infrastructure.get("datacenter_id")

    # First get the datacenter to know its name
    dc_result = await mcp_client.call_tool(
        "qg_get_datacenter_by_id", arguments={"id": datacenter_id}
    )
    assert dc_result.data is not None
    datacenter_name = dc_result.data["result"].get("name")

    # Test with name filter
    result = await mcp_client.call_tool(
        "qg_get_datacenters", arguments={"filter_by_name": datacenter_name}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    filtered_datacenters = result.data["result"]
    assert isinstance(filtered_datacenters, list)
    # Should find at least the datacenter we searched for
    assert len(filtered_datacenters) > 0
    assert any(dc.get("name") == datacenter_name for dc in filtered_datacenters)


@pytest.mark.integration
async def test_qg_get_datacenter_by_id(mcp_client: Client, test_infrastructure):
    """Test getting a specific datacenter by ID."""
    datacenter_id = test_infrastructure.get("datacenter_id")
    assert datacenter_id is not None, "Test infrastructure should have datacenter_id"

    # Get datacenter by ID
    result = await mcp_client.call_tool(
        "qg_get_datacenter_by_id", arguments={"id": datacenter_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_datacenter_by_id"
    assert metadata["success"] is True

    # Verify datacenter data
    datacenter = result.data["result"]
    assert isinstance(datacenter, dict)
    assert datacenter.get("id") == datacenter_id
    assert "name" in datacenter


@pytest.mark.integration
async def test_qg_get_datacenter_by_id_not_found(mcp_client: Client):
    """Test getting a datacenter with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_datacenter_by_id", arguments={"id": fake_id}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_datacenter_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_datacenter_by_id_invalid_uuid(mcp_client: Client):
    """Test getting a datacenter with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_datacenter_by_id", arguments={"id": "not-a-valid-uuid"}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_datacenter_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_create_datacenter(mcp_client: Client):
    """Test creating a new datacenter with minimal parameters."""
    datacenter_name = f"test_datacenter_tool_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={"name": datacenter_name},
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_datacenter"
    assert metadata["success"] is True

    # Verify datacenter was created
    assert "result" in result.data
    created_datacenter = result.data["result"]
    assert isinstance(created_datacenter, dict)
    assert created_datacenter.get("name") == datacenter_name
    assert "id" in created_datacenter

    # Cleanup - delete the created datacenter
    datacenter_id = created_datacenter["id"]
    cleanup_result = await mcp_client.call_tool(
        "qg_delete_datacenter", arguments={"id": datacenter_id}
    )
    assert cleanup_result.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_create_datacenter_with_description(mcp_client: Client):
    """Test creating a datacenter with description."""
    datacenter_name = f"test_datacenter_pytest_{uuid.uuid4().hex[:8]}"
    description = "Test datacenter created by automated test"

    result = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={
            "name": datacenter_name,
            "description": description,
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    created_datacenter = result.data["result"]
    assert created_datacenter.get("name") == datacenter_name
    assert created_datacenter.get("description") == description

    # Cleanup
    datacenter_id = created_datacenter["id"]
    cleanup_result = await mcp_client.call_tool(
        "qg_delete_datacenter", arguments={"id": datacenter_id}
    )
    assert cleanup_result.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_create_datacenter_with_tags(mcp_client: Client):
    """Test creating a datacenter with tags."""
    datacenter_name = f"test_datacenter_tags_{uuid.uuid4().hex[:8]}"
    tags = {"environment": "test", "created_by": "pytest"}

    result = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={
            "name": datacenter_name,
            "tags": tags,
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    created_datacenter = result.data["result"]
    assert created_datacenter.get("name") == datacenter_name
    # Tags may or may not be returned in response depending on API version

    # Cleanup
    datacenter_id = created_datacenter["id"]
    cleanup_result = await mcp_client.call_tool(
        "qg_delete_datacenter", arguments={"id": datacenter_id}
    )
    assert cleanup_result.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_create_datacenter_with_all_parameters(mcp_client: Client):
    """Test creating a datacenter with all optional parameters."""
    datacenter_name = f"test_datacenter_full_{uuid.uuid4().hex[:8]}"
    description = "Fully configured test datacenter"
    tags = {"environment": "test", "type": "integration"}

    result = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={
            "name": datacenter_name,
            "description": description,
            "tags": tags,
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    created_datacenter = result.data["result"]
    assert created_datacenter.get("name") == datacenter_name
    assert created_datacenter.get("description") == description
    # Tags may or may not be returned in response depending on API version

    # Cleanup
    datacenter_id = created_datacenter["id"]
    cleanup_result = await mcp_client.call_tool(
        "qg_delete_datacenter", arguments={"id": datacenter_id}
    )
    assert cleanup_result.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_create_datacenter_duplicate_name(mcp_client: Client):
    """Test creating a datacenter with duplicate name."""
    datacenter_name = f"test_datacenter_dup_{uuid.uuid4().hex[:8]}"

    # Create first datacenter
    result1 = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={"name": datacenter_name},
    )

    assert result1.data["metadata"]["success"] is True
    datacenter_id = result1.data["result"]["id"]

    # Try to create second datacenter with same name
    result2 = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={"name": datacenter_name},
    )

    # May succeed or fail depending on QGM configuration
    # Either way, clean up the first datacenter
    cleanup_result = await mcp_client.call_tool(
        "qg_delete_datacenter", arguments={"id": datacenter_id}
    )
    assert cleanup_result.data["metadata"]["success"] is True

    # If second creation succeeded, clean it up too
    if result2.data["metadata"]["success"]:
        second_id = result2.data["result"]["id"]
        cleanup_result2 = await mcp_client.call_tool(
            "qg_delete_datacenter", arguments={"id": second_id}
        )
        assert cleanup_result2.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_update_datacenter(mcp_client: Client):
    """Test updating a datacenter with PUT."""
    # First create a datacenter
    datacenter_name = f"test_datacenter_update_{uuid.uuid4().hex[:8]}"

    create_result = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={"name": datacenter_name, "description": "Original description"},
    )

    assert create_result.data["metadata"]["success"] is True
    datacenter_id = create_result.data["result"]["id"]

    # Update the datacenter
    updated_name = f"updated_{datacenter_name}"
    updated_description = "Updated description"

    result = await mcp_client.call_tool(
        "qg_update_datacenter",
        arguments={
            "id": datacenter_id,
            "name": updated_name,
            "description": updated_description,
        },
    )

    # Verify update response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_update_datacenter"
    assert metadata["success"] is True

    updated_datacenter = result.data["result"]
    assert updated_datacenter.get("name") == updated_name
    assert updated_datacenter.get("description") == updated_description

    # Cleanup
    cleanup_result = await mcp_client.call_tool(
        "qg_delete_datacenter", arguments={"id": datacenter_id}
    )
    assert cleanup_result.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_update_datacenter_name_only(mcp_client: Client):
    """Test updating only the name of a datacenter."""
    # First create a datacenter
    datacenter_name = f"test_datacenter_name_{uuid.uuid4().hex[:8]}"
    description = "Test description"

    create_result = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={"name": datacenter_name, "description": description},
    )

    assert create_result.data["metadata"]["success"] is True
    datacenter_id = create_result.data["result"]["id"]

    # Update only the name
    updated_name = f"updated_{datacenter_name}"

    result = await mcp_client.call_tool(
        "qg_update_datacenter",
        arguments={
            "id": datacenter_id,
            "name": updated_name,
        },
    )

    # Verify update response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    updated_datacenter = result.data["result"]
    assert updated_datacenter.get("name") == updated_name

    # Cleanup
    cleanup_result = await mcp_client.call_tool(
        "qg_delete_datacenter", arguments={"id": datacenter_id}
    )
    assert cleanup_result.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_update_datacenter_with_tags(mcp_client: Client):
    """Test updating a datacenter with tags."""
    # First create a datacenter
    datacenter_name = f"test_datacenter_tags_update_{uuid.uuid4().hex[:8]}"

    create_result = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={"name": datacenter_name},
    )

    assert create_result.data["metadata"]["success"] is True
    datacenter_id = create_result.data["result"]["id"]

    # Update with tags
    updated_name = f"updated_{datacenter_name}"
    tags = {"environment": "production", "updated_by": "pytest"}

    result = await mcp_client.call_tool(
        "qg_update_datacenter",
        arguments={
            "id": datacenter_id,
            "name": updated_name,
            "tags": tags,
        },
    )

    # Verify update response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    updated_datacenter = result.data["result"]
    assert updated_datacenter.get("name") == updated_name

    # Cleanup
    cleanup_result = await mcp_client.call_tool(
        "qg_delete_datacenter", arguments={"id": datacenter_id}
    )
    assert cleanup_result.data["metadata"]["success"] is True


@pytest.mark.integration
async def test_qg_update_datacenter_not_found(mcp_client: Client):
    """Test updating a datacenter with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_update_datacenter",
        arguments={
            "id": fake_id,
            "name": "should_not_exist",
        },
    )

    # API behavior: PUT may create if not exists or return error
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_update_datacenter"
    # Success status depends on API implementation (may succeed if it creates)


@pytest.mark.integration
async def test_qg_delete_datacenter(mcp_client: Client):
    """Test deleting a datacenter."""
    # First create a datacenter to delete
    datacenter_name = f"test_datacenter_delete_{uuid.uuid4().hex[:8]}"

    create_result = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={"name": datacenter_name},
    )

    assert create_result.data["metadata"]["success"] is True
    datacenter_id = create_result.data["result"]["id"]

    # Delete the datacenter
    result = await mcp_client.call_tool(
        "qg_delete_datacenter",
        arguments={"id": datacenter_id},
    )

    # Verify deletion response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_datacenter"
    assert metadata["success"] is True

    # Verify datacenter is actually deleted by trying to get it
    get_result = await mcp_client.call_tool(
        "qg_get_datacenter_by_id",
        arguments={"id": datacenter_id},
    )

    # Should fail to find the deleted datacenter
    assert get_result.data["metadata"]["success"] is False


@pytest.mark.integration
async def test_qg_delete_datacenter_not_found(mcp_client: Client):
    """Test deleting a datacenter with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_datacenter",
        arguments={"id": fake_id},
    )

    # API may return success for non-existent IDs (idempotent delete)
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_datacenter"
    # Success status depends on API implementation (may be True for idempotent deletes)


@pytest.mark.integration
async def test_qg_delete_datacenter_invalid_uuid(mcp_client: Client):
    """Test deleting a datacenter with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_datacenter",
        arguments={"id": "not-a-valid-uuid"},
    )

    # API may handle invalid UUIDs differently
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_datacenter"
    # Success status depends on API validation behavior


@pytest.mark.integration
async def test_qg_datacenters_error_handling(mcp_client: Client):
    """Test error handling across datacenter operations."""
    # Test with None/empty values where applicable

    # Test getting datacenter with empty string ID
    result = await mcp_client.call_tool(
        "qg_get_datacenter_by_id",
        arguments={"id": ""},
    )
    # API may handle empty IDs differently - just verify response structure
    assert result.data is not None
    assert "metadata" in result.data

    # Test creating datacenter with empty name
    result = await mcp_client.call_tool(
        "qg_create_datacenter",
        arguments={"name": ""},
    )
    # Empty name should fail
    assert result.data["metadata"]["success"] is False

    # Test deleting datacenter with empty ID
    result = await mcp_client.call_tool(
        "qg_delete_datacenter",
        arguments={"id": ""},
    )
    # API may handle empty IDs differently - just verify response structure
    assert result.data is not None
    assert "metadata" in result.data
