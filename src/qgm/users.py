"""Manager for QueryGrid users."""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class UserClient(BaseClient):
    """Manager for QueryGrid users."""

    BASE_ENDPOINT = "/api/users"

    def get_users(self) -> Any:
        """Retrieve the list of QueryGrid user objects from the API.

        Returns:
            The API response parsed as JSON.
        """
        api_endpoint = self.BASE_ENDPOINT
        return self._request("GET", api_endpoint)

    def get_user_by_username(self, username: str) -> Any:
        """Retrieve a specific user by username.

        Args:
            username: The username.

        Returns:
            The user details from the API.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{username}"
        return self._request("GET", api_endpoint)

    def delete_user(self, username: str) -> Any:
        """Delete a user by username.

        Args:
            username: The username of the user to delete.

        Returns:
            The API response.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{username}"
        return self._request("DELETE", api_endpoint)

    def create_user(
        self, username: str, password: str, description: str | None = None
    ) -> Any:
        """Create a new user in QueryGrid Manager.

        Args:
            username: The username for the new user.
            password: The password for the new user.
            description: Optional description of the user.

        Returns:
            The API response parsed as JSON.
        """
        api_endpoint = self.BASE_ENDPOINT
        data = {
            "username": username,
            "password": password,
        }
        if description is not None:
            data["description"] = description
        return self._request("POST", api_endpoint, json=data)

    def update_user(
        self, username: str, password: str, description: str | None = None
    ) -> Any:
        """Update an existing user in QueryGrid Manager.

        Args:
            username: The username of the user to update.
            password: The password for the user (required by API).
            description: Optional new description of the user.

        Returns:
            The API response parsed as JSON.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{username}"
        data: dict[str, Any] = {
            "password": password,
        }
        if description is not None:
            data["description"] = description
        return self._request("PUT", api_endpoint, json=data)
