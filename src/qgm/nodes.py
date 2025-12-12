"""
Manager for QueryGrid nodes.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class NodeClient(BaseClient):
    """Manager for QueryGrid nodes."""

    BASE_ENDPOINT = "/api/nodes"

    def get_nodes(
        self,
        filter_by_system_id: str | None = None,
        filter_by_bridge_id: str | None = None,
        filter_by_fabric_id: str | None = None,
        filter_by_connector_id: str | None = None,
        extra_info: bool = False,
        fabric_version: str | None = None,
        connector_version: str | None = None,
        drivers: str | None = None,
        details: bool = False,
        filter_by_name: str | None = None,
    ) -> dict[str, Any]:
        """Get all nodes configured in QueryGrid Manager."""
        params: dict[str, Any] = {}
        if self._is_valid_param(filter_by_system_id):
            params["filterBySystemId"] = filter_by_system_id
        if self._is_valid_param(filter_by_bridge_id):
            params["filterByBridgeId"] = filter_by_bridge_id
        if self._is_valid_param(filter_by_fabric_id):
            params["filterByFabricId"] = filter_by_fabric_id
        if self._is_valid_param(filter_by_connector_id):
            params["filterByConnectorId"] = filter_by_connector_id
        if extra_info:
            params["extraInfo"] = extra_info
        if self._is_valid_param(fabric_version):
            params["fabricVersion"] = fabric_version
        if self._is_valid_param(connector_version):
            params["connectorVersion"] = connector_version
        if self._is_valid_param(drivers):
            params["drivers"] = drivers
        if details:
            params["details"] = details
        if self._is_valid_param(filter_by_name):
            params["filterByName"] = filter_by_name
        return self._request("GET", self.BASE_ENDPOINT, params=params)

    def get_node_by_id(self, id: str) -> dict[str, Any]:
        """Get a specific node configured in QueryGrid Manager by its ID."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}")

    def get_node_heartbeat_by_id(self, id: str) -> dict[str, Any]:
        """Get the latest node heartbeat sent by a node to the QueryGrid Manager by its ID."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/heartbeat")

    def delete_node(self, id: str) -> dict[str, Any] | list[Any] | str:
        """Delete a node by ID.
        Args:
            id: The ID of the node to delete.

        Returns:
            dict[str, Any]: The API response.
        """
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}")