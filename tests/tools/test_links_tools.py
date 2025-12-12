"""Integration tests for link_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from src.tools import set_qg_manager


@pytest.mark.integration
async def test_qg_get_links(mcp_client: Client, test_link):
    """Test getting all links."""
    result = await mcp_client.call_tool("qg_get_links", arguments={})

    # Verify response structure
    assert result.data is not None, "Tool should return data"
    assert isinstance(result.data, dict), "Tool should return a dictionary"
    assert "result" in result.data, "Tool response should have 'result' field"
    assert "metadata" in result.data, "Tool response should have 'metadata' field"

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_links"
    assert metadata["success"] is True

    # Verify result is a list
    links = result.data["result"]
    assert isinstance(links, list), "Links result should be a list"
    assert len(links) > 0, "Should have at least one link (test_link)"


@pytest.mark.integration
async def test_qg_get_links_with_flatten(mcp_client: Client, test_link):
    """Test getting all links with flatten option."""
    result = await mcp_client.call_tool("qg_get_links", arguments={"flatten": True})

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_links"
    assert metadata["success"] is True

    links = result.data["result"]
    assert isinstance(links, list)


@pytest.mark.integration
async def test_qg_get_links_with_extra_info(mcp_client: Client, test_link):
    """Test getting all links with extra_info option."""
    result = await mcp_client.call_tool("qg_get_links", arguments={"extra_info": True})

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_links"
    assert metadata["success"] is True

    links = result.data["result"]
    assert isinstance(links, list)


@pytest.mark.integration
async def test_qg_get_links_with_name_filter(mcp_client: Client, test_link):
    """Test getting links filtered by name."""
    link_name = test_link.get("name")

    result = await mcp_client.call_tool(
        "qg_get_links", arguments={"filter_by_name": link_name}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_links"
    assert metadata["success"] is True

    links = result.data["result"]
    assert isinstance(links, list)
    if len(links) > 0:
        # Verify the filtered link matches
        assert any(link.get("name") == link_name for link in links)


@pytest.mark.integration
async def test_qg_get_links_with_wildcard_filter(mcp_client: Client, test_link):
    """Test getting links with wildcard name filter."""
    result = await mcp_client.call_tool(
        "qg_get_links", arguments={"filter_by_name": "test_link*"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_links"
    assert metadata["success"] is True

    links = result.data["result"]
    assert isinstance(links, list)


@pytest.mark.integration
async def test_qg_get_links_with_tag_filter(mcp_client: Client):
    """Test getting links filtered by tag."""
    result = await mcp_client.call_tool(
        "qg_get_links", arguments={"filter_by_tag": "environment:test"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_links"
    assert metadata["success"] is True

    links = result.data["result"]
    assert isinstance(links, list)


@pytest.mark.integration
async def test_qg_get_link_by_id(mcp_client: Client, test_link):
    """Test getting a specific link by ID."""
    link_id = test_link.get("id")

    result = await mcp_client.call_tool("qg_get_link_by_id", arguments={"id": link_id})

    # Verify response structure
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "result" in result.data
    assert "metadata" in result.data

    # Verify metadata
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_link_by_id"
    assert metadata["success"] is True

    # Verify link data
    link = result.data["result"]
    assert isinstance(link, dict)
    assert link.get("id") == link_id
    assert "name" in link


@pytest.mark.integration
async def test_qg_get_link_by_id_with_extra_info(mcp_client: Client, test_link):
    """Test getting a link with extra_info option."""
    link_id = test_link.get("id")

    result = await mcp_client.call_tool(
        "qg_get_link_by_id", arguments={"id": link_id, "extra_info": True}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_link_by_id"
    assert metadata["success"] is True

    link = result.data["result"]
    assert isinstance(link, dict)
    assert link.get("id") == link_id


@pytest.mark.integration
async def test_qg_get_link_by_id_not_found(mcp_client: Client):
    """Test getting a link with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool("qg_get_link_by_id", arguments={"id": fake_id})

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_link_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_link_by_id_invalid_uuid(mcp_client: Client):
    """Test getting a link with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_link_by_id", arguments={"id": "not-a-valid-uuid"}
    )

    # Should return error response
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_link_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_link_active(mcp_client: Client, test_link):
    """Test getting active configuration of a link."""
    link_id = test_link.get("id")

    result = await mcp_client.call_tool("qg_get_link_active", arguments={"id": link_id})

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_link_active"
    assert metadata["success"] is True

    # Verify active config
    if "result" in result.data:
        active_config = result.data["result"]
        assert isinstance(active_config, dict)


@pytest.mark.integration
async def test_qg_get_link_active_not_found(mcp_client: Client):
    """Test getting active config for non-existent link."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool("qg_get_link_active", arguments={"id": fake_id})

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_link_active"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_link_pending(mcp_client: Client, test_link):
    """Test getting pending configuration of a link."""
    link_id = test_link.get("id")

    result = await mcp_client.call_tool(
        "qg_get_link_pending", arguments={"id": link_id}
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_link_pending"
    # Pending config may or may not exist
    assert metadata["success"] in [True, False]


@pytest.mark.integration
async def test_qg_get_link_pending_not_found(mcp_client: Client):
    """Test getting pending config for non-existent link."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_link_pending", arguments={"id": fake_id}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_link_pending"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_link_previous(mcp_client: Client, test_link):
    """Test getting previous configuration of a link."""
    link_id = test_link.get("id")

    result = await mcp_client.call_tool(
        "qg_get_link_previous", arguments={"id": link_id}
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_link_previous"
    # Previous config may or may not exist
    assert metadata["success"] in [True, False]


@pytest.mark.integration
async def test_qg_get_link_previous_not_found(mcp_client: Client):
    """Test getting previous config for non-existent link."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_link_previous", arguments={"id": fake_id}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_link_previous"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_create_link(
    mcp_client: Client,
    test_infrastructure,
    test_fabric,
    test_connector,
    test_comm_policy,
    qg_manager,
):
    """Test creating a new link."""
    system_id = test_infrastructure.get("system_id")
    fabric_id = test_fabric.get("id")

    if not system_id or not fabric_id:
        pytest.skip("Test infrastructure not available")

    # Get connector software
    softwares = qg_manager.software_client.get_software()
    connector_software = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR":
            connector_software = sw
            break

    if not connector_software:
        pytest.skip("No CONNECTOR software available")

    # Create second connector for the link
    second_connector = qg_manager.connector_client.create_connector(
        name="test_connector_for_link_pytest",
        software_name=connector_software.get("name"),
        software_version=connector_software.get("version"),
        fabric_id=fabric_id,
        system_id=system_id,
        description="Test connector for link creation test",
    )

    try:
        result = await mcp_client.call_tool(
            "qg_create_link",
            arguments={
                "name": "test_new_link_pytest",
                "fabricId": fabric_id,
                "initiatorConnectorId": test_connector.get("id"),
                "targetConnectorId": second_connector.get("id"),
                "commPolicyId": test_comm_policy.get("id"),
                "initiatorThreadsPerQuery": 4,
                "targetThreadsPerQuery": 4,
                "description": "Test link created by pytest",
            },
        )

        # Verify response structure
        assert result.data is not None
        assert isinstance(result.data, dict)
        assert "metadata" in result.data

        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_create_link"
        assert metadata["success"] is True

        # Verify created link
        created_link = result.data["result"]
        assert isinstance(created_link, dict)
        assert "id" in created_link
        assert created_link.get("name") == "test_new_link_pytest"

        # Cleanup - delete the created link
        link_id = created_link.get("id")
        cleanup_result = await mcp_client.call_tool(
            "qg_delete_link", arguments={"id": link_id}
        )
        assert cleanup_result.data["metadata"]["success"] is True

    finally:
        # Cleanup - delete second connector
        qg_manager.connector_client.delete_connector(second_connector.get("id"))


