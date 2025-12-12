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

    Args:
        flatten (bool): Flatten the response structure
        extra_info (bool): Include extra information. Values are boolean True/False, not string.
        fabric_version (str | None): [Optional] Filter connectors by fabric version
        filter_by_name (str | None): [Optional] Get connector associated with the specified name (case insensitive).
             Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [Optional] Get connector associated with the specified tag.
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

    Args:
        id (str): The ID of the connector to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
        extra_info (bool): Include extra information. Values are boolean True/False, not string.

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

    Args:
        id (str): The ID of the connector. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

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

    Args:
        id (str): The ID of the connector. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

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

    Args:
        id (str): The ID of the connector. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

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

    Args:
        id (str): The ID of the connector. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.
        version_id (str): The version ID of the connector

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

    Args:
        name (str): The name of the connector.
        software_name (str): The name of the software package to use for this connector.
        software_version (str): The version of the software package to use for this connector.
        fabric_id (str): The ID of the fabric this connector belongs to.
        system_id (str): The ID of the system this connector belongs to.
        description (str | None): Optional description of the connector.
        driver_nodes (list[str] | None): Optional list of node IDs where drivers should be installed.
        properties (dict[str, Any] | None): Optional properties to configure the connector.
        overrideable_properties (list[str] | None): Optional list of property names that can be overridden at runtime.
        allowed_os_users (list[str] | None): Optional list of OS users allowed to access this connector.
        tags (dict[str, Any] | None): Optional string key/value pairs for associating some context with the connector.

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

    Args:
        id (str): The ID of the connector to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

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
