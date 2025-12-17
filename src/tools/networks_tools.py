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

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify filters, retrieve all networks.

    Args:
        flatten (bool): [OPTIONAL] Flatten out the active, pending, and previous versions into array elements instead of
             nesting them.
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.
        filter_by_name (str | None): [OPTIONAL] Get network associated with the specified name (case insensitive).
            Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [OPTIONAL] Get network associated with the specified tag.
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

    MANDATORY PARAMETER: Ask the user for the network ID if not provided.
    OPTIONAL PARAMETERS: 'extra_info' can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the network to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_networks to list all networks.
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.

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

    MANDATORY PARAMETER: Ask the user for the network ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the network. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_networks to list all networks.

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

    MANDATORY PARAMETER: Ask the user for the network ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the network. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_networks to list all networks.

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

    MANDATORY PARAMETER: Ask the user for the network ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the network. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_networks to list all networks.

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

    MANDATORY PARAMETERS: Ask the user for 'name' and 'connection_type' if not provided.
    OPTIONAL PARAMETERS: Other parameters can be omitted depending on connection_type.

    Args:
        name (str): [MANDATORY] The name of the network.
            Ask the user: "What would you like to name the network?"
        connection_type (str): [MANDATORY] The type of connection. Valid values: STANDARD, LOAD_BALANCER, NO_INGRESS.
            Note: STANDARD connection type requires matching_rules to be provided.
        description (str | None): [OPTIONAL] Description of the network.
        matching_rules (list[dict[str, Any]] | None): [OPTIONAL - Required for STANDARD] Rules for identifying
            network interfaces. Required when connection_type is STANDARD. Each rule should have 'type' and
            'value' fields. Valid types: 'CIDR_NOTATION' (e.g., '192.168.1.0/24' or '0.0.0.0/0'),
            'INTERFACE_NAME' (e.g., 'eth0').
        load_balancer_address (str | None): [OPTIONAL - Required for LOAD_BALANCER] Load balancer address
            (required if connection_type is LOAD_BALANCER).
        tags (dict | None): [OPTIONAL] String key/value pairs for associating context with the network.

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

    MANDATORY PARAMETER: Ask the user for the network ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the network to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_networks to list all networks.

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


