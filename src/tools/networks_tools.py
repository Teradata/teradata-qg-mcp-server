from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp

from src.utils import run_tool

from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_networks(
    flatten: bool = False,
    extra_info: bool = False,
    filter_by_name: str | None = None,
    filter_by_tag: str | None = None,
) -> dict[str, Any]:
    """
    Get details of all QueryGrid networks.

    Args:
        flatten (bool): Flatten out the active, pending, and previous versions into array elements instead of
             nesting them.
        extra_info (bool): Include extra information. Values are boolean True/False, not string.
        filter_by_name (str | None): [Optional] Get network associated with the specified name (case insensitive).
            Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [Optional] Get network associated with the specified tag.
            Provide ','(comma) separated list of key:value pairs.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_get_networks called with flatten=%s, extra_info=%s, filter_by_name=%s, filter_by_tag=%s",
        flatten,
        extra_info,
        filter_by_name,
        filter_by_tag,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.get_networks(
            flatten=flatten,
            extra_info=extra_info,
            filter_by_name=filter_by_name,
            filter_by_tag=filter_by_tag,
        )

    return run_tool("qg_get_networks", _call)


@mcp.tool
def qg_get_network_by_id(
    id: str,
    extra_info: bool = False,
) -> dict[str, Any]:
    """
    Get a specific QueryGrid network by ID.

    Args:
        id (str): The ID of the network to retrieve. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.
        extra_info (bool): Include extra information. Values are boolean True/False, not string.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_get_network_by_id called with id=%s, extra_info=%s", id, extra_info
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.get_network_by_id(id, extra_info=extra_info)

    return run_tool("qg_get_network_by_id", _call)


@mcp.tool
def qg_get_network_active(id: str) -> dict[str, Any]:
    """
    Get the active configuration for a QueryGrid network.

    Args:
        id (str): The ID of the network. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_network_active called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.get_network_active(id)

    return run_tool("qg_get_network_active", _call)


@mcp.tool
def qg_get_network_pending(
    id: str,
) -> dict[str, Any]:
    """
    Get the pending configuration for a QueryGrid network.

    Args:
        id (str): The ID of the network. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_network_pending called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.get_network_pending(id)

    return run_tool("qg_get_network_pending", _call)


@mcp.tool
def qg_get_network_previous(
    id: str,
) -> dict[str, Any]:
    """
    Get the previous configuration for a QueryGrid network.

    Args:
        id (str): The ID of the network. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_network_previous called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.get_network_previous(id)

    return run_tool("qg_get_network_previous", _call)


@mcp.tool
def qg_create_network(
    name: str,
    connection_type: str,
    description: str | None = None,
    matching_rules: list[dict[str, Any]] | None = None,
    load_balancer_address: str | None = None,
    tags: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Create a new QueryGrid network.

    Args:
        name (str): The name of the network.
        connection_type (str): The type of connection. Valid values: STANDARD, LOAD_BALANCER, NO_INGRESS.
            Note: STANDARD connection type requires matching_rules to be provided.
        description (str | None): Optional description of the network.
        matching_rules (list[dict[str, Any]] | None): Rules for identifying network interfaces.
            Required when connection_type is STANDARD. Each rule should have 'type' and 'value' fields.
            Valid types: 'CIDR_NOTATION' (e.g., '192.168.1.0/24' or '0.0.0.0/0'), 'INTERFACE_NAME' (e.g., 'eth0').
        load_balancer_address (str | None): Load balancer address (required if connection_type is LOAD_BALANCER).
        tags (dict | None): Optional string key/value pairs for associating context with the network.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_create_network called with name=%s, connection_type=%s",
        name,
        connection_type,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.create_network(
            name=name,
            connection_type=connection_type,
            description=description,
            matching_rules=matching_rules,
            load_balancer_address=load_balancer_address,
            tags=tags,
        )

    return run_tool("qg_create_network", _call)


@mcp.tool
def qg_delete_network(
    id: str,
) -> dict[str, Any]:
    """
    Delete a network by ID.

    Args:
        id (str): The ID of the network to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_network called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.delete_network(id)

    return run_tool("qg_delete_network", _call)
