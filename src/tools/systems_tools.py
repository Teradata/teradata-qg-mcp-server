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

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify filters, retrieve all systems.

    Args:
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.
        filter_by_proxy_support (str | None): [OPTIONAL] Filter systems based on proxy support type.
            Available values : NO_PROXY, LOCAL_PROXY, BRIDGE_PROXY
        filter_by_name (str | None): [OPTIONAL] Get system associated with the specified name (case insensitive).
            Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [OPTIONAL] Get system associated with the specified tag.
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

    MANDATORY PARAMETER: Ask the user for the system ID if not provided.
    OPTIONAL PARAMETERS: 'extra_info' can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the system to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_systems to list all systems.
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.

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

    MANDATORY PARAMETERS: Ask the user for 'name', 'system_type', 'platform_type', 'software_version',
        and 'data_center_id' if not provided.
    OPTIONAL PARAMETERS: All other parameters can be omitted.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. System name MUST be unique - duplicate names will cause creation to FAIL
    2. data_center_id MUST reference an existing datacenter - use qg_get_datacenters to find valid IDs
    3. software_version MUST be a valid NODE software version - use qg_get_software to find available versions
    4. maximum_memory_per_node is typically specified in bytes (e.g., 1073741824 for 1GB)
    5. All 5 mandatory parameters must be provided - missing any will cause FAIL

    Args:
        name (str): [MANDATORY] The name of the system.
            Ask the user: "What would you like to name the system?"
            Must be unique across all systems.
        system_type (str): [MANDATORY] The type of the system (e.g., TERADATA).
        platform_type (str): [MANDATORY] The platform type of the system (e.g., ON_PREM).
        software_version (str): [MANDATORY] Software version.
            Must be a valid NODE software version. Use qg_get_software to list available versions.
        data_center_id (str): [MANDATORY] Data center ID. ID is in UUID format.
            If the user doesn't know the data center ID, suggest using qg_get_datacenters to list available datacenters.
            The datacenter MUST already exist.
        description (str | None): [OPTIONAL] Description of the system.
        region (str | None): [OPTIONAL] Region.
        maximum_memory_per_node (float | None): [OPTIONAL] Maximum memory per node in bytes
            (e.g., 1073741824 for 1GB).
        bridge_only (bool | None): [OPTIONAL] Bridge only flag.
        proxy_support_type (str | None): [OPTIONAL] Proxy support type.
        proxy_port (int | None): [OPTIONAL] Proxy port.
        proxy_network_id (str | None): [OPTIONAL] Proxy network ID.
        proxy_bridge_id (str | None): [OPTIONAL] Proxy bridge ID.
        enable_proxy (bool | None): [OPTIONAL] Enable proxy flag.
        enable_override_port (bool | None): [OPTIONAL] Enable override port flag.
        override_port (int | None): [OPTIONAL] Override port.
        auto_node_delete (bool | None): [OPTIONAL] Auto node delete flag.
        auto_node_delete_minutes (int | None): [OPTIONAL] Auto node delete minutes.
        system_flavor (str | None): [OPTIONAL] System flavor.
        tags (dict | None): [OPTIONAL] String key/value pairs for context.

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
    Delete a SINGLE system by ID.

    Use this tool to delete ONE system at a time. For deleting multiple systems at once, do NOT use this tool.

    MANDATORY PARAMETER: Ask the user for the system ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the system to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_systems to list all systems.

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


