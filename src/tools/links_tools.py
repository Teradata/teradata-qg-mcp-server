from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp

from src.utils import run_tool

from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_links(
    flatten: bool = False,
    extra_info: bool = False,
    filter_by_name: str | None = None,
    filter_by_tag: str | None = None,
) -> dict[str, Any]:
    """
    Get details of all QueryGrid links. Optional filters can be applied to narrow down the results.

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify filters, retrieve all links.

    Args:
        flatten (bool): [OPTIONAL] Flatten the response structure
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.
        filter_by_name (str | None): [OPTIONAL] Get link associated with the specified name (case insensitive).
            Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [OPTIONAL] Get link associated with the specified tag.
            Provide ','(comma) separated list of key:value pairs.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_links called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.get_links(
            flatten=flatten,
            extra_info=extra_info,
            filter_by_name=filter_by_name,
            filter_by_tag=filter_by_tag,
        )

    return run_tool("qg_get_links", _call)


@mcp.tool
def qg_get_link_by_id(
    id: str,
    extra_info: bool = False,
) -> dict[str, Any]:
    """
    Get a specific QueryGrid link by ID.

    MANDATORY PARAMETER: Ask the user for the link ID if not provided.
    OPTIONAL PARAMETERS: 'extra_info' can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the link to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_links to list all links.
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_link_by_id called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.get_link_by_id(id, extra_info=extra_info)

    return run_tool("qg_get_link_by_id", _call)


@mcp.tool
def qg_get_link_active(
    id: str,
) -> dict[str, Any]:
    """
    Get the active configuration for a QueryGrid link.

    MANDATORY PARAMETER: Ask the user for the link ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the link. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_links to list all links.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_link_active called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.get_link_active(id)

    return run_tool("qg_get_link_active", _call)


@mcp.tool
def qg_get_link_pending(
    id: str,
) -> dict[str, Any]:
    """
    Get the pending configuration for a QueryGrid link.

    MANDATORY PARAMETER: Ask the user for the link ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the link. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_links to list all links.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_link_pending called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.get_link_pending(id)

    return run_tool("qg_get_link_pending", _call)


