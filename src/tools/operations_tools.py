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
    Bulk delete nodes or issues.

    Args:
        config_type (str): Type of the configuration object (NODE or ISSUE).
        ids (list[str]): List of IDs to delete.

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

    Args:
        system_id (str | None): The system to which nodes will be added.
        nodes (list[str] | None): List of node hostnames or IPs to install.
        username (str | None): The SSH username.
        password (str | None): The SSH password.

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

    Args:
        id (str): The installation ID. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

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

    Args:
        system_id (str): Id of the system participating in the install.
        expiration_days (int | None): The number of days before the access token expires.
        cluster_option (str | None): Cluster option (PRIMARY).

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

    Args:
        system_id (str): The system ID.
        issue_problem_type (str): The issue problem type (e.g., NODES_OFFLINE).

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: qg_disable_system_alerts called with system_id=%s, issue_problem_type=%s", system_id, issue_problem_type
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