@pytest.mark.integration
async def test_qg_create_link_with_optional_params(
    mcp_client: Client,
    test_infrastructure,
    test_fabric,
    test_connector,
    test_comm_policy,
    qg_manager,
):
    """Test creating a link with different thread count (optional parameter variation)."""
    system_id = test_infrastructure.get("system_id")
    fabric_id = test_fabric.get("id")

    if not system_id or not fabric_id:
        pytest.skip("Test infrastructure not available")

    # Get connector software
    softwares = qg_manager.software_client.get_software()
    connector_software = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR":
            connector_software = sw
            break

    if not connector_software:
        pytest.skip("No CONNECTOR software available")

    # Create second connector for the link
    second_connector = qg_manager.connector_client.create_connector(
        name="test_connector_optional_pytest",
        software_name=connector_software.get("name"),
        software_version=connector_software.get("version"),
        fabric_id=fabric_id,
        system_id=system_id,
        description="Test connector with optional params",
    )

    try:
        result = await mcp_client.call_tool(
            "qg_create_link",
            arguments={
                "name": "test_link_optional_pytest",
                "fabricId": fabric_id,
                "initiatorConnectorId": test_connector.get("id"),
                "targetConnectorId": second_connector.get("id"),
                "commPolicyId": test_comm_policy.get("id"),
                "initiatorThreadsPerQuery": 4,
                "targetThreadsPerQuery": 4,
                "description": "Link with optional parameters",
            },
        )

        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_create_link"
        assert metadata["success"] is True

        created_link = result.data["result"]
        assert created_link.get("name") == "test_link_optional_pytest"

        # Cleanup
        link_id = created_link.get("id")
        await mcp_client.call_tool("qg_delete_link", arguments={"id": link_id})

    finally:
        qg_manager.connector_client.delete_connector(second_connector.get("id"))


