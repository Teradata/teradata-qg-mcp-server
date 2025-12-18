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

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify a filter, retrieve all user mappings.

    Args:
        filter_by_name (str | None): [OPTIONAL] Filter user mappings by name.

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

    MANDATORY PARAMETER: Ask the user for the user mapping ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the user mapping to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
            If the user doesn't know the ID, suggest using qg_get_user_mappings to list all user mappings.

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

    MANDATORY PARAMETER: Ask the user for 'name' if not provided.
    OPTIONAL PARAMETERS: 'user_mapping', 'role_mapping', and 'description' can be omitted.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:
    1. At least one of user_mapping or role_mapping should typically be provided for a useful mapping
    2. user_mapping defines how usernames are mapped between systems
    3. role_mapping defines how roles/groups are mapped between systems
    4. Both mappings can be complex dictionaries with mapping rules

    Args:
        name (str): [MANDATORY] The name of the user mapping.
            Ask the user: "What would you like to name this user mapping?"
        user_mapping (dict | None): [OPTIONAL] User mapping dictionary defining username translations.
        role_mapping (dict | None): [OPTIONAL] Role mapping dictionary defining role/group translations.
        description (str | None): [OPTIONAL] Description of the user mapping.

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
    Delete a SINGLE user mapping by ID.

    Use this tool to delete ONE user mapping at a time.
    For deleting multiple user mappings at once, do NOT use this tool.

    MANDATORY PARAMETER: Ask the user for the user mapping ID if not provided.

    Args:
        mapping_id (str): [MANDATORY] The ID of the user mapping to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'
            If the user doesn't know the ID, suggest using qg_get_user_mappings to list all user mappings.

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


@mcp.tool
def qg_put_user_mapping(
    mapping_id: str,
    name: str,
    user_mapping: dict[str, Any] | None = None,
    role_mapping: dict[str, Any] | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """
    Update an existing QueryGrid user mapping by ID.

    ⚠️ CRITICAL GOTCHAS FOR LLMs:

    1. MANDATORY PARAMETERS:
       - 'mapping_id': UUID of the existing user mapping to update
       - 'name': User mapping name (can be same or different from original)

    2. FULL REPLACEMENT (not partial):
       - PUT replaces the entire user mapping configuration
       - All optional parameters (user_mapping, role_mapping, description) not provided will be cleared
       - To preserve existing mappings, you MUST retrieve them first with qg_get_user_mapping_by_id
       - Then include all fields you want to keep when calling this tool

    3. NO VERSION MANAGEMENT:
       - User mappings do NOT have version lifecycle (no pending/active/previous)
       - Changes take effect immediately
       - No activate/deactivate operations

    4. ID MUST EXIST:
       - The 'mapping_id' parameter must match an existing user mapping
       - If mapping doesn't exist, you'll get a 404 error
       - Use qg_get_user_mappings first to verify the mapping exists

    5. MAPPING STRUCTURE:
       - user_mapping: Dictionary mapping local usernames to remote usernames
         Example: {"local_user1": "remote_user1", "local_user2": "remote_user2"}
       - role_mapping: Dictionary mapping local roles to remote roles
         Example: {"local_role1": "remote_role1", "local_role2": "remote_role2"}
       - Both mappings are optional but at least one is typically provided
       - Keys and values must be strings

    6. ERROR CONDITIONS:
       - 400 Bad Request: Invalid data (malformed mapping, empty name)
       - 404 Not Found: User mapping with specified ID doesn't exist
       - 409 Conflict: Name conflict with another user mapping (if changing name)

    7. WHEN TO USE THIS vs CREATE:
       - Use qg_put_user_mapping when: Updating an existing user mapping
       - Use qg_create_user_mapping when: Creating a brand new user mapping
       - If unsure whether mapping exists, check with qg_get_user_mappings first

    8. IMPACT:
       - Changes are immediate (no activation step)
       - Affects all links using this user mapping
       - Active queries may use old mappings until they reconnect
       - Test mappings carefully before applying to production links

    9. BEST PRACTICES:
       - Always retrieve current configuration first with qg_get_user_mapping_by_id
       - Preserve mappings you don't want to change
       - Validate mapping dictionaries before calling
       - Consider impact on active links and queries
       - Update mapping name carefully (affects references in links)
       - Document mapping purpose in description field

    10. COMMON USE CASES:
        - Adding new user/role mappings to existing mapping object
        - Removing user/role mappings (by omitting them in PUT)
        - Changing mapping name for better organization
        - Updating description for documentation

    Args:
        mapping_id (str): [MANDATORY] The UUID of the user mapping to update.
            Get from qg_get_user_mappings if you don't know it.
            Format: '123e4567-e89b-12d3-a456-426614174000'

        name (str): [MANDATORY] The name of the user mapping.
            Must be unique across all user mappings unless updating the same mapping.
            Used to identify the mapping in link configurations.

        user_mapping (dict[str, Any] | None): [OPTIONAL] Dictionary mapping local users to remote users.
            Keys: Local usernames on the initiator system
            Values: Remote usernames on the target system
            Example: {"tduser": "hiveuser", "admin": "hadoop_admin"}
            If not provided, existing user mappings will be cleared.

        role_mapping (dict[str, Any] | None): [OPTIONAL] Dictionary mapping local roles to remote roles.
            Keys: Local roles on the initiator system
            Values: Remote roles on the target system
            Example: {"dbc": "supergroup", "public": "users"}
            If not provided, existing role mappings will be cleared.

        description (str | None): [OPTIONAL] Description of the user mapping.
            Useful for documenting the purpose and usage of this mapping.
            If not provided, existing description will be cleared.

    Returns:
        dict[str, Any]: formatted response with updated user mapping data + metadata
            On success: returns complete updated user mapping object with id, name, mappings
            On error: returns error details with status code

    Example:
        To update a user mapping's user mappings while preserving role mappings:
        1. Get current config:
           current = qg_get_user_mapping_by_id(mapping_id="abc-123")
        2. Update with preserved values:
           qg_put_user_mapping(
               mapping_id="abc-123",
               name=current["name"],  # preserve
               user_mapping={"new_user": "new_remote_user"},  # new mappings
               role_mapping=current.get("roleMapping"),  # preserve existing
               description=current.get("description")  # preserve
           )
    """
    logger.debug(
        "Tool: qg_put_user_mapping called with mapping_id=%s, name=%s", mapping_id, name
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.user_mapping_client.put_user_mapping(
            mapping_id=mapping_id,
            name=name,
            user_mapping=user_mapping,
            role_mapping=role_mapping,
            description=description,
        )

    return run_tool("qg_put_user_mapping", _call)
