from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp

from src.utils import run_tool

from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_systems(
    extra_info: bool = False,
    filter_by_proxy_support: str | None = None,
    filter_by_name: str | None = None,
    filter_by_tag: str | None = None,
) -> dict[str, Any]:
    """
    Get details of all QueryGrid systems.

    Args:
        extra_info (bool): Include extra information. Values are boolean True/False, not string.
        filter_by_proxy_support (str | None): [Optional] Filter systems based on proxy support type.
            Available values : NO_PROXY, LOCAL_PROXY, BRIDGE_PROXY
        filter_by_name (str | None): [Optional] Get system associated with the specified name (case insensitive).
            Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [Optional] Get system associated with the specified tag.
            Provide ','(comma) separated list of key:value pairs.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_systems called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.system_client.get_systems(
            extra_info=extra_info,
            filter_by_proxy_support=filter_by_proxy_support,
            filter_by_name=filter_by_name,
            filter_by_tag=filter_by_tag,
        )

    return run_tool("qg_get_systems", _call)


@mcp.tool
def qg_get_system_by_id(id: str, extra_info: bool = False) -> dict[str, Any]:
    """
    Get a specific QueryGrid system by ID.

    Args:
        id (str): The ID of the system to retrieve. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.
        extra_info (bool): Include extra information. Values are boolean True/False, not string.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_system_by_id called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.system_client.get_system_by_id(id, extra_info=extra_info)

    return run_tool("qg_get_system_by_id", _call)


@mcp.tool
def qg_create_system(
    name: str,
    system_type: str,
    platform_type: str,
    software_version: str,
    data_center_id: str,
    description: str | None = None,
    region: str | None = None,
    maximum_memory_per_node: float | None = None,
    bridge_only: bool | None = None,
    proxy_support_type: str | None = None,
    proxy_port: int | None = None,
    proxy_network_id: str | None = None,
    proxy_bridge_id: str | None = None,
    enable_proxy: bool | None = None,
    enable_override_port: bool | None = None,
    override_port: int | None = None,
    auto_node_delete: bool | None = None,
    auto_node_delete_minutes: int | None = None,
    system_flavor: str | None = None,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a new QueryGrid system.

    Args:
        name (str): The name of the system.
        system_type (str): The type of the system.
        platform_type (str): The platform type of the system.
        description (str | None): Optional description of the system.
        data_center_id (str): Data center ID.
        region (str | None): Optional region.
        software_version (str): Software version.
        maximum_memory_per_node (float | None): Optional maximum memory per node.
        bridge_only (bool | None): Optional bridge only flag.
        proxy_support_type (str | None): Optional proxy support type.
        proxy_port (int | None): Optional proxy port.
        proxy_network_id (str | None): Optional proxy network ID.
        proxy_bridge_id (str | None): Optional proxy bridge ID.
        enable_proxy (bool | None): Optional enable proxy flag.
        enable_override_port (bool | None): Optional enable override port flag.
        override_port (int | None): Optional override port.
        auto_node_delete (bool | None): Optional auto node delete flag.
        auto_node_delete_minutes (int | None): Optional auto node delete minutes.
        system_flavor (str | None): Optional system flavor.
        tags (dict | None): Optional string key/value pairs for context.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_create_system called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.system_client.create_system(
            name=name,
            system_type=system_type,
            platform_type=platform_type,
            description=description,
            data_center_id=data_center_id,
            region=region,
            software_version=software_version,
            maximum_memory_per_node=maximum_memory_per_node,
            bridge_only=bridge_only,
            proxy_support_type=proxy_support_type,
            proxy_port=proxy_port,
            proxy_network_id=proxy_network_id,
            proxy_bridge_id=proxy_bridge_id,
            enable_proxy=enable_proxy,
            enable_override_port=enable_override_port,
            override_port=override_port,
            auto_node_delete=auto_node_delete,
            auto_node_delete_minutes=auto_node_delete_minutes,
            system_flavor=system_flavor,
            tags=tags,
        )

    return run_tool("qg_create_system", _call)


@mcp.tool
def qg_delete_system(
    id: str,
) -> dict[str, Any]:
    """
    Delete a system by ID.

    Args:
        id (str): The ID of the system to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_system called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.system_client.delete_system(id)

    return run_tool("qg_delete_system", _call)
