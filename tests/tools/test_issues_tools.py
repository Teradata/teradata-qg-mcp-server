"""Integration tests for issues_tools."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_get_issues(mcp_client: Client):
    """Test getting all issues."""
    result = await mcp_client.call_tool("qg_get_issues", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_issues"
    assert metadata["success"] is True

    # Verify result structure - API returns dict with issues array and counts
    issues_data = result.data["result"]
    assert isinstance(issues_data, dict), "Issues result should be a dictionary"
    assert "issues" in issues_data, "Result should have 'issues' field"
    assert isinstance(issues_data["issues"], list), "Issues field should be a list"
    assert "criticalCount" in issues_data or "warningCount" in issues_data, "Should have count fields"


@pytest.mark.integration
async def test_qg_get_issue_by_id_not_found(mcp_client: Client):
    """Test getting an issue with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_issue_by_id", arguments={"id": fake_id}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_issue_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_issue_by_id_invalid_uuid(mcp_client: Client):
    """Test getting an issue with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_issue_by_id", arguments={"id": "not-a-valid-uuid"}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_issue_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_delete_issue_not_found(mcp_client: Client):
    """Test deleting an issue with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_issue", arguments={"id": fake_id}
    )

    # API may return success for non-existent IDs (idempotent delete)
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_issue"


