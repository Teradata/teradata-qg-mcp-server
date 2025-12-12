"""
Manager for QueryGrid diagnostic checks.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class DiagnosticCheckClient(BaseClient):
    """Manager for QueryGrid diagnostic operations."""

    BASE_ENDPOINT = "/api/operations/diagnostic-check"

    def get_diagnostic_check_status(self, id: str) -> Any:
        """Get the status of a diagnostic check operation."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}")

    def run_diagnostic_check(
        self,
        type: str,
        component_id: str | None = None,
        data_flow: str | None = None,
        node_id: str | None = None,
        version: str | None = None,
        bandwidth_mb_per_node: float | None = None,
        properties: str | None = None,
    ) -> Any:
        """Run a diagnostic check or connector install.

        Args:
            type: Type of diagnostic check (LINK, LINK_BANDWIDTH, CONNECTOR, CONNECTOR_INSTALL).
            component_id: Id of the link or connector to check.
            data_flow: Data flow direction.
            node_id: Id of the node.
            version: Version to use.
            bandwidth_mb_per_node: Bandwidth in MB per node.
            properties: Additional properties as JSON string.

        Returns:
            The diagnostic check operation result.
        """
        data = {"type": type}
        if component_id is not None:
            data["componentId"] = component_id
        if data_flow is not None:
            data["dataFlow"] = data_flow
        if node_id is not None:
            data["nodeId"] = node_id
        if version is not None:
            data["version"] = version
        if bandwidth_mb_per_node is not None:
            data["bandwidthMBPerNode"] = str(bandwidth_mb_per_node)
        if properties is not None:
            data["properties"] = properties
        return self._request("POST", self.BASE_ENDPOINT, json=data)
