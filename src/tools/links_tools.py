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

    Args:
        flatten (bool): Flatten the response structure
        extra_info (bool): Include extra information. Values are boolean True/False, not string.
        filter_by_name (str | None): [Optional] Get link associated with the specified name (case insensitive).
            Wildcard matching with '*' is supported.
        filter_by_tag (str | None): [Optional] Get link associated with the specified tag.
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

    Args:
        id (str): The ID of the link to retrieve. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.
        extra_info (bool): Include extra information. Values are boolean True/False, not string.

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

    Args:
        id (str): The ID of the link. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

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

    Args:
        id (str): The ID of the link. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

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

    Args:
        id (str): The ID of the link. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

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

    Args:
        name (str): The name of the link.
        fabricId (str): The ID of the fabric the link belongs to.
        initiatorConnectorId (str): The ID of the initiating connector.
        targetConnectorId (str): The ID of the target connector.
        commPolicyId (str): The ID of the communication policy to use.
        description (str | None): Optional description of the link.
        initiatorProperties (dict | None): Optional initiating connector properties.
        overridableInitiatorPropertyNames (list[str] | None): Optional overridable initiator properties.
        initiatorNetworkId (str | None): Optional network ID for initiator.
        initiatorThreadsPerQuery (int | None): Optional threads per query for initiator.
        targetProperties (dict | None): Optional target connector properties.
        overridableTargetPropertyNames (list[str] | None): Optional overridable target properties.
        targetNetworkId (str | None): Optional network ID for target.
        targetThreadsPerQuery (int | None): Optional threads per query for target.
        userMappingId (str | None): Optional user mapping ID.
        usersToTroubleshoot (dict | None): Optional The local system users for which to enable debug logging.
        enableAcks (bool | None): Optional flag for sending acknowledgments for data blocks and
            attempt to retry if the connection gets somehow broken.
        bridges (list[dict] | None): Optional bridges configuration.
        tags (dict | None): Optional string key/value pairs for context.

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
    Delete a link by ID.

    Args:
        id (str): The ID of the link to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

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
