"""Manager for QueryGrid create foreign server operations."""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class CreateForeignServerClient(BaseClient):
    """Manager for QueryGrid create foreign server operations."""

    BASE_ENDPOINT = "/api/operations"

    def get_create_foreign_server_status(self, id: str) -> Any:
        """
        Get the status of the CONNECTOR_CFS diagnostic check for foreign server creation.

        Args:
            id (str): The diagnostic check ID. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

        Returns:
            dict[str, Any]: The diagnostic check status.
        """
        return self._request("GET", f"{self.BASE_ENDPOINT}/create-foreign-server/{id}")

    def create_foreign_server(
        self,
        initiator_admin_user: str,
        initiator_admin_password: str,
        link_id: str,
        version: str,
        foreign_server_name: str,
    ) -> Any:
        """Create a foreign server.

        Args:
            initiator_admin_user: Admin user on initiator system.
            initiator_admin_password: Password of the initiator's admin user.
            link_id: Id of the link to create the foreign server for.
            version: Version of the link (ACTIVE, PENDING). Required.
            foreign_server_name: Name of the foreign server to create. Required.

        Returns:
            The create foreign server operation result.
        """
        data = {
            "initiatorAdminUser": initiator_admin_user,
            "initiatorAdminPassword": initiator_admin_password,
            "linkId": link_id,
            "version": version,
            "foreignServerName": foreign_server_name,
        }
        return self._request("POST", f"{self.BASE_ENDPOINT}/create-foreign-server", json=data)
