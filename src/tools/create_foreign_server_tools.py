from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_create_foreign_server(
    initiator_admin_user: str,
    initiator_admin_password: str,
    link_id: str,
    version: str,
    foreign_server_name: str,
) -> dict[str, Any]:
    """
    Create a foreign server.

    Args:
        initiator_admin_user (str): Admin user on initiator system.
        initiator_admin_password (str): Password of the initiator's admin user.
        link_id (str): Id of the link to create the foreign server for.
        version (str): Version of the link (ACTIVE, PENDING). Required.
        foreign_server_name (str): Name of the foreign server to create. Required.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_create_foreign_server: initiator_admin_user=%s, initiator_admin_password=%s, link_id=%s, version=%s, foreign_server_name=%s",
        initiator_admin_user,
        "***" if initiator_admin_password else None,
        link_id,
        version,
        foreign_server_name,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.create_foreign_server_client.create_foreign_server(
            initiator_admin_user=initiator_admin_user,
            initiator_admin_password=initiator_admin_password,
            link_id=link_id,
            version=version,
            foreign_server_name=foreign_server_name,
        )

    return run_tool("qg_create_foreign_server", _call)


@mcp.tool
def qg_get_create_foreign_server_status(id: str) -> dict[str, Any]:
    """
    Get the status of the CONNECTOR_CFS diagnostic check for foreign server creation.

    Args:
        id (str): The diagnostic check ID. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_create_foreign_server_status called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.create_foreign_server_client.get_create_foreign_server_status(id)

    return run_tool("qg_get_create_foreign_server_status", _call)
