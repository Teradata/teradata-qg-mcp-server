from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp

from src.utils import run_tool

from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_users() -> dict[str, Any]:
    """
    Get all QueryGrid user accounts.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_users called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.user_client.get_users()

    return run_tool("qg_get_users", _call)


@mcp.tool
def qg_get_user_by_username(username: str) -> dict[str, Any]:
    """
    Get a specific QueryGrid user account by username.

    Args:
        username (str): The username of the user to retrieve

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_user_by_username called with username=%s", username)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.user_client.get_user_by_username(username)

    return run_tool("qg_get_user_by_username", _call)


@mcp.tool
def qg_create_user(username: str, password: str, description: str | None = None) -> dict[str, Any]:
    """
    Create a new user in QueryGrid Manager.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        description (str | None): Optional description of the user.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_create_user called with username=%s, description=%s",
        username,
        description,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.user_client.create_user(username, password, description)

    return run_tool("qg_create_user", _call)


@mcp.tool
def qg_delete_user(
    username: str,
) -> dict[str, Any]:
    """
    Delete a user by username.

    Args:
        username (str): The username of the user to delete.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_user called with username=%s", username)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.user_client.delete_user(username)

    return run_tool("qg_delete_user", _call)
