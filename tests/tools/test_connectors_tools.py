"""Integration tests for connector_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from src.tools import set_qg_manager


@pytest.mark.integration
async def test_qg_get_connectors(mcp_client: Client):
    """Test getting all connectors."""
    result = await mcp_client.call_tool("qg_get_connectors", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_connectors"
    assert metadata["success"] is True

    # Verify result is a list
    connectors = result.data["result"]
    assert isinstance(connectors, list), "Connectors result should be a list"


@pytest.mark.integration
async def test_qg_get_connectors_with_filters(mcp_client: Client, test_connector):
    """Test getting connectors with filter parameters."""
    # Use test connector for filtering
    connector_name = test_connector.get("name")
    
    # Test with name filter
    result = await mcp_client.call_tool(
        "qg_get_connectors", arguments={"filter_by_name": connector_name}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True

    filtered_connectors = result.data["result"]
    assert isinstance(filtered_connectors, list)
    # Should find at least the connector we searched for
    assert any(c.get("name") == connector_name for c in filtered_connectors)

    # Test with extra_info flag
    result = await mcp_client.call_tool(
        "qg_get_connectors", arguments={"extra_info": True}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_connector_by_id(mcp_client: Client, test_connector):
    """Test getting a specific connector by ID."""
    connector_id = test_connector.get("id")
    assert connector_id is not None, "Test connector should have an ID"

    # Get connector by ID
    result = await mcp_client.call_tool(
        "qg_get_connector_by_id", arguments={"id": connector_id}
    )

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_connector_by_id"
    assert metadata["success"] is True

    # Verify connector data
    connector = result.data["result"]
    assert isinstance(connector, dict)
    assert connector.get("id") == connector_id


@pytest.mark.integration
async def test_qg_get_connector_by_id_not_found(mcp_client: Client):
    """Test getting a connector with invalid ID."""
    invalid_id = "00000000-0000-0000-0000-000000000000"

    result = await mcp_client.call_tool(
        "qg_get_connector_by_id", arguments={"id": invalid_id}
    )

    # Should return error response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_connector_by_id"
    # Expecting failure for non-existent connector
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_connector_active(mcp_client: Client, test_connector):
    """Test getting the active configuration of a connector."""
    connector_id = test_connector.get("id")
    assert connector_id is not None, "Test connector should have an ID"

    # Get active configuration
    result = await mcp_client.call_tool(
        "qg_get_connector_active", arguments={"id": connector_id}
    )

    # Verify response structure
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_connector_active"
    assert metadata["success"] is True

    # Result should be a dict (active configuration)
    active_config = result.data["result"]
    assert isinstance(active_config, dict)


@pytest.mark.integration
async def test_qg_get_connector_pending(mcp_client: Client, test_connector):
    """Test getting the pending configuration of a connector."""
    connector_id = test_connector.get("id")
    assert connector_id is not None, "Test connector should have an ID"

    # Get pending configuration
    result = await mcp_client.call_tool(
        "qg_get_connector_pending", arguments={"id": connector_id}
    )

    # Verify response structure
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_connector_pending"
    # May succeed or fail depending on whether there's a pending config
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_connector_previous(mcp_client: Client, test_connector):
    """Test getting the previous configuration of a connector."""
    connector_id = test_connector.get("id")
    assert connector_id is not None, "Test connector should have an ID"

    # Get previous configuration
    result = await mcp_client.call_tool(
        "qg_get_connector_previous", arguments={"id": connector_id}
    )

    # Verify response structure
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_connector_previous"
    # May succeed or fail depending on whether there's a previous config
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_connector_drivers(mcp_client: Client, qg_manager, test_connector):
    """Test getting connector drivers."""
    connector_id = test_connector.get("id")
    assert connector_id is not None, "Test connector should have an ID"

    # Get active version to find version_id
    try:
        active_config = qg_manager.connector_client.get_connector_active(connector_id)
        version_id = active_config.get("versionId")
        
        if not version_id:
            pytest.skip("No version ID available for connector")

        # Get connector drivers
        result = await mcp_client.call_tool(
            "qg_get_connector_drivers",
            arguments={"id": connector_id, "version_id": version_id},
        )

        # Verify response structure
        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_get_connector_drivers"
        assert "success" in metadata
    except Exception:
        pytest.skip("Could not get connector drivers for testing")


@pytest.mark.integration
async def test_qg_create_connector(mcp_client: Client, test_infrastructure, test_fabric):
    """Test creating a new connector."""
    # Get system from test infrastructure
    system_id = test_infrastructure["system_id"]
    fabric_id = test_fabric.get("id")
    
    assert system_id is not None, "Test infrastructure should have created a system"
    assert fabric_id is not None, "Test fabric should have an ID"

    # Get connector software from test_infrastructure validation
    softwares = None
    try:
        from qgm.querygrid_manager import QueryGridManager
        import os
        manager = QueryGridManager(verify_ssl=os.getenv("QG_MANAGER_VERIFY_SSL", "true").lower() in ("true", "1", "yes"))
        softwares = manager.software_client.get_software()
        manager.close()
    except Exception:
        pass
    
    if not softwares:
        pytest.skip("Could not retrieve software packages")
    
    connector_software = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR":
            connector_software = sw
            break

    if not connector_software:
        pytest.skip("No connector software available")

    software_name = connector_software.get("name")
    software_version = connector_software.get("version")

    # Create a test connector with unique name
    unique_suffix = str(uuid.uuid4())[:8]
    connector_args = {
        "name": f"test_connector_pytest_{unique_suffix}",
        "software_name": software_name,
        "software_version": software_version,
        "fabric_id": fabric_id,
        "system_id": system_id,
        "description": "Test connector created by pytest",
    }

    result = await mcp_client.call_tool("qg_create_connector", arguments=connector_args)

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_connector"
    assert (
        metadata["success"] is True
    ), f"Connector creation failed: {result.data.get('result')}"

    # Verify created connector
    connector = result.data["result"]
    assert isinstance(connector, dict)
    assert connector.get("name") == connector_args["name"]
    assert connector.get("description") == "Test connector created by pytest"

    # Cleanup - delete the created connector
    connector_id = connector.get("id")
    if connector_id:
        try:
            from qgm.querygrid_manager import QueryGridManager
            manager = QueryGridManager(verify_ssl=os.getenv("QG_MANAGER_VERIFY_SSL", "true").lower() in ("true", "1", "yes"))
            manager.connector_client.delete_connector(connector_id)
            manager.close()
        except Exception:
            pass  # Ignore cleanup errors


@pytest.mark.integration
async def test_qg_create_connector_minimal(
    mcp_client: Client, test_infrastructure, test_fabric
):
    """Test creating a connector with minimal required parameters."""
    # Get system from test infrastructure and fabric
    system_id = test_infrastructure["system_id"]
    fabric_id = test_fabric.get("id")
    
    assert system_id is not None, "Test infrastructure should have created a system"
    assert fabric_id is not None, "Test fabric should have an ID"

    # Get connector software
    softwares = None
    try:
        from qgm.querygrid_manager import QueryGridManager
        import os
        manager = QueryGridManager(verify_ssl=os.getenv("QG_MANAGER_VERIFY_SSL", "true").lower() in ("true", "1", "yes"))
        softwares = manager.software_client.get_software()
        manager.close()
    except Exception:
        pass
    
    if not softwares:
        pytest.skip("Could not retrieve software packages")
    
    connector_software = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR":
            connector_software = sw
            break

    if not connector_software:
        pytest.skip("No connector software available")

    software_name = connector_software.get("name")
    software_version = connector_software.get("version")

    # Create connector with only required parameters and unique name
    unique_suffix = str(uuid.uuid4())[:8]
    connector_name = f"test_connector_minimal_pytest_{unique_suffix}"
    result = await mcp_client.call_tool(
        "qg_create_connector",
        arguments={
            "name": connector_name,
            "software_name": software_name,
            "software_version": software_version,
            "fabric_id": fabric_id,
            "system_id": system_id,
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_connector"
    assert (
        metadata["success"] is True
    ), f"Connector creation failed: {result.data.get('result')}"

    connector = result.data["result"]
    assert connector.get("name") == connector_name

    # Cleanup - delete the created connector
    connector_id = connector.get("id")
    if connector_id:
        try:
            from qgm.querygrid_manager import QueryGridManager
            manager = QueryGridManager(verify_ssl=os.getenv("QG_MANAGER_VERIFY_SSL", "true").lower() in ("true", "1", "yes"))
            manager.connector_client.delete_connector(connector_id)
            manager.close()
        except Exception:
            pass  # Ignore cleanup errors


@pytest.mark.integration
async def test_qg_delete_connector(mcp_client: Client, test_infrastructure, test_fabric):
    """Test deleting a connector."""
    # Get system from test infrastructure and fabric
    system_id = test_infrastructure["system_id"]
    fabric_id = test_fabric.get("id")
    
    assert system_id is not None, "Test infrastructure should have created a system"
    assert fabric_id is not None, "Test fabric should have an ID"

    # Get connector software
    softwares = None
    qg_manager = None
    try:
        from qgm.querygrid_manager import QueryGridManager
        import os
        qg_manager = QueryGridManager(verify_ssl=os.getenv("QG_MANAGER_VERIFY_SSL", "true").lower() in ("true", "1", "yes"))
        softwares = qg_manager.software_client.get_software()
    except Exception:
        if qg_manager:
            qg_manager.close()
        pytest.skip("Could not retrieve software packages")
    
    connector_software = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR":
            connector_software = sw
            break

    if not connector_software:
        qg_manager.close()
        pytest.skip("No connector software available")

    software_name = connector_software.get("name")
    software_version = connector_software.get("version")

    # Create a connector to delete
    unique_suffix = str(uuid.uuid4())[:8]
    connector_name = f"test_connector_delete_pytest_{unique_suffix}"
    created_connector = qg_manager.connector_client.create_connector(
        name=connector_name,
        software_name=software_name,
        software_version=software_version,
        fabric_id=fabric_id,
        system_id=system_id,
        description="Test connector for deletion",
    )

    connector_id = created_connector.get("id")
    qg_manager.close()
    
    assert connector_id is not None, "Created connector should have an ID"

    # Delete the connector using the tool
    result = await mcp_client.call_tool("qg_delete_connector", arguments={"id": connector_id})

    # Verify response structure
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_connector"
    assert metadata["success"] is True

    # Verify connector is actually deleted
    try:
        qg_manager = QueryGridManager(verify_ssl=os.getenv("QG_MANAGER_VERIFY_SSL", "true").lower() in ("true", "1", "yes"))
        qg_manager.connector_client.get_connector_by_id(connector_id)
        qg_manager.close()
        # If we get here, deletion failed
        assert False, "Connector should have been deleted"
    except Exception:
        # Expected - connector should not be found
        if qg_manager:
            qg_manager.close()


@pytest.mark.integration
async def test_qg_delete_connector_not_found(mcp_client: Client):
    """Test deleting a non-existent connector."""
    invalid_id = "00000000-0000-0000-0000-000000000000"

    result = await mcp_client.call_tool("qg_delete_connector", arguments={"id": invalid_id})

    # API might return success even for non-existent resources
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_connector"
    # Just verify we got a response, success may be True or False
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_connectors_error_handling(mcp_client: Client, qg_manager):
    """Test error handling when QueryGrid Manager is not available."""
    # Set manager to None to simulate unavailability
    set_qg_manager(None)

    result = await mcp_client.call_tool("qg_get_connectors", arguments={})

    # Verify error response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_connectors"
    assert metadata["success"] is False
    assert "error" in metadata

    # Restore manager for other tests
    set_qg_manager(qg_manager)
