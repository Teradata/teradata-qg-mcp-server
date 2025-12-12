"""
Manager for QueryGrid node virtual IPs.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class NodeVirtualIPClient(BaseClient):
    """Manager for QueryGrid node virtual IPs."""

    BASE_ENDPOINT = "/api/config/node-virtual-ips"

    def get_node_virtual_ips(self) -> dict[str, Any]:
        """
        Retrieve the list of QueryGrid node virtual IP objects from the API.

        Returns:
            dict[str, Any]: A dictionary containing the list of node virtual IPs.
        """
        return self._request("GET", self.BASE_ENDPOINT)

    def get_node_virtual_ip_by_id(self, id: str) -> dict[str, Any]:
        """
        Retrieve a specific node virtual IP by ID.

        Args:
            id (str): The virtual IP ID.

        Returns:
            dict[str, Any]: The node virtual IP details.
        """
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}")

    def delete_node_virtual_ip(self, id: str) -> dict[str, Any]:
        """
        Delete a node virtual IP by ID.

        Args:
            id (str): The virtual IP ID.

        Returns:
            dict[str, Any]: The deletion response.
        """
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}")
