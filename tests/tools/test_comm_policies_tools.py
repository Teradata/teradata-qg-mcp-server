"""Integration tests for comm_policies_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from src.tools import set_qg_manager


@pytest.mark.integration
async def test_qg_get_comm_policies(mcp_client: Client):
    """Test getting all communication policies."""
    result = await mcp_client.call_tool("qg_get_comm_policies", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_comm_policies"
    assert metadata["success"] is True

    # Verify result is a list
    comm_policies = result.data["result"]
    assert isinstance(comm_policies, list), "Communication policies result should be a list"


@pytest.mark.integration
async def test_qg_get_comm_policies_with_filters(mcp_client: Client, qg_manager):
    """Test getting communication policies with filter parameters."""
    # First get all comm policies to find valid filter values
    all_policies = qg_manager.comm_policy_client.get_comm_policies()

    if not all_policies:
        pytest.skip("No communication policies available to test filtering")

    first_policy = all_policies[0]

    # Test with name filter
    policy_name = first_policy.get("name")
    if policy_name:
        result = await mcp_client.call_tool(
            "qg_get_comm_policies", arguments={"filter_by_name": policy_name}
        )

        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["success"] is True

        filtered_policies = result.data["result"]
        assert isinstance(filtered_policies, list)
        # Should find at least the policy we searched for
        if filtered_policies:
            assert any(p.get("name") == policy_name for p in filtered_policies)

    # Test with fabric_id filter
    fabric_id = first_policy.get("fabric", {}).get("id") if "fabric" in first_policy else None
    if fabric_id:
        result = await mcp_client.call_tool(
            "qg_get_comm_policies", arguments={"filter_by_fabric_id": fabric_id}
        )

        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["success"] is True

        filtered_policies = result.data["result"]
        assert isinstance(filtered_policies, list)


@pytest.mark.integration
async def test_qg_get_comm_policy_by_id(mcp_client: Client, qg_manager):
    """Test getting a specific communication policy by ID."""
    # First get all policies to find a valid policy ID
    policies = qg_manager.comm_policy_client.get_comm_policies()

    if not policies:
        pytest.skip("No communication policies available to test")

    policy_id = policies[0].get("id")
    assert policy_id is not None, "Policy should have an ID"

    # Get policy by ID
    result = await mcp_client.call_tool(
        "qg_get_comm_policy_by_id", arguments={"id": policy_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_comm_policy_by_id"
    assert metadata["success"] is True

    # Verify policy data
    policy = result.data["result"]
    assert isinstance(policy, dict)
    assert policy.get("id") == policy_id


@pytest.mark.integration
async def test_qg_get_comm_policy_by_id_not_found(mcp_client: Client):
    """Test getting a communication policy with invalid ID."""
    invalid_id = "00000000-0000-0000-0000-000000000000"

    result = await mcp_client.call_tool(
        "qg_get_comm_policy_by_id", arguments={"id": invalid_id}
    )

    # Should return error response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_comm_policy_by_id"
    # Expecting failure for non-existent policy
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_comm_policy_active(mcp_client: Client, qg_manager):
    """Test getting the active version of a communication policy."""
    # First get all policies to find one with active version
    policies = qg_manager.comm_policy_client.get_comm_policies()

    if not policies:
        pytest.skip("No communication policies available to test")

    policy_id = policies[0].get("id")

    result = await mcp_client.call_tool(
        "qg_get_comm_policy_active", arguments={"id": policy_id}
    )

    # Verify response structure
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_comm_policy_active"

    # May succeed or fail depending on whether active version exists
    if metadata["success"]:
        active_policy = result.data["result"]
        assert isinstance(active_policy, dict)


@pytest.mark.integration
async def test_qg_get_comm_policy_pending(mcp_client: Client, qg_manager):
    """Test getting the pending version of a communication policy."""
    # First get all policies to find one with pending version
    policies = qg_manager.comm_policy_client.get_comm_policies()

    if not policies:
        pytest.skip("No communication policies available to test")

    policy_id = policies[0].get("id")

    result = await mcp_client.call_tool(
        "qg_get_comm_policy_pending", arguments={"id": policy_id}
    )

    # Verify response structure
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_comm_policy_pending"

    # May succeed or fail depending on whether pending version exists
    if metadata["success"]:
        pending_policy = result.data["result"]
        assert isinstance(pending_policy, dict)


@pytest.mark.integration
async def test_qg_get_comm_policy_previous(mcp_client: Client, qg_manager):
    """Test getting the previous version of a communication policy."""
    # First get all policies to find one with previous version
    policies = qg_manager.comm_policy_client.get_comm_policies()

    if not policies:
        pytest.skip("No communication policies available to test")

    policy_id = policies[0].get("id")

    result = await mcp_client.call_tool(
        "qg_get_comm_policy_previous", arguments={"id": policy_id}
    )

    # Verify response structure
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_comm_policy_previous"

    # May succeed or fail depending on whether previous version exists
    if metadata["success"]:
        previous_policy = result.data["result"]
        assert isinstance(previous_policy, dict)


@pytest.mark.integration
async def test_qg_create_comm_policy(mcp_client: Client, qg_manager):
    """Test creating a new communication policy."""
    # Create a test comm policy with unique name
    unique_suffix = str(uuid.uuid4())[:8]
    policy_args = {
        "name": f"test_comm_policy_pytest_{unique_suffix}",
        "transfer_concurrency": 4,
        "description": "Test communication policy created by pytest",
        "security_algorithm": "AES_GCM",
        "compression_algorithm": "ZSTD",
    }

    result = await mcp_client.call_tool("qg_create_comm_policy", arguments=policy_args)

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_comm_policy"
    assert metadata["success"] is True, f"Policy creation failed: {result.data.get('result')}"

    # Verify created policy
    policy = result.data["result"]
    assert isinstance(policy, dict)
    assert policy.get("name") == policy_args["name"]
    assert policy.get("description") == "Test communication policy created by pytest"

    # Cleanup - delete the created policy
    policy_id = policy.get("id")
    if policy_id:
        try:
            qg_manager.comm_policy_client.delete_comm_policy(policy_id)
        except Exception:
            pass  # Ignore cleanup errors


@pytest.mark.integration
async def test_qg_create_comm_policy_minimal(mcp_client: Client, qg_manager):
    """Test creating a communication policy with minimal required parameters."""
    # Create policy with only required parameters and unique name
    unique_suffix = str(uuid.uuid4())[:8]
    policy_name = f"test_comm_policy_minimal_pytest_{unique_suffix}"
    result = await mcp_client.call_tool(
        "qg_create_comm_policy",
        arguments={
            "name": policy_name,
            "transfer_concurrency": 2,
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_comm_policy"
    assert metadata["success"] is True, f"Policy creation failed: {result.data.get('result')}"

    policy = result.data["result"]
    assert policy.get("name") == policy_name

    # Cleanup - delete the created policy
    policy_id = policy.get("id")
    if policy_id:
        try:
            qg_manager.comm_policy_client.delete_comm_policy(policy_id)
        except Exception:
            pass  # Ignore cleanup errors


@pytest.mark.integration
async def test_qg_delete_comm_policy(mcp_client: Client, qg_manager):
    """Test deleting a communication policy."""
    # Create a policy to delete
    unique_suffix = str(uuid.uuid4())[:8]
    policy_name = f"test_comm_policy_delete_pytest_{unique_suffix}"
    created_policy = qg_manager.comm_policy_client.create_comm_policy(
        name=policy_name,
        transfer_concurrency=2,
        description="Test policy for deletion",
    )

    assert isinstance(created_policy, dict), "Policy creation should return a dict"
    policy_id = created_policy.get("id")
    assert policy_id is not None, "Created policy should have an ID"

    # Delete the policy
    result = await mcp_client.call_tool(
        "qg_delete_comm_policy", arguments={"id": policy_id}
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_comm_policy"
    assert metadata["success"] is True, f"Policy deletion failed: {result.data.get('result')}"

    # Verify policy is deleted by trying to get it
    try:
        qg_manager.comm_policy_client.get_comm_policy_by_id(policy_id)
        # If we get here, policy still exists - test should fail
        pytest.fail("Policy should have been deleted but still exists")
    except Exception:
        # Expected - policy should not be found
        pass


@pytest.mark.integration
async def test_qg_delete_comm_policy_not_found(mcp_client: Client):
    """Test deleting a non-existent communication policy."""
    invalid_id = "00000000-0000-0000-0000-000000000000"

    result = await mcp_client.call_tool(
        "qg_delete_comm_policy", arguments={"id": invalid_id}
    )

    # API might return success even for non-existent resources
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_comm_policy"
    # Just verify we got a response, success may be True or False
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_comm_policies_error_handling(mcp_client: Client, qg_manager):
    """Test error handling when QueryGrid Manager is not available."""
    # Set manager to None to simulate unavailability
    set_qg_manager(None)

    result = await mcp_client.call_tool("qg_get_comm_policies", arguments={})

    # Verify error response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_comm_policies"
    assert metadata["success"] is False
    assert "error" in metadata

    # Restore manager for other tests
    set_qg_manager(qg_manager)