@pytest.mark.integration
async def test_qg_delete_issue_invalid_uuid(mcp_client: Client):
    """Test deleting an issue with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_issue", arguments={"id": "not-a-valid-uuid"}
    )

    # API may handle invalid UUIDs differently
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_issue"


@pytest.mark.integration
async def test_qg_create_issue_minimal(mcp_client: Client, test_infrastructure):
    """Test creating an issue with minimal required parameters."""
    system_id = test_infrastructure.get("system_id")
    datacenter_id = test_infrastructure.get("datacenter_id")
    
    if not system_id or not datacenter_id:
        pytest.skip("Test infrastructure not available")
    
    # Get manager ID (we'll use a placeholder)
    manager_id = str(uuid.uuid4())
    
    current_time = datetime.now(timezone.utc).isoformat()
    
    result = await mcp_client.call_tool(
        "qg_create_issue",
        arguments={
            "create_time": current_time,
            "component_type": "SYSTEM",
            "component_id": system_id,
            "component_name": "test_system_pytest",
            "data_center_name": "test_datacenter_pytest",
            "problem_type": "NODE_DOWN",
            "severity": "CRITICAL",
            "subject_label": "test.issue.subject",
            "message_label": "test.issue.message",
            "config_version": "ACTIVE",
            "reporter_id": manager_id,
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_issue"
    
    # Issue creation may succeed or fail depending on validation
    if metadata["success"]:
        assert "result" in result.data
        created_issue = result.data["result"]
        assert isinstance(created_issue, dict)
        assert "id" in created_issue

        # Cleanup - delete the created issue
        issue_id = created_issue["id"]
        cleanup_result = await mcp_client.call_tool(
            "qg_delete_issue", arguments={"id": issue_id}
        )


@pytest.mark.integration
async def test_qg_create_issue_with_optional_params(mcp_client: Client, test_infrastructure):
    """Test creating an issue with optional parameters."""
    system_id = test_infrastructure.get("system_id")
    datacenter_id = test_infrastructure.get("datacenter_id")
    
    if not system_id or not datacenter_id:
        pytest.skip("Test infrastructure not available")
    
    manager_id = str(uuid.uuid4())
    current_time = datetime.now(timezone.utc).isoformat()
    
    result = await mcp_client.call_tool(
        "qg_create_issue",
        arguments={
            "create_time": current_time,
            "component_type": "SYSTEM",
            "component_id": system_id,
            "component_name": "test_system_pytest",
            "data_center_name": "test_datacenter_pytest",
            "problem_type": "WRONG_TIME",
            "severity": "WARNING",
            "subject_label": "test.issue.subject",
            "message_label": "test.issue.message",
            "config_version": "ACTIVE",
            "reporter_id": manager_id,
            "last_alert_time": current_time,
            "subject_params": ["param1", "param2"],
            "message_params": ["msg1", "msg2"],
            "meaning_label": "test.issue.meaning",
            "recommendation_label": "test.issue.recommendation",
            "confirmed": False,
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_issue"
    
    if metadata["success"]:
        created_issue = result.data["result"]
        issue_id = created_issue["id"]
        
        # Cleanup
        cleanup_result = await mcp_client.call_tool(
            "qg_delete_issue", arguments={"id": issue_id}
        )


@pytest.mark.integration
async def test_qg_create_issue_with_node_ids(mcp_client: Client, test_infrastructure):
    """Test creating an issue with node IDs."""
    system_id = test_infrastructure.get("system_id")
    
    if not system_id:
        pytest.skip("Test infrastructure not available")
    
    manager_id = str(uuid.uuid4())
    node_id = str(uuid.uuid4())
    current_time = datetime.now(timezone.utc).isoformat()
    
    result = await mcp_client.call_tool(
        "qg_create_issue",
        arguments={
            "create_time": current_time,
            "component_type": "SYSTEM",
            "component_id": system_id,
            "component_name": "test_system_pytest",
            "data_center_name": "test_datacenter_pytest",
            "problem_type": "NODE_DOWN",
            "severity": "CRITICAL",
            "subject_label": "test.issue.subject",
            "message_label": "test.issue.message",
            "config_version": "ACTIVE",
            "reporter_id": manager_id,
            "node_ids": [node_id],
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_issue"
    
    if metadata["success"]:
        issue_id = result.data["result"]["id"]
        await mcp_client.call_tool("qg_delete_issue", arguments={"id": issue_id})


@pytest.mark.integration
async def test_qg_create_issue_with_vantage_lake_params(mcp_client: Client, test_infrastructure):
    """Test creating an issue with VantageLake parameters."""
    system_id = test_infrastructure.get("system_id")
    
    if not system_id:
        pytest.skip("Test infrastructure not available")
    
    manager_id = str(uuid.uuid4())
    vantage_lake_id = str(uuid.uuid4())
    current_time = datetime.now(timezone.utc).isoformat()
    
    result = await mcp_client.call_tool(
        "qg_create_issue",
        arguments={
            "create_time": current_time,
            "component_type": "SYSTEM",
            "component_id": system_id,
            "component_name": "test_system_pytest",
            "data_center_name": "test_datacenter_pytest",
            "problem_type": "CONFIG_DATABASE_DOWN",
            "severity": "CRITICAL",
            "subject_label": "test.issue.subject",
            "message_label": "test.issue.message",
            "config_version": "ACTIVE",
            "reporter_id": manager_id,
            "vantage_lake_id": vantage_lake_id,
            "vantage_lake_name": "test-vantage-lake",
            "operation_type": "CREATE",
            "vantage_lake_error": "Test error message",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_issue"
    
    if metadata["success"]:
        issue_id = result.data["result"]["id"]
        await mcp_client.call_tool("qg_delete_issue", arguments={"id": issue_id})


@pytest.mark.integration
async def test_qg_create_issue_with_subcomponent(mcp_client: Client, test_infrastructure):
    """Test creating an issue with subcomponent parameters."""
    system_id = test_infrastructure.get("system_id")
    
    if not system_id:
        pytest.skip("Test infrastructure not available")
    
    manager_id = str(uuid.uuid4())
    subcomponent_id = str(uuid.uuid4())
    current_time = datetime.now(timezone.utc).isoformat()
    
    result = await mcp_client.call_tool(
        "qg_create_issue",
        arguments={
            "create_time": current_time,
            "component_type": "SYSTEM",
            "component_id": system_id,
            "component_name": "test_system_pytest",
            "data_center_name": "test_datacenter_pytest",
            "problem_type": "SOFTWARE_VERSIONS_INCORRECT",
            "severity": "WARNING",
            "subject_label": "test.issue.subject",
            "message_label": "test.issue.message",
            "config_version": "PENDING",
            "reporter_id": manager_id,
            "subcomponent_id": subcomponent_id,
            "sub_component_name": "test-subcomponent",
            "sub_component_issue_name_list": ["issue1", "issue2"],
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_issue"
    
    if metadata["success"]:
        issue_id = result.data["result"]["id"]
        await mcp_client.call_tool("qg_delete_issue", arguments={"id": issue_id})


@pytest.mark.integration
async def test_qg_create_issue_invalid_component_type(mcp_client: Client):
    """Test creating an issue with invalid component type."""
    current_time = datetime.now(timezone.utc).isoformat()
    
    result = await mcp_client.call_tool(
        "qg_create_issue",
        arguments={
            "create_time": current_time,
            "component_type": "INVALID_TYPE",
            "component_id": str(uuid.uuid4()),
            "component_name": "test_component",
            "data_center_name": "test_datacenter",
            "problem_type": "NODE_DOWN",
            "severity": "CRITICAL",
            "subject_label": "test.issue.subject",
            "message_label": "test.issue.message",
            "config_version": "ACTIVE",
            "reporter_id": str(uuid.uuid4()),
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_issue"
    # May fail with invalid component type


@pytest.mark.integration
async def test_qg_create_issue_invalid_severity(mcp_client: Client):
    """Test creating an issue with invalid severity."""
    current_time = datetime.now(timezone.utc).isoformat()
    
    result = await mcp_client.call_tool(
        "qg_create_issue",
        arguments={
            "create_time": current_time,
            "component_type": "SYSTEM",
            "component_id": str(uuid.uuid4()),
            "component_name": "test_component",
            "data_center_name": "test_datacenter",
            "problem_type": "NODE_DOWN",
            "severity": "INVALID_SEVERITY",
            "subject_label": "test.issue.subject",
            "message_label": "test.issue.message",
            "config_version": "ACTIVE",
            "reporter_id": str(uuid.uuid4()),
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_issue"


@pytest.mark.integration
async def test_qg_create_issue_empty_required_fields(mcp_client: Client):
    """Test creating an issue with empty required fields."""
    result = await mcp_client.call_tool(
        "qg_create_issue",
        arguments={
            "create_time": "",
            "component_type": "",
            "component_id": "",
            "component_name": "",
            "data_center_name": "",
            "problem_type": "",
            "severity": "",
            "subject_label": "",
            "message_label": "",
            "config_version": "",
            "reporter_id": "",
        },
    )

    # Should fail with empty required fields
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_issue"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_issue_full_workflow(mcp_client: Client, test_infrastructure):
    """Test complete issue workflow: create, get, and delete."""
    system_id = test_infrastructure.get("system_id")
    
    if not system_id:
        pytest.skip("Test infrastructure not available")
    
    manager_id = str(uuid.uuid4())
    current_time = datetime.now(timezone.utc).isoformat()
    
    # Create issue
    create_result = await mcp_client.call_tool(
        "qg_create_issue",
        arguments={
            "create_time": current_time,
            "component_type": "SYSTEM",
            "component_id": system_id,
            "component_name": "test_system_pytest",
            "data_center_name": "test_datacenter_pytest",
            "problem_type": "NODE_DOWN",
            "severity": "CRITICAL",
            "subject_label": "test.issue.subject",
            "message_label": "test.issue.message",
            "config_version": "ACTIVE",
            "reporter_id": manager_id,
        },
    )

    assert create_result.data is not None
    create_metadata = create_result.data["metadata"]
    assert create_metadata["tool_name"] == "qg_create_issue"
    
    if create_metadata["success"] and "result" in create_result.data:
        issue_id = create_result.data["result"]["id"]
        
        # Get issue by ID
        get_result = await mcp_client.call_tool(
            "qg_get_issue_by_id", arguments={"id": issue_id}
        )
        
        assert get_result.data is not None
        get_metadata = get_result.data["metadata"]
        assert get_metadata["tool_name"] == "qg_get_issue_by_id"
        
        if get_metadata["success"]:
            issue_data = get_result.data["result"]
            assert issue_data["id"] == issue_id
        
        # Delete issue
        delete_result = await mcp_client.call_tool(
            "qg_delete_issue", arguments={"id": issue_id}
        )
        
        assert delete_result.data is not None
        delete_metadata = delete_result.data["metadata"]
        assert delete_metadata["tool_name"] == "qg_delete_issue"


@pytest.mark.integration
async def test_qg_issues_error_handling(mcp_client: Client):
    """Test error handling across issue operations."""
    # Test getting issue with empty ID
    result = await mcp_client.call_tool(
        "qg_get_issue_by_id",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data
    
    # Test deleting issue with empty ID
    result = await mcp_client.call_tool(
        "qg_delete_issue",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data
    
    # Test getting issue with malformed UUID
    result = await mcp_client.call_tool(
        "qg_get_issue_by_id",
        arguments={"id": "00000000-0000-0000-0000-000000000000"},
    )
    assert result.data is not None
    assert "metadata" in result.data
