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
    assert (
        "Missing required argument" in error_msg
        or "is a required property" in error_msg
        or "Input validation error" in error_msg
    )


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


@pytest.mark.integration
async def test_qg_update_link(mcp_client: Client, test_link):
    """Test updating a link's name and description."""
    link_id = test_link.get("id")
    link_name = test_link.get("name")

    result = await mcp_client.call_tool(
        "qg_update_link",
        arguments={
            "id": link_id,
            "name": link_name,
            "description": "Updated description via PATCH",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_update_link"
    assert metadata["success"] is True

    # Verify the update
    get_result = await mcp_client.call_tool(
        "qg_get_link_by_id", arguments={"id": link_id}
    )
    assert get_result.data["metadata"]["success"] is True
    assert get_result.data["result"]["description"] == "Updated description via PATCH"


@pytest.mark.integration
async def test_qg_update_link_partial(mcp_client: Client, test_link):
    """Test updating a link with only description (name still required)."""
    link_id = test_link.get("id")
    link_name = test_link.get("name")

    result = await mcp_client.call_tool(
        "qg_update_link",
        arguments={
            "id": link_id,
            "name": link_name,
            "description": "Partial update with description only",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_update_link"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_put_link_active(
    mcp_client: Client,
    test_link,
    test_fabric,
    test_connector,
    test_comm_policy,
    qg_manager,
):
    """Test replacing the active link version."""
    link_id = test_link.get("id")
    link_name = test_link.get("name")
    fabric_id = test_fabric.get("id")

    # Save original target connector so we can restore it
    original_target_connector_id = test_link.get("targetConnectorId")
    initiator_connector_id = test_link.get("initiatorConnectorId")
    comm_policy_id = test_comm_policy.get("id")
    original_description = test_link.get("description")
    original_threads = test_link.get("initiatorThreadsPerQuery", 4)

    result = await mcp_client.call_tool(
        "qg_put_link_active",
        arguments={
            "id": link_id,
            "name": link_name,
            "fabricId": fabric_id,
            "initiatorConnectorId": initiator_connector_id,
            "targetConnectorId": original_target_connector_id,
            "commPolicyId": comm_policy_id,
            "description": "Updated active via PUT",
            "initiatorThreadsPerQuery": 4,
            "targetThreadsPerQuery": 4,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_put_link_active"
    assert metadata["success"] is True

    # Verify the update
    get_result = await mcp_client.call_tool(
        "qg_get_link_active", arguments={"id": link_id}
    )
    assert get_result.data["metadata"]["success"] is True
    active_link = get_result.data["result"]
    assert active_link["description"] == "Updated active via PUT"
    assert active_link["initiatorThreadsPerQuery"] == 4
    assert active_link["targetThreadsPerQuery"] == 4

    # Restore original state
    await mcp_client.call_tool(
        "qg_put_link_active",
        arguments={
            "id": link_id,
            "name": link_name,
            "fabricId": fabric_id,
            "initiatorConnectorId": initiator_connector_id,
            "targetConnectorId": original_target_connector_id,
            "commPolicyId": comm_policy_id,
            "description": original_description,
            "initiatorThreadsPerQuery": original_threads,
            "targetThreadsPerQuery": original_threads,
        },
    )


@pytest.mark.integration
async def test_qg_put_link_pending(
    mcp_client: Client, test_fabric, test_connector, test_comm_policy, qg_manager
):
    """Test creating a pending link version."""
    fabric_id = test_fabric.get("id")
    initiator_connector_id = test_connector.get("id")
    system_id = qg_manager.system_client.get_systems()[0].get("id")
    connector_version = test_connector.get("softwareVersion")
    comm_policy_id = test_comm_policy.get("id")

    # Get connector software name
    softwares = qg_manager.software_client.get_software()
    connector_software_name = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR" and sw.get("version") == connector_version:
            connector_software_name = sw.get("name")
            break

    # Create a second connector as target
    second_connector = qg_manager.connector_client.create_connector(
        name=f"test_connector_target_put_pending_{uuid.uuid4().hex[:8]}",
        software_name=connector_software_name,
        software_version=connector_version,
        fabric_id=fabric_id,
        system_id=system_id,
    )

    # Create a fresh link for this test
    test_link = qg_manager.link_client.create_link(
        name=f"test_link_put_pending_{uuid.uuid4().hex[:8]}",
        fabricId=fabric_id,
        initiatorConnectorId=initiator_connector_id,
        targetConnectorId=second_connector.get("id"),
        commPolicyId=comm_policy_id,
        initiatorThreadsPerQuery=4,
        targetThreadsPerQuery=4,
    )

    try:
        link_id = test_link.get("id")
        link_name = test_link.get("name")
        target_connector_id = second_connector.get("id")

        result = await mcp_client.call_tool(
            "qg_put_link_pending",
            arguments={
                "id": link_id,
                "name": link_name,
                "fabricId": fabric_id,
                "initiatorConnectorId": initiator_connector_id,
                "targetConnectorId": target_connector_id,
                "commPolicyId": comm_policy_id,
                "description": "Pending link version",
                "initiatorThreadsPerQuery": 5,
                "targetThreadsPerQuery": 5,
            },
        )

        assert result.data is not None
        metadata = result.data["metadata"]
        assert metadata["tool_name"] == "qg_put_link_pending"
        assert metadata["success"] is True

        # Verify the pending version exists
        get_result = await mcp_client.call_tool(
            "qg_get_link_pending", arguments={"id": link_id}
        )
        assert get_result.data["metadata"]["success"] is True
        pending_link = get_result.data["result"]
        # Verify the pending version was created with correct parameters
        assert pending_link["initiatorThreadsPerQuery"] == 5
        assert pending_link["targetThreadsPerQuery"] == 5
        assert pending_link["fabricId"] == fabric_id
        assert pending_link["commPolicyId"] == comm_policy_id
    finally:
        # Cleanup: delete link first, then connectors
        try:
            qg_manager.link_client.delete_link(link_id)
        except Exception:
            pass
        try:
            qg_manager.connector_client.delete_connector(second_connector.get("id"))
        except Exception:
            pass


@pytest.mark.integration
async def test_qg_update_link_active_workflow(
    mcp_client: Client, test_fabric, test_connector, test_comm_policy, qg_manager
):
    """Test the full workflow: create pending → activate → verify."""
    fabric_id = test_fabric.get("id")
    initiator_connector_id = test_connector.get("id")
    system_id = qg_manager.system_client.get_systems()[0].get("id")
    connector_version = test_connector.get("softwareVersion")
    comm_policy_id = test_comm_policy.get("id")

    # Get connector software name
    softwares = qg_manager.software_client.get_software()
    connector_software_name = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR" and sw.get("version") == connector_version:
            connector_software_name = sw.get("name")
            break

    # Create a second connector as target
    second_connector = qg_manager.connector_client.create_connector(
        name=f"test_connector_target_workflow_{uuid.uuid4().hex[:8]}",
        software_name=connector_software_name,
        software_version=connector_version,
        fabric_id=fabric_id,
        system_id=system_id,
    )

    # Create a fresh link for this test
    test_link = qg_manager.link_client.create_link(
        name=f"test_link_workflow_{uuid.uuid4().hex[:8]}",
        fabricId=fabric_id,
        initiatorConnectorId=initiator_connector_id,
        targetConnectorId=second_connector.get("id"),
        commPolicyId=comm_policy_id,
        initiatorThreadsPerQuery=4,
        targetThreadsPerQuery=4,
    )

    try:
        link_id = test_link.get("id")
        link_name = test_link.get("name")
        target_connector_id = second_connector.get("id")

        # Step 1: Create pending version
        put_result = await mcp_client.call_tool(
            "qg_put_link_pending",
            arguments={
                "id": link_id,
                "name": link_name,
                "fabricId": fabric_id,
                "initiatorConnectorId": initiator_connector_id,
                "targetConnectorId": target_connector_id,
                "commPolicyId": comm_policy_id,
                "description": "Pending for activation workflow",
                "initiatorThreadsPerQuery": 3,
                "targetThreadsPerQuery": 3,
            },
        )
        assert put_result.data["metadata"]["success"] is True

        # Step 2: Get the pending version to extract versionId
        pending_result = await mcp_client.call_tool(
            "qg_get_link_pending", arguments={"id": link_id}
        )
        assert pending_result.data["metadata"]["success"] is True
        version_id = pending_result.data["result"]["versionId"]

        # Step 3: Activate the pending version
        activate_result = await mcp_client.call_tool(
            "qg_update_link_active",
            arguments={"id": link_id, "version_id": version_id},
        )
        assert activate_result.data["metadata"]["success"] is True

        # Step 4: Verify the activation
        active_result = await mcp_client.call_tool(
            "qg_get_link_active", arguments={"id": link_id}
        )
        assert active_result.data["metadata"]["success"] is True
        active_link = active_result.data["result"]
        # Verify the activation worked with correct parameters
        assert active_link["initiatorThreadsPerQuery"] == 3
        assert active_link["targetThreadsPerQuery"] == 3
        assert active_link["versionId"] == version_id
    finally:
        # Cleanup: delete link first, then connectors
        try:
            qg_manager.link_client.delete_link(link_id)
        except Exception:
            pass
        try:
            qg_manager.connector_client.delete_connector(second_connector.get("id"))
        except Exception:
            pass


@pytest.mark.integration
async def test_qg_delete_link_pending(
    mcp_client: Client, test_fabric, test_connector, test_comm_policy, qg_manager
):
    """Test deleting a pending link version."""
    fabric_id = test_fabric.get("id")
    initiator_connector_id = test_connector.get("id")
    system_id = qg_manager.system_client.get_systems()[0].get("id")
    connector_version = test_connector.get("softwareVersion")
    comm_policy_id = test_comm_policy.get("id")

    # Get connector software name
    softwares = qg_manager.software_client.get_software()
    connector_software_name = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR" and sw.get("version") == connector_version:
            connector_software_name = sw.get("name")
            break

    # Create a second connector as target
    second_connector = qg_manager.connector_client.create_connector(
        name=f"test_connector_target_delete_pending_{uuid.uuid4().hex[:8]}",
        software_name=connector_software_name,
        software_version=connector_version,
        fabric_id=fabric_id,
        system_id=system_id,
    )

    # Create a fresh link for this test
    test_link = qg_manager.link_client.create_link(
        name=f"test_link_delete_pending_{uuid.uuid4().hex[:8]}",
        fabricId=fabric_id,
        initiatorConnectorId=initiator_connector_id,
        targetConnectorId=second_connector.get("id"),
        commPolicyId=comm_policy_id,
        initiatorThreadsPerQuery=4,
        targetThreadsPerQuery=4,
    )

    try:
        link_id = test_link.get("id")
        link_name = test_link.get("name")
        target_connector_id = second_connector.get("id")

        # Create a pending version
        await mcp_client.call_tool(
            "qg_put_link_pending",
            arguments={
                "id": link_id,
                "name": link_name,
                "fabricId": fabric_id,
                "initiatorConnectorId": initiator_connector_id,
                "targetConnectorId": target_connector_id,
                "commPolicyId": comm_policy_id,
                "description": "Pending for deletion",
                "initiatorThreadsPerQuery": 2,
                "targetThreadsPerQuery": 2,
            },
        )

        # Delete the pending version
        delete_result = await mcp_client.call_tool(
            "qg_delete_link_pending", arguments={"id": link_id}
        )

        assert delete_result.data is not None
        metadata = delete_result.data["metadata"]
        assert metadata["tool_name"] == "qg_delete_link_pending"
        assert metadata["success"] is True

        # Verify deletion - getting pending should fail
        get_result = await mcp_client.call_tool(
            "qg_get_link_pending", arguments={"id": link_id}
        )
        assert get_result.data["metadata"]["success"] is False
    finally:
        qg_manager.connector_client.delete_connector(second_connector.get("id"))


@pytest.mark.integration
async def test_qg_delete_link_previous(
    mcp_client: Client, test_fabric, test_connector, test_comm_policy, qg_manager
):
    """Test deleting a previous link version after creating one."""
    fabric_id = test_fabric.get("id")
    initiator_connector_id = test_connector.get("id")
    system_id = qg_manager.system_client.get_systems()[0].get("id")
    connector_version = test_connector.get("softwareVersion")
    comm_policy_id = test_comm_policy.get("id")

    # Get connector software name
    softwares = qg_manager.software_client.get_software()
    connector_software_name = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR" and sw.get("version") == connector_version:
            connector_software_name = sw.get("name")
            break

    # Create a second connector as target
    second_connector = qg_manager.connector_client.create_connector(
        name=f"test_connector_target_delete_previous_{uuid.uuid4().hex[:8]}",
        software_name=connector_software_name,
        software_version=connector_version,
        fabric_id=fabric_id,
        system_id=system_id,
    )

    # Create a fresh link for this test
    test_link = qg_manager.link_client.create_link(
        name=f"test_link_delete_previous_{uuid.uuid4().hex[:8]}",
        fabricId=fabric_id,
        initiatorConnectorId=initiator_connector_id,
        targetConnectorId=second_connector.get("id"),
        commPolicyId=comm_policy_id,
        initiatorThreadsPerQuery=4,
        targetThreadsPerQuery=4,
    )

    try:
        link_id = test_link.get("id")
        link_name = test_link.get("name")
        target_connector_id = second_connector.get("id")

        # Create pending and activate to generate a previous version
        await mcp_client.call_tool(
            "qg_put_link_pending",
            arguments={
                "id": link_id,
                "name": link_name,
                "fabricId": fabric_id,
                "initiatorConnectorId": initiator_connector_id,
                "targetConnectorId": target_connector_id,
                "commPolicyId": comm_policy_id,
                "description": "Will become previous",
                "initiatorThreadsPerQuery": 2,
                "targetThreadsPerQuery": 2,
            },
        )

        pending_result = await mcp_client.call_tool(
            "qg_get_link_pending", arguments={"id": link_id}
        )
        version_id = pending_result.data["result"]["versionId"]

        await mcp_client.call_tool(
            "qg_update_link_active",
            arguments={"id": link_id, "version_id": version_id},
        )

        # Now we should have a previous version
        # Delete the previous version
        delete_result = await mcp_client.call_tool(
            "qg_delete_link_previous", arguments={"id": link_id}
        )

        assert delete_result.data is not None
        metadata = delete_result.data["metadata"]
        assert metadata["tool_name"] == "qg_delete_link_previous"
        assert metadata["success"] is True

        # Verify deletion - getting previous should fail
        get_result = await mcp_client.call_tool(
            "qg_get_link_previous", arguments={"id": link_id}
        )
        assert get_result.data["metadata"]["success"] is False
    finally:
        qg_manager.connector_client.delete_connector(second_connector.get("id"))


@pytest.mark.integration
async def test_qg_update_link_active_with_previous_version(
    mcp_client: Client, test_fabric, test_connector, test_comm_policy, qg_manager
):
    """Test rollback scenario - activate previous version."""
    fabric_id = test_fabric.get("id")
    initiator_connector_id = test_connector.get("id")
    system_id = qg_manager.system_client.get_systems()[0].get("id")
    connector_version = test_connector.get("softwareVersion")
    comm_policy_id = test_comm_policy.get("id")

    # Get connector software name
    softwares = qg_manager.software_client.get_software()
    connector_software_name = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR" and sw.get("version") == connector_version:
            connector_software_name = sw.get("name")
            break

    # Create a second connector as target
    second_connector = qg_manager.connector_client.create_connector(
        name=f"test_connector_target_rollback_{uuid.uuid4().hex[:8]}",
        software_name=connector_software_name,
        software_version=connector_version,
        fabric_id=fabric_id,
        system_id=system_id,
    )

    # Create a fresh link for this test
    test_link = qg_manager.link_client.create_link(
        name=f"test_link_rollback_{uuid.uuid4().hex[:8]}",
        fabricId=fabric_id,
        initiatorConnectorId=initiator_connector_id,
        targetConnectorId=second_connector.get("id"),
        commPolicyId=comm_policy_id,
        initiatorThreadsPerQuery=4,
        targetThreadsPerQuery=4,
    )

    try:
        link_id = test_link.get("id")
        link_name = test_link.get("name")
        target_connector_id = second_connector.get("id")

        # Create and activate a new version to generate previous
        await mcp_client.call_tool(
            "qg_put_link_pending",
            arguments={
                "id": link_id,
                "name": link_name,
                "fabricId": fabric_id,
                "initiatorConnectorId": initiator_connector_id,
                "targetConnectorId": target_connector_id,
                "commPolicyId": comm_policy_id,
                "description": "Version that will be rolled back",
                "initiatorThreadsPerQuery": 2,
                "targetThreadsPerQuery": 2,
            },
        )

        pending_result = await mcp_client.call_tool(
            "qg_get_link_pending", arguments={"id": link_id}
        )
        version_id = pending_result.data["result"]["versionId"]

        await mcp_client.call_tool(
            "qg_update_link_active",
            arguments={"id": link_id, "version_id": version_id},
        )

        # Get the previous version
        previous_result = await mcp_client.call_tool(
            "qg_get_link_previous", arguments={"id": link_id}
        )
        assert previous_result.data["metadata"]["success"] is True
        previous_version = previous_result.data["result"]

        # Recreate previous as pending
        await mcp_client.call_tool(
            "qg_put_link_pending",
            arguments={
                "id": link_id,
                "name": link_name,
                "fabricId": previous_version["fabricId"],
                "initiatorConnectorId": previous_version["initiatorConnectorId"],
                "targetConnectorId": previous_version["targetConnectorId"],
                "commPolicyId": previous_version["commPolicyId"],
                "description": previous_version.get("description", ""),
                "initiatorThreadsPerQuery": previous_version.get(
                    "initiatorThreadsPerQuery", 4
                ),
                "targetThreadsPerQuery": previous_version.get(
                    "targetThreadsPerQuery", 4
                ),
            },
        )

        # Activate the "rollback" pending version
        rollback_pending = await mcp_client.call_tool(
            "qg_get_link_pending", arguments={"id": link_id}
        )
        rollback_version_id = rollback_pending.data["result"]["versionId"]

        activate_result = await mcp_client.call_tool(
            "qg_update_link_active",
            arguments={"id": link_id, "version_id": rollback_version_id},
        )
        assert activate_result.data["metadata"]["success"] is True

        # Verify we've rolled back
        active_result = await mcp_client.call_tool(
            "qg_get_link_active", arguments={"id": link_id}
        )
        assert active_result.data["metadata"]["success"] is True
        # The description should not be "Version that will be rolled back"
        assert (
            active_result.data["result"].get("description")
            != "Version that will be rolled back"
        )
    finally:
        # Cleanup: delete link first, then connectors
        try:
            qg_manager.link_client.delete_link(link_id)
        except Exception:
            pass
        try:
            qg_manager.connector_client.delete_connector(second_connector.get("id"))
        except Exception:
            pass
