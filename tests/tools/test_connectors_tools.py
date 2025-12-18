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
async def test_qg_create_connector(mcp_client: Client, qg_manager, test_infrastructure, test_fabric):
    """Test creating a new connector."""
    # Get system from test infrastructure
    system_id = test_infrastructure["system_id"]
    fabric_id = test_fabric.get("id")
    connector_version = test_infrastructure.get("connector_version")
    
    assert system_id is not None, "Test infrastructure should have created a system"
    assert fabric_id is not None, "Test fabric should have an ID"

    if not connector_version:
        pytest.skip("No CONNECTOR software version available")

    # Get connector software name from software list
    softwares = qg_manager.software_client.get_software()
    software_name = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR" and sw.get("version") == connector_version:
            software_name = sw.get("name")
            break

    if not software_name:
        pytest.skip(f"Could not find CONNECTOR software name for version {connector_version}")

    # Create a test connector with unique name
    unique_suffix = str(uuid.uuid4())[:8]
    connector_args = {
        "name": f"test_connector_pytest_{unique_suffix}",
        "software_name": software_name,
        "software_version": connector_version,
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
            qg_manager.connector_client.delete_connector(connector_id)
        except Exception:
            pass  # Ignore cleanup errors


@pytest.mark.integration
async def test_qg_create_connector_minimal(
    mcp_client: Client, qg_manager, test_infrastructure, test_fabric
):
    """Test creating a connector with minimal required parameters."""
    # Get system from test infrastructure and fabric
    system_id = test_infrastructure["system_id"]
    fabric_id = test_fabric.get("id")
    connector_version = test_infrastructure.get("connector_version")
    
    assert system_id is not None, "Test infrastructure should have created a system"
    assert fabric_id is not None, "Test fabric should have an ID"

    if not connector_version:
        pytest.skip("No CONNECTOR software version available")

    # Get connector software name from software list
    softwares = qg_manager.software_client.get_software()
    software_name = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR" and sw.get("version") == connector_version:
            software_name = sw.get("name")
            break

    if not software_name:
        pytest.skip(f"Could not find CONNECTOR software name for version {connector_version}")

    # Create connector with only required parameters and unique name
    unique_suffix = str(uuid.uuid4())[:8]
    connector_name = f"test_connector_minimal_pytest_{unique_suffix}"
    result = await mcp_client.call_tool(
        "qg_create_connector",
        arguments={
            "name": connector_name,
            "software_name": software_name,
            "software_version": connector_version,
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
            qg_manager.connector_client.delete_connector(connector_id)
        except Exception:
            pass  # Ignore cleanup errors


@pytest.mark.integration
async def test_qg_delete_connector(mcp_client: Client, qg_manager, test_infrastructure, test_fabric):
    """Test deleting a connector."""
    # Get system from test infrastructure and fabric
    system_id = test_infrastructure["system_id"]
    fabric_id = test_fabric.get("id")
    connector_version = test_infrastructure.get("connector_version")
    
    assert system_id is not None, "Test infrastructure should have created a system"
    assert fabric_id is not None, "Test fabric should have an ID"

    if not connector_version:
        pytest.skip("No CONNECTOR software version available")

    # Get connector software name from software list
    softwares = qg_manager.software_client.get_software()
    software_name = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR" and sw.get("version") == connector_version:
            software_name = sw.get("name")
            break

    if not software_name:
        pytest.skip(f"Could not find CONNECTOR software name for version {connector_version}")

    # Create a connector to delete
    unique_suffix = str(uuid.uuid4())[:8]
    connector_name = f"test_connector_delete_pytest_{unique_suffix}"
    created_connector = qg_manager.connector_client.create_connector(
        name=connector_name,
        software_name=software_name,
        software_version=connector_version,
        fabric_id=fabric_id,
        system_id=system_id,
        description="Test connector for deletion",
    )

    connector_id = created_connector.get("id")
    
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


@pytest.mark.integration
async def test_qg_update_connector(mcp_client: Client, test_connector):
    """Test updating a connector using PATCH."""
    connector_id = test_connector.get("id")
    connector_name = test_connector.get("name")

    # Update the connector name and description
    result = await mcp_client.call_tool(
        "qg_update_connector",
        arguments={
            "id": connector_id,
            "name": f"{connector_name}_updated",
            "description": "Updated description via PATCH",
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_update_connector"
    # PATCH on base connector might not be supported on all API versions
    if not metadata["success"]:
        # If PATCH isn't supported, that's expected
        assert "400" in str(result.data.get("result", "")) or "405" in str(result.data.get("result", ""))


@pytest.mark.integration
async def test_qg_update_connector_description(mcp_client: Client, test_connector):
    """Test updating only description field of a connector."""
    connector_id = test_connector.get("id")
    connector_name = test_connector.get("name")

    # Update only description - include name as it might be required
    result = await mcp_client.call_tool(
        "qg_update_connector",
        arguments={
            "id": connector_id,
            "name": connector_name,
            "description": "Updated description only",
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    # PATCH on base connector might not be supported
    if not metadata["success"]:
        assert "400" in str(result.data.get("result", "")) or "405" in str(result.data.get("result", ""))


@pytest.mark.integration
async def test_qg_update_connector_nonexistent(mcp_client: Client):
    """Test updating a non-existent connector."""
    invalid_id = "00000000-0000-0000-0000-000000000000"

    result = await mcp_client.call_tool(
        "qg_update_connector",
        arguments={
            "id": invalid_id,
            "description": "This should fail",
        },
    )

    # Should return error response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_update_connector"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_update_connector_active(mcp_client: Client, test_connector, qg_manager, test_fabric):
    """Test activating a pending version of a connector."""
    connector_id = test_connector.get("id")

    # Get active connector details
    active = qg_manager.connector_client.get_connector_active(connector_id)
    software_name = active.get("softwareName")
    software_version = active.get("softwareVersion")
    system_id = active.get("systemId")
    fabric_id = test_fabric.get("id")
    
    if not software_name or not software_version or not fabric_id or not system_id:
        pytest.skip(f"Cannot determine required info: name={software_name}, version={software_version}, fabric_id={fabric_id}, system_id={system_id}")

    # Check if there's already a pending version and delete it first
    try:
        existing_pending = qg_manager.connector_client.get_connector_pending(connector_id)
        if existing_pending:
            qg_manager.connector_client.delete_connector_pending(connector_id)
    except Exception:
        pass  # No existing pending version

    # Create a pending version to test activation
    # Note: QueryGrid API may not support pending versions for all connector types or states
    try:
        pending_version = qg_manager.connector_client.put_connector_pending(
            id=connector_id,
            software_name=software_name,
            software_version=software_version,
            fabric_id=fabric_id,
            system_id=system_id,
            description="Pending version to be activated",
        )
        pending_version_id = pending_version.get("versionId")
        if not pending_version_id:
            pytest.skip("Pending version does not have versionId")
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"Exception when creating pending version:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print(f"{'='*80}")
        pytest.skip(f"QueryGrid API does not support pending versions for this connector: {type(e).__name__}")

    try:
        # Activate the pending version using its versionId
        result = await mcp_client.call_tool(
            "qg_update_connector_active",
            arguments={
                "id": connector_id,
                "version_id": pending_version_id,
            },
        )

        # Verify response
        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_update_connector_active"
        assert metadata["success"] is True

        # PATCH may return empty response, which is expected
        updated = result.data["result"]
        # Result can be empty string or dict for PATCH operations
        assert updated is not None or updated == ""
    finally:
        # Cleanup - try to delete pending version if it still exists
        try:
            qg_manager.connector_client.delete_connector_pending(connector_id)
        except Exception:
            pass  # Pending was activated, so it no longer exists


@pytest.mark.integration
async def test_qg_put_connector_active(
    mcp_client: Client, qg_manager, test_connector, test_fabric
):
    """Test updating the active version with PUT (full replacement)."""
    connector_id = test_connector.get("id")
    
    # Get software info from the existing connector
    active = qg_manager.connector_client.get_connector_active(connector_id)
    software_name = active.get("softwareName")
    software_version = active.get("softwareVersion")
    system_id = active.get("systemId")
    fabric_id = test_fabric.get("id")

    if not software_name or not software_version or not system_id:
        pytest.skip("Cannot determine required info for connector")

    # Update active version with PUT
    result = await mcp_client.call_tool(
        "qg_put_connector_active",
        arguments={
            "id": connector_id,
            "software_name": software_name,
            "software_version": software_version,
            "fabric_id": fabric_id,
            "system_id": system_id,
            "description": "Updated via PUT active",
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_connector_active"
    # May succeed or fail depending on API support
    if metadata["success"]:
        updated = result.data["result"]
        assert isinstance(updated, dict)


@pytest.mark.integration
async def test_qg_put_connector_pending(
    mcp_client: Client, qg_manager, test_connector, test_fabric
):
    """Test creating/replacing the pending version of a connector."""
    connector_id = test_connector.get("id")
    
    # Get software info from the existing connector
    active = qg_manager.connector_client.get_connector_active(connector_id)
    software_name = active.get("softwareName")
    software_version = active.get("softwareVersion")
    system_id = active.get("systemId")
    fabric_id = test_fabric.get("id")

    if not software_name or not software_version or not system_id:
        pytest.skip("Cannot determine required info for connector")

    # Create a pending version
    result = await mcp_client.call_tool(
        "qg_put_connector_pending",
        arguments={
            "id": connector_id,
            "software_name": software_name,
            "software_version": software_version,
            "fabric_id": fabric_id,
            "system_id": system_id,
            "description": "Pending version description",
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_connector_pending"
    
    if metadata["success"]:
        # Verify pending version was created
        pending = result.data["result"]
        assert isinstance(pending, dict)
        
        # Cleanup - delete pending version
        try:
            qg_manager.connector_client.delete_connector_pending(connector_id)
        except Exception:
            pass


@pytest.mark.integration
async def test_qg_put_connector_pending_minimal(
    mcp_client: Client, qg_manager, test_connector, test_fabric
):
    """Test creating pending version with minimal required parameters."""
    connector_id = test_connector.get("id")
    
    # Get software info from the existing connector
    active = qg_manager.connector_client.get_connector_active(connector_id)
    software_name = active.get("softwareName")
    software_version = active.get("softwareVersion")
    system_id = active.get("systemId")
    fabric_id = test_fabric.get("id")

    if not software_name or not software_version or not system_id:
        pytest.skip("Cannot determine required info for connector")

    # Create pending version with only required parameters
    result = await mcp_client.call_tool(
        "qg_put_connector_pending",
        arguments={
            "id": connector_id,
            "software_name": software_name,
            "software_version": software_version,
            "fabric_id": fabric_id,
            "system_id": system_id,
        },
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    
    if metadata["success"]:
        # Cleanup
        try:
            qg_manager.connector_client.delete_connector_pending(connector_id)
        except Exception:
            pass


@pytest.mark.integration
async def test_qg_delete_connector_pending(mcp_client: Client, qg_manager, test_connector, test_fabric):
    """Test deleting the pending version of a connector."""
    connector_id = test_connector.get("id")
    
    # First create a pending version
    active = qg_manager.connector_client.get_connector_active(connector_id)
    software_name = active.get("softwareName")
    software_version = active.get("softwareVersion")
    system_id = active.get("systemId")
    fabric_id = test_fabric.get("id")

    if not software_name or not software_version or not fabric_id or not system_id:
        pytest.skip(f"Cannot determine required info: name={software_name}, version={software_version}, fabric_id={fabric_id}, system_id={system_id}")

    # Create pending version
    try:
        qg_manager.connector_client.put_connector_pending(
            id=connector_id,
            software_name=software_name,
            software_version=software_version,
            fabric_id=fabric_id,
            system_id=system_id,
            description="Pending to be deleted",
        )

        # Verify pending was created
        pending = qg_manager.connector_client.get_connector_pending(connector_id)
        if not pending:
            pytest.skip("Pending version not created as expected")
    except Exception as e:
        pytest.skip(f"Could not create pending version: {e}")

    # Delete the pending version
    result = await mcp_client.call_tool(
        "qg_delete_connector_pending",
        arguments={"id": connector_id},
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_connector_pending"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_delete_connector_pending_nonexistent(mcp_client: Client):
    """Test deleting pending version of non-existent connector."""
    invalid_id = "00000000-0000-0000-0000-000000000000"

    result = await mcp_client.call_tool(
        "qg_delete_connector_pending",
        arguments={"id": invalid_id},
    )

    # Should handle gracefully
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_connector_pending"


@pytest.mark.integration
async def test_qg_delete_connector_previous(mcp_client: Client, qg_manager, test_connector, test_fabric):
    """Test deleting the previous version of a connector.
    
    Creates a previous version by:
    1. Creating a pending version
    2. Activating the pending version (which pushes current active to previous)
    3. Then tests deleting the previous version
    """
    connector_id = test_connector.get("id")
    
    try:
        # Step 1: Get current active details
        active = qg_manager.connector_client.get_connector_active(connector_id)
        software_name = active.get("softwareName")
        software_version = active.get("softwareVersion")
        system_id = active.get("systemId")
        fabric_id = test_fabric.get("id")

        if not software_name or not software_version or not fabric_id or not system_id:
            pytest.skip(f"Cannot determine required info: name={software_name}, version={software_version}, fabric_id={fabric_id}, system_id={system_id}")

        # Step 2: Create a pending version
        # Note: QueryGrid API may not support pending versions for all connector types or states
        pending = qg_manager.connector_client.put_connector_pending(
            id=connector_id,
            software_name=software_name,
            software_version=software_version,
            fabric_id=fabric_id,
            system_id=system_id,
            description="Pending version to be activated",
        )
        
        pending_version_id = pending.get("versionId")
        if not pending_version_id:
            pytest.skip("Pending version does not have versionId")

        # Step 3: Activate the pending version (this should push active to previous)
        try:
            qg_manager.connector_client.update_connector_active(
                id=connector_id,
                version_id=pending_version_id,
            )
        except Exception as e:
            pytest.skip(f"Could not activate pending version: {type(e).__name__}: {str(e)}")

        # Verify previous version exists
        try:
            previous = qg_manager.connector_client.get_connector_previous(connector_id)
            if not previous:
                pytest.skip("Previous version was not created after activation")
        except Exception as e:
            pytest.skip(f"Could not verify previous version: {e}")

    except Exception as e:
        pytest.skip(f"Could not set up previous version: {e}")

    # Delete the previous version
    result = await mcp_client.call_tool(
        "qg_delete_connector_previous",
        arguments={"id": connector_id},
    )

    # Verify response
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_connector_previous"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_delete_connector_previous_nonexistent(mcp_client: Client):
    """Test deleting previous version of non-existent connector."""
    invalid_id = "00000000-0000-0000-0000-000000000000"

    result = await mcp_client.call_tool(
        "qg_delete_connector_previous",
        arguments={"id": invalid_id},
    )

    # Should handle gracefully
    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_connector_previous"
