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

    ALL PARAMETERS ARE MANDATORY. Ask the user for any missing values.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. link_id MUST reference an existing link - use qg_get_links to find valid IDs
    2. The specified link version (ACTIVE or PENDING) MUST exist - will FAIL if version doesn't exist
    3. Invalid credentials (admin user/password) will cause creation to FAIL
    4. Empty credentials will cause creation to FAIL
    5. version MUST be exactly "ACTIVE" or "PENDING" - other values will FAIL

    Args:
        initiator_admin_user (str): [MANDATORY] Admin user on initiator system.
            Ask the user: "What is the admin username on the initiator system?"
            Cannot be empty.
        initiator_admin_password (str): [MANDATORY] Password of the initiator's admin user.
            Ask the user: "What is the admin password?"
            Cannot be empty. Must be valid credentials.
        link_id (str): [MANDATORY] Id of the link to create the foreign server for. ID is in UUID format.
            If the user doesn't know the link ID, suggest using qg_get_links to list all links.
            The link MUST already exist.
        version (str): [MANDATORY] Version of the link to use.
            MUST be exactly "ACTIVE" or "PENDING".
            The specified version must exist for the link - will return 404 if version doesn't exist.
            Ask the user: "Which version should be used: ACTIVE or PENDING?"
        foreign_server_name (str): [MANDATORY] Name of the foreign server to create.
            Ask the user: "What would you like to name the foreign server?"

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_create_foreign_server: initiator_admin_user=%s, initiator_admin_password=%s, "
        "link_id=%s, version=%s, foreign_server_name=%s",
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

    MANDATORY PARAMETER: Ask the user for the diagnostic check ID if not provided.

    Args:
        id (str): [MANDATORY] The diagnostic check ID. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
            Use qg_create_foreign_server to initiate creation and get an ID.

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
