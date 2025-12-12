"""Integration tests for user_mapping_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.fixture(scope="function")
async def test_user_mapping(mcp_client: Client):
    """
    Create a test user mapping for integration tests.

    This fixture creates a user mapping that can be used across test cases.
    The mapping is cleaned up after all tests complete.

    Returns:
        dict: Contains 'mapping_id' and 'mapping_name'
    """
    mapping_name = f"test_mapping_pytest_{uuid.uuid4().hex[:8]}"

    # Create test user mapping
    result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
            "description": "Test user mapping created by pytest fixture",
        },
    )

    mapping_data = {
        "mapping_id": None,
        "mapping_name": mapping_name,
    }

    if result.data and result.data.get("metadata", {}).get("success"):
        mapping_data["mapping_id"] = result.data["result"].get("id")
        print(f"\n✓ Created test user mapping: {mapping_data['mapping_id']}")

    yield mapping_data

    # Cleanup - delete the test user mapping
    if mapping_data.get("mapping_id"):
        try:
            await mcp_client.call_tool(
                "qg_delete_user_mapping",
                arguments={"mapping_id": mapping_data["mapping_id"]},
            )
            print(f"\n✓ Deleted test user mapping: {mapping_data['mapping_id']}")
        except Exception as e:
            print(f"\n⚠ Failed to delete test user mapping: {e}")


# Tests for qg_get_user_mappings


@pytest.mark.integration
async def test_qg_get_user_mappings_basic(mcp_client: Client):
    """Test getting all user mappings."""
    result = await mcp_client.call_tool(
        "qg_get_user_mappings",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_user_mappings"
    assert metadata["success"] is True

    # Should return list of user mappings
    if "result" in result.data:
        result_data = result.data["result"]
        assert isinstance(result_data, (list, dict))


@pytest.mark.integration
async def test_qg_get_user_mappings_filter_by_name(
    mcp_client: Client, test_user_mapping
):
    """Test getting user mappings filtered by name."""
    mapping_name = test_user_mapping["mapping_name"]

    result = await mcp_client.call_tool(
        "qg_get_user_mappings",
        arguments={
            "filter_by_name": mapping_name,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_user_mappings"
    assert metadata["success"] is True

    # Should find the test mapping
    if "result" in result.data:
        result_data = result.data["result"]
        if isinstance(result_data, list) and len(result_data) > 0:
            assert any(m.get("name") == mapping_name for m in result_data)


@pytest.mark.integration
async def test_qg_get_user_mappings_filter_by_name_wildcard(
    mcp_client: Client, test_user_mapping
):
    """Test getting user mappings filtered by name with wildcard."""
    result = await mcp_client.call_tool(
        "qg_get_user_mappings",
        arguments={
            "filter_by_name": "test_mapping_pytest*",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_user_mappings"
    assert metadata["success"] is True

    # Should find the test mapping with wildcard
    if "result" in result.data:
        result_data = result.data["result"]
        if isinstance(result_data, list):
            assert len(result_data) > 0


@pytest.mark.integration
async def test_qg_get_user_mappings_response_structure(mcp_client: Client):
    """Test user mappings response structure validation."""
    result = await mcp_client.call_tool(
        "qg_get_user_mappings",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


# Tests for qg_get_user_mapping_by_id


@pytest.mark.integration
async def test_qg_get_user_mapping_by_id_existing(
    mcp_client: Client, test_user_mapping
):
    """Test getting an existing user mapping by ID."""
    mapping_id = test_user_mapping["mapping_id"]

    if not mapping_id:
        pytest.skip("Test user mapping was not created successfully")

    result = await mcp_client.call_tool(
        "qg_get_user_mapping_by_id",
        arguments={"id": mapping_id},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_user_mapping_by_id"
    assert metadata["success"] is True

    # Should return the user mapping details
    if "result" in result.data:
        result_data = result.data["result"]
        assert isinstance(result_data, dict)
        assert result_data.get("id") == mapping_id


@pytest.mark.integration
async def test_qg_get_user_mapping_by_id_not_found(mcp_client: Client):
    """Test getting user mapping by non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_user_mapping_by_id",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_user_mapping_by_id"
    # API may return success=False or empty result for non-existent IDs
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_user_mapping_by_id_invalid_uuid(mcp_client: Client):
    """Test getting user mapping by invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_user_mapping_by_id",
        arguments={"id": "invalid-uuid-format"},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_user_mapping_by_id"
    # API may accept or reject invalid UUID formats


@pytest.mark.integration
async def test_qg_get_user_mapping_by_id_empty_id(mcp_client: Client):
    """Test getting user mapping by empty ID."""
    result = await mcp_client.call_tool(
        "qg_get_user_mapping_by_id",
        arguments={"id": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_user_mapping_by_id"
    # Empty ID may be accepted or rejected by API


@pytest.mark.integration
async def test_qg_get_user_mapping_by_id_response_structure(mcp_client: Client):
    """Test user mapping by ID response structure."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_user_mapping_by_id",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


