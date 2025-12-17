from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp

from src.utils import run_tool

from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_datacenters(filter_by_name: str | None = None) -> dict[str, Any]:
    """
    Get details of all QueryGrid datacenters.

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify filters, retrieve all datacenters.

    Args:
        filter_by_name (str | None): [OPTIONAL] Filter datacenters by name

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_get_datacenters called with filter_by_name=%s", filter_by_name
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.datacenter_client.get_datacenters(
            filter_by_name=filter_by_name,
        )

    return run_tool("qg_get_datacenters", _call)


@mcp.tool
def qg_get_datacenter_by_id(
    id: str,
) -> dict[str, Any]:
    """
    Get a specific QueryGrid datacenter by ID.

    MANDATORY PARAMETER: Ask the user for the datacenter ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the datacenter to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_datacenters to list all datacenters.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_datacenter_by_id called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.datacenter_client.get_datacenter_by_id(id)

    return run_tool("qg_get_datacenter_by_id", _call)


@mcp.tool
def qg_create_datacenter(
    name: str,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a new data center in QueryGrid Manager.

    MANDATORY PARAMETER: Ask the user for 'name' if not provided.
    OPTIONAL PARAMETERS: 'description' and 'tags' can be omitted.

    Args:
        name (str): [MANDATORY] The name of the data center.
            Ask the user: "What would you like to name the data center?"
        description (str | None): [OPTIONAL] Description of the data center.
        tags (dict[str, Any] | None): [OPTIONAL] String key/value pairs for associating some context
            with the data center.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_create_datacenter called with name=%s, description=%s, tags=%s",
        name,
        description,
        tags,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.datacenter_client.create_datacenter(
            name=name,
            description=description,
            tags=tags,
        )

    return run_tool("qg_create_datacenter", _call)


@mcp.tool
def qg_update_datacenter(
    id: str,
    name: str,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Update a data center using PUT (full replacement).

    MANDATORY PARAMETERS: Ask the user for 'id' and 'name' if not provided.
    OPTIONAL PARAMETERS: 'description' and 'tags' can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the data center to update. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_datacenters to list all datacenters.
        name (str): [MANDATORY] The name of the data center.
        description (str | None): [OPTIONAL] Description of the data center.
        tags (dict[str, Any] | None): [OPTIONAL] String key/value pairs for associating some context
            with the data center.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_update_datacenter called with id=%s, name=%s, description=%s, tags=%s",
        id,
        name,
        description,
        tags,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.datacenter_client.update_datacenter(
            id=id,
            name=name,
            description=description,
            tags=tags,
        )

    return run_tool("qg_update_datacenter", _call)


@mcp.tool
def qg_delete_datacenter(
    id: str,
) -> dict[str, Any]:
    """
    Delete a data center by ID.

    MANDATORY PARAMETER: Ask the user for the datacenter ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the data center to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_datacenters to list all datacenters.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_datacenter called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.datacenter_client.delete_datacenter(id)

    return run_tool("qg_delete_datacenter", _call)
