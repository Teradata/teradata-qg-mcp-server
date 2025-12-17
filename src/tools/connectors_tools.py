from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp

from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_connectors(
    flatten: bool = False,
    extra_info: bool = False,
    filter_by_name: str | None = None,
    fabric_version: str | None = None,
    filter_by_tag: str | None = None,
) -> dict[str, Any]:
    """
    Get details of all QueryGrid connectors. Optional filters can be applied to narrow down the results.

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify filters, retrieve all connectors.

    Args:
        flatten (bool): [OPTIONAL] Flatten the response structure
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.
        fabric_version (str | None): [OPTIONAL] Filter connectors by fabric version
        filter_by_name (str | None): [OPTIONAL] Get connector associated with the specified name (case insensitive).
             Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [OPTIONAL] Get connector associated with the specified tag.
            Provide ','(comma) separated list of key:value pairs.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_connectors called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.get_connectors(
            flatten=flatten,
            extra_info=extra_info,
            filter_by_name=filter_by_name,
            filter_by_tag=filter_by_tag,
            fabric_version=fabric_version,
        )

    return run_tool("qg_get_connectors", _call)


@mcp.tool
def qg_get_connector_by_id(
    id: str,
    extra_info: bool = False,
) -> dict[str, Any]:
    """
    Get details of a specific QueryGrid connector by ID.

    MANDATORY PARAMETER: Ask the user for the connector ID if not provided.
    OPTIONAL PARAMETERS: 'extra_info' can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the connector to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_connector_by_id called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.get_connector_by_id(
            id=id,
            extra_info=extra_info,
        )

    return run_tool("qg_get_connector_by_id", _call)


@mcp.tool
def qg_get_connector_active(
    id: str,
) -> dict[str, Any]:
    """
    Get the active configuration for a QueryGrid connector.

    MANDATORY PARAMETER: Ask the user for the connector ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the connector. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_connector_active called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.get_connector_active(id)

    return run_tool("qg_get_connector_active", _call)


@mcp.tool
def qg_get_connector_pending(
    id: str,
) -> dict[str, Any]:
    """
    Get details of the pending configuration for a QueryGrid connector.

    MANDATORY PARAMETER: Ask the user for the connector ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the connector. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_connector_pending called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.get_connector_pending(id)

    return run_tool("qg_get_connector_pending", _call)


@mcp.tool
def qg_get_connector_previous(
    id: str,
) -> dict[str, Any]:
    """
    Get the previous configuration for a QueryGrid connector.

    MANDATORY PARAMETER: Ask the user for the connector ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the connector. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_connector_previous called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.get_connector_previous(id)

    return run_tool("qg_get_connector_previous", _call)


@mcp.tool
def qg_get_connector_drivers(
    id: str,
    version_id: str,
) -> dict[str, Any]:
    """
    Get details of the drivers for a QueryGrid connector.

    MANDATORY PARAMETERS: Ask the user for 'id' and 'version_id' if not provided.

    Args:
        id (str): [MANDATORY] The ID of the connector. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.
        version_id (str): [MANDATORY] The version ID of the connector

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_connector_drivers called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.get_connector_drivers(
            id=id,
            version_id=version_id,
        )

    return run_tool("qg_get_connector_drivers", _call)


