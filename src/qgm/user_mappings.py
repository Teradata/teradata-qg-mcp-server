"""
Manager for QueryGrid user mappings.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class UserMappingClient(BaseClient):
    """Manager for QueryGrid user/role mappings."""

    BASE_ENDPOINT = "/api/config/user-mappings"

    def get_user_mappings(self, filter_by_name: str | None = None) -> Any:
        """
        Retrieve the list of QueryGrid user mapping objects from the API.

        Args:
            filter_by_name (str | None): If provided, filters the user mappings by name.

        Returns:
            dict[str, Any]: A dictionary containing the list of user mappings.
        """
        params = {}
        if self._is_valid_param(filter_by_name):
            params["filterByName"] = filter_by_name
        return self._request("GET", self.BASE_ENDPOINT, params=params)

    def get_user_mapping_by_id(self, mapping_id: str) -> Any:
        """
        Retrieve a specific user mapping by ID.

        Args:
            mapping_id (str): The mapping ID.

        Returns:
            dict[str, Any]: The user mapping details.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{mapping_id}"
        return self._request("GET", api_endpoint)

    def delete_user_mapping(self, mapping_id: str) -> Any:
        """Delete a user mapping by ID.

        Args:
            mapping_id: The ID of the user mapping to delete.

        Returns:
            The API response.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{mapping_id}"
        return self._request("DELETE", api_endpoint)

    def create_user_mapping(
        self,
        name: str,
        user_mapping: dict[str, str] | None = None,
        role_mapping: dict[str, str] | None = None,
        description: str | None = None,
    ) -> Any:
        """Create a new user mapping.

        Args:
            name: The name of the user mapping.
            user_mapping: Optional map of local users to remote users.
            role_mapping: Optional map of local roles to remote roles.
            description: Optional description of the user mapping.

        Returns:
            The created user mapping data.
        """
        data: dict[str, Any] = {"name": name}
        if user_mapping is not None:
            data["userMapping"] = user_mapping
        if role_mapping is not None:
            data["roleMapping"] = role_mapping
        if description is not None:
            data["description"] = description
        return self._request("POST", self.BASE_ENDPOINT, json=data)
