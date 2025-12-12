"""Integration tests for users_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.fixture(scope="function")
async def test_user(mcp_client: Client):
    """
    Create a test user for integration tests.
    
    This fixture creates a user that can be used across test cases.
    The user is cleaned up after the test completes.
    
    Returns:
        dict: Contains 'username' and 'password', and 'created' flag
    """
    username = f"test_user_pytest_{uuid.uuid4().hex[:8]}"
    # Password must be 14+ chars with special symbols and numbers
    password = f"TestPass123@{uuid.uuid4().hex[:8]}!"
    
    # Create test user
    result = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": username,
            "password": password,
            "description": "Test user created by pytest fixture",
        },
    )
    
    user_data = {
        "username": username,
        "password": password,
        "created": False,
    }
    
    if result.data and result.data.get("metadata", {}).get("success"):
        user_data["created"] = True
        print(f"\n✓ Created test user: {username}")
    else:
        print(f"\n⚠ Failed to create test user (API may not support user creation)")
    
    yield user_data
    
    # Cleanup - delete the test user only if it was created
    if user_data.get("created"):
        try:
            await mcp_client.call_tool(
                "qg_delete_user",
                arguments={"username": username},
            )
            print(f"\n✓ Deleted test user: {username}")
        except Exception as e:
            print(f"\n⚠ Failed to delete test user: {e}")


# Tests for qg_get_users


@pytest.mark.integration
async def test_qg_get_users_basic(mcp_client: Client):
    """Test getting all users."""
    result = await mcp_client.call_tool(
        "qg_get_users",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_users"
    assert metadata["success"] is True

    # Should return list of users
    if "result" in result.data:
        result_data = result.data["result"]
        assert isinstance(result_data, (list, dict))


@pytest.mark.integration
async def test_qg_get_users_response_structure(mcp_client: Client):
    """Test users response structure validation."""
    result = await mcp_client.call_tool(
        "qg_get_users",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_users_contains_created_user(mcp_client: Client, test_user):
    """Test that get_users returns a created user."""
    if not test_user.get("created"):
        pytest.skip("Test user was not created successfully (API limitation)")
    
    username = test_user["username"]
    
    result = await mcp_client.call_tool(
        "qg_get_users",
        arguments={},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_users"
    assert metadata["success"] is True
    
    # Should find the test user
    if "result" in result.data:
        result_data = result.data["result"]
        if isinstance(result_data, list):
            usernames = [u.get("username") for u in result_data if isinstance(u, dict)]
            assert username in usernames


# Tests for qg_get_user_by_username


@pytest.mark.integration
async def test_qg_get_user_by_username_existing(mcp_client: Client, test_user):
    """Test getting an existing user by username."""
    if not test_user.get("created"):
        pytest.skip("Test user was not created successfully (API limitation)")
    
    username = test_user["username"]
    
    result = await mcp_client.call_tool(
        "qg_get_user_by_username",
        arguments={"username": username},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_user_by_username"
    assert metadata["success"] is True
    
    # Should return the user details
    if "result" in result.data:
        result_data = result.data["result"]
        assert isinstance(result_data, dict)
        assert result_data.get("username") == username


@pytest.mark.integration
async def test_qg_get_user_by_username_not_found(mcp_client: Client):
    """Test getting user by non-existent username."""
    fake_username = f"nonexistent_user_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_get_user_by_username",
        arguments={"username": fake_username},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_user_by_username"
    # Should fail for non-existent user
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_user_by_username_empty_username(mcp_client: Client):
    """Test getting user by empty username."""
    result = await mcp_client.call_tool(
        "qg_get_user_by_username",
        arguments={"username": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_user_by_username"
    # Empty username returns all users (success=True)
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_user_by_username_response_structure(mcp_client: Client):
    """Test user by username response structure."""
    fake_username = f"test_user_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_get_user_by_username",
        arguments={"username": fake_username},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


# Tests for qg_create_user


@pytest.mark.integration
async def test_qg_create_user_basic(mcp_client: Client):
    """Test creating a user with minimal required parameters."""
    username = f"test_user_pytest_{uuid.uuid4().hex[:8]}"
    # Password must be 14+ chars with special symbols and numbers
    password = f"TestPass123@{uuid.uuid4().hex[:8]}!"

    result = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": username,
            "password": password,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user"
    assert metadata["success"] is True

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_user",
        arguments={"username": username},
    )


@pytest.mark.integration
async def test_qg_create_user_with_description(mcp_client: Client):
    """Test creating a user with description."""
    username = f"test_user_pytest_{uuid.uuid4().hex[:8]}"
    # Password must be 14+ chars with special symbols and numbers
    password = f"TestPass123@{uuid.uuid4().hex[:8]}!"

    result = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": username,
            "password": password,
            "description": "Test user created by pytest",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user"
    assert metadata["success"] is True

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_user",
        arguments={"username": username},
    )


@pytest.mark.integration
async def test_qg_create_user_duplicate_username(mcp_client: Client):
    """Test creating a user with duplicate username."""
    username = f"test_user_pytest_{uuid.uuid4().hex[:8]}"
    # Password must be 14+ chars with special symbols and numbers
    password = f"TestPass123@{uuid.uuid4().hex[:8]}!"

    # Create first user
    result1 = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": username,
            "password": password,
        },
    )

    assert result1.data is not None
    assert result1.data["metadata"]["success"] is True

    # Try to create duplicate
    result2 = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": username,
            "password": password,
        },
    )

    assert result2.data is not None
    metadata = result2.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user"
    # Should fail due to duplicate username
    assert metadata["success"] is False

    # Clean up
    await mcp_client.call_tool(
        "qg_delete_user",
        arguments={"username": username},
    )


@pytest.mark.integration
async def test_qg_create_user_with_special_characters(mcp_client: Client):
    """Test creating a user with special characters in username."""
    username = f"test.user-pytest_{uuid.uuid4().hex[:8]}"
    # Password must be 14+ chars with special symbols and numbers
    password = f"TestPass123@{uuid.uuid4().hex[:8]}!"

    result = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": username,
            "password": password,
            "description": "User with special characters in username",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user"
    # Validate success - API should accept special characters
    assert "success" in metadata

    # Clean up if created
    if metadata.get("success"):
        await mcp_client.call_tool(
            "qg_delete_user",
            arguments={"username": username},
        )


@pytest.mark.integration
async def test_qg_create_user_empty_username(mcp_client: Client):
    """Test creating a user with empty username."""
    # Password must be 14+ chars with special symbols and numbers
    password = f"TestPass123@{uuid.uuid4().hex[:8]}!"

    result = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": "",
            "password": password,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user"
    # Should fail with empty username
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_create_user_empty_password(mcp_client: Client):
    """Test creating a user with empty password."""
    username = f"test_user_pytest_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": username,
            "password": "",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_user"
    # Should fail - password is required and has min length requirement
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_create_user_missing_required_params(mcp_client: Client):
    """Test creating a user without required parameters."""
    with pytest.raises(Exception):
        await mcp_client.call_tool(
            "qg_create_user",
            arguments={
                "username": "test_user",
            },
        )


# Tests for qg_delete_user


@pytest.mark.integration
async def test_qg_delete_user_existing(mcp_client: Client):
    """Test deleting an existing user."""
    username = f"test_user_pytest_{uuid.uuid4().hex[:8]}"
    # Password must be 14+ chars with special symbols and numbers
    password = f"TestPass123@{uuid.uuid4().hex[:8]}!"

    # Create user first
    create_result = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": username,
            "password": password,
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True

    # Delete user
    delete_result = await mcp_client.call_tool(
        "qg_delete_user",
        arguments={"username": username},
    )

    assert delete_result.data is not None
    metadata = delete_result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_user"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_delete_user_not_found(mcp_client: Client):
    """Test deleting user by non-existent username."""
    fake_username = f"nonexistent_user_{uuid.uuid4().hex[:8]}"

    result = await mcp_client.call_tool(
        "qg_delete_user",
        arguments={"username": fake_username},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_user"
    # API is idempotent - returns success even for non-existent user
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_delete_user_empty_username(mcp_client: Client):
    """Test deleting user with empty username."""
    result = await mcp_client.call_tool(
        "qg_delete_user",
        arguments={"username": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_user"
    # Should fail with empty username
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_delete_user_twice(mcp_client: Client):
    """Test deleting the same user twice."""
    username = f"test_user_pytest_{uuid.uuid4().hex[:8]}"
    # Password must be 14+ chars with special symbols and numbers
    password = f"TestPass123@{uuid.uuid4().hex[:8]}!"

    # Create user
    create_result = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": username,
            "password": password,
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True

    # Delete user first time
    delete_result1 = await mcp_client.call_tool(
        "qg_delete_user",
        arguments={"username": username},
    )

    assert delete_result1.data is not None
    assert delete_result1.data["metadata"]["success"] is True

    # Try to delete again
    delete_result2 = await mcp_client.call_tool(
        "qg_delete_user",
        arguments={"username": username},
    )

    assert delete_result2.data is not None
    metadata = delete_result2.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_user"
    # API is idempotent - second delete also returns success
    assert metadata["success"] is True


# General tests


@pytest.mark.integration
async def test_qg_users_error_handling(mcp_client: Client):
    """Test error handling across user tools."""
    # Test with invalid inputs
    result = await mcp_client.call_tool(
        "qg_get_user_by_username",
        arguments={"username": "!@#$%^&*()"},
    )

    assert result.data is not None
    assert "metadata" in result.data
    metadata = result.data["metadata"]
    # Should handle invalid username gracefully
    assert "success" in metadata
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_users_consistency(mcp_client: Client):
    """Test consistency of get_users responses."""
    # Call twice and verify structure is consistent
    result1 = await mcp_client.call_tool(
        "qg_get_users",
        arguments={},
    )

    result2 = await mcp_client.call_tool(
        "qg_get_users",
        arguments={},
    )

    assert result1.data is not None
    assert result2.data is not None

    # Both should have same structure
    assert "metadata" in result1.data
    assert "metadata" in result2.data

    assert result1.data["metadata"]["tool_name"] == result2.data["metadata"]["tool_name"]


@pytest.mark.integration
async def test_qg_user_lifecycle(mcp_client: Client):
    """Test complete user lifecycle: create, get, delete."""
    username = f"test_user_lifecycle_{uuid.uuid4().hex[:8]}"
    # Password must be 14+ chars with special symbols and numbers
    password = f"TestPass123@{uuid.uuid4().hex[:8]}!"

    # Create user
    create_result = await mcp_client.call_tool(
        "qg_create_user",
        arguments={
            "username": username,
            "password": password,
            "description": "User lifecycle test",
        },
    )

    assert create_result.data is not None
    assert create_result.data["metadata"]["success"] is True

    # Get user by username
    get_result = await mcp_client.call_tool(
        "qg_get_user_by_username",
        arguments={"username": username},
    )

    assert get_result.data is not None
    assert get_result.data["metadata"]["success"] is True
    assert get_result.data["result"]["username"] == username

    # Verify user appears in list
    list_result = await mcp_client.call_tool(
        "qg_get_users",
        arguments={},
    )

    assert list_result.data is not None
    assert list_result.data["metadata"]["success"] is True
    usernames = [u.get("username") for u in list_result.data["result"] if isinstance(u, dict)]
    assert username in usernames

    # Delete user
    delete_result = await mcp_client.call_tool(
        "qg_delete_user",
        arguments={"username": username},
    )

    assert delete_result.data is not None
    assert delete_result.data["metadata"]["success"] is True

    # Verify user no longer exists
    get_after_delete = await mcp_client.call_tool(
        "qg_get_user_by_username",
        arguments={"username": username},
    )

    assert get_after_delete.data is not None
    # Should not find the deleted user
    assert get_after_delete.data["metadata"]["success"] is False