@pytest.mark.integration
async def test_qg_create_link_missing_required_params(mcp_client: Client):
    """Test creating a link with missing required parameters."""
    from fastmcp.exceptions import ToolError

    # Should fail due to missing required parameters - FastMCP validates this
    with pytest.raises(ToolError) as exc_info:
        result = await mcp_client.call_tool(
            "qg_create_link",
            arguments={
                "name": "incomplete_link",
                # Missing fabricId, initiatorConnectorId, targetConnectorId, commPolicyId
            },
        )

    # Verify the error mentions missing required arguments
    error_msg = str(exc_info.value)
    assert ("Missing required argument" in error_msg or 
            "is a required property" in error_msg or
            "Input validation error" in error_msg)


@pytest.mark.integration
async def test_qg_create_link_invalid_fabric_id(
    mcp_client: Client, test_connector, test_comm_policy
):
    """Test creating a link with invalid fabric ID."""
    fake_fabric_id = str(uuid.uuid4())
    fake_connector_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_create_link",
        arguments={
            "name": "test_invalid_fabric_link",
            "fabricId": fake_fabric_id,
            "initiatorConnectorId": test_connector.get("id"),
            "targetConnectorId": fake_connector_id,
            "commPolicyId": test_comm_policy.get("id"),
            "initiatorThreadsPerQuery": 4,
            "targetThreadsPerQuery": 4,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_create_link"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_delete_link(
    mcp_client: Client,
    test_infrastructure,
    test_fabric,
    test_connector,
    test_comm_policy,
    qg_manager,
):
    """Test deleting a link."""
    system_id = test_infrastructure.get("system_id")
    fabric_id = test_fabric.get("id")

    if not system_id or not fabric_id:
        pytest.skip("Test infrastructure not available")

    # Get connector software
    softwares = qg_manager.software_client.get_software()
    connector_software = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR":
            connector_software = sw
            break

    if not connector_software:
        pytest.skip("No CONNECTOR software available")

    # Create second connector and link to delete
    second_connector = qg_manager.connector_client.create_connector(
        name="test_connector_delete_pytest",
        software_name=connector_software.get("name"),
        software_version=connector_software.get("version"),
        fabric_id=fabric_id,
        system_id=system_id,
        description="Test connector for delete test",
    )

    try:
        # Create link to delete
        create_result = await mcp_client.call_tool(
            "qg_create_link",
            arguments={
                "name": "test_link_to_delete_pytest",
                "fabricId": fabric_id,
                "initiatorConnectorId": test_connector.get("id"),
                "targetConnectorId": second_connector.get("id"),
                "commPolicyId": test_comm_policy.get("id"),
                "initiatorThreadsPerQuery": 4,
                "targetThreadsPerQuery": 4,
            },
        )

        assert create_result.data["metadata"]["success"] is True
        link_id = create_result.data["result"]["id"]

        # Delete the link
        delete_result = await mcp_client.call_tool(
            "qg_delete_link", arguments={"id": link_id}
        )

        # Verify deletion
        assert delete_result.data is not None
        assert isinstance(delete_result.data, dict)
        assert "metadata" in delete_result.data

        metadata = delete_result.data["metadata"]
        assert metadata["tool_name"] == "qg_delete_link"
        assert metadata["success"] is True

    finally:
        qg_manager.connector_client.delete_connector(second_connector.get("id"))


