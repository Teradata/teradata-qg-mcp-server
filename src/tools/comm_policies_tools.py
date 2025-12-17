from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_comm_policies(
    flatten: bool = False,
    extra_info: bool = False,
    filter_by_name: str | None = None,
    filter_by_tag: str | None = None,
) -> dict[str, Any]:
    """
    Get all QueryGrid communication policies. Optional arguments can be ignored if not needed.

    ALL PARAMETERS ARE OPTIONAL. If the user does not specify filters, retrieve all communication policies.

    Args:
        flatten (bool): [OPTIONAL] Flatten out the active, pending, and previous versions into array elements instead of
            nesting them.
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.
        filter_by_name (str | None): [OPTIONAL] Get communication policy associated with the specified name
            (case insensitive). Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [OPTIONAL] Get communication policy associated with the specified tag.
            Provide ','(comma) separated list of key:value pairs.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.get_comm_policies(
            flatten=flatten,
            extra_info=extra_info,
            filter_by_name=filter_by_name,
            filter_by_tag=filter_by_tag,
        )

    return run_tool("qg_get_comm_policies", _call)


@mcp.tool
def qg_get_comm_policy_by_id(
    id: str,
    extra_info: bool = False,
) -> dict[str, Any]:
    """
    Get a specific QueryGrid communication policy by ID.

    MANDATORY PARAMETER: Ask the user for the communication policy ID if not provided.
    OPTIONAL PARAMETERS: 'extra_info' can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the communication policy to retrieve. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all communication policies.
        extra_info (bool): [OPTIONAL] Include extra information. Values are boolean True/False, not string.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_comm_policy_by_id called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.get_comm_policy_by_id(
            id, extra_info=extra_info
        )

    return run_tool("qg_get_comm_policy_by_id", _call)


@mcp.tool
def qg_get_comm_policy_active(
    id: str,
) -> dict[str, Any]:
    """
    Get the active configuration for a QueryGrid communication policy.

    MANDATORY PARAMETER: Ask the user for the communication policy ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the communication policy. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all communication policies.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_comm_policy_active called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.get_comm_policy_active(id)

    return run_tool("qg_get_comm_policy_active", _call)


@mcp.tool
def qg_get_comm_policy_pending(
    id: str,
) -> dict[str, Any]:
    """
    Get the pending configuration for a QueryGrid communication policy.

    MANDATORY PARAMETER: Ask the user for the communication policy ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the communication policy. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all communication policies.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_comm_policy_pending called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.get_comm_policy_pending(id)

    return run_tool("qg_get_comm_policy_pending", _call)


@mcp.tool
def qg_get_comm_policy_previous(
    id: str,
) -> dict[str, Any]:
    """
    Get the previous configuration for a QueryGrid communication policy.

    MANDATORY PARAMETER: Ask the user for the communication policy ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the communication policy. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all communication policies.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_comm_policy_previous called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.get_comm_policy_previous(id)

    return run_tool("qg_get_comm_policy_previous", _call)


@mcp.tool
def qg_create_comm_policy(
    name: str,
    transfer_concurrency: int,
    description: str | None = None,
    security_option: str = "INTEGRITY_SECURE_ENCRYPTION_ALL",
    security_algorithm: str = "AES_GCM",
    integrity_headers_only: bool = False,
    authentication_key_size: int = 1536,
    encryption_key_size: int = 128,
    compression_algorithm: str | None = None,
    policy_version: int = 2,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a new communication policy in QueryGrid Manager. Ask user for values for the parameters if not provided.

    MANDATORY PARAMETERS: Ask the user for 'name' and 'transfer_concurrency' if not provided.
    OPTIONAL PARAMETERS: All other parameters have defaults and can be omitted.

    Args:
       name (str): [MANDATORY] The name of the communication policy.
           Ask the user: "What would you like to name the communication policy?"
       transfer_concurrency (int): [MANDATORY] The number of streams to use for communication between node pairs for
        transferring data.
       description (str | None): [OPTIONAL] Description of the communication policy.
       security_option (str): [OPTIONAL] Type of security mechanisms to enable for communication.
           Valid options:
           - INTEGRITY_NONE_ENCRYPTION_NONE: IP-based Authentication, no integrity check, no encryption
           - INTEGRITY_CHECKSUM_ENCRYPTION_NONE: IP-based authentication, checksum integrity check, no encryption
           - INTEGRITY_SECURE_ENCRYPTION_CREDENTIALS_ONLY: Key-based authentication, secure Integrity
            checks, encrypt credentials
           - INTEGRITY_SECURE_ENCRYPTION_ALL: Key-based authentication, secure Integrity checks,
            encrypt all data (default)
       security_algorithm (str): [OPTIONAL] The algorithm to use for integrity checks and encryption.
           Defaults to "AES_GCM". Valid options: AES_CRC32C, AES_GCM, AES_SHA256, AES_SHA512
       integrity_headers_only (bool): [OPTIONAL] Only perform integrity checks on message headers. Defaults to False.
       authentication_key_size (int): [OPTIONAL] The size of the authentication key. Defaults to 1536.
       encryption_key_size (int): [OPTIONAL] The size of the encryption key. Defaults to 128.
       compression_algorithm (str | None): [OPTIONAL] Compression algorithm to use.
           Defaults to "NONE" when not provided.
           Valid options: NONE, ZSTD
       policy_version (int): [OPTIONAL] The version of comm-policy. Defaults to 2.
           Valid options: 1, 2
       tags (dict | None): [OPTIONAL] String key/value pairs for associating some context with the communication policy.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_create_comm_policy called with name=%s", name)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.create_comm_policy(
            name=name,
            transfer_concurrency=transfer_concurrency,
            description=description,
            security_option=security_option,
            security_algorithm=security_algorithm,
            integrity_headers_only=integrity_headers_only,
            authentication_key_size=authentication_key_size,
            encryption_key_size=encryption_key_size,
            compression_algorithm=compression_algorithm,
            policy_version=policy_version,
            tags=tags,
        )

    return run_tool("qg_create_comm_policy", _call)


@mcp.tool
def qg_delete_comm_policy(
    id: str,
) -> dict[str, Any]:
    """
    Delete a communication policy by ID.

    MANDATORY PARAMETER: Ask the user for the communication policy ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the communication policy to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all communication policies.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_comm_policy called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.delete_comm_policy(id)

    return run_tool("qg_delete_comm_policy", _call)