@mcp.tool
def qg_get_link_previous(
    id: str,
) -> dict[str, Any]:
    """
    Get the previous configuration for a QueryGrid link.

    MANDATORY PARAMETER: Ask the user for the link ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the link. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_links to list all links.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_link_previous called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.get_link_previous(id)

    return run_tool("qg_get_link_previous", _call)


@mcp.tool
def qg_create_link(
    name: str,
    fabricId: str,
    initiatorConnectorId: str,
    targetConnectorId: str,
    commPolicyId: str,
    description: str | None = None,
    initiatorProperties: dict[str, Any] | None = None,
    overridableInitiatorPropertyNames: list[str] | None = None,
    initiatorNetworkId: str | None = None,
    initiatorThreadsPerQuery: int | None = None,
    targetProperties: dict[str, Any] | None = None,
    overridableTargetPropertyNames: list[str] | None = None,
    targetNetworkId: str | None = None,
    targetThreadsPerQuery: int | None = None,
    userMappingId: str | None = None,
    usersToTroubleshoot: dict[str, Any] | None = None,
    enableAcks: bool | None = None,
    bridges: list[dict[str, Any]] | None = None,
    tags: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Create a new QueryGrid link.

    MANDATORY PARAMETERS: Ask the user for 'name', 'fabricId', 'initiatorConnectorId', 'targetConnectorId',
        and 'commPolicyId' if not provided.
    OPTIONAL PARAMETERS: All other parameters can be omitted.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. fabricId MUST reference an existing fabric - use qg_get_fabrics to find valid IDs
    2. initiatorConnectorId and targetConnectorId MUST reference existing connectors - use qg_get_connectors
    3. commPolicyId MUST reference an existing communication policy - use qg_get_comm_policies
    4. Missing any of the 5 mandatory parameters will cause creation to FAIL
    5. Invalid fabric, connector, or comm policy IDs will cause creation to FAIL
    6. The fabric must match what the connectors belong to

    Args:
        name (str): [MANDATORY] The name of the link.
            Ask the user: "What would you like to name the link?"
        fabricId (str): [MANDATORY] The ID of the fabric the link belongs to. ID is in UUID format.
            If the user doesn't know the fabric ID, suggest using qg_get_fabrics to list all fabrics.
            The fabric MUST already exist.
        initiatorConnectorId (str): [MANDATORY] The ID of the initiating connector. ID is in UUID format.
            If the user doesn't know the connector ID, suggest using qg_get_connectors to list all connectors.
            The connector MUST already exist.
        targetConnectorId (str): [MANDATORY] The ID of the target connector. ID is in UUID format.
            If the user doesn't know the connector ID, suggest using qg_get_connectors to list all connectors.
            The connector MUST already exist.
        commPolicyId (str): [MANDATORY] The ID of the communication policy to use. ID is in UUID format.
            If the user doesn't know the comm policy ID, suggest using qg_get_comm_policies to list all policies.
            The policy MUST already exist.
        description (str | None): [OPTIONAL] Description of the link.
        initiatorProperties (dict | None): [OPTIONAL] Initiating connector properties.
        overridableInitiatorPropertyNames (list[str] | None): [OPTIONAL] Overridable initiator properties.
        initiatorNetworkId (str | None): [OPTIONAL] Network ID for initiator.
        initiatorThreadsPerQuery (int | None): [OPTIONAL] Threads per query for initiator.
        targetProperties (dict | None): [OPTIONAL] Target connector properties.
        overridableTargetPropertyNames (list[str] | None): [OPTIONAL] Overridable target properties.
        targetNetworkId (str | None): [OPTIONAL] Network ID for target.
        targetThreadsPerQuery (int | None): [OPTIONAL] Threads per query for target.
        userMappingId (str | None): [OPTIONAL] User mapping ID.
        usersToTroubleshoot (dict | None): [OPTIONAL] The local system users for which to enable debug logging.
        enableAcks (bool | None): [OPTIONAL] Flag for sending acknowledgments for data blocks and
            attempt to retry if the connection gets somehow broken.
        bridges (list[dict] | None): [OPTIONAL] Bridges configuration.
        tags (dict | None): [OPTIONAL] String key/value pairs for context.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_create_link called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.create_link(
            name=name,
            fabricId=fabricId,
            initiatorConnectorId=initiatorConnectorId,
            targetConnectorId=targetConnectorId,
            commPolicyId=commPolicyId,
            description=description,
            initiatorProperties=initiatorProperties,
            overridableInitiatorPropertyNames=overridableInitiatorPropertyNames,
            initiatorNetworkId=initiatorNetworkId,
            initiatorThreadsPerQuery=initiatorThreadsPerQuery,
            targetProperties=targetProperties,
            overridableTargetPropertyNames=overridableTargetPropertyNames,
            targetNetworkId=targetNetworkId,
            targetThreadsPerQuery=targetThreadsPerQuery,
            userMappingId=userMappingId,
            usersToTroubleshoot=usersToTroubleshoot,
            enableAcks=enableAcks,
            bridges=bridges,
            tags=tags,
        )

    return run_tool("qg_create_link", _call)


@mcp.tool
def qg_delete_link(
    id: str,
) -> dict[str, Any]:
    """
    Delete a SINGLE link by ID.

    Use this tool to delete ONE link at a time. For deleting multiple links at once, do NOT use this tool.

    MANDATORY PARAMETER: Ask the user for the link ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the link to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_links to list all links.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_link called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.delete_link(id)

    return run_tool("qg_delete_link", _call)


