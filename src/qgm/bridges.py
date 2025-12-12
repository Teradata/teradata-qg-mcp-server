"""
Manager for QueryGrid bridges.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class BridgeClient(BaseClient):
    """Manager for QueryGrid bridges."""

    BASE_ENDPOINT = "/api/config/bridges"

    def get_bridges(self, filter_by_system_id: str | None = None, filter_by_name: str | None = None) -> Any:
        """
        Retrieve the list of QueryGrid bridge objects from the API.

        Args:
            filter_by_system_id (str | None): Get bridges associated with the specified system ID.
            filter_by_name (str | None): If provided, filters the bridges by name.

        Returns:
            Any: The API response which may be a dictionary, a list, or a string
                 depending on the endpoint and response.
        """
        api_endpoint = self.BASE_ENDPOINT
        params = {}
        if self._is_valid_param(filter_by_system_id):
            params["filterBySystemId"] = filter_by_system_id
        if self._is_valid_param(filter_by_name):
            params["filterByName"] = filter_by_name
        return self._request("GET", api_endpoint, params=params)

    def get_bridge_by_id(self, id: str) -> Any:
        """
        Retrieve a specific QueryGrid bridge object by its ID.

        Args:
            id (str): The unique identifier of the bridge.

        Returns:
            Any: The API response which may be a dictionary, a list, or a string
                 depending on the endpoint and response.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}"
        return self._request("GET", api_endpoint)

    def create_bridge(
        self,
        name: str,
        system_id: str,
        node_ids: list[str] | None = None,
        description: str | None = None,
    ) -> Any:
        """
        Create a new bridge in QueryGrid Manager.

        Args:
            name (str): The name of the bridge.
            system_id (str): The system ID associated with the bridge.
            node_ids (list[str] | None): List of node IDs from the specified system to act as a bridge.
            description (str | None): Optional description of the bridge.

        Returns:
            Any: The response from the API. May be a dict, list, or string depending on the endpoint.
        """
        api_endpoint = self.BASE_ENDPOINT
        data: dict[str, Any] = {
            "name": name,
            "systemId": system_id,
        }
        if node_ids is not None:
            data["nodeIds"] = node_ids
        if description is not None:
            data["description"] = description
        return self._request("POST", api_endpoint, json=data)

    def delete_bridge(self, id: str) -> Any:
        """Delete a bridge by ID.

        Args:
            id: The ID of the bridge to delete.

        Returns:
            The API response.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}"
        return self._request("DELETE", api_endpoint)