@mcp.tool
def qg_update_comm_policy(
    id: str,
    name: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """
    Update Communication Policy name or description (PATCH - partial update).

    MANDATORY PARAMETER: Ask the user for the communication policy 'id' if not provided.
    OPTIONAL PARAMETERS: All other parameters can be omitted. Only provide fields you want to update.

    Args:
        id (str): [MANDATORY] The ID of the communication policy to update. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all policies.
        name (str | None): [MANDATORY] The name of the communication policy.
        description (str | None): [MANDATORY] Description of the communication policy.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_update_comm_policy called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.update_comm_policy(
            id=id, name=name, description=description
        )

    return run_tool("qg_update_comm_policy", _call)


@mcp.tool
def qg_update_comm_policy_active(id: str, version_id: str) -> dict[str, Any]:
    """
    Activate a specific pending or previous communication policy version (PATCH).

    NOTE FOR LLMs: Communication policies have two types of IDs:
    - 'id': The policy wrapper ID (constant across all versions)
    - 'versionId': Specific to each version (active, pending, previous)

    To activate a pending or previous version:
    1. Use qg_get_comm_policy_pending() or qg_get_comm_policy_previous() to get the version
    2. Extract 'versionId' from that response
    3. Call this tool with the policy 'id' and the 'versionId'

    MANDATORY PARAMETERS: Both 'id' and 'version_id' are required.

    Args:
        id (str): [MANDATORY] The policy wrapper ID (UUID format, constant across versions).
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all policies.
        version_id (str): [MANDATORY] The specific version ID to activate (UUID format).
            Get this from the pending or previous version response.
            e.g., '987fcdeb-51a2-43f1-b123-426614174999'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_update_comm_policy_active called with id=%s, version_id=%s",
        id,
        version_id,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.update_comm_policy_active(
            id=id,
            version_id=version_id,
        )

    return run_tool("qg_update_comm_policy_active", _call)


@mcp.tool
def qg_put_comm_policy_active(
    id: str,
    name: str,
    transfer_concurrency: int,
    description: str | None = None,
    security_option: str = "INTEGRITY_SECURE_ENCRYPTION_ALL",
    security_algorithm: str = "AES_GCM",
    integrity_headers_only: bool = False,
    authentication_key_size: int = 1536,
    encryption_key_size: int = 128,
    compression_algorithm: str | None = None,
    policy_version: int = 2,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Replace the active version of a communication policy (PUT - full replacement).

    MANDATORY PARAMETERS: Ask the user for 'id', 'name', and 'transfer_concurrency' if not provided.
    OPTIONAL PARAMETERS: All other parameters have defaults and can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the communication policy. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all policies.
        name (str): [MANDATORY] The name of the communication policy.
        transfer_concurrency (int): [MANDATORY] The number of streams for communication.
        description (str | None): [OPTIONAL] Description of the communication policy.
        security_option (str): [OPTIONAL] Type of security mechanisms.
            Valid: INTEGRITY_NONE_ENCRYPTION_NONE, INTEGRITY_CHECKSUM_ENCRYPTION_NONE,
            INTEGRITY_SECURE_ENCRYPTION_CREDENTIALS_ONLY, INTEGRITY_SECURE_ENCRYPTION_ALL (default)
        security_algorithm (str): [OPTIONAL] Algorithm for integrity checks. Default: AES_GCM
            Valid: AES_CRC32C, AES_GCM, AES_SHA256, AES_SHA512
        integrity_headers_only (bool): [OPTIONAL] Only check integrity on headers. Default: False
        authentication_key_size (int): [OPTIONAL] Size of the authentication key. Default: 1536
        encryption_key_size (int): [OPTIONAL] Size of the encryption key. Default: 128
        compression_algorithm (str | None): [OPTIONAL] Compression algorithm. Valid: NONE, ZSTD
        policy_version (int): [OPTIONAL] Version of comm-policy. Default: 2. Valid: 1, 2
        tags (dict | None): [OPTIONAL] String key/value pairs for context.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_put_comm_policy_active called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.put_comm_policy_active(
            id=id,
            name=name,
            transfer_concurrency=transfer_concurrency,
            description=description,
            security_option=security_option,
            security_algorithm=security_algorithm,
            integrity_headers_only=integrity_headers_only,
            authentication_key_size=authentication_key_size,
            encryption_key_size=encryption_key_size,
            compression_algorithm=compression_algorithm,
            policy_version=policy_version,
            tags=tags,
        )

    return run_tool("qg_put_comm_policy_active", _call)


@mcp.tool
def qg_put_comm_policy_pending(
    id: str,
    transfer_concurrency: int,
    description: str | None = None,
    security_option: str = "INTEGRITY_SECURE_ENCRYPTION_ALL",
    security_algorithm: str = "AES_GCM",
    integrity_headers_only: bool = False,
    authentication_key_size: int = 1536,
    encryption_key_size: int = 128,
    compression_algorithm: str | None = None,
    policy_version: int = 2,
    tags: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create or replace the pending version of a communication policy (PUT - full update).

    MANDATORY PARAMETERS: Ask the user for 'id' and 'transfer_concurrency' if not provided.
    OPTIONAL PARAMETERS: All other parameters have defaults and can be omitted.

    Args:
        id (str): [MANDATORY] The ID of the communication policy. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all policies.
        transfer_concurrency (int): [MANDATORY] The number of streams for communication.
        description (str | None): [OPTIONAL] Description of the communication policy.
        security_option (str): [OPTIONAL] Type of security mechanisms.
            Valid: INTEGRITY_NONE_ENCRYPTION_NONE, INTEGRITY_CHECKSUM_ENCRYPTION_NONE,
            INTEGRITY_SECURE_ENCRYPTION_CREDENTIALS_ONLY, INTEGRITY_SECURE_ENCRYPTION_ALL (default)
        security_algorithm (str): [OPTIONAL] Algorithm for integrity checks. Default: AES_GCM
            Valid: AES_CRC32C, AES_GCM, AES_SHA256, AES_SHA512
        integrity_headers_only (bool): [OPTIONAL] Only check integrity on headers. Default: False
        authentication_key_size (int): [OPTIONAL] Size of the authentication key. Default: 1536
        encryption_key_size (int): [OPTIONAL] Size of the encryption key. Default: 128
        compression_algorithm (str | None): [OPTIONAL] Compression algorithm. Valid: NONE, ZSTD
        policy_version (int): [OPTIONAL] Version of comm-policy. Default: 2. Valid: 1, 2
        tags (dict | None): [OPTIONAL] String key/value pairs for context.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_put_comm_policy_pending called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.put_comm_policy_pending(
            id=id,
            transfer_concurrency=transfer_concurrency,
            description=description,
            security_option=security_option,
            security_algorithm=security_algorithm,
            integrity_headers_only=integrity_headers_only,
            authentication_key_size=authentication_key_size,
            encryption_key_size=encryption_key_size,
            compression_algorithm=compression_algorithm,
            policy_version=policy_version,
            tags=tags,
        )

    return run_tool("qg_put_comm_policy_pending", _call)


@mcp.tool
def qg_delete_comm_policy_pending(
    id: str,
) -> dict[str, Any]:
    """
    Delete the pending version of a communication policy.

    MANDATORY PARAMETER: Ask the user for the communication policy ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the communication policy. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all policies.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_comm_policy_pending called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.delete_comm_policy_pending(id)

    return run_tool("qg_delete_comm_policy_pending", _call)


@mcp.tool
def qg_delete_comm_policy_previous(
    id: str,
) -> dict[str, Any]:
    """
    Delete the previous version of a communication policy.

    MANDATORY PARAMETER: Ask the user for the communication policy ID if not provided.

    Args:
        id (str): [MANDATORY] The ID of the communication policy. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.
            If the user doesn't know the ID, suggest using qg_get_comm_policies to list all policies.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_comm_policy_previous called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.comm_policy_client.delete_comm_policy_previous(id)

    return run_tool("qg_delete_comm_policy_previous", _call)
