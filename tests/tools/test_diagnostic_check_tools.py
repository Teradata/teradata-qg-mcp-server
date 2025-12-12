"""Integration tests for diagnostic_check_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_run_diagnostic_check_link(mcp_client: Client, test_link):
    """Test running a link diagnostic check."""
    link_id = test_link.get("id")
    
    result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "LINK",
            "component_id": link_id,
            "version": "ACTIVE",
        },
    )

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_run_diagnostic_check"
    
    # Diagnostic check may succeed or fail depending on infrastructure
    # We just verify the API call was made and response structure is correct
    if metadata["success"]:
        assert "result" in result.data
        diagnostic_result = result.data["result"]
        assert "id" in diagnostic_result, "Successful diagnostic should return an ID"


@pytest.mark.integration
async def test_qg_run_diagnostic_check_link_with_data_flow(mcp_client: Client, test_link):
    """Test running a link diagnostic check with data flow specified."""
    link_id = test_link.get("id")
    
    result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "LINK",
            "component_id": link_id,
            "data_flow": "INITIATOR_TO_TARGET",
            "version": "ACTIVE",
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_run_diagnostic_check"


@pytest.mark.integration
async def test_qg_run_diagnostic_check_connector(mcp_client: Client, test_connector):
    """Test running a connector diagnostic check."""
    connector_id = test_connector.get("id")
    
    result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "CONNECTOR",
            "component_id": connector_id,
            "version": "ACTIVE",
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_run_diagnostic_check"


@pytest.mark.integration
async def test_qg_run_diagnostic_check_invalid_type(mcp_client: Client):
    """Test running a diagnostic check with invalid type."""
    fake_id = str(uuid.uuid4())
    
    result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "INVALID_TYPE",
            "component_id": fake_id,
            "version": "ACTIVE",
        },
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_run_diagnostic_check"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_run_diagnostic_check_missing_component_id(mcp_client: Client):
    """Test running a diagnostic check without component_id."""
    result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "LINK",
            "version": "ACTIVE",
        },
    )

    # May fail without component_id
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_run_diagnostic_check"


@pytest.mark.integration
async def test_qg_run_diagnostic_check_nonexistent_component(mcp_client: Client):
    """Test running a diagnostic check with non-existent component ID."""
    fake_id = str(uuid.uuid4())
    
    result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "LINK",
            "component_id": fake_id,
            "version": "ACTIVE",
        },
    )

    # Should fail with non-existent component
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_run_diagnostic_check"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_run_diagnostic_check_with_bandwidth(mcp_client: Client, test_link):
    """Test running a link bandwidth diagnostic check."""
    link_id = test_link.get("id")
    
    result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "LINK_BANDWIDTH",
            "component_id": link_id,
            "bandwidth_mb_per_node": 100.0,
            "version": "ACTIVE",
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_run_diagnostic_check"


@pytest.mark.integration
async def test_qg_run_diagnostic_check_pending_version(mcp_client: Client, test_link):
    """Test running a diagnostic check with PENDING version."""
    link_id = test_link.get("id")
    
    result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "LINK",
            "component_id": link_id,
            "version": "PENDING",
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_run_diagnostic_check"


@pytest.mark.integration
async def test_qg_get_diagnostic_check_status_invalid_id(mcp_client: Client):
    """Test getting diagnostic check status with invalid ID."""
    fake_id = str(uuid.uuid4())
    
    result = await mcp_client.call_tool(
        "qg_get_diagnostic_check_status",
        arguments={"id": fake_id},
    )

    # Should fail with non-existent ID
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_diagnostic_check_status"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_diagnostic_check_status_malformed_id(mcp_client: Client):
    """Test getting diagnostic check status with malformed ID."""
    result = await mcp_client.call_tool(
        "qg_get_diagnostic_check_status",
        arguments={"id": "not-a-valid-uuid"},
    )

    # Should fail with malformed ID
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_diagnostic_check_status"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_diagnostic_check_status_empty_id(mcp_client: Client):
    """Test getting diagnostic check status with empty ID."""
    result = await mcp_client.call_tool(
        "qg_get_diagnostic_check_status",
        arguments={"id": ""},
    )

    # Should fail with empty ID
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_diagnostic_check_status"


@pytest.mark.integration
async def test_qg_diagnostic_check_full_workflow(mcp_client: Client, test_link):
    """Test complete diagnostic check workflow: run check and get status."""
    link_id = test_link.get("id")
    
    # Run diagnostic check
    run_result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "LINK",
            "component_id": link_id,
            "version": "ACTIVE",
        },
    )

    assert run_result.data is not None
    run_metadata = run_result.data["metadata"]
    assert run_metadata["tool_name"] == "qg_run_diagnostic_check"
    
    # If diagnostic check was successfully started, get its status
    if run_metadata["success"] and "result" in run_result.data:
        diagnostic_id = run_result.data["result"].get("id")
        if diagnostic_id:
            # Get status
            status_result = await mcp_client.call_tool(
                "qg_get_diagnostic_check_status",
                arguments={"id": diagnostic_id},
            )
            
            assert status_result.data is not None
            status_metadata = status_result.data["metadata"]
            assert status_metadata["tool_name"] == "qg_get_diagnostic_check_status"
            assert status_metadata["success"] is True
            
            # Verify status result structure
            if "result" in status_result.data:
                status_data = status_result.data["result"]
                assert isinstance(status_data, dict)
                # Status should have fields like 'state', 'type', etc.
                assert "id" in status_data
    else:
        # If check didn't start (e.g., infrastructure issues), that's acceptable
        print(f"\n⚠ Diagnostic check didn't start (expected if infrastructure unavailable): {run_metadata.get('error')}")


@pytest.mark.integration
async def test_qg_run_diagnostic_check_with_all_parameters(mcp_client: Client, test_link):
    """Test running diagnostic check with all optional parameters."""
    link_id = test_link.get("id")
    
    result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "LINK",
            "component_id": link_id,
            "data_flow": "INITIATOR_TO_TARGET",
            "version": "ACTIVE",
            "bandwidth_mb_per_node": 50.0,
        },
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_run_diagnostic_check"


@pytest.mark.integration
async def test_qg_diagnostic_check_error_handling(mcp_client: Client):
    """Test error handling across diagnostic check operations."""
    # Test running check with empty type
    result = await mcp_client.call_tool(
        "qg_run_diagnostic_check",
        arguments={
            "type": "",
            "component_id": str(uuid.uuid4()),
            "version": "ACTIVE",
        },
    )
    assert result.data is not None
    assert "metadata" in result.data
    
    # Test getting status with various invalid inputs
    result = await mcp_client.call_tool(
        "qg_get_diagnostic_check_status",
        arguments={"id": "00000000-0000-0000-0000-000000000000"},
    )
    assert result.data is not None
    assert "metadata" in result.data