# Tests for qg_create_user_mapping


@pytest.mark.integration
async def test_qg_create_user_mapping_basic(mcp_client: Client):
    """Test creating a user mapping with minimal required parameters."""
    mapping_name = f"test_mapping_pytest_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user_mapping"
    assert metadata["success"] is True

    # Clean up - delete created user mapping
    if "result" in result.data:
        created_mapping_id = result.data["result"].get("id")
        if created_mapping_id:
            await mcp_client.call_tool(
                "qg_delete_user_mapping",
                arguments={"mapping_id": created_mapping_id},
            )


@pytest.mark.integration
async def test_qg_create_user_mapping_with_description(mcp_client: Client):
    """Test creating a user mapping with description."""
    mapping_name = f"test_mapping_pytest_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
            "description": "Test user mapping created by pytest",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user_mapping"
    assert metadata["success"] is True

    # Clean up
    if "result" in result.data:
        created_mapping_id = result.data["result"].get("id")
        if created_mapping_id:
            await mcp_client.call_tool(
                "qg_delete_user_mapping",
                arguments={"mapping_id": created_mapping_id},
            )


@pytest.mark.integration
async def test_qg_create_user_mapping_with_user_mapping(mcp_client: Client):
    """Test creating a user mapping with user mapping dictionary."""
    mapping_name = f"test_mapping_pytest_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
            "user_mapping": {"test_user": "mapped_user"},
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user_mapping"
    assert metadata["success"] is True

    # Clean up
    if "result" in result.data:
        created_mapping_id = result.data["result"].get("id")
        if created_mapping_id:
            await mcp_client.call_tool(
                "qg_delete_user_mapping",
                arguments={"mapping_id": created_mapping_id},
            )


@pytest.mark.integration
async def test_qg_create_user_mapping_with_role_mapping(mcp_client: Client):
    """Test creating a user mapping with role mapping dictionary."""
    mapping_name = f"test_mapping_pytest_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
            "role_mapping": {"test_role": "mapped_role"},
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user_mapping"
    assert metadata["success"] is True

    # Clean up
    if "result" in result.data:
        created_mapping_id = result.data["result"].get("id")
        if created_mapping_id:
            await mcp_client.call_tool(
                "qg_delete_user_mapping",
                arguments={"mapping_id": created_mapping_id},
            )


@pytest.mark.integration
async def test_qg_create_user_mapping_with_all_parameters(mcp_client: Client):
    """Test creating a user mapping with all optional parameters."""
    mapping_name = f"test_mapping_pytest_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
            "user_mapping": {"test_user": "mapped_user"},
            "role_mapping": {"test_role": "mapped_role"},
            "description": "Test user mapping with all parameters",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user_mapping"
    assert metadata["success"] is True

    # Clean up
    if "result" in result.data:
        created_mapping_id = result.data["result"].get("id")
        if created_mapping_id:
            await mcp_client.call_tool(
                "qg_delete_user_mapping",
                arguments={"mapping_id": created_mapping_id},
            )