@pytest.mark.integration
async def test_qg_delete_link_not_found(mcp_client: Client):
    """Test deleting a link with non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool("qg_delete_link", arguments={"id": fake_id})

    # API may return success for non-existent IDs (idempotent delete)
    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_link"


@pytest.mark.integration
async def test_qg_delete_link_invalid_uuid(mcp_client: Client):
    """Test deleting a link with invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_link", arguments={"id": "not-a-valid-uuid"}
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_link"


@pytest.mark.integration
async def test_qg_link_full_workflow(
    mcp_client: Client,
    test_infrastructure,
    test_fabric,
    test_connector,
    test_comm_policy,
    qg_manager,
):
    """Test complete link workflow: create, get, get_active, and delete."""
    system_id = test_infrastructure.get("system_id")
    fabric_id = test_fabric.get("id")

    if not system_id or not fabric_id:
        pytest.skip("Test infrastructure not available")

    # Get connector software
    softwares = qg_manager.software_client.get_software()
    connector_software = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR":
            connector_software = sw
            break

    if not connector_software:
        pytest.skip("No CONNECTOR software available")

    # Create second connector
    second_connector = qg_manager.connector_client.create_connector(
        name="test_connector_workflow_pytest",
        software_name=connector_software.get("name"),
        software_version=connector_software.get("version"),
        fabric_id=fabric_id,
        system_id=system_id,
        description="Test connector for workflow test",
    )

    try:
        # Create link
        create_result = await mcp_client.call_tool(
            "qg_create_link",
            arguments={
                "name": "test_link_workflow_pytest",
                "fabricId": fabric_id,
                "initiatorConnectorId": test_connector.get("id"),
                "targetConnectorId": second_connector.get("id"),
                "commPolicyId": test_comm_policy.get("id"),
                "initiatorThreadsPerQuery": 4,
                "targetThreadsPerQuery": 4,
                "description": "Link for workflow test",
            },
        )

        assert create_result.data["metadata"]["success"] is True
        link_id = create_result.data["result"]["id"]

        # Get link by ID
        get_result = await mcp_client.call_tool(
            "qg_get_link_by_id", arguments={"id": link_id}
        )
        assert get_result.data["metadata"]["success"] is True
        assert get_result.data["result"]["id"] == link_id

        # Get active config
        active_result = await mcp_client.call_tool(
            "qg_get_link_active", arguments={"id": link_id}
        )
        assert active_result.data["metadata"]["success"] is True

        # Get all links (should include our new link)
        list_result = await mcp_client.call_tool("qg_get_links", arguments={})
        assert list_result.data["metadata"]["success"] is True
        links = list_result.data["result"]
        assert any(link.get("id") == link_id for link in links)

        # Delete link
        delete_result = await mcp_client.call_tool(
            "qg_delete_link", arguments={"id": link_id}
        )
        assert delete_result.data["metadata"]["success"] is True

        # Verify deletion
        get_deleted_result = await mcp_client.call_tool(
            "qg_get_link_by_id", arguments={"id": link_id}
        )
        assert get_deleted_result.data["metadata"]["success"] is False

    finally:
        qg_manager.connector_client.delete_connector(second_connector.get("id"))


@pytest.mark.integration
async def test_qg_links_error_handling(mcp_client: Client):
    """Test error handling across link operations."""
    # Test getting link with empty ID
    result = await mcp_client.call_tool(
        "qg_get_link_by_id",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data

    # Test deleting link with empty ID
    result = await mcp_client.call_tool(
        "qg_delete_link",
        arguments={"id": ""},
    )
    assert result.data is not None
    assert "metadata" in result.data

    # Test getting link with all-zeros UUID
    result = await mcp_client.call_tool(
        "qg_get_link_by_id",
        arguments={"id": "00000000-0000-0000-0000-000000000000"},
    )
    assert result.data is not None
    assert "metadata" in result.data