@mcp.tool
def qg_create_connector(
    name: str,
    software_name: str,
    software_version: str,
    fabric_id: str,
    system_id: str,
    description: str | None = None,
    driver_nodes: list[str] | None = None,
    properties: dict[str, Any] | None = None,
    overrideable_properties: list[str] | None = None,
    allowed_os_users: list[str] | None = None,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a new connector in QueryGrid Manager. Inform and ask for missing mandatory parameters before
    creating the connector. Do not fill in dummy values. Always confirm with the user before creating resources.

    MANDATORY PARAMETERS: Ask the user for 'name', 'software_name', 'software_version', 'fabric_id',
        and 'system_id' if not provided.
    OPTIONAL PARAMETERS: All other parameters can be omitted.

    Args:
        name (str): [MANDATORY] The name of the connector.
            Ask the user: "What would you like to name the connector?"
        software_name (str): [MANDATORY] The name of the software package to use for this connector.
        software_version (str): [MANDATORY] The version of the software package to use for this connector.
        fabric_id (str): [MANDATORY] The ID of the fabric this connector belongs to. ID is in UUID format.
            If the user doesn't know the fabric ID, suggest using qg_get_fabrics to list all fabrics.
        system_id (str): [MANDATORY] The ID of the system this connector belongs to. ID is in UUID format.
            If the user doesn't know the system ID, suggest using qg_get_systems to list all systems.
        description (str | None): [OPTIONAL] Description of the connector.
        driver_nodes (list[str] | None): [OPTIONAL] List of node IDs where drivers should be installed.
        properties (dict[str, Any] | None): [OPTIONAL] Properties to configure the connector.
        overrideable_properties (list[str] | None): [OPTIONAL] List of property names that can be overridden at runtime.
        allowed_os_users (list[str] | None): [OPTIONAL] List of OS users allowed to access this connector.
        tags (dict[str, Any] | None): [OPTIONAL] String key/value pairs for associating some context with the connector.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: handle_qg_create_connector called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.create_connector(
            name=name,
            software_name=software_name,
            software_version=software_version,
            fabric_id=fabric_id,
            system_id=system_id,
            description=description,
            driver_nodes=driver_nodes,
            properties=properties,
            overrideable_properties=overrideable_properties,
            allowed_os_users=allowed_os_users,
            tags=tags,
        )

    return run_tool("qg_create_connector", _call)


@mcp.tool
def qg_delete_connector(
    id: str,
) -> dict[str, Any]:
    """
    Delete a connector by ID.

    MANDATORY PARAMETER: Ask the user for the connector ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the connector to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_connector called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.delete_connector(id)

    return run_tool("qg_delete_connector", _call)


@mcp.tool
def qg_update_connector(
    id: str,
    name: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """
    Update Connector name or description using PATCH (partial update).

    MANDATORY PARAMETER: Ask the user for the connector 'id' if not provided.
    OPTIONAL PARAMETERS: All other parameters can be omitted. Only provide fields you want to update.

    Args:
        id (str): [MANDATORY] The ID of the connector to update. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.
        name (str | None): [OPTIONAL] The name of the connector.
        description (str | None): [OPTIONAL] Description of the connector.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_update_connector called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.update_connector(
            id=id,
            name=name,
            description=description,
        )

    return run_tool("qg_update_connector", _call)


@mcp.tool
def qg_update_connector_active(id: str, version_id: str) -> dict[str, Any]:
    """
    Activate a specific pending or previous connector version (PATCH).

    NOTE FOR LLMs: Connectors have two types of IDs:
    - 'id': The connector wrapper ID (constant across all versions)
    - 'versionId': Specific to each version (active, pending, previous)
    
    To activate a pending or previous version:
    1. Use qg_get_connector_pending() or qg_get_connector_previous() to get the version
    2. Extract 'versionId' from that response
    3. Call this tool with the connector 'id' and the 'versionId'

    MANDATORY PARAMETERS: Both 'id' and 'version_id' are required.

    Args:
        id (str): [MANDATORY] The connector wrapper ID (UUID format, constant across versions).
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.
        version_id (str): [MANDATORY] The specific version ID to activate (UUID format).
            Get this from the pending or previous version response.
            e.g., '987fcdeb-51a2-43f1-b123-426614174999'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_update_connector_active called with id=%s, version_id=%s",
        id,
        version_id,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.update_connector_active(
            id=id,
            version_id=version_id,
        )

    return run_tool("qg_update_connector_active", _call)


@mcp.tool
def qg_put_connector_active(
    id: str,
    software_name: str,
    software_version: str,
    fabric_id: str,
    system_id: str,
    description: str | None = None,
    driver_nodes: list[str] | None = None,
    properties: dict[str, Any] | None = None,
    overrideable_properties: list[str] | None = None,
    allowed_os_users: list[str] | None = None,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Update the active version of a connector (PUT - full replacement).

    MANDATORY PARAMETERS: Ask the user for 'id', 'software_name', 'software_version', 'fabric_id',
        and 'system_id' if not provided.
    OPTIONAL PARAMETERS: All other parameters can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the connector. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.
        software_name (str): [MANDATORY] The name of the software package.
        software_version (str): [MANDATORY] The version of the software package.
        fabric_id (str): [MANDATORY] The ID of the fabric this connector belongs to.
            If the user doesn't know the fabric ID, suggest using qg_get_fabrics to list all fabrics.
        system_id (str): [MANDATORY] The ID of the system this connector belongs to.
            If the user doesn't know the system ID, suggest using qg_get_systems to list all systems.
        description (str | None): [OPTIONAL] Description of the connector.
        driver_nodes (list[str] | None): [OPTIONAL] List of node IDs where drivers should be installed.
        properties (dict | None): [OPTIONAL] Properties to configure the connector.
        overrideable_properties (list[str] | None): [OPTIONAL] Property names that can be overridden.
        allowed_os_users (list[str] | None): [OPTIONAL] OS users allowed to access this connector.
        tags (dict | None): [OPTIONAL] String key/value pairs for context.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_put_connector_active called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.put_connector_active(
            id=id,
            software_name=software_name,
            software_version=software_version,
            fabric_id=fabric_id,
            system_id=system_id,
            description=description,
            driver_nodes=driver_nodes,
            properties=properties,
            overrideable_properties=overrideable_properties,
            allowed_os_users=allowed_os_users,
            tags=tags,
        )

    return run_tool("qg_put_connector_active", _call)


@mcp.tool
def qg_put_connector_pending(
    id: str,
    software_name: str,
    software_version: str,
    fabric_id: str,
    system_id: str,
    description: str | None = None,
    driver_nodes: list[str] | None = None,
    properties: dict[str, Any] | None = None,
    overrideable_properties: list[str] | None = None,
    allowed_os_users: list[str] | None = None,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create or replace the pending version of a connector (PUT - full update).

    MANDATORY PARAMETERS: Ask the user for 'id', 'software_name', 'software_version', 'fabric_id',
        and 'system_id' if not provided.
    OPTIONAL PARAMETERS: All other parameters can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the connector. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.
        software_name (str): [MANDATORY] The name of the software package.
        software_version (str): [MANDATORY] The version of the software package.
        fabric_id (str): [MANDATORY] The ID of the fabric this connector belongs to.
            If the user doesn't know the fabric ID, suggest using qg_get_fabrics to list all fabrics.
        system_id (str): [MANDATORY] The ID of the system this connector belongs to.
            If the user doesn't know the system ID, suggest using qg_get_systems to list all systems.
        description (str | None): [OPTIONAL] Description of the connector.
        driver_nodes (list[str] | None): [OPTIONAL] List of node IDs where drivers should be installed.
        properties (dict | None): [OPTIONAL] Properties to configure the connector.
        overrideable_properties (list[str] | None): [OPTIONAL] Property names that can be overridden.
        allowed_os_users (list[str] | None): [OPTIONAL] OS users allowed to access this connector.
        tags (dict | None): [OPTIONAL] String key/value pairs for context.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_put_connector_pending called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.put_connector_pending(
            id=id,
            software_name=software_name,
            software_version=software_version,
            fabric_id=fabric_id,
            system_id=system_id,
            description=description,
            driver_nodes=driver_nodes,
            properties=properties,
            overrideable_properties=overrideable_properties,
            allowed_os_users=allowed_os_users,
            tags=tags,
        )

    return run_tool("qg_put_connector_pending", _call)


@mcp.tool
def qg_delete_connector_pending(
    id: str,
) -> dict[str, Any]:
    """
    Delete the pending version of a connector.

    MANDATORY PARAMETER: Ask the user for the connector ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the connector. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_connector_pending called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.delete_connector_pending(id)

    return run_tool("qg_delete_connector_pending", _call)


@mcp.tool
def qg_delete_connector_previous(
    id: str,
) -> dict[str, Any]:
    """
    Delete the previous version of a connector.

    MANDATORY PARAMETER: Ask the user for the connector ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the connector. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_connectors to list all connectors.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_connector_previous called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.connector_client.delete_connector_previous(id)

    return run_tool("qg_delete_connector_previous", _call)
