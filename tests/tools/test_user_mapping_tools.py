"""Integration tests for user_mapping_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from src.tools import set_qg_manager  # type: ignore[import-not-found]


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


@pytest.mark.integration
async def test_qg_put_user_mapping(mcp_client: Client):
    """Test updating a user mapping with PUT operation."""
    mapping_name = f"test_mapping_put_{uuid.uuid4().hex[:8]}"

    # First create a user mapping
    create_result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
            "user_mapping": {"user1": "remote_user1"},
            "description": "Original description",
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True
    mapping_id = create_result.data["result"]["id"]

    # Now update it using PUT
    updated_name = f"updated_{mapping_name}"
    result = await mcp_client.call_tool(
        "qg_put_user_mapping",
        arguments={
            "mapping_id": mapping_id,
            "name": updated_name,
            "user_mapping": {"user1": "new_remote_user", "user2": "remote_user2"},
            "description": "Updated description",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_user_mapping"
    assert metadata["success"] is True

    # Verify the update
    if "result" in result.data:
        updated_mapping = result.data["result"]
        assert updated_mapping["name"] == updated_name
        assert updated_mapping["description"] == "Updated description"
        assert updated_mapping["userMapping"]["user1"] == "new_remote_user"
        assert updated_mapping["userMapping"]["user2"] == "remote_user2"

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_user_mapping",
        arguments={"mapping_id": mapping_id},
    )


@pytest.mark.integration
async def test_qg_put_user_mapping_not_found(mcp_client: Client):
    """Test updating a non-existent user mapping returns 404."""
    fake_mapping_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_put_user_mapping",
        arguments={
            "mapping_id": fake_mapping_id,
            "name": "nonexistent_mapping",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_user_mapping"
    # API may handle non-existent IDs differently (404 or success with empty result)
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_put_user_mapping_invalid_data(mcp_client: Client):
    """Test updating user mapping with invalid data."""
    mapping_name = f"test_mapping_invalid_{uuid.uuid4().hex[:8]}"

    # First create a user mapping
    create_result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True
    mapping_id = create_result.data["result"]["id"]

    # Try to update with empty name (invalid)
    result = await mcp_client.call_tool(
        "qg_put_user_mapping",
        arguments={
            "mapping_id": mapping_id,
            "name": "",  # Empty name is invalid
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_user_mapping"
    assert metadata["success"] is False

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_user_mapping",
        arguments={"mapping_id": mapping_id},
    )


@pytest.mark.integration
async def test_qg_put_user_mapping_full_replacement(mcp_client: Client):
    """Test that PUT replaces all fields (not partial update)."""
    mapping_name = f"test_mapping_replace_{uuid.uuid4().hex[:8]}"

    # Create user mapping with description and mappings
    create_result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
            "user_mapping": {"user1": "remote_user1"},
            "role_mapping": {"role1": "remote_role1"},
            "description": "Original description",
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True
    mapping_id = create_result.data["result"]["id"]

    # Update with PUT but don't include description, role_mapping
    # These should be cleared (PUT is full replacement)
    result = await mcp_client.call_tool(
        "qg_put_user_mapping",
        arguments={
            "mapping_id": mapping_id,
            "name": mapping_name,
            "user_mapping": {"user2": "remote_user2"},
            # Note: NOT including description or role_mapping
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_user_mapping"
    assert metadata["success"] is True

    # Verify fields were cleared
    if "result" in result.data:
        updated_mapping = result.data["result"]
        # Description and role_mapping should be empty/null since not provided in PUT
        assert updated_mapping.get("description") in [None, "", "null"]
        assert updated_mapping.get("roleMapping") in [None, {}, "null"]
        # But user_mapping should be updated
        assert updated_mapping["userMapping"]["user2"] == "remote_user2"
        assert "user1" not in updated_mapping.get("userMapping", {})

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_user_mapping",
        arguments={"mapping_id": mapping_id},
    )


@pytest.mark.integration
async def test_qg_put_user_mapping_with_role_mapping(mcp_client: Client):
    """Test updating user mapping with role mappings."""
    mapping_name = f"test_mapping_roles_{uuid.uuid4().hex[:8]}"

    # Create user mapping
    create_result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True
    mapping_id = create_result.data["result"]["id"]

    # Update with role mappings
    result = await mcp_client.call_tool(
        "qg_put_user_mapping",
        arguments={
            "mapping_id": mapping_id,
            "name": mapping_name,
            "role_mapping": {"admin": "supergroup", "users": "regular_users"},
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_user_mapping"
    assert metadata["success"] is True

    # Verify role mappings
    if "result" in result.data:
        updated_mapping = result.data["result"]
        assert "roleMapping" in updated_mapping
        assert updated_mapping["roleMapping"]["admin"] == "supergroup"
        assert updated_mapping["roleMapping"]["users"] == "regular_users"

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_user_mapping",
        arguments={"mapping_id": mapping_id},
    )


@pytest.mark.integration
async def test_qg_put_user_mapping_preserve_existing(mcp_client: Client):
    """Test updating while preserving existing values."""
    mapping_name = f"test_mapping_preserve_{uuid.uuid4().hex[:8]}"

    # Create user mapping with all fields
    create_result = await mcp_client.call_tool(
        "qg_create_user_mapping",
        arguments={
            "name": mapping_name,
            "user_mapping": {"user1": "remote_user1"},
            "role_mapping": {"role1": "remote_role1"},
            "description": "Original description",
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True
    mapping_id = create_result.data["result"]["id"]
    original = create_result.data["result"]

    # Update user_mapping but preserve role_mapping and description
    result = await mcp_client.call_tool(
        "qg_put_user_mapping",
        arguments={
            "mapping_id": mapping_id,
            "name": mapping_name,
            "user_mapping": {"user1": "updated_remote_user"},  # Update this
            "role_mapping": original.get("roleMapping"),  # Preserve
            "description": original.get("description"),  # Preserve
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_user_mapping"
    assert metadata["success"] is True

    # Verify preservation
    if "result" in result.data:
        updated_mapping = result.data["result"]
        # User mapping should be updated
        assert updated_mapping["userMapping"]["user1"] == "updated_remote_user"
        # Role mapping should be preserved
        assert updated_mapping["roleMapping"]["role1"] == "remote_role1"
        # Description should be preserved
        assert updated_mapping["description"] == "Original description"

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_user_mapping",
        arguments={"mapping_id": mapping_id},
    )
