"""
Manager for QueryGrid fabrics.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class FabricClient(BaseClient):
    """Manager for QueryGrid fabrics."""

    BASE_ENDPOINT = "/api/config/fabrics"

    def get_fabrics(
        self,
        flatten: bool = False,
        extra_info: bool = False,
        filter_by_name: str | None = None,
        filter_by_tag: str | None = None,
    ) -> dict[str, Any]:
        """Get all fabrics."""
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

    def get_fabric_by_id(self, id: str, extra_info: bool = False) -> dict[str, Any]:
        """Get a fabric by ID."""
        params = {}
        if extra_info:
            params["extraInfo"] = extra_info
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}", params=params)

    def get_fabric_active(self, id: str) -> dict[str, Any]:
        """Get the active version of a fabric."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/active")

    def get_fabric_pending(self, id: str) -> dict[str, Any]:
        """Get the pending version of a fabric."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/pending")

    def get_fabric_previous(self, id: str) -> dict[str, Any]:
        """Get the previous version of a fabric."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/previous")

    def delete_fabric(self, id: str) -> dict[str, Any]:
        """Delete a fabric by ID.

        Args:
            id: The ID of the fabric to delete.

        Returns:
            The API response.
        """
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}")

    def create_fabric(
        self,
        name: str,
        port: int,
        softwareVersion: str,
        authKeySize: int,
        description: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Create a new fabric in QueryGrid Manager.

        Args:
            name (str): The name of the fabric.
            description (str | None): Optional description of the fabric.
            tags (dict[str, str] | None): Optional string key/value pairs for associating some context with the fabric.
            port (int): The port for the fabric to use for communication between systems
            softwareVersion (str): The software version of the fabric.
            authKeySize (int): The size of the authentication key in bits.
                Options: 1536, 2048, 3072, 4096

        Returns:
            dict[str, Any]: The response from the API containing the created fabric details.
        """
        data: dict[str, Any] = {"name": name}
        if description is not None:
            data["description"] = description
        if tags is not None:
            data["tags"] = tags
        if port is not None:
            data["port"] = port
        if softwareVersion is not None:
            data["softwareVersion"] = softwareVersion
        if authKeySize is not None:
            data["authKeySize"] = authKeySize
        return self._request("POST", self.BASE_ENDPOINT, json=data)
