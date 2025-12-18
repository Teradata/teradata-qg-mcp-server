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

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify filters, retrieve all managers.

    Args:
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.
        filter_by_name (str | None): [OPTIONAL] Get manager associated with the specified hostname
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

    MANDATORY PARAMETER: Ask the user for the manager ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the manager to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
            If the user doesn't know the ID, suggest using qg_get_managers to list all managers.

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
