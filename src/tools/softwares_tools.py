from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_software(
    filter_by_name: str | None = None,
) -> dict[str, Any]:
    """
    Get QueryGrid software information for all of the uploaded software packages.
    Args:
        filter_by_name (str | None): [Optional] Get software associated with the specified name (case insensitive).
            Wildcard matching with '*' is supported.
    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_software called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.software_client.get_software(filter_by_name=filter_by_name)

    return run_tool("qg_get_software", _call)


@mcp.tool
def qg_get_software_jdbc_driver() -> dict[str, Any]:
    """
    Get QueryGrid software information for all of the uploaded JDBC driver software packages.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_software_jdbc_driver called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.software_client.get_software_jdbc_driver()

    return run_tool("qg_get_software_jdbc_driver", _call)


@mcp.tool
def qg_get_software_jdbc_driver_by_name(
    jdbc_driver_name: str,
) -> dict[str, Any]:
    """
    Get QueryGrid software information for the uploaded software packages related to a specific JDBC driver name.

    Args:
        jdbc_driver_name (str): The JDBC driver name to find

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_software_jdbc_driver_by_name called with jdbc_driver_name=%s", jdbc_driver_name)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.software_client.get_software_jdbc_driver_by_name(jdbc_driver_name)

    return run_tool("qg_get_software_jdbc_driver_by_name", _call)


@mcp.tool
def qg_get_software_by_id(
    id: str,
) -> dict[str, Any]:
    """
    Get a specific QueryGrid software by ID.

    Args:
        id (str): The ID of the software to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_software_by_id called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.software_client.get_software_by_id(id)

    return run_tool("qg_get_software_by_id", _call)


@mcp.tool
def qg_delete_software(
    id: str,
) -> dict[str, Any]:
    """
    Delete a software by ID.

    Args:
        id (str): The ID of the software to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_software called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.software_client.delete_software(id)

    return run_tool("qg_delete_software", _call)


@mcp.tool
def qg_delete_jdbc_driver(
    id: str,
) -> dict[str, Any]:
    """
    Delete a JDBC driver by ID.

    Args:
        id (str): The ID of the JDBC driver to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_jdbc_driver called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.software_client.delete_jdbc_driver(id)

    return run_tool("qg_delete_jdbc_driver", _call)