@pytest.mark.integration
async def test_qg_create_user_mapping_duplicate_name(mcp_client: Client):
    """Test creating a user mapping with duplicate name."""
    mapping_name = f"test_mapping_pytest_{uuid.uuid4().hex[:8]}"

    # Create first user mapping
    result1 = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
        },
    )

    assert result1.data is not None
    assert result1.data["metadata"]["success"] is True
    created_mapping_id = result1.data["result"].get("id")

    # Try to create duplicate
    result2 = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
        },
    )

    assert result2.data is not None
    metadata = result2.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user_mapping"
    # Should fail due to duplicate name
    assert metadata["success"] is False

    # Clean up
    if created_mapping_id:
        await mcp_client.call_tool(
            "qg_delete_user_mapping",
            arguments={"mapping_id": created_mapping_id},
        )


@pytest.mark.integration
async def test_qg_create_user_mapping_missing_required_params(mcp_client: Client):
    """Test creating a user mapping without required name parameter."""
    with pytest.raises(Exception):
        await mcp_client.call_tool(
            "qg_create_user_mapping",
            arguments={},
        )


# Tests for qg_delete_user_mapping


@pytest.mark.integration
async def test_qg_delete_user_mapping_not_found(mcp_client: Client):
    """Test deleting user mapping by non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_user_mapping",
        arguments={"mapping_id": fake_id},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_user_mapping"
    # Delete operations may be idempotent (success=True for non-existent IDs)


@pytest.mark.integration
async def test_qg_delete_user_mapping_invalid_uuid(mcp_client: Client):
    """Test deleting user mapping by invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_user_mapping",
        arguments={"mapping_id": "invalid-uuid-format"},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_user_mapping"


@pytest.mark.integration
async def test_qg_delete_user_mapping_empty_id(mcp_client: Client):
    """Test deleting user mapping by empty ID."""
    result = await mcp_client.call_tool(
        "qg_delete_user_mapping",
        arguments={"mapping_id": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_user_mapping"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_delete_user_mapping_success(mcp_client: Client):
    """Test successfully deleting a user mapping."""
    mapping_name = f"test_mapping_pytest_{uuid.uuid4().hex[:8]}"

    # Create user mapping first
    create_result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True

    created_mapping_id = create_result.data["result"].get("id")

    # Delete user mapping
    delete_result = await mcp_client.call_tool(
        "qg_delete_user_mapping",
        arguments={"mapping_id": created_mapping_id},
    )

    assert delete_result.data is not None
    metadata = delete_result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_user_mapping"
    assert metadata["success"] is True


# General tests


@pytest.mark.integration
async def test_qg_user_mappings_error_handling(mcp_client: Client):
    """Test error handling across user mapping tools."""
    # Test with completely invalid inputs
    result = await mcp_client.call_tool(
        "qg_get_user_mapping_by_id",
        arguments={"id": "not-a-valid-id"},
    )

    assert result.data is not None
    assert "metadata" in result.data


@pytest.mark.integration
async def test_qg_get_user_mappings_consistency(mcp_client: Client):
    """Test consistency of get_user_mappings responses."""
    # Call twice and verify structure is consistent
    result1 = await mcp_client.call_tool(
        "qg_get_user_mappings",
        arguments={},
    )

    result2 = await mcp_client.call_tool(
        "qg_get_user_mappings",
        arguments={},
    )

    assert result1.data is not None
    assert result2.data is not None

    # Both should have same structure
    assert "metadata" in result1.data
    assert "metadata" in result2.data

    assert (
        result1.data["metadata"]["tool_name"] == result2.data["metadata"]["tool_name"]
    )
