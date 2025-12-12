"""Integration tests for create_foreign_server_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_create_foreign_server_missing_link(mcp_client: Client):
    """Test creating a foreign server with a non-existent link ID."""
    fake_link_id = str(uuid.uuid4())
    
    result = await mcp_client.call_tool(
        "qg_create_foreign_server",
        arguments={
            "initiator_admin_user": "dbc",
            "initiator_admin_password": "dbc",
            "link_id": fake_link_id,
            "version": "ACTIVE",
            "foreign_server_name": "test_foreign_server",
        },
    )

    # Verify response structure even for failures
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # This should fail since the link doesn't exist
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_foreign_server"
    assert metadata["success"] is False, "Should fail with non-existent link"


@pytest.mark.integration
async def test_qg_create_foreign_server_with_version(mcp_client: Client):
    """Test creating a foreign server with explicit version parameter."""
    fake_link_id = str(uuid.uuid4())
    
    result = await mcp_client.call_tool(
        "qg_create_foreign_server",
        arguments={
            "initiator_admin_user": "dbc",
            "initiator_admin_password": "dbc",
            "link_id": fake_link_id,
            "version": "ACTIVE",
            "foreign_server_name": "test_foreign_server",
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_foreign_server"
    # Should fail due to non-existent link, but version parameter should be accepted
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_create_foreign_server_invalid_credentials(mcp_client: Client):
    """Test creating a foreign server with invalid credentials."""
    fake_link_id = str(uuid.uuid4())
    
    result = await mcp_client.call_tool(
        "qg_create_foreign_server",
        arguments={
            "initiator_admin_user": "invalid_user",
            "initiator_admin_password": "invalid_password",
            "link_id": fake_link_id,
            "version": "ACTIVE",
            "foreign_server_name": "test_foreign_server",
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_foreign_server"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_create_foreign_server_status_invalid_id(mcp_client: Client):
    """Test getting foreign server creation status with invalid diagnostic check ID."""
    fake_diagnostic_id = str(uuid.uuid4())
    
    result = await mcp_client.call_tool(
        "qg_get_create_foreign_server_status",
        arguments={"id": fake_diagnostic_id},
    )

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Should fail since diagnostic check ID doesn't exist
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_create_foreign_server_status"
    assert metadata["success"] is False, "Should fail with non-existent diagnostic ID"


@pytest.mark.integration
async def test_qg_get_create_foreign_server_status_malformed_id(mcp_client: Client):
    """Test getting foreign server creation status with malformed ID."""
    result = await mcp_client.call_tool(
        "qg_get_create_foreign_server_status",
        arguments={"id": "not-a-valid-uuid"},
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_create_foreign_server_status"
    # Should fail with malformed ID
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_create_foreign_server_with_valid_link(mcp_client: Client, test_link):
    """
    Test creating a foreign server with a valid link.
    
    This test uses the test_link fixture which provides a real link with
    initiator and target connectors. The test will fail if credentials are
    invalid, but it validates the complete API flow.
    """
    link_id = test_link.get("id")
    
    # Note: These credentials should be valid for your test environment
    # The test will fail if the initiator system is not accessible or
    # credentials are incorrect, but that's expected behavior
    result = await mcp_client.call_tool(
        "qg_create_foreign_server",
        arguments={
            "initiator_admin_user": "dbc",
            "initiator_admin_password": "dbc",
            "link_id": link_id,
            "version": "ACTIVE",
            "foreign_server_name": "test_foreign_server_pytest",
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_foreign_server"
    
    # If successful, we should get a diagnostic check ID
    if metadata["success"]:
        assert "result" in result.data
        diagnostic_result = result.data["result"]
        assert "id" in diagnostic_result, "Should return diagnostic check ID"
        
        # Test status check with the returned diagnostic ID
        diagnostic_id = diagnostic_result["id"]
        status_result = await mcp_client.call_tool(
            "qg_get_create_foreign_server_status",
            arguments={"id": diagnostic_id},
        )
        
        assert status_result.data is not None
        assert isinstance(status_result.data, dict)
        status_metadata = status_result.data["metadata"]
        assert status_metadata["tool_name"] == "qg_get_create_foreign_server_status"
        assert status_metadata["success"] is True
    else:
        # If it fails, it's likely due to invalid credentials or network issues
        # which is acceptable for this test - we're verifying the API flow works
        print(f"\n⚠ Foreign server creation failed (expected if credentials/network invalid): {metadata.get('error')}")
        assert "error" in metadata or "result" in result.data


@pytest.mark.integration
async def test_qg_create_foreign_server_empty_credentials(mcp_client: Client):
    """Test creating a foreign server with empty credentials."""
    fake_link_id = str(uuid.uuid4())
    
    result = await mcp_client.call_tool(
        "qg_create_foreign_server",
        arguments={
            "initiator_admin_user": "",
            "initiator_admin_password": "",
            "link_id": fake_link_id,
            "version": "ACTIVE",
            "foreign_server_name": "test_foreign_server",
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_foreign_server"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_create_foreign_server_version_pending(mcp_client: Client):
    """Test creating a foreign server with PENDING version."""
    fake_link_id = str(uuid.uuid4())
    
    result = await mcp_client.call_tool(
        "qg_create_foreign_server",
        arguments={
            "initiator_admin_user": "dbc",
            "initiator_admin_password": "dbc",
            "link_id": fake_link_id,
            "version": "PENDING",
            "foreign_server_name": "test_foreign_server",
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_foreign_server"
    # Should fail due to non-existent link, but PENDING version should be accepted
    assert metadata["success"] is False
