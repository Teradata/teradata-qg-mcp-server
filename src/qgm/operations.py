"""
Manager for QueryGrid operations.
"""

from __future__ import annotations

from typing import Any


from .base import BaseClient


class OperationsClient(BaseClient):
    """Manager for QueryGrid operations."""

    BASE_ENDPOINT = "/api/operations"

    def bulk_delete(self, config_type: str, ids: list[str]) -> Any:
        """Bulk delete nodes or issues.

        Args:
            config_type: Type of the configuration object (NODE or ISSUE).
            ids: List of IDs to delete.

        Returns:
            The bulk delete operation result.
        """
        data: dict[str, Any] = {
            "configType": config_type,
            "ids": ids,
        }
        return self._request("POST", f"{self.BASE_ENDPOINT}/bulk-delete", json=data)

    def get_nodes_auto_install_status(self, id: str) -> dict[str, Any]:
        """
        Get the status of the automatic node installation.

        Args:
            id (str): The installation ID. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

        Returns:
            dict[str, Any]: The installation status.
        """
        return self._request("GET", f"{self.BASE_ENDPOINT}/nodes-auto-install/{id}")

    def auto_install_nodes(
        self,
        system_id: str | None = None,
        nodes: list[str] | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> dict[str, Any]:
        """Automatically install node packages.

        Args:
            system_id: The system to which nodes will be added.
            nodes: List of node hostnames or IPs to install.
            username: The SSH username.
            password: The SSH password.

        Returns:
            The auto install operation result.
        """
        data: dict[str, Any] = {}
        if system_id is not None:
            data["systemId"] = system_id
        if nodes is not None:
            data["nodes"] = nodes
        if username is not None:
            data["username"] = username
        if password is not None:
            data["password"] = password
        return self._request("POST", f"{self.BASE_ENDPOINT}/nodes-auto-install", json=data)

    def manual_install_nodes(
        self,
        system_id: str,
        expiration_days: int | None = None,
        cluster_option: str | None = None,
    ) -> dict[str, Any]:
        """Manually install node packages.

        Args:
            system_id: Id of the system participating in the install.
            expiration_days: The number of days before the access token expires.
            cluster_option: Cluster option (PRIMARY).

        Returns:
            The manual install operation result.
        """
        data: dict[str, Any] = {"systemId": system_id}
        if expiration_days is not None:
            data["expirationDays"] = expiration_days
        if cluster_option is not None:
            data["clusterOption"] = cluster_option
        return self._request("POST", f"{self.BASE_ENDPOINT}/nodes-manual-install", json=data)

    def disable_system_alerts(
        self,
        system_id: str,
        issue_problem_type: str,
    ) -> dict[str, Any]:
        """Disable alerts for a system for a specific issue type.

        Args:
            system_id: The system ID.
            issue_problem_type: The issue problem type (e.g., NODES_OFFLINE).

        Returns:
            The disable alerts operation result.
        """
        data = {
            "systemId": system_id,
            "issueProblemType": issue_problem_type,
        }
        return self._request("POST", f"{self.BASE_ENDPOINT}/system-alerts/disable", json=data)
