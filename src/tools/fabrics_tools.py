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

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify filters, retrieve all fabrics.

    Args:
        flatten (bool): [OPTIONAL] Flatten the response structure
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.
        filter_by_name (str | None): [OPTIONAL] Get fabric associated with the specified name (case insensitive).
            Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [OPTIONAL] Get fabric associated with the specified tag.
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

    MANDATORY PARAMETER: Ask the user for the fabric ID if not provided.
    OPTIONAL PARAMETERS: 'extra_info' can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the fabric to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_fabrics to list all fabrics.
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.

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

    MANDATORY PARAMETER: Ask the user for the fabric ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the fabric. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_fabrics to list all fabrics.

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

    MANDATORY PARAMETER: Ask the user for the fabric ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the fabric. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_fabrics to list all fabrics.

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

    MANDATORY PARAMETER: Ask the user for the fabric ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the fabric. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_fabrics to list all fabrics.

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

    MANDATORY PARAMETERS: Ask the user for 'name', 'port', 'softwareVersion', and 'authKeySize' if not provided.
    OPTIONAL PARAMETERS: 'description' and 'tags' can be omitted.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. authKeySize MUST be one of: 1536, 2048, 3072, or 4096 - other values will FAIL
    2. softwareVersion MUST reference a valid FABRIC software version - use qg_get_software to find available versions
    3. Invalid authKeySize (e.g., 1024) will cause creation to FAIL
    4. The port must be available and not in use by other fabrics

    Args:
        name (str): [MANDATORY] The name of the fabric.
            Ask the user: "What would you like to name the fabric?"
        port (int): [MANDATORY] The port for the fabric to use for communication between systems.
        softwareVersion (str): [MANDATORY] The software version of the fabric.
            Must be a valid FABRIC software version. Use qg_get_software to list available versions.
        authKeySize (int): [MANDATORY] The size of the authentication key in bits.
            MUST be one of: 1536, 2048, 3072, or 4096. Other values will FAIL.
        description (str | None): [OPTIONAL] Description of the fabric.
        tags (dict | None): [OPTIONAL] String key/value pairs for associating some context with the fabric.

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
    Delete a SINGLE fabric by ID.

    Use this tool to delete ONE fabric at a time. For deleting multiple fabrics at once, do NOT use this tool.

    MANDATORY PARAMETER: Ask the user for the fabric ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the fabric to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_fabrics to list all fabrics.

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