@mcp.tool
def qg_update_link(
    id: str,
    name: str,
    description: str | None = None,
) -> dict[str, Any]:
    """
    Update a link's name and/or description (PATCH operation).

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. 'name' is MANDATORY even for PATCH operations (API requirement, not truly optional)
    2. This ONLY updates wrapper-level metadata (name, description)
    3. To update version-specific properties (fabricId, connectors, etc.), use qg_put_link_active or qg_put_link_pending

    MANDATORY PARAMETERS: 'id' and 'name' must be provided
    OPTIONAL PARAMETERS: 'description' can be omitted

    Args:
        id (str): [MANDATORY] The ID of the link wrapper. ID is in UUID format.
        name (str): [MANDATORY] The name of the link. Required even when only updating description.
        description (str | None): [OPTIONAL] Description of the link.

    ERROR CONDITIONS:
        - 400 Bad Request: Invalid link ID format or name is missing
        - 404 Not Found: Link with the given ID doesn't exist

    WHEN TO USE:
        - Renaming a link (changes apply to the wrapper, not versions)
        - Updating the link description
        - Simple metadata updates that don't require version changes

    WHEN NOT TO USE:
        - To change fabricId, connectors, commPolicyId, etc. (use PUT operations instead)
        - To activate a pending version (use qg_update_link_active)

    Returns:
        dict[str, Any]: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_update_link called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.update_link(
            id=id, name=name, description=description
        )

    return run_tool("qg_update_link", _call)


@mcp.tool
def qg_update_link_active(
    id: str,
    version_id: str,
) -> dict[str, Any]:
    """
    Activate a specific version (pending or previous) of a link using PATCH. (PATCH operation with plain text body).

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. Response is plain TEXT (versionId string), NOT a JSON object
    2. To verify activation, call qg_get_link_active after this operation
    3. Current active version becomes 'previous', pending becomes 'active'
    4. If a previous version already exists, it gets DELETED (only 3 version slots)
    5. This operation is IRREVERSIBLE without a previous version to roll back to

    MANDATORY PARAMETERS: Both 'id' and 'version_id' must be provided

    VERSION LIFECYCLE WORKFLOW:
    1. Create a pending version: qg_put_link_pending
    2. Get the pending version to extract versionId: qg_get_link_pending
    3. Activate it using this tool: qg_update_link_active(id, versionId)
    4. Verify activation: qg_get_link_active

    ROLLBACK WORKFLOW (if previous version exists):
    1. Get previous version: qg_get_link_previous
    2. Extract its versionId from the response
    3. Create pending from previous: qg_put_link_pending with previous config
    4. Activate the pending: qg_update_link_active

    Args:
        id (str): [MANDATORY] The ID of the link wrapper.
        version_id (str): [MANDATORY] The versionId to activate (from pending version).
            Get this from qg_get_link_pending response's 'versionId' field.

    ERROR CONDITIONS:
        - 400 Bad Request: Invalid versionId or no pending version exists
        - 404 Not Found: Link with the given ID doesn't exist

    BEST PRACTICES:
        - Always verify the pending version before activating
        - Keep the previous version for potential rollback
        - Document the reason for version changes

    Returns:
        dict[str, Any]: formatted response with plain text versionId + metadata
    """
    logger.debug("Tool: qg_update_link_active called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.update_link_active(id=id, version_id=version_id)

    return run_tool("qg_update_link_active", _call)


@mcp.tool
def qg_put_link_active(
    id: str,
    name: str,
    fabricId: str,
    initiatorConnectorId: str,
    targetConnectorId: str,
    commPolicyId: str,
    description: str | None = None,
    initiatorProperties: dict[str, Any] | None = None,
    overridableInitiatorPropertyNames: list[str] | None = None,
    initiatorNetworkId: str | None = None,
    initiatorThreadsPerQuery: int | None = None,
    targetProperties: dict[str, Any] | None = None,
    overridableTargetPropertyNames: list[str] | None = None,
    targetNetworkId: str | None = None,
    targetThreadsPerQuery: int | None = None,
    userMappingId: str | None = None,
    usersToTroubleshoot: dict[str, Any] | None = None,
    enableAcks: bool | None = None,
    bridges: list[dict[str, Any]] | None = None,
    tags: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Replace the active link version completely (PUT operation).

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. This is a FULL REPLACEMENT - all fields must be provided (not a partial update)
    2. Current active version moves to 'previous' slot
    3. fabricId, connectorIds, and commPolicyId MUST exist and be valid
    4. All referenced IDs must match the correct resource types
    5. Changes take effect IMMEDIATELY on active queries
    6. initiatorThreadsPerQuery and targetThreadsPerQuery are MANDATORY (range: 1-5)

    MANDATORY PARAMETERS: 'id', 'name', 'fabricId', 'initiatorConnectorId', 'targetConnectorId', 'commPolicyId',
                          'initiatorThreadsPerQuery', 'targetThreadsPerQuery'
    OPTIONAL PARAMETERS: All other parameters

    Args:
        id (str): [MANDATORY] The ID of the link wrapper.
        name (str): [MANDATORY] The name of the link.
        fabricId (str): [MANDATORY] The ID of the fabric (must exist and be valid).
        initiatorConnectorId (str): [MANDATORY] The ID of the initiating connector.
        targetConnectorId (str): [MANDATORY] The ID of the target connector.
        commPolicyId (str): [MANDATORY] The ID of the communication policy.
        description (str | None): [OPTIONAL] Description of the link.
        initiatorProperties (dict | None): [OPTIONAL] Initiating connector properties.
        overridableInitiatorPropertyNames (list[str] | None): [OPTIONAL] Overridable initiator properties.
        initiatorNetworkId (str | None): [OPTIONAL] Network ID for initiator.
        initiatorThreadsPerQuery (int | None): [MANDATORY] Threads per query for initiator (range: 1-5).
        targetProperties (dict | None): [OPTIONAL] Target connector properties.
        overridableTargetPropertyNames (list[str] | None): [OPTIONAL] Overridable target properties.
        targetNetworkId (str | None): [OPTIONAL] Network ID for target.
        targetThreadsPerQuery (int | None): [MANDATORY] Threads per query for target (range: 1-5).
        userMappingId (str | None): [OPTIONAL] User mapping ID for authentication.
        usersToTroubleshoot (dict | None): [OPTIONAL] Users to enable debug logging.
        enableAcks (bool | None): [OPTIONAL] Enable acknowledgments for data blocks.
        bridges (list[dict] | None): [OPTIONAL] Bridge configuration for indirect connectivity.
        tags (dict | None): [OPTIONAL] String key/value pairs for context.

    ERROR CONDITIONS:
        - 400 Bad Request: Missing mandatory fields, invalid IDs, or connector type mismatch
        - 404 Not Found: Link, fabric, connector, or commPolicy doesn't exist

    WHEN TO USE:
        - Making immediate configuration changes to active link
        - Emergency fixes that can't wait for pending→active workflow
        - Replacing all link properties at once

    WHEN NOT TO USE (use qg_put_link_pending + qg_update_link_active instead):
        - In production environments (safer workflow with validation)
        - When you want to review changes before activation
        - When you need rollback capability

    BEST PRACTICES:
        - Validate all IDs exist before calling (use qg_get_fabrics, qg_get_connectors, qg_get_comm_policies)
        - Use qg_put_link_pending + qg_update_link_active for safer deployments
        - Keep previous version for rollback capability

    Returns:
        dict[str, Any]: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_put_link_active called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.put_link_active(
            id=id,
            name=name,
            fabricId=fabricId,
            initiatorConnectorId=initiatorConnectorId,
            targetConnectorId=targetConnectorId,
            commPolicyId=commPolicyId,
            description=description,
            initiatorProperties=initiatorProperties,
            overridableInitiatorPropertyNames=overridableInitiatorPropertyNames,
            initiatorNetworkId=initiatorNetworkId,
            initiatorThreadsPerQuery=initiatorThreadsPerQuery,
            targetProperties=targetProperties,
            overridableTargetPropertyNames=overridableTargetPropertyNames,
            targetNetworkId=targetNetworkId,
            targetThreadsPerQuery=targetThreadsPerQuery,
            userMappingId=userMappingId,
            usersToTroubleshoot=usersToTroubleshoot,
            enableAcks=enableAcks,
            bridges=bridges,
            tags=tags,
        )

    return run_tool("qg_put_link_active", _call)


@mcp.tool
def qg_put_link_pending(
    id: str,
    name: str,
    fabricId: str,
    initiatorConnectorId: str,
    targetConnectorId: str,
    commPolicyId: str,
    description: str | None = None,
    initiatorProperties: dict[str, Any] | None = None,
    overridableInitiatorPropertyNames: list[str] | None = None,
    initiatorNetworkId: str | None = None,
    initiatorThreadsPerQuery: int | None = None,
    targetProperties: dict[str, Any] | None = None,
    overridableTargetPropertyNames: list[str] | None = None,
    targetNetworkId: str | None = None,
    targetThreadsPerQuery: int | None = None,
    userMappingId: str | None = None,
    usersToTroubleshoot: dict[str, Any] | None = None,
    enableAcks: bool | None = None,
    bridges: list[dict[str, Any]] | None = None,
    tags: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Create or replace a pending link version (PUT operation).

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. This REPLACES any existing pending version (not an update)
    2. Only ONE pending version allowed at a time
    3. Validation happens IMMEDIATELY - invalid configs fail on creation
    4. Pending version does NOT affect active queries until activated
    5. fabricId, connectorIds, and commPolicyId must be valid
    6. initiatorThreadsPerQuery and targetThreadsPerQuery are MANDATORY (range: 1-5)

    MANDATORY PARAMETERS: 'id', 'name', 'fabricId', 'initiatorConnectorId', 'targetConnectorId', 'commPolicyId',
                          'initiatorThreadsPerQuery', 'targetThreadsPerQuery'
    OPTIONAL PARAMETERS: All other parameters

    RECOMMENDED WORKFLOW:
    1. Create pending version: qg_put_link_pending
    2. Review pending: qg_get_link_pending
    3. Test/validate the configuration
    4. Activate when ready: qg_update_link_active
    5. Verify: qg_get_link_active

    Args:
        id (str): [MANDATORY] The ID of the link wrapper.
        name (str): [MANDATORY] The name of the link.
        fabricId (str): [MANDATORY] The ID of the fabric (must exist).
        initiatorConnectorId (str): [MANDATORY] The ID of the initiating connector.
        targetConnectorId (str): [MANDATORY] The ID of the target connector.
        commPolicyId (str): [MANDATORY] The ID of the communication policy.
        description (str | None): [OPTIONAL] Description of the link.
        initiatorProperties (dict | None): [OPTIONAL] Initiating connector properties.
        overridableInitiatorPropertyNames (list[str] | None): [OPTIONAL] Overridable initiator properties.
        initiatorNetworkId (str | None): [OPTIONAL] Network ID for initiator.
        initiatorThreadsPerQuery (int | None): [OPTIONAL] Threads per query for initiator.
        targetProperties (dict | None): [OPTIONAL] Target connector properties.
        overridableTargetPropertyNames (list[str] | None): [OPTIONAL] Overridable target properties.
        targetNetworkId (str | None): [OPTIONAL] Network ID for target.
        targetThreadsPerQuery (int | None): [OPTIONAL] Threads per query for target.
        userMappingId (str | None): [OPTIONAL] User mapping ID.
        usersToTroubleshoot (dict | None): [OPTIONAL] Users to troubleshoot.
        enableAcks (bool | None): [OPTIONAL] Enable acknowledgments.
        bridges (list[dict] | None): [OPTIONAL] Bridge configuration.
        tags (dict | None): [OPTIONAL] Tags for context.

    ERROR CONDITIONS:
        - 400 Bad Request: Missing mandatory fields, invalid IDs, connector type mismatch
        - 404 Not Found: Link, fabric, connector, or commPolicy doesn't exist

    BEST PRACTICES:
        - Use this instead of qg_put_link_active for safer deployments
        - Validate all referenced IDs exist before creating pending
        - Review pending version before activating
        - Document the reason for the change

    Returns:
        dict[str, Any]: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_put_link_pending called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.put_link_pending(
            id=id,
            name=name,
            fabricId=fabricId,
            initiatorConnectorId=initiatorConnectorId,
            targetConnectorId=targetConnectorId,
            commPolicyId=commPolicyId,
            description=description,
            initiatorProperties=initiatorProperties,
            overridableInitiatorPropertyNames=overridableInitiatorPropertyNames,
            initiatorNetworkId=initiatorNetworkId,
            initiatorThreadsPerQuery=initiatorThreadsPerQuery,
            targetProperties=targetProperties,
            overridableTargetPropertyNames=overridableTargetPropertyNames,
            targetNetworkId=targetNetworkId,
            targetThreadsPerQuery=targetThreadsPerQuery,
            userMappingId=userMappingId,
            usersToTroubleshoot=usersToTroubleshoot,
            enableAcks=enableAcks,
            bridges=bridges,
            tags=tags,
        )

    return run_tool("qg_put_link_pending", _call)


@mcp.tool
def qg_delete_link_pending(
    id: str,
) -> dict[str, Any]:
    """
    Delete the pending link version.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. Link MUST have a pending version, or this will return 404
    2. This is PERMANENT deletion - cannot be undone
    3. Active and previous versions are NOT affected
    4. After deletion, you can create a new pending version

    MANDATORY PARAMETER: 'id' must be provided

    Args:
        id (str): [MANDATORY] The ID of the link wrapper.

    ERROR CONDITIONS:
        - 404 Not Found: Link doesn't exist OR has no pending version

    WHEN TO USE:
        - Abandoning a pending configuration that's no longer needed
        - Clearing space to create a new pending version
        - Cleaning up after deciding not to proceed with changes

    WHEN NOT TO USE:
        - To delete the active link (use qg_delete_link instead)
        - To delete the previous version (use qg_delete_link_previous)

    SAFER ALTERNATIVE:
        - Instead of deleting, you can replace the pending version with qg_put_link_pending

    Returns:
        dict[str, Any]: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_link_pending called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.delete_link_pending(id=id)

    return run_tool("qg_delete_link_pending", _call)


