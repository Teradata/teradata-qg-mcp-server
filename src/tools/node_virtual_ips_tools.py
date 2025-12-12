from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_node_virtual_ips() -> dict[str, Any]:
    """
    Get all QueryGrid node virtual IPs associated with the QueryGrid nodes.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_node_virtual_ips called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_virtual_ip_client.get_node_virtual_ips()

    return run_tool("qg_get_node_virtual_ips", _call)


@mcp.tool
def qg_get_node_virtual_ip_by_id(id: str) -> dict[str, Any]:
    """
    Get a specific QueryGrid node virtual IP by ID.

    Args:
        id (str): The ID of the virtual IP to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_node_virtual_ip_by_id called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_virtual_ip_client.get_node_virtual_ip_by_id(id)

    return run_tool("qg_get_node_virtual_ip_by_id", _call)


@mcp.tool
def qg_delete_node_virtual_ip(
    id: str,
) -> dict[str, Any]:
    """
    Delete a node virtual IP by ID.

    Args:
        id (str): The ID of the node virtual IP to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_node_virtual_ip called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_virtual_ip_client.delete_node_virtual_ip(id)

    return run_tool("qg_delete_node_virtual_ip", _call)
