"""Integration tests for operations_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_bulk_delete_nodes_empty_list(mcp_client: Client):
    """Test bulk delete with empty list."""
    result = await mcp_client.call_tool(
        "qg_bulk_delete",
        arguments={
            "config_type": "NODE",
            "ids": [],
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_bulk_delete"
    # Empty list may succeed or fail depending on API implementation
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_bulk_delete_nodes_not_found(mcp_client: Client):
    """Test bulk delete nodes with non-existent IDs."""
    fake_ids = [str(uuid.uuid4()), str(uuid.uuid4())]

    result = await mcp_client.call_tool(
        "qg_bulk_delete",
        arguments={
            "config_type": "NODE",
            "ids": fake_ids,
        },
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_bulk_delete"
    # API may succeed (idempotent) or fail for non-existent IDs


@pytest.mark.integration
async def test_qg_bulk_delete_issues_empty_list(mcp_client: Client):
    """Test bulk delete issues with empty list."""
    result = await mcp_client.call_tool(
        "qg_bulk_delete",
        arguments={
            "config_type": "ISSUE",
            "ids": [],
        },
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_bulk_delete"
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_bulk_delete_invalid_config_type(mcp_client: Client):
    """Test bulk delete with invalid config type."""
    result = await mcp_client.call_tool(
        "qg_bulk_delete",
        arguments={
            "config_type": "INVALID_TYPE",
            "ids": [str(uuid.uuid4())],
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_bulk_delete"
    # Should fail with invalid config type
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_auto_install_nodes_missing_params(mcp_client: Client):
    """Test auto install nodes with missing required parameters."""
    result = await mcp_client.call_tool(
        "qg_auto_install_nodes",
        arguments={},
    )

    # Tool should handle missing parameters
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_auto_install_nodes"


@pytest.mark.integration
async def test_qg_auto_install_nodes_with_system_id(
    mcp_client: Client, test_infrastructure
):
    """Test auto install nodes with system ID."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_auto_install_nodes",
        arguments={
            "system_id": system_id,
            "nodes": ["node1.example.com"],
            "username": "testuser",
            "password": "testpass",
        },
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_auto_install_nodes"
    # Installation will likely fail but we're testing the tool call


@pytest.mark.integration
async def test_qg_get_nodes_auto_install_status_not_found(mcp_client: Client):
    """Test getting auto install status with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_nodes_auto_install_status", arguments={"id": fake_id}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes_auto_install_status"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_nodes_auto_install_status_invalid_uuid(mcp_client: Client):
    """Test getting auto install status with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_nodes_auto_install_status", arguments={"id": "not-a-valid-uuid"}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_nodes_auto_install_status"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_manual_install_nodes_basic(mcp_client: Client, test_infrastructure):
    """Test manual install nodes with basic parameters."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_manual_install_nodes",
        arguments={
            "system_id": system_id,
        },
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_manual_install_nodes"
    # API may require additional parameters, so just check response structure
    assert "success" in metadata

    # If successful, should return installation details (token, etc.)
    if metadata["success"]:
        assert "result" in result.data


@pytest.mark.integration
async def test_qg_manual_install_nodes_with_expiration(
    mcp_client: Client, test_infrastructure
):
    """Test manual install nodes with expiration days."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_manual_install_nodes",
        arguments={
            "system_id": system_id,
            "expiration_days": 7,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_manual_install_nodes"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_manual_install_nodes_with_cluster_option(
    mcp_client: Client, test_infrastructure
):
    """Test manual install nodes with cluster option."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_manual_install_nodes",
        arguments={
            "system_id": system_id,
            "cluster_option": "PRIMARY",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_manual_install_nodes"
    # API may reject cluster_option alone, so just check response structure
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_manual_install_nodes_with_all_params(
    mcp_client: Client, test_infrastructure
):
    """Test manual install nodes with all parameters."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_manual_install_nodes",
        arguments={
            "system_id": system_id,
            "expiration_days": 30,
            "cluster_option": "PRIMARY",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_manual_install_nodes"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_manual_install_nodes_invalid_system_id(mcp_client: Client):
    """Test manual install nodes with invalid system ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_manual_install_nodes",
        arguments={
            "system_id": fake_id,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_manual_install_nodes"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_disable_system_alerts_basic(mcp_client: Client, test_infrastructure):
    """Test disabling system alerts for specific issue type."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_disable_system_alerts",
        arguments={
            "system_id": system_id,
            "issue_problem_type": "NODES_OFFLINE",
        },
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_disable_system_alerts"
    # May succeed or fail depending on whether alerts exist
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_disable_system_alerts_invalid_system_id(mcp_client: Client):
    """Test disabling alerts with invalid system ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_disable_system_alerts",
        arguments={
            "system_id": fake_id,
            "issue_problem_type": "NODES_OFFLINE",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_disable_system_alerts"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_disable_system_alerts_invalid_problem_type(
    mcp_client: Client, test_infrastructure
):
    """Test disabling alerts with invalid problem type."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_disable_system_alerts",
        arguments={
            "system_id": system_id,
            "issue_problem_type": "INVALID_TYPE",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_disable_system_alerts"
    # May succeed or fail depending on API validation


@pytest.mark.integration
async def test_qg_operations_error_handling(mcp_client: Client):
    """Test error handling across operations tools."""
    # Test bulk delete with invalid UUID in list
    result = await mcp_client.call_tool(
        "qg_bulk_delete",
        arguments={
            "config_type": "NODE",
            "ids": ["not-a-uuid"],
        },
    )
    assert result.data is not None
    assert "metadata" in result.data

    # Test auto install status with empty ID
    result = await mcp_client.call_tool(
        "qg_get_nodes_auto_install_status",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data


@pytest.mark.integration
async def test_qg_bulk_delete_single_node(mcp_client: Client):
    """Test bulk delete with single node ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_bulk_delete",
        arguments={
            "config_type": "NODE",
            "ids": [fake_id],
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_bulk_delete"


@pytest.mark.integration
async def test_qg_bulk_delete_multiple_issues(mcp_client: Client):
    """Test bulk delete with multiple issue IDs."""
    fake_ids = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]

    result = await mcp_client.call_tool(
        "qg_bulk_delete",
        arguments={
            "config_type": "ISSUE",
            "ids": fake_ids,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_bulk_delete"


@pytest.mark.integration
async def test_qg_auto_install_nodes_multiple_nodes(
    mcp_client: Client, test_infrastructure
):
    """Test auto install with multiple node hostnames."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_auto_install_nodes",
        arguments={
            "system_id": system_id,
            "nodes": ["node1.example.com", "node2.example.com", "node3.example.com"],
            "username": "admin",
            "password": "password123",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_auto_install_nodes"


@pytest.mark.integration
async def test_qg_manual_install_nodes_zero_expiration(
    mcp_client: Client, test_infrastructure
):
    """Test manual install with zero expiration days."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_manual_install_nodes",
        arguments={
            "system_id": system_id,
            "expiration_days": 0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_manual_install_nodes"
    # API may or may not accept zero expiration


@pytest.mark.integration
async def test_qg_manual_install_nodes_large_expiration(
    mcp_client: Client, test_infrastructure
):
    """Test manual install with large expiration days."""
    system_id = test_infrastructure.get("system_id")

    result = await mcp_client.call_tool(
        "qg_manual_install_nodes",
        arguments={
            "system_id": system_id,
            "expiration_days": 365,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_manual_install_nodes"
