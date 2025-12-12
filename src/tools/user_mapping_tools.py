from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp

from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_user_mappings(filter_by_name: str | None = None) -> dict[str, Any]:
    """
    Get details of all QueryGrid user mappings.

    Args:
        filter_by_name (str | None): [Optional] Filter user mappings by name.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_user_mappings called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.user_mapping_client.get_user_mappings(
            filter_by_name=filter_by_name,
        )

    return run_tool("qg_get_user_mappings", _call)


@mcp.tool
def qg_get_user_mapping_by_id(id: str) -> dict[str, Any]:
    """
    Get a specific QueryGrid user mapping by ID.

    Args:
        id (str): The ID of the user mapping to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_user_mapping_by_id called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.user_mapping_client.get_user_mapping_by_id(id)

    return run_tool("qg_get_user_mapping_by_id", _call)


@mcp.tool
def qg_create_user_mapping(
    name: str,
    user_mapping: dict[str, Any] | None = None,
    role_mapping: dict[str, Any] | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """
    Create a new QueryGrid user mapping.

    Args:
        name (str): The name of the user mapping.
        user_mapping (dict | None): Optional user mapping dictionary.
        role_mapping (dict | None): Optional role mapping dictionary.
        description (str | None): Optional description of the user mapping.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_create_user_mapping called with name=%s", name)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.user_mapping_client.create_user_mapping(
            name=name,
            user_mapping=user_mapping,
            role_mapping=role_mapping,
            description=description,
        )

    return run_tool("qg_create_user_mapping", _call)


@mcp.tool
def qg_delete_user_mapping(
    mapping_id: str,
) -> dict[str, Any]:
    """
    Delete a user mapping by ID.

    Args:
        mapping_id (str): The ID of the user mapping to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_user_mapping called with mapping_id=%s", mapping_id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.user_mapping_client.delete_user_mapping(mapping_id)

    return run_tool("qg_delete_user_mapping", _call)
