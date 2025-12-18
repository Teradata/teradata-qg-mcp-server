from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool

from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_bulk_delete(config_type: str, ids: list[str]) -> dict[str, Any]:
    """
    Bulk delete MULTIPLE nodes or issues in a single operation.

    CRITICAL CONSTRAINTS:
    - This tool ONLY supports NODE and ISSUE entity types
    - For deleting multiple bridges, links, systems, connectors, fabrics, networks, etc.,
      there is NO bulk delete - you MUST use the individual delete tools multiple times
    - For deleting a single node or issue, use qg_delete_node or qg_delete_issue instead

    MANDATORY PARAMETERS: Ask the user for 'config_type' and 'ids' if not provided.

    Args:
        config_type (str): [MANDATORY] Type of the configuration object. ONLY accepts: NODE or ISSUE.
        ids (list[str]): [MANDATORY] List of IDs to delete. IDs are in UUID format.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_bulk_delete called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.operations_client.bulk_delete(
            config_type=config_type,
            ids=ids,
        )

    return run_tool("qg_bulk_delete", _call)


@mcp.tool
def qg_auto_install_nodes(
    system_id: str | None = None,
    nodes: list[str] | None = None,
    username: str | None = None,
    password: str | None = None,
) -> dict[str, Any]:
    """
    Automatically install node packages.

    ALL PARAMETERS ARE OPTIONAL but typically need to be provided for successful installation.

    Args:
        system_id (str | None): [OPTIONAL] The system to which nodes will be added. ID is in UUID format.
            If the user doesn't know the system ID, suggest using qg_get_systems to list all systems.
        nodes (list[str] | None): [OPTIONAL] List of node hostnames or IPs to install.
        username (str | None): [OPTIONAL] The SSH username.
        password (str | None): [OPTIONAL] The SSH password.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_auto_install_nodes: system_id=%s, nodes=%s, username=%s, password=%s",
        system_id,
        nodes,
        username,
        "***" if password else None,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.operations_client.auto_install_nodes(
            system_id=system_id,
            nodes=nodes,
            username=username,
            password=password,
        )

    return run_tool("qg_auto_install_nodes", _call)


@mcp.tool
def qg_get_nodes_auto_install_status(
    id: str,
) -> dict[str, Any]:
    """
    Get the status of the automatic node installation.

    MANDATORY PARAMETER: Ask the user for the installation ID if not provided.

    Args:
        id (str): [MANDATORY] The installation ID. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_nodes_auto_install_status called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.operations_client.get_nodes_auto_install_status(id)

    return run_tool("qg_get_nodes_auto_install_status", _call)


@mcp.tool
def qg_manual_install_nodes(
    system_id: str,
    expiration_days: int | None = None,
    cluster_option: str | None = None,
) -> dict[str, Any]:
    """
    Manually install node packages.

    MANDATORY PARAMETER: Ask the user for 'system_id' if not provided.
    OPTIONAL PARAMETERS: 'expiration_days' and 'cluster_option' can be omitted.

    Args:
        system_id (str): [MANDATORY] Id of the system participating in the install. ID is in UUID format.
            If the user doesn't know the system ID, suggest using qg_get_systems to list all systems.
        expiration_days (int | None): [OPTIONAL] The number of days before the access token expires.
        cluster_option (str | None): [OPTIONAL] Cluster option (PRIMARY).

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_manual_install_nodes: system_id=%s, expiration_days=%s, cluster_option=%s",
        system_id,
        expiration_days,
        cluster_option,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.operations_client.manual_install_nodes(
            system_id=system_id,
            expiration_days=expiration_days,
            cluster_option=cluster_option,
        )

    return run_tool("qg_manual_install_nodes", _call)


@mcp.tool
def qg_disable_system_alerts(system_id: str, issue_problem_type: str) -> dict[str, Any]:
    """
    Disable alerts for a system for a specific issue type.

    MANDATORY PARAMETERS: Ask the user for 'system_id' and 'issue_problem_type' if not provided.

    Args:
        system_id (str): [MANDATORY] The system ID. ID is in UUID format.
            If the user doesn't know the system ID, suggest using qg_get_systems to list all systems.
        issue_problem_type (str): [MANDATORY] The issue problem type (e.g., NODES_OFFLINE).

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_disable_system_alerts called with system_id=%s, issue_problem_type=%s",
        system_id,
        issue_problem_type,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.operations_client.disable_system_alerts(
            system_id=system_id,
            issue_problem_type=issue_problem_type,
        )

    return run_tool("qg_disable_system_alerts", _call)
