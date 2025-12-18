from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_node_virtual_ips() -> dict[str, Any]:
    """
    Get all QueryGrid node virtual IPs associated with the QueryGrid nodes.

    NO PARAMETERS REQUIRED.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_node_virtual_ips called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_virtual_ip_client.get_node_virtual_ips()

    return run_tool("qg_get_node_virtual_ips", _call)


@mcp.tool
def qg_get_node_virtual_ip_by_id(id: str) -> dict[str, Any]:
    """
    Get a specific QueryGrid node virtual IP by ID.

    MANDATORY PARAMETER: Ask the user for the virtual IP ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the virtual IP to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
            If the user doesn't know the ID, suggest using qg_get_node_virtual_ips to list all virtual IPs.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_node_virtual_ip_by_id called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_virtual_ip_client.get_node_virtual_ip_by_id(id)

    return run_tool("qg_get_node_virtual_ip_by_id", _call)


@mcp.tool
def qg_delete_node_virtual_ip(
    id: str,
) -> dict[str, Any]:
    """
    Delete a SINGLE node virtual IP by ID.

    Use this tool to delete ONE virtual IP at a time. For deleting multiple virtual IPs at once, do NOT use this tool.

    MANDATORY PARAMETER: Ask the user for the virtual IP ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the node virtual IP to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
            If the user doesn't know the ID, suggest using qg_get_node_virtual_ips to list all virtual IPs.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_node_virtual_ip called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_virtual_ip_client.delete_node_virtual_ip(id)

    return run_tool("qg_delete_node_virtual_ip", _call)


@mcp.tool
def qg_put_node_virtual_ip(
    id: str,
    virtual_ips: list[dict[str, str]],
) -> dict[str, Any]:
    """
    Save or update node virtual IPs by ID.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. The 'id' parameter MUST match an existing QgNode object's ID
    2. This is a FULL REPLACEMENT - all virtual IPs for the node must be provided
    3. Each virtual IP object must have both 'name' and 'address' keys
    4. No version management - changes take effect immediately
    5. This does NOT create a new node - only updates virtual IPs for existing nodes

    MANDATORY PARAMETERS: 'id', 'virtual_ips'

    Args:
        id (str): [MANDATORY] The ID of the QueryGrid node (must match an existing QgNode object).
            Format: UUID string (e.g., '123e4567-e89b-12d3-a456-426614174000')
            Use qg_get_nodes() to find valid node IDs.

        virtual_ips (list[dict[str, str]]): [MANDATORY] Array of virtual IP objects.
            Each object must contain:
            - 'name' (str): Network interface name (e.g., 'eth0', 'eth1')
            - 'address' (str): IP address (e.g., '10.10.10.10')

            Example: [{"name": "eth0", "address": "192.168.1.100"}, {"name": "eth1", "address": "10.0.0.50"}]

    ERROR CONDITIONS:
        - 400 Bad Request: Missing 'name' or 'address' in virtual IP objects, invalid IP format
        - 404 Not Found: Node ID doesn't exist

    WHEN TO USE:
        - Assigning virtual IPs to QueryGrid nodes
        - Updating virtual IP configuration for existing nodes
        - Configuring network interfaces for node connectivity

    WHEN NOT TO USE:
        - Creating new nodes (use node creation APIs instead)
        - Deleting all virtual IPs (use qg_delete_node_virtual_ip instead)
        - When node ID doesn't exist (create node first)

    BEST PRACTICES:
        - Validate node ID exists before calling (use qg_get_nodes)
        - Provide all virtual IPs for the node (this is a full replacement)
        - Verify IP addresses are valid and available
        - Ensure network interface names match actual interfaces on the node

    Returns:
        dict[str, Any]: formatted response with updated node virtual IP details + metadata
    """
    logger.debug(
        "Tool: qg_put_node_virtual_ip called with id=%s, virtual_ips=%s",
        id,
        virtual_ips,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.node_virtual_ip_client.put_node_virtual_ip(id, virtual_ips)

    return run_tool("qg_put_node_virtual_ip", _call)
