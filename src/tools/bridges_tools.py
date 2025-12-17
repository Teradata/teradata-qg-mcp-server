from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool

from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_bridges(
    filter_by_system_id: str | None = None, filter_by_name: str | None = None
) -> dict[str, Any]:
    """
    Get all QueryGrid bridges.

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify filters, retrieve all bridges.

    Args:
        filter_by_system_id (str | None): [OPTIONAL] Filter by system ID. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
        filter_by_name (str | None): [OPTIONAL] Filter bridges by name

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_get_bridges called with filter_by_system_id=%s, filter_by_name=%s",
        filter_by_system_id,
        filter_by_name,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.bridge_client.get_bridges(
            filter_by_system_id=filter_by_system_id, filter_by_name=filter_by_name
        )

    return run_tool("qg_get_bridges", _call)


@mcp.tool
def qg_get_bridge_by_id(id: str) -> dict[str, Any]:
    """
    Get a specific QueryGrid bridge by ID.

    MANDATORY PARAMETER: Ask the user for the bridge ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the bridge to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
            If the user doesn't know the ID, suggest using qg_get_bridges first to list all bridges.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_bridge_by_id called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.bridge_client.get_bridge_by_id(id)

    return run_tool("qg_get_bridge_by_id", _call)


@mcp.tool
def qg_create_bridge(
    name: str,
    system_id: str,
    node_ids: list[str] | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """
    Create a new bridge in QueryGrid Manager.

    MANDATORY PARAMETERS: Ask the user for 'name' and 'system_id' if not provided.
    OPTIONAL PARAMETERS: 'node_ids' and 'description' can be omitted.

    Args:
        name (str): [MANDATORY] The name of the bridge.
            Ask the user: "What would you like to name the bridge?"
        system_id (str): [MANDATORY] The system ID associated with the bridge. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
            If the user doesn't know the system ID, suggest using qg_get_systems to list available systems.
        node_ids (list[str] | None): [OPTIONAL] List of node IDs from the specified system to act as a bridge.
            If not provided, all nodes from the system will be used.
        description (str | None): [OPTIONAL] Description of the bridge.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_create_bridge called with name=%s, system_id=%s, node_ids=%s, description=%s",
        name,
        system_id,
        node_ids,
        description,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.bridge_client.create_bridge(
            name, system_id, node_ids, description
        )

    return run_tool("qg_create_bridge", _call)


@mcp.tool
def qg_delete_bridge(
    id: str,
) -> dict[str, Any]:
    """
    Delete a bridge by ID.

    MANDATORY PARAMETER: Ask the user for the bridge ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the bridge to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
            If the user doesn't know the ID, suggest using qg_get_bridges first to list all bridges.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_bridge called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.bridge_client.delete_bridge(id)

    return run_tool("qg_delete_bridge", _call)


@mcp.tool
def qg_update_bridge(
    id: str,
    name: str | None = None,
    system_id: str | None = None,
    node_ids: list[str] | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """
    Update an existing bridge in QueryGrid Manager.

    MANDATORY PARAMETER: 'id' is required - ask the user if not provided.
    OPTIONAL PARAMETERS: All other parameters are optional - only provide the fields the user wants to update.

    Note: The API requires 'name' and 'system_id' internally, but if not provided here,
    the current values will be automatically retrieved and preserved.

    Args:
        id (str): [MANDATORY] The ID of the bridge to update. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
            If the user doesn't know the ID, suggest using qg_get_bridges first to list all bridges.
        name (str | None): [OPTIONAL] New name for the bridge.
            Only provide this if the user wants to change the bridge name.
        system_id (str | None): [OPTIONAL] New system ID associated with the bridge. ID is in UUID format.
            Only provide this if the user wants to move the bridge to a different system.
        node_ids (list[str] | None): [OPTIONAL] New list of node IDs from the specified system to act as a bridge.
            Only provide this if the user wants to change which nodes are used.
        description (str | None): [OPTIONAL] New description of the bridge.
            Only provide this if the user wants to change the description.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_update_bridge called with id=%s, name=%s, system_id=%s, node_ids=%s, description=%s",
        id,
        name,
        system_id,
        node_ids,
        description,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.bridge_client.update_bridge(
            id, name, system_id, node_ids, description
        )

    return run_tool("qg_update_bridge", _call)
