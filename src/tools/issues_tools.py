from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_issues() -> dict[str, Any]:
    """
    Get all QueryGrid issues.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_issues called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.issue_client.get_issues()

    return run_tool("qg_get_issues", _call)


@mcp.tool
def qg_get_issue_by_id(id: str) -> dict[str, Any]:
    """
    Get a specific QueryGrid issue by ID.

    Args:
        id (str): The ID of the issue to retrieve. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_issue_by_id called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.issue_client.get_issue_by_id(id)

    return run_tool("qg_get_issue_by_id", _call)


@mcp.tool
def qg_delete_issue(
    id: str,
) -> dict[str, Any]:
    """
    Delete an issue by ID.

    Args:
        id (str): The ID of the issue to delete. ID is in UUID format.
            e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_delete_issue called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.issue_client.delete_issue(id)

    return run_tool("qg_delete_issue", _call)


@mcp.tool
def qg_create_issue(
    create_time: str,
    component_type: str,
    component_id: str,
    component_name: str,
    data_center_name: str,
    problem_type: str,
    severity: str,
    subject_label: str,
    message_label: str,
    config_version: str,
    reporter_id: str,
    last_alert_time: str | None = None,
    subject_params: list[str] | None = None,
    message_params: list[str] | None = None,
    meaning_label: str | None = None,
    recommendation_label: str | None = None,
    subcomponent_id: str | None = None,
    node_ids: list[str] | None = None,
    confirmed: bool | None = None,
    vantage_lake_id: str | None = None,
    vantage_lake_name: str | None = None,
    operation_type: str | None = None,
    vantage_lake_error: str | None = None,
    sub_component_name: str | None = None,
    sub_component_issue_name_list: list[str] | None = None,
) -> dict[str, Any]:
    """
    Create a new issue in QueryGrid Manager.

    Args:
        create_time (str): The time the issue was created (ISO 8601 format).
        component_type (str): The type of component the issue applies (e.g. SYSTEM or MANAGER).
        component_id (str): The UUID of the component the issue applies.
        component_name (str): The name of the component.
        data_center_name (str): The name of the data center.
        problem_type (str): The type of the problem (e.g. NODE_DOWN, WRONG_TIME, CONFIG_DATABASE_DOWN, 
            SOFTWARE_VERSIONS_INCORRECT, etc).
        severity (str): The severity of the problem (e.g. CRITICAL or WARNING).
        subject_label (str): The localizable label that denotes the subject of the issue.
        message_label (str): The localizable label that denotes the message of the issue.
        config_version (str): The version of the configuration the issue applies to (e.g. ACTIVE, PENDING, PREVIOUS).
        reporter_id (str): The ID of the manager that reported the issue.
        last_alert_time (str | None): The last time an alert was sent for this issue (ISO 8601 format).
        subject_params (list[str] | None): The parameters to substitute into the subject.
        message_params (list[str] | None): The parameters to substitute into the message.
        meaning_label (str | None): The localizable label that denotes the meaning of the issue.
        recommendation_label (str | None): The localizable label that denotes the recommendation of the issue.
        subcomponent_id (str | None): The ID of the sub component the issue refers to.
        node_ids (list[str] | None): The list of node IDs associated with the issue.
        confirmed (bool | None): Flags if the issue has been confirmed.
        vantage_lake_id (str | None): ID of the VantageLake deployment.
        vantage_lake_name (str | None): Name of the VantageLake deployment.
        operation_type (str | None): Type of Operation failed on the VantageLake deployment.
        vantage_lake_error (str | None): Error for the Operation failed on the VantageLake deployment.
        sub_component_name (str | None): Name of the subComponent.
        sub_component_issue_name_list (list[str] | None): List of subComponentIssue.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_create_issue called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.issue_client.create_issue(
            create_time=create_time,
            component_type=component_type,
            component_id=component_id,
            component_name=component_name,
            data_center_name=data_center_name,
            problem_type=problem_type,
            severity=severity,
            subject_label=subject_label,
            message_label=message_label,
            config_version=config_version,
            reporter_id=reporter_id,
            last_alert_time=last_alert_time,
            subject_params=subject_params,
            message_params=message_params,
            meaning_label=meaning_label,
            recommendation_label=recommendation_label,
            subcomponent_id=subcomponent_id,
            node_ids=node_ids,
            confirmed=confirmed,
            vantage_lake_id=vantage_lake_id,
            vantage_lake_name=vantage_lake_name,
            operation_type=operation_type,
            vantage_lake_error=vantage_lake_error,
            sub_component_name=sub_component_name,
            sub_component_issue_name_list=sub_component_issue_name_list,
        )

    return run_tool("qg_create_issue", _call)