@mcp.tool
def qg_update_network(
    id: str,
    name: str,
    description: str | None = None,
) -> dict[str, Any]:
    """
    Update network metadata (name and description only).

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    - This ONLY updates the wrapper-level metadata (name, description)
    - Does NOT modify active/pending/previous version configurations
    - To change connectionType, matchingRules, etc., use qg_put_network_active or qg_put_network_pending
    - The 'name' parameter is MANDATORY even if you only want to update description

    MANDATORY PARAMETER: Ask the user for the network ID and name if not provided.
    OPTIONAL PARAMETER: 'description' can be omitted if not changing.

    When to use this tool:
    - Renaming a network without changing its configuration
    - Updating the description of a network
    - Simple metadata updates that don't require version management

    When NOT to use this tool:
    - Changing connectionType, matchingRules, or loadBalancerAddress (use PUT tools instead)
    - Creating new versions (use qg_put_network_pending)
    - Activating pending versions (use qg_update_network_active)

    Args:
        id (str): [MANDATORY] The ID of the network wrapper. UUID format.
        name (str): [MANDATORY] The name of the network. Required even if not changing.
        description (str | None): [OPTIONAL] Updated description. Omit to keep existing.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_update_network called with id=%s, name=%s", id, name)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.update_network(id, name, description)

    return run_tool("qg_update_network", _call)


@mcp.tool
def qg_update_network_active(
    id: str,
    version_id: str,
) -> dict[str, Any]:
    """
    Activate a specific version (pending or previous) of a network using PATCH.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    - This is the RECOMMENDED way to activate changes - safer than PUT /active
    - Requires a pending version to exist first (create with qg_put_network_pending)
    - The version_id must be from the pending version's 'versionId' field
    - When activated, the current active becomes previous (if previous exists, it's lost)
    - Only 3 version slots exist: active (mandatory), pending (optional), previous (optional)

    VERSION LIFECYCLE WORKFLOW:
    1. Network has active version (current configuration)
    2. Create pending version with qg_put_network_pending (for review/testing)
    3. Get pending version details with qg_get_network_pending to obtain versionId
    4. Use THIS TOOL to promote pending → active (old active → previous)
    5. Previous version becomes rollback point

    IMPORTANT: This operation takes effect IMMEDIATELY across all nodes using this network.

    MANDATORY PARAMETERS: Ask user for network ID and version_id if not provided.

    Common workflow:
    ```
    # 1. Create pending version for review
    pending = qg_put_network_pending(id="uuid", name="MyNetwork", ...)

    # 2. Get the versionId from pending
    pending_version = qg_get_network_pending(id="uuid")
    version_id = pending_version["versionId"]

    # 3. Activate it
    qg_update_network_active(id="uuid", version_id=version_id)
    ```

    Error conditions:
    - 404: Network ID not found
    - 404: Pending version doesn't exist (must create with qg_put_network_pending first)
    - 400: Invalid version_id format or doesn't match pending version

    Args:
        id (str): [MANDATORY] The ID of the network wrapper. UUID format.
        version_id (str): [MANDATORY] The versionId from the pending version to activate.
            Get this from qg_get_network_pending response.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_update_network_active called with id=%s, version_id=%s",
        id,
        version_id,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.update_network_active(id, version_id)

    return run_tool("qg_update_network_active", _call)


@mcp.tool
def qg_put_network_active(
    id: str,
    name: str,
    connection_type: str,
    description: str | None = None,
    matching_rules: list[dict[str, Any]] | None = None,
    load_balancer_address: str | None = None,
    tags: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Replace the active network version with a new configuration.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    - This IMMEDIATELY replaces the active configuration (takes effect right away!)
    - The old active version moves to previous (overwrites any existing previous)
    - NO pending version is created - this is a direct replacement
    - RECOMMENDED: Use qg_put_network_pending + qg_update_network_active instead for safer workflow
    - This is a FULL replacement - all parameters must be provided

    WHEN TO USE THIS TOOL:
    - Emergency configuration changes that need immediate effect
    - Simple network setups where review workflow isn't needed
    - You are absolutely certain the new configuration is correct

    WHEN NOT TO USE (use qg_put_network_pending instead):
    - Production environments where changes should be reviewed
    - Complex configurations that need testing before activation
    - When you want to preserve the ability to easily rollback

    MANDATORY PARAMETERS:
    - id: Network wrapper ID
    - name: Network name
    - connection_type: Must be one of: STANDARD, LOAD_BALANCER, NO_INGRESS

    CONNECTION TYPE REQUIREMENTS:
    - STANDARD: Requires matching_rules (typically CIDR_NOTATION or INTERFACE_NAME)
    - LOAD_BALANCER: Requires load_balancer_address
    - NO_INGRESS: Doesn't require matching_rules or load_balancer_address

    Error conditions:
    - 404: Network ID not found
    - 400: Invalid connection_type
    - 400: STANDARD without matching_rules
    - 400: LOAD_BALANCER without load_balancer_address

    Args:
        id (str): [MANDATORY] The ID of the network wrapper. UUID format.
        name (str): [MANDATORY] The name of the network.
        connection_type (str): [MANDATORY] Connection type: STANDARD, LOAD_BALANCER, or NO_INGRESS.
        description (str | None): [OPTIONAL] Description of the network.
        matching_rules (list[dict] | None): [REQUIRED for STANDARD] Rules for identifying network interfaces.
            Each rule needs 'type' and 'value'. Types: CIDR_NOTATION, INTERFACE_NAME.
            Example: [{"type": "CIDR_NOTATION", "value": "192.168.1.0/24"}]
        load_balancer_address (str | None): [REQUIRED for LOAD_BALANCER] Load balancer address.
        tags (dict | None): [OPTIONAL] Key/value pairs for context.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_put_network_active called with id=%s, name=%s, connection_type=%s",
        id,
        name,
        connection_type,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.put_network_active(
            id=id,
            name=name,
            connection_type=connection_type,
            description=description,
            matching_rules=matching_rules,
            load_balancer_address=load_balancer_address,
            tags=tags,
        )

    return run_tool("qg_put_network_active", _call)


@mcp.tool
def qg_put_network_pending(
    id: str,
    name: str,
    connection_type: str,
    description: str | None = None,
    matching_rules: list[dict[str, Any]] | None = None,
    load_balancer_address: str | None = None,
    tags: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Create or replace a pending network version for review before activation.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    - This creates a PENDING version that does NOT take effect immediately
    - RECOMMENDED WORKFLOW: Create pending → review → activate with qg_update_network_active
    - If a pending version already exists, it will be REPLACED (overwritten)
    - The pending version can be reviewed with qg_get_network_pending
    - Activate the pending version with qg_update_network_active
    - Delete pending with qg_delete_network_pending if you change your mind

    RECOMMENDED WORKFLOW:
    1. Create pending version with THIS TOOL (for review/testing)
    2. Review the configuration with qg_get_network_pending
    3. Activate when ready with qg_update_network_active
    4. Old active becomes previous (automatic rollback point)

    WHEN TO USE THIS TOOL:
    - Production environments where changes need review
    - Complex configurations that should be validated before going live
    - When you want a clear separation between "proposed" and "active" config

    MANDATORY PARAMETERS:
    - id: Network wrapper ID
    - name: Network name
    - connection_type: Must be one of: STANDARD, LOAD_BALANCER, NO_INGRESS

    CONNECTION TYPE REQUIREMENTS:
    - STANDARD: Requires matching_rules (typically CIDR_NOTATION or INTERFACE_NAME)
    - LOAD_BALANCER: Requires load_balancer_address
    - NO_INGRESS: Doesn't require matching_rules or load_balancer_address

    Error conditions:
    - 404: Network ID not found
    - 400: Invalid connection_type
    - 400: STANDARD without matching_rules
    - 400: LOAD_BALANCER without load_balancer_address

    Args:
        id (str): [MANDATORY] The ID of the network wrapper. UUID format.
        name (str): [MANDATORY] The name of the network.
        connection_type (str): [MANDATORY] Connection type: STANDARD, LOAD_BALANCER, or NO_INGRESS.
        description (str | None): [OPTIONAL] Description of the network.
        matching_rules (list[dict] | None): [REQUIRED for STANDARD] Rules for identifying network interfaces.
            Each rule needs 'type' and 'value'. Types: CIDR_NOTATION, INTERFACE_NAME.
            Example: [{"type": "CIDR_NOTATION", "value": "192.168.1.0/24"}]
        load_balancer_address (str | None): [REQUIRED for LOAD_BALANCER] Load balancer address.
        tags (dict | None): [OPTIONAL] Key/value pairs for context.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_put_network_pending called with id=%s, name=%s, connection_type=%s",
        id,
        name,
        connection_type,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.put_network_pending(
            id=id,
            name=name,
            connection_type=connection_type,
            description=description,
            matching_rules=matching_rules,
            load_balancer_address=load_balancer_address,
            tags=tags,
        )

    return run_tool("qg_put_network_pending", _call)


@mcp.tool
def qg_delete_network_pending(
    id: str,
) -> dict[str, Any]:
    """
    Delete the pending network version.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    - This deletes the pending version (if it exists)
    - Does NOT affect the active or previous versions
    - The active configuration remains unchanged
    - Use this to discard proposed changes that haven't been activated yet
    - After deletion, you can create a new pending version with qg_put_network_pending

    WHEN TO USE THIS TOOL:
    - Discarding a pending version you decided not to activate
    - Clearing pending to create a fresh new pending version
    - Cleaning up after testing/review shows pending version has issues

    SAFER ALTERNATIVES:
    - Instead of deleting and recreating, just use qg_put_network_pending again (replaces pending)

    IMPORTANT: If no pending version exists, this will return a 404 error (not a problem).

    Error conditions:
    - 404: Network ID not found
    - 404: No pending version exists (not necessarily an error - just means nothing to delete)

    Args:
        id (str): [MANDATORY] The ID of the network wrapper. UUID format.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_network_pending called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.delete_network_pending(id)

    return run_tool("qg_delete_network_pending", _call)


@mcp.tool
def qg_delete_network_previous(
    id: str,
) -> dict[str, Any]:
    """
    Delete the previous network version (removes rollback capability).

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    - This deletes the previous version (your rollback point!)
    - Does NOT affect the active or pending versions
    - After deletion, you CANNOT easily rollback to the previous configuration
    - The previous version is automatically created when you activate a pending version
    - Only one previous version exists at a time (newest previous replaces older)

    VERSION LIFECYCLE REMINDER:
    - Active: Current running configuration
    - Pending: Proposed changes (optional, can be reviewed before activation)
    - Previous: Last active configuration before current (automatic rollback point)

    WHEN TO USE THIS TOOL:
    - Cleaning up old configurations you're certain you won't need
    - Free up storage space (though minimal)
    - You're absolutely confident the current active version is correct

    WHEN NOT TO USE:
    - Shortly after activating a new version (previous is your safety net!)
    - In production environments where rollback capability is important
    - When the active version hasn't been thoroughly tested yet

    IMPORTANT: You can manually rollback by:
    1. Get previous version details with qg_get_network_previous
    2. Create it as pending with qg_put_network_pending
    3. Activate it with qg_update_network_active
    But this is MORE WORK than just keeping the previous version!

    Error conditions:
    - 404: Network ID not found
    - 404: No previous version exists (not necessarily an error)

    Args:
        id (str): [MANDATORY] The ID of the network wrapper. UUID format.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_network_previous called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.network_client.delete_network_previous(id)

    return run_tool("qg_delete_network_previous", _call)