@mcp.tool
def qg_delete_link_previous(
    id: str,
) -> dict[str, Any]:
    """
    Delete the previous link version (removes rollback capability).

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. This REMOVES your rollback capability - think carefully before deleting
    2. Link MUST have a previous version, or this will return 404
    3. Previous version is created when you activate a pending version
    4. This is PERMANENT deletion - cannot be undone
    5. Active and pending versions are NOT affected

    MANDATORY PARAMETER: 'id' must be provided

    Args:
        id (str): [MANDATORY] The ID of the link wrapper.

    VERSION CREATION TIMING:
        - Previous version is created when pending → active (old active → previous)
        - Only ONE previous version exists at a time
        - Activating another pending will DELETE the old previous version

    ERROR CONDITIONS:
        - 404 Not Found: Link doesn't exist OR has no previous version

    WHEN TO USE:
        - After confirming new active version is stable and working
        - To free up the previous version slot
        - When you're certain you won't need to roll back

    WHEN NOT TO USE:
        - Immediately after activation (wait to ensure stability)
        - When there's any uncertainty about the new active version
        - In production environments without proper validation

    BEST PRACTICE:
        - Wait at least a few days after activating before deleting previous
        - Monitor the active version for issues before removing rollback capability
        - Document why you're removing the previous version

    Returns:
        dict[str, Any]: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_link_previous called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.link_client.delete_link_previous(id=id)

    return run_tool("qg_delete_link_previous", _call)
