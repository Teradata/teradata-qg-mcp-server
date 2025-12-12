"""Manager for QueryGrid data centers."""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class DataCenterClient(BaseClient):
    """Manager for QueryGrid data centers."""

    BASE_ENDPOINT = "/api/config/datacenters"

    def get_datacenters(self, filter_by_name: str | None = None) -> Any:
        """Retrieve the list of QueryGrid data center objects from the API.

        Args:
            filter_by_name: If provided, filters the data centers by name.

        Returns:
            The API response parsed as JSON.
        """
        params = {}
        if self._is_valid_param(filter_by_name):
            params["filterByName"] = filter_by_name
        return self._request("GET", self.BASE_ENDPOINT, params=params)

    def get_datacenter_by_id(self, id: str) -> Any:
        """Retrieve a specific QueryGrid data center object by its ID.

        Args:
            id: The unique identifier of the data center (UUID).

        Returns:
            The API response parsed as JSON.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}"
        return self._request("GET", api_endpoint)

    def create_datacenter(
        self,
        name: str,
        description: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> Any:
        """Create a new data center in QueryGrid Manager.

        Args:
            name: The name of the data center.
            description: Optional description of the data center.
            tags: Optional tags mapping.

        Returns:
            The API response parsed as JSON.
        """
        data: dict[str, Any] = {"name": name}
        if description is not None:
            data["description"] = description
        if tags is not None:
            data["tags"] = tags
        return self._request("POST", self.BASE_ENDPOINT, json=data)

    def delete_datacenter(self, id: str) -> Any:
        """Delete a data center by ID.

        Args:
            id: The ID of the data center to delete.

        Returns:
            The API response parsed as JSON.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}"
        return self._request("DELETE", api_endpoint)
