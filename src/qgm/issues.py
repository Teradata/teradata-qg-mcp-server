"""
Manager for QueryGrid issues.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class IssueClient(BaseClient):
    """Manager for QueryGrid issues."""

    BASE_ENDPOINT = "/api/issues"

    def get_issues(self) -> dict[str, Any]:
        """Retrieve all active issues from the system.

        This method sends a GET request to the '/api/issues' endpoint and returns
        the response as a dictionary containing details of all currently active issues.
        If no issues are present, an empty dictionary or appropriate response may be returned.

        Returns:
            dict[str, Any]: A dictionary representing the active issues data.

        Raises:
            Any exceptions raised by the underlying _request method, such as network errors
            or API-specific errors (e.g., authentication failures).
        """
        return self._request("GET", self.BASE_ENDPOINT)

    def get_issue_by_id(self, id: str) -> dict[str, Any]:
        """
        Retrieve a specific active issue by its unique identifier.

        This method sends a GET request to the '/api/issues/{id}' endpoint and returns
        the response as a dictionary containing details of the specified issue.
        If the issue does not exist, the API may return an error or an empty response.

        Args:
            id (str): The unique identifier of the issue to retrieve.

        Returns:
            dict[str, Any]: A dictionary representing the issue data.

        Raises:
            Any exceptions raised by the underlying _request method, such as network errors
            authentication failures, or API-specific errors (e.g., issue not found).
        """
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}")

    def delete_issue(self, id: str) -> dict[str, Any]:
        """
        Delete an issue by ID.

        Args:
            id: The ID of the issue to delete.

        Returns:
            dict[str, Any]: The API response.
        """
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}")

    def create_issue(
        self,
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
            dict[str, Any]: The response from the API containing the created issue details.
        """
        data: dict[str, Any] = {
            "createTime": create_time,
            "componentType": component_type,
            "componentId": component_id,
            "componentName": component_name,
            "dataCenterName": data_center_name,
            "problemType": problem_type,
            "severity": severity,
            "subjectLabel": subject_label,
            "messageLabel": message_label,
            "configVersion": config_version,
            "reporterId": reporter_id,
        }
        
        if last_alert_time is not None:
            data["lastAlertTime"] = last_alert_time
        if subject_params is not None:
            data["subjectParams"] = subject_params
        if message_params is not None:
            data["messageParams"] = message_params
        if meaning_label is not None:
            data["meaningLabel"] = meaning_label
        if recommendation_label is not None:
            data["recommendationLabel"] = recommendation_label
        if subcomponent_id is not None:
            data["subcomponentId"] = subcomponent_id
        if node_ids is not None:
            data["nodeIds"] = node_ids
        if confirmed is not None:
            data["confirmed"] = confirmed
        if vantage_lake_id is not None:
            data["vantageLakeId"] = vantage_lake_id
        if vantage_lake_name is not None:
            data["vantageLakeName"] = vantage_lake_name
        if operation_type is not None:
            data["operationType"] = operation_type
        if vantage_lake_error is not None:
            data["vantageLakeError"] = vantage_lake_error
        if sub_component_name is not None:
            data["subComponentName"] = sub_component_name
        if sub_component_issue_name_list is not None:
            data["subComponentIssueNameList"] = sub_component_issue_name_list
            
        return self._request("POST", self.BASE_ENDPOINT, json=data)