@mcp.tool()
def qg_put_system(
    id: str,
    name: str,
    system_type: str,
    platform_type: str,
    description: str | None = None,
    data_center_id: str | None = None,
    region: str | None = None,
    software_version: str | None = None,
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
    Update an existing QueryGrid system configuration by ID.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:

    1. MANDATORY PARAMETERS:
       - 'id': UUID of the existing system to update (get from qg_get_systems if unknown)
       - 'name': System name (can be same or different from original)
       - 'system_type': Must be one of: TERADATA, PRESTO, HADOOP, OTHER
       - 'platform_type': Must be one of: AWS, AZURE, GC, PRIVATE, ON_PREM

    2. FULL REPLACEMENT (not partial):
       - PUT replaces the entire system configuration
       - All optional parameters not provided will be cleared/reset to defaults
       - To preserve existing values, you MUST retrieve them first with qg_get_system_by_id
       - Then include all fields you want to keep when calling this tool

    3. SYSTEM LIFECYCLE:
       - Unlike links/networks, systems do NOT have version management
       - Changes take effect immediately
       - No activate/deactivate states
       - No draft/active versions

    4. ID MUST EXIST:
       - The 'id' parameter must match an existing system
       - If system doesn't exist, you'll get a 404 error
       - Use qg_get_systems first to verify the system exists

    5. VALIDATION RULES:
       - system_type: Must be valid enum (TERADATA, PRESTO, HADOOP, OTHER)
       - platform_type: Must be valid enum (AWS, AZURE, GC, PRIVATE, ON_PREM)
       - proxy_support_type: Must be NO_PROXY, LOCAL_PROXY, or BRIDGE_PROXY (if provided)
       - system_flavor: Must be emr, cdp, dataproc, or hdinsight (if provided)
       - data_center_id: Must reference existing datacenter (if provided)
       - proxy_network_id: Must reference existing network rule (if provided)
       - proxy_bridge_id: Must reference existing bridge system (if provided)
       - maximum_memory_per_node: Must be positive number in bytes (if provided)
       - proxy_port, override_port: Must be valid port numbers 1-65535 (if provided)
       - auto_node_delete_minutes: Must be positive integer (if provided)

    6. ERROR CONDITIONS:
       - 400 Bad Request: Invalid data (wrong enum, missing field, validation failure)
       - 404 Not Found: System with specified ID doesn't exist
       - 409 Conflict: Name conflict with another system (if changing name)

    7. WHEN TO USE THIS vs CREATE:
       - Use qg_put_system when: Updating an existing system's configuration
       - Use qg_create_system when: Creating a brand new system
       - If unsure whether system exists, check with qg_get_systems first

    8. IMPACT:
       - Changes are immediate (no activation step)
       - Affects all nodes associated with this system
       - May require node restarts for some changes (e.g., software version)
       - Connections using this system may be temporarily disrupted

    9. BEST PRACTICES:
       - Always retrieve current configuration first with qg_get_system_by_id
       - Preserve fields you don't want to change
       - Validate enum values before calling
       - Consider impact on active connections
       - Update system name carefully (affects references)

    Args:
        id (str): [MANDATORY] The UUID of the system to update.
            Get from qg_get_systems if you don't know it.

        name (str): [MANDATORY] The name of the system.
            Must be unique across all systems unless updating the same system.

        system_type (str): [MANDATORY] The type of data source.
            Must be one of: TERADATA, PRESTO, HADOOP, OTHER

        platform_type (str): [MANDATORY] The platform where system is deployed.
            Must be one of: AWS, AZURE, GC, PRIVATE, ON_PREM

        description (str | None): [OPTIONAL] A description of the system.
            If not provided, will be cleared/empty.

        data_center_id (str | None): [OPTIONAL] The UUID of the data center.
            Must reference an existing datacenter object.
            If not provided, system won't be associated with a datacenter.

        region (str | None): [OPTIONAL] Region where the system is located.
            Free-form string (e.g., 'us-east-1', 'Europe', etc.)

        software_version (str | None): [OPTIONAL] Version of the tdqg-node package.
            Used for compatibility tracking.

        maximum_memory_per_node (float | None): [OPTIONAL] Max memory per node in bytes.
            Must be positive number. Used for resource planning.

        bridge_only (bool | None): [OPTIONAL] Flags if this system is bridge-only.
            Bridge-only systems don't store data, only facilitate connections.

        proxy_support_type (str | None): [OPTIONAL] Type of proxy support.
            Must be one of: NO_PROXY, LOCAL_PROXY, BRIDGE_PROXY
            Determines how connections are proxied to this system.

        proxy_port (int | None): [OPTIONAL] Port number for proxying connections.
            Valid range: 1-65535. Required if proxy is enabled.

        proxy_network_id (str | None): [OPTIONAL] UUID of network rule for proxy.
            Must reference an existing network rule.

        proxy_bridge_id (str | None): [OPTIONAL] ID of remote bridge system.
            Used when proxy_support_type is BRIDGE_PROXY.

        enable_proxy (bool | None): [OPTIONAL] Flags if this system runs a proxy.
            When true, system acts as proxy for other systems.

        enable_override_port (bool | None): [OPTIONAL] Override fabric TCP socket port.
            When true, uses override_port instead of default.

        override_port (int | None): [OPTIONAL] Port number for tdqg-node service.
            Valid range: 1-65535. Used when enable_override_port is true.

        auto_node_delete (bool | None): [OPTIONAL] Enable auto node deletion.
            When true, offline nodes are automatically deleted after timeout.

        auto_node_delete_minutes (int | None): [OPTIONAL] Minutes before auto delete.
            Positive integer. Required when auto_node_delete is true.

        system_flavor (str | None): [OPTIONAL] Flavor of Hadoop system.
            Must be one of: emr, cdp, dataproc, hdinsight
            Only applicable for HADOOP system_type.

        tags (dict[str, Any] | None): [OPTIONAL] String key/value pairs for metadata.
            Used for organization and filtering.

    Returns:
        dict[str, Any]: formatted response with updated system data + metadata
            On success: returns complete updated system object
            On error: returns error details with status code

    Example:
        To update a system's description and region:
        1. Get current config: current = qg_get_system_by_id(id="abc-123", extra_info=True)
        2. Update with preserved values:
           qg_put_system(
               id="abc-123",
               name=current["name"],
               system_type=current["systemType"],
               platform_type=current["platformType"],
               description="Updated description",  # new value
               region="us-west-2",  # new value
               software_version=current["softwareVersion"],  # preserve
               # ... include other fields to preserve them
           )
    """
    logger.debug("Tool: qg_put_system called with id=%s, name=%s", id, name)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.system_client.put_system(
            id=id,
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

    return run_tool("qg_put_system", _call)