@mcp.tool
def qg_update_fabric(
    id: str, name: str, description: str | None = None
) -> dict[str, Any]:
    """
    Update a fabric's name or description using PATCH.

    Args:
        id (str): [MANDATORY] The fabric ID to update. ID is in UUID format.
        name (str): [MANDATORY] The name of the fabric (required by API).
        description (str | None): [OPTIONAL] The new description for the fabric.

    IMPORTANT GOTCHAS FOR LLMs:
    ==========================
    1. MANDATORY NAME: Even though this is PATCH (partial update), the API requires 'name' field.
       You MUST provide the name even if you're only updating the description.

    2. CANNOT UPDATE VERSION PROPERTIES: This endpoint only updates name/description.
       To update port, softwareVersion, or authKeySize, use qg_put_fabric_active or qg_put_fabric_pending.

    3. UPDATES WRAPPER ENTITY: This updates the fabric wrapper, not a specific version.
       Changes apply across all versions (active/pending/previous).

    COMMON USE CASES:
    - Rename a fabric: Provide new name with existing or new description
    - Update description only: Provide existing name with new description
    - Update both: Provide both new name and new description

    Returns:
        ResponseType: formatted response with updated fabric details + metadata
    """
    logger.debug(
        "Tool: qg_update_fabric called with id=%s, name=%s, description=%s",
        id,
        name,
        description,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.update_fabric(id, name, description)

    return run_tool("qg_update_fabric", _call)


@mcp.tool
def qg_update_fabric_active(id: str, version_id: str) -> dict[str, Any]:
    """
    Activate a specific version (pending or previous) of a fabric using PATCH.

    USAGE GUIDANCE FOR LLMs:
    =======================
    When working with fabric versions, understand the distinction:
    - 'id': The fabric wrapper ID - this stays constant across all versions
    - 'versionId': The specific version identifier - unique for each active/pending/previous version

    WORKFLOW TO ACTIVATE A VERSION:
    1. Get the version you want to activate:
       - For pending: Use qg_get_fabric_pending(id)
       - For previous: Use qg_get_fabric_previous(id)

    2. Extract the 'versionId' from the response (NOT the 'id'):
       Example response structure:
       {
         "id": "fab-001",              # ← Fabric wrapper ID (constant)
         "versionId": "fab-v123",      # ← Version ID to use (changes per version)
         "versionNumber": 2,
         "version": "PENDING",
         ...
       }

    3. Call this tool with:
       - id: The fabric wrapper ID (from step 1's 'id' field)
       - version_id: The version-specific ID (from step 1's 'versionId' field)

    Args:
        id (str): [MANDATORY] The fabric wrapper ID (remains constant across versions).
        version_id (str): [MANDATORY] The version ID to activate (from pending or previous version).

    CRITICAL GOTCHAS FOR LLMs:
    ==========================
    1. RESPONSE FORMAT: This endpoint returns the version_id as a STRING, not a full fabric object.
       To verify activation, you must call qg_get_fabric_active(id) after activation.

    2. SOURCE VERSION MUST EXIST: The version_id must be from an existing pending or previous version.
       You cannot activate a version that doesn't exist or is already active.

    3. VERSION BECOMES ACTIVE: When you activate a pending version:
       - Current active → becomes previous
       - Pending version → becomes active
       - Previous version → gets deleted (if one existed)

    4. ROLLBACK SCENARIO: To rollback, activate the previous version:
       - Get previous version: qg_get_fabric_previous(id)
       - Extract versionId from response
       - Activate it: qg_update_fabric_active(id, previous_version_id)

    5. NO UNDO: Once a version is activated, the previous 'previous' version is permanently deleted.
       Make sure you want to activate before calling this endpoint.

    ERROR CONDITIONS:
    - 404: version_id doesn't exist or fabric doesn't exist
    - 400: Trying to activate an already active version

    Returns:
        ResponseType: formatted response with activated version details + metadata
    """
    logger.debug(
        "Tool: qg_update_fabric_active called with id=%s, version_id=%s",
        id,
        version_id,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.update_fabric_active(id, version_id)

    return run_tool("qg_update_fabric_active", _call)


@mcp.tool
def qg_put_fabric_active(
    id: str,
    name: str,
    port: int,
    softwareVersion: str,
    authKeySize: int,
    description: str | None = None,
    tags: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Update the active version of a fabric using PUT (full replacement).

    NOTE: This is a full replacement - all mandatory fields must be provided.

    Args:
        id (str): [MANDATORY] The fabric ID. ID is in UUID format.
        name (str): [MANDATORY] The name of the fabric (required by API).
        port (int): [MANDATORY] The port for the fabric to use for communication.
        softwareVersion (str): [MANDATORY] The software version of the fabric.
        authKeySize (int): [MANDATORY] The size of the authentication key in bits (1536, 2048, 3072, or 4096).
        description (str | None): [OPTIONAL] Description of the fabric.
        tags (dict[str, str] | None): [OPTIONAL] String key/value pairs for context.

    CRITICAL GOTCHAS FOR LLMs:
    ==========================
    1. FULL REPLACEMENT: This is PUT, not PATCH. You MUST provide ALL mandatory fields.
       If you omit any mandatory field, the API will return a 400 error.
       - Always include: name, port, softwareVersion, authKeySize

    2. SOFTWARE VERSION MUST BE VALID: The softwareVersion must be a version that's registered
       in the QueryGrid Manager. Invalid versions will cause a 400 error.
       - Get valid versions using qg_get_softwares(filter_by_type="FABRIC")
       - Or use the current softwareVersion from the active fabric

    3. AUTH KEY SIZE VALIDATION: Only these values are allowed: 1536, 2048, 3072, 4096
       Any other value will cause a 400 error.

    4. PREVIOUS VERSION CREATED: When you PUT a new active version:
       - Current active → becomes previous
       - New values → become active
       - Old previous → gets deleted (if one existed)

    5. NAME CANNOT BE EMPTY: Even though name is for the wrapper entity, it's required in PUT.
       Use the current fabric name if you don't want to change it.

    6. PORT RANGE: Port must be valid and not conflicting with other fabrics.
       Common range: 1024-65535 (avoid well-known ports 0-1023)

    WHEN TO USE THIS VS qg_update_fabric_active:
    - Use PUT (this tool) when you want to change configuration (port, software, authKey)
    - Use PATCH (qg_update_fabric_active) when activating an existing pending/previous version

    ERROR CONDITIONS:
    - 400: Missing mandatory field, invalid softwareVersion, invalid authKeySize, invalid port
    - 404: Fabric ID doesn't exist

    Returns:
        ResponseType: formatted response with updated active version details + metadata
    """
    logger.debug(
        "Tool: qg_put_fabric_active called with id=%s, name=%s, port=%s, softwareVersion=%s, authKeySize=%s",
        id,
        name,
        port,
        softwareVersion,
        authKeySize,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.put_fabric_active(
            id, name, port, softwareVersion, authKeySize, description, tags
        )

    return run_tool("qg_put_fabric_active", _call)


@mcp.tool
def qg_put_fabric_pending(
    id: str,
    name: str,
    port: int,
    softwareVersion: str,
    authKeySize: int,
    description: str | None = None,
    tags: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Create or replace the pending version of a fabric using PUT.

    USAGE GUIDANCE:
    This creates a pending version that can be reviewed before activation.
    After creating a pending version, you can:
    1. Review it using qg_get_fabric_pending(id)
    2. Activate it using qg_update_fabric_active(id, version_id)
    3. Or delete it using qg_delete_fabric_pending(id)

    Args:
        id (str): [MANDATORY] The fabric ID. ID is in UUID format.
        name (str): [MANDATORY] The name of the fabric (required by API).
        port (int): [MANDATORY] The port for the fabric to use for communication.
        softwareVersion (str): [MANDATORY] The software version of the fabric.
        authKeySize (int): [MANDATORY] The size of the authentication key in bits (1536, 2048, 3072, or 4096).
        description (str | None): [OPTIONAL] Description of the fabric.
        tags (dict[str, str] | None): [OPTIONAL] String key/value pairs for context.

    CRITICAL GOTCHAS FOR LLMs:
    ==========================
    1. REPLACES EXISTING PENDING: If a pending version already exists, this will REPLACE it.
       The old pending version is lost. There's no warning or error.
       - Check for pending: qg_get_fabric_pending(id) first if you want to preserve it

    2. SAME VALIDATION AS ACTIVE: All the same requirements as qg_put_fabric_active apply:
       - softwareVersion must be valid and registered
       - authKeySize must be 1536, 2048, 3072, or 4096
       - All mandatory fields required
       - Port must be valid

    3. ONLY ONE PENDING: A fabric can only have ONE pending version at a time.
       You cannot create multiple pending versions for comparison.

    4. PENDING DOESN'T AFFECT ACTIVE: Creating a pending version does NOT change the active version.
       Active version continues to operate until you explicitly activate the pending.

    5. AUTO-DELETED ON ACTIVATION: When you activate a pending version:
       - The pending version becomes active
       - There's no longer a pending version
       - You'll need to PUT a new pending if you want another staged change

    6. VALIDATION HAPPENS IMMEDIATELY: Even though it's pending, the API validates all fields now.
       If softwareVersion is invalid, you get a 400 error immediately.

    RECOMMENDED WORKFLOW:
    1. Check if pending exists: qg_get_fabric_pending(id)
    2. If you want to preserve it, get the details first
    3. PUT new pending version with this tool
    4. Review the pending: qg_get_fabric_pending(id)
    5. When ready, activate: qg_update_fabric_active(id, pending_version_id)

    ERROR CONDITIONS:
    - 400: Invalid parameters (same as qg_put_fabric_active)
    - 404: Fabric ID doesn't exist

    Returns:
        ResponseType: formatted response with created pending version details + metadata
    """
    logger.debug(
        "Tool: qg_put_fabric_pending called with id=%s, name=%s, port=%s, softwareVersion=%s, authKeySize=%s",
        id,
        name,
        port,
        softwareVersion,
        authKeySize,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.put_fabric_pending(
            id, name, port, softwareVersion, authKeySize, description, tags
        )

    return run_tool("qg_put_fabric_pending", _call)


@mcp.tool
def qg_delete_fabric_pending(id: str) -> dict[str, Any]:
    """
    Delete the pending version of a fabric.

    USAGE GUIDANCE:
    Use this to discard a pending version that you don't want to activate.
    This does not affect the active version.

    Args:
        id (str): [MANDATORY] The fabric ID. ID is in UUID format.

    CRITICAL GOTCHAS FOR LLMs:
    ==========================
    1. MUST HAVE PENDING VERSION: This will fail if no pending version exists.
       - Check first: qg_get_fabric_pending(id)
       - API may return 404 or 400 if no pending exists

    2. PERMANENT DELETION: Once deleted, the pending version cannot be recovered.
       There's no undo or rollback for this operation.

    3. ACTIVE UNAFFECTED: Deleting pending does NOT change the active version.
       Active version continues to operate normally.

    4. NO PREVIOUS PROMOTION: Deleting pending does NOT make previous become pending.
       After deletion, there is simply no pending version.

    5. IDEMPOTENT BEHAVIOR: Some APIs may succeed even if no pending exists (return 200).
       Always check the response to confirm the operation.

    WHEN TO USE:
    - Staged changes no longer needed
    - Want to create a different pending version (delete first, then PUT new)
    - Cleaning up after testing
    - Decided not to proceed with planned changes

    SAFER ALTERNATIVE:
    If unsure, you can just PUT a new pending version - it will replace the old one.
    Only use delete if you want NO pending version at all.

    ERROR CONDITIONS:
    - 404: Fabric doesn't exist OR no pending version exists
    - 400: Possible if pending doesn't exist (depends on API implementation)

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_fabric_pending called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.delete_fabric_pending(id)

    return run_tool("qg_delete_fabric_pending", _call)


@mcp.tool
def qg_delete_fabric_previous(id: str) -> dict[str, Any]:
    """
    Delete the previous version of a fabric.

    USAGE GUIDANCE:
    Use this to remove the previous version if you no longer need to roll back.
    This does not affect the active version.

    Args:
        id (str): [MANDATORY] The fabric ID. ID is in UUID format.

    CRITICAL GOTCHAS FOR LLMs:
    ==========================
    1. MUST HAVE PREVIOUS VERSION: This will fail if no previous version exists.
       - Previous version only exists after activating a new version
       - Check first: qg_get_fabric_previous(id)
       - API may return 404 or 400 if no previous exists

    2. REMOVES ROLLBACK CAPABILITY: Once deleted, you CANNOT roll back to this version.
       This is permanent - you lose the ability to revert to the previous configuration.

    3. ACTIVE UNAFFECTED: Deleting previous does NOT change the active version.
       Active version continues to operate normally.

    4. WHEN PREVIOUS IS CREATED: Previous version is created when:
       - You activate a pending version (old active → previous)
       - You PUT new active version (old active → previous)
       - Previous previous is automatically deleted in both cases

    5. ONLY ONE PREVIOUS: A fabric can only have ONE previous version at a time.
       When you activate another version, the current previous is automatically deleted.

    6. NO CASCADING HISTORY: QueryGrid doesn't maintain version history beyond:
       - 1 active version
       - 1 pending version (optional)
       - 1 previous version (optional)

    WHEN TO USE:
    - Confirmed new active version is working correctly
    - Don't need rollback capability anymore
    - Cleaning up old configurations
    - Disk space considerations (rare)

    WHEN NOT TO USE:
    - Just activated a new version (wait to ensure it works)
    - Testing or migration in progress
    - Production changes without confirmation period

    BEST PRACTICE:
    After activating a new version, wait for a confirmation period (hours/days)
    before deleting previous. This gives you a safety net to roll back if issues arise.

    ERROR CONDITIONS:
    - 404: Fabric doesn't exist OR no previous version exists
    - 400: Possible if previous doesn't exist (depends on API implementation)

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_fabric_previous called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.fabric_client.delete_fabric_previous(id)

    return run_tool("qg_delete_fabric_previous", _call)
