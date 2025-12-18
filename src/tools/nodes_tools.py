from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_nodes(
    filter_by_system_id: str | None = None,
    filter_by_bridge_id: str | None = None,
    filter_by_fabric_id: str | None = None,
    filter_by_connector_id: str | None = None,
    extra_info: bool = False,
    fabric_version: str | None = None,
    connector_version: str | None = None,
    drivers: str | None = None,
    details: bool = False,
    filter_by_name: str | None = None,
) -> dict[str, Any]:
    """
    Retrieve information about QueryGrid nodes. Use optional filter parameters to narrow results by specific
    criteria such as system ID, fabric ID, connector ID, or node name. Leave optional parameters unset
    if no filtering is required.

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify filters, retrieve all nodes.

    Args:
        filter_by_system_id (str | None): [OPTIONAL] Filter nodes by system ID. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
        filter_by_bridge_id (str | None): [OPTIONAL] Filter nodes by bridge ID. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
        filter_by_fabric_id (str | None): [OPTIONAL] Filter nodes by fabric ID. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
        filter_by_connector_id (str | None): [OPTIONAL] Filter nodes by connector ID. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.
        fabric_version (str | None): [OPTIONAL] Filter nodes by fabric version. e.g., "03.10.00.01".
        connector_version (str | None): [OPTIONAL] Filter nodes by connector version. e.g., "03.10.00.01".
        drivers (str | None): [OPTIONAL] Works with filter_by_connector_id to make status relative to the
            drivers for the specified connector. Values can be True/False.
        details (bool): [OPTIONAL] Include detailed information
        filter_by_name (str | None): [OPTIONAL] Filter nodes by name. The name can be any sequence of characters
            representing the node's name, such as 'Node1'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_nodes called")

    def _call() -> dict[str, Any]:
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_client.get_nodes(
            filter_by_system_id=filter_by_system_id,
            filter_by_bridge_id=filter_by_bridge_id,
            filter_by_fabric_id=filter_by_fabric_id,
            filter_by_connector_id=filter_by_connector_id,
            extra_info=extra_info,
            fabric_version=fabric_version,
            connector_version=connector_version,
            drivers=drivers,
            details=details,
            filter_by_name=filter_by_name,
        )

    return run_tool("qg_get_nodes", _call)


@mcp.tool
def qg_get_node_by_id(id: str) -> dict[str, Any]:
    """
    Get details of a specific QueryGrid node by ID.

    MANDATORY PARAMETER: Ask the user for the node ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the node to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_nodes to list all nodes.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_node_by_id called")

    def _call() -> dict[str, Any]:
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_client.get_node_by_id(id)

    return run_tool("qg_get_node_by_id", _call)


@mcp.tool
def qg_get_node_heartbeat_by_id(id: str) -> dict[str, Any]:
    """
    Get the latest heartbeat sent by a specific QueryGrid node by ID.

    MANDATORY PARAMETER: Ask the user for the node ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the node to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_nodes to list all nodes.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_node_heartbeat_by_id called")

    def _call() -> dict[str, Any]:
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_client.get_node_heartbeat_by_id(id)

    return run_tool("qg_get_node_heartbeat_by_id", _call)


@mcp.tool
def qg_delete_node(
    id: str,
) -> dict[str, Any]:
    """
    Delete a SINGLE node by ID.

    Use this tool to delete ONE node at a time. For deleting multiple nodes at once, use qg_bulk_delete instead.

    MANDATORY PARAMETER: Ask the user for the node ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the node to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_nodes to list all nodes.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_node called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_client.delete_node(id)

    return run_tool("qg_delete_node", _call)
