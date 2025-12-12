"""
Manager for QueryGrid networks.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class NetworkClient(BaseClient):
    """Manager for QueryGrid networks."""

    BASE_ENDPOINT = "/api/config/networks"

    def get_networks(
        self,
        flatten: bool = False,
        extra_info: bool = False,
        filter_by_name: str | None = None,
        filter_by_tag: str | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve the list of QueryGrid network objects from the API.

        Args:
            flatten (bool): Flatten versions into array elements. Defaults to False.
            extra_info (bool): Include extra details. Defaults to False.
            filter_by_name (str | None): Filter by name.
            filter_by_tag (str | None): Filter by tag (comma-separated key:value pairs).

        Returns:
            dict[str, Any]: A dictionary containing the list of networks.
        """
        params: dict[str, Any] = {}
        if flatten:
            params["flatten"] = flatten
        if extra_info:
            params["extraInfo"] = extra_info
        if self._is_valid_param(filter_by_name):
            params["filterByName"] = filter_by_name
        if self._is_valid_param(filter_by_tag):
            params["filterByTag"] = filter_by_tag
        return self._request("GET", self.BASE_ENDPOINT, params=params)

    def get_network_by_id(self, id: str, extra_info: bool = False) -> dict[str, Any]:
        """
        Retrieve a specific network by ID.

        Args:
            id (str): The network ID.
            extra_info (bool): Include extra details.

        Returns:
            dict[str, Any]: The network details.
        """
        params = {}
        if extra_info:
            params["extraInfo"] = extra_info
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}", params=params if params else None)

    def get_network_active(self, id: str) -> dict[str, Any]:
        """Get the active version of a network."""
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}/active"
        return self._request("GET", api_endpoint)

    def get_network_pending(self, id: str) -> dict[str, Any]:
        """Get the pending version of a network."""
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}/pending"
        return self._request("GET", api_endpoint)

    def get_network_previous(self, id: str) -> dict[str, Any]:
        """Get the previous version of a network."""
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}/previous"
        return self._request("GET", api_endpoint)

    def delete_network(self, id: str) -> dict[str, Any]:
        """Delete a network by ID."""
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}")

    def create_network(
        self,
        name: str,
        connection_type: str,
        description: str | None = None,
        matching_rules: list[dict[str, Any]] | None = None,
        load_balancer_address: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Create a new network in QueryGrid Manager.

        Args:
            name (str): The name of the network.
            connection_type (str): The type of connection (STANDARD, LOAD_BALANCER, NO_INGRESS).
            description (str | None): Optional description of the network.
            matching_rules (list[dict[str, Any]] | None): Optional rules for identifying network interfaces.
            load_balancer_address (str | None): Optional load balancer address.
            tags (dict | None): Optional string key/value pairs for context.

        Returns:
            dict[str, Any]: The response from the API.
        """
        data: dict[str, Any] = {
            "name": name,
            "connectionType": connection_type,
        }
        
        # Only include optional parameters if they are provided
        if description is not None:
            data["description"] = description
        if matching_rules is not None:
            data["matchingRules"] = matching_rules
        if load_balancer_address is not None:
            data["loadBalancerAddress"] = load_balancer_address
        if tags is not None:
            data["tags"] = tags
            
        return self._request("POST", self.BASE_ENDPOINT, json=data)
