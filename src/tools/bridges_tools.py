from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool

from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_bridges(filter_by_system_id: str | None = None, filter_by_name: str | None = None) -> dict[str, Any]:
    """
    Get all QueryGrid bridges. Optional arguments can be ignored if not needed.

    Args:
        filter_by_system_id (str | None): [Optional] Filter by system ID. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
        filter_by_name (str | None): [Optional] Filter bridges by name

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

    Args:
        id (str): The ID of the bridge to retrieve. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

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

    Args:
        name (str): The name of the bridge.
        system_id (str): The system ID associated with the bridge. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
        node_ids (list[str] | None): List of node IDs from the specified system to act as a bridge.
        description (str | None): Optional description of the bridge.

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
        return qg_manager.bridge_client.create_bridge(name, system_id, node_ids, description)

    return run_tool("qg_create_bridge", _call)


@mcp.tool
def qg_delete_bridge(
    id: str,
) -> dict[str, Any]:
    """
    Delete a bridge by ID.

    Args:
        id (str): The ID of the bridge to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

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
