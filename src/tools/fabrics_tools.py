from __future__ import annotations

import logging
from typing import Any
from src.mcp_server import qg_mcp_server as mcp

from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_fabrics(
    flatten: bool = False,
    extra_info: bool = False,
    filter_by_name: str | None = None,
    filter_by_tag: str | None = None,
) -> dict[str, Any]:
    """
    Get details of all QueryGrid fabrics. Optional filters can be applied to narrow down the results.

    Args:
        flatten (bool): Flatten the response structure
        extra_info (bool): Include extra information. Values are boolean True/False, not string.
        filter_by_name (str | None): [Optional] Get fabric associated with the specified name (case insensitive).
            Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [Optional] Get fabric associated with the specified tag.
            Provide ','(comma) separated list of key:value pairs.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_fabrics called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.get_fabrics(
            flatten=flatten,
            extra_info=extra_info,
            filter_by_name=filter_by_name,
            filter_by_tag=filter_by_tag,
        )

    return run_tool("qg_get_fabrics", _call)


@mcp.tool
def qg_get_fabric_by_id(
    id: str,
    extra_info: bool = False,
) -> dict[str, Any]:
    """
    Get details of a specific QueryGrid fabric by ID.

    Args:
        id (str): The ID of the fabric to retrieve. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.
        extra_info (bool): Include extra information. Values are boolean True/False, not string.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_fabric_by_id called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.get_fabric_by_id(id=id, extra_info=extra_info)

    return run_tool("qg_get_fabric_by_id", _call)


@mcp.tool
def qg_get_fabric_active(
    id: str,
) -> dict[str, Any]:
    """
    Get the active configuration for a QueryGrid fabric.

    Args:
        id (str): The ID of the fabric. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_fabric_active called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.get_fabric_active(id)

    return run_tool("qg_get_fabric_active", _call)


@mcp.tool
def qg_get_fabric_pending(
    id: str,
) -> dict[str, Any]:
    """
    Get the pending configuration for a QueryGrid fabric.

    Args:
        id (str): The ID of the fabric. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_fabric_pending called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.get_fabric_pending(id)

    return run_tool("qg_get_fabric_pending", _call)


@mcp.tool
def qg_get_fabric_previous(
    id: str,
) -> dict[str, Any]:
    """
    Get the previous configuration for a QueryGrid fabric.

    Args:
        id (str): The ID of the fabric. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_fabric_previous called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.get_fabric_previous(id)

    return run_tool("qg_get_fabric_previous", _call)


@mcp.tool
def qg_create_fabric(
    name: str,
    port: int,
    softwareVersion: str,
    authKeySize: int,
    description: str | None = None,
    tags: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Create a new QueryGrid fabric.

    Args:
        name (str): The name of the fabric.
        port (int): The port for the fabric to use for communication between systems.
        softwareVersion (str): The software version of the fabric.
        authKeySize (int): The size of the authentication key in bits. Options: 1536, 2048, 3072, 4096.
        description (str | None): Optional description of the fabric.
        tags (dict | None): Optional string key/value pairs for associating some context with the fabric.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_create_fabric called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.create_fabric(
            name=name,
            port=port,
            softwareVersion=softwareVersion,
            authKeySize=authKeySize,
            description=description,
            tags=tags,
        )

    return run_tool("qg_create_fabric", _call)


@mcp.tool
def qg_delete_fabric(
    id: str,
) -> dict[str, Any]:
    """
    Delete a fabric by ID.

    Args:
        id (str): The ID of the fabric to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_fabric called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.delete_fabric(id)

    return run_tool("qg_delete_fabric", _call)
