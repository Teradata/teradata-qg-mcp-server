from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp

from src.utils import run_tool

from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_managers(extra_info: bool = False, filter_by_name: str | None = None) -> dict[str, Any]:
    """
    Get details of all QueryGrid managers.

    Args:
        extra_info (bool): Include extra information. Values are boolean True/False, not string.
        filter_by_name (str | None): [Optional] Get manager associated with the specified hostname
            (case insensitive). Wildcard matching with '*' is supported.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_managers called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        # Run the synchronous operation
        return qg_manager.manager_client.get_managers(
            extra_info=extra_info,
            filter_by_name=filter_by_name,
        )

    return run_tool("qg_get_managers", _call)


@mcp.tool
def qg_get_manager_by_id(id: str) -> dict[str, Any]:
    """

    Get a specific QueryGrid manager by ID.

    Args:
        id (str): The ID of the manager to retrieve. ID is in UUID format.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_manager_by_id called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.manager_client.get_manager_by_id(id)

    return run_tool("qg_get_manager_by_id", _call)
