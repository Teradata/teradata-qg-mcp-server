"""
Manager for QueryGrid systems.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class SystemClient(BaseClient):
    """Manager for QueryGrid systems."""

    BASE_ENDPOINT = "/api/config/systems"

    def get_systems(
        self,
        extra_info: bool = False,
        filter_by_proxy_support: str | None = None,
        filter_by_name: str | None = None,
        filter_by_tag: str | None = None,
    ) -> dict[str, Any] | list[Any] | str:
        """Get all systems."""
        params: dict[str, Any] = {}
        if extra_info:
            params["extraInfo"] = extra_info
        if self._is_valid_param(filter_by_proxy_support):
            params["filterByProxySupport"] = filter_by_proxy_support
        if self._is_valid_param(filter_by_name):
            params["filterByName"] = filter_by_name
        if self._is_valid_param(filter_by_tag):
            params["filterByTag"] = filter_by_tag
        return self._request("GET", self.BASE_ENDPOINT, params=params)

    def get_system_by_id(self, id: str, extra_info: bool = False) -> dict[str, Any] | list[Any] | str:
        """Get a system by ID."""
        params = {}
        if extra_info:
            params["extraInfo"] = extra_info
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}", params=params)

    def create_system(
        self,
        name: str,
        system_type: str,
        platform_type: str,
        description: str | None = None,
        data_center_id: str | None = None,
        region: str | None = None,
        software_version: str | None = None,
        maximum_memory_per_node: float | None = None,
        bridge_only: bool | None = None,
        proxy_support_type: str | None = None,
        proxy_port: int | None = None,
        proxy_network_id: str | None = None,
        proxy_bridge_id: str | None = None,
        enable_proxy: bool | None = None,
        enable_override_port: bool | None = None,
        override_port: int | None = None,
        auto_node_delete: bool | None = None,
        auto_node_delete_minutes: int | None = None,
        system_flavor: str | None = None,
        tags: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any] | str:
        """Create a new system.

        Args:
            name: The name of the system.
            system_type: The type of the data source (TERADATA, PRESTO, HADOOP, OTHER).
            platform_type: The platform (AWS, AZURE, GC, PRIVATE, ON_PREM).
            description: A description of the system.
            data_center_id: The ID of the data center.
            region: Region the system is located in.
            software_version: The version of the tdqg-node package.
            maximum_memory_per_node: Maximum memory per node in bytes.
            bridge_only: Flags if this system is a bridge only system.
            proxy_support_type: Proxy support type (NO_PROXY, LOCAL_PROXY, BRIDGE_PROXY).
            proxy_port: The port number for proxying connections.
            proxy_network_id: The UUID of a network rule for proxy support.
            proxy_bridge_id: The ID of a remote bridge system.
            enable_proxy: Flags if this system should run a proxy.
            enable_override_port: Flags if overriding the fabric TCP server socket.
            override_port: The port number for the tdqg-node service.
            auto_node_delete: Flag to enable auto node delete.
            auto_node_delete_minutes: Minutes a node is offline before auto delete.
            system_flavor: The flavor of the Hadoop system (emr, cdp, dataproc, hdinsight).
            tags: Optional string key/value pairs.

        Returns:
            The created system data.
        """
        data: dict[str, Any] = {
            "name": name,
            "systemType": system_type,
            "platformType": platform_type,
        }
        if description is not None:
            data["description"] = description
        if data_center_id is not None:
            data["dataCenterId"] = data_center_id
        if region is not None:
            data["region"] = region
        if software_version is not None:
            data["softwareVersion"] = software_version
        if maximum_memory_per_node is not None:
            data["maximumMemoryPerNode"] = maximum_memory_per_node
        if bridge_only is not None:
            data["bridgeOnly"] = bridge_only
        if proxy_support_type is not None:
            data["proxySupportType"] = proxy_support_type
        if proxy_port is not None:
            data["proxyPort"] = proxy_port
        if proxy_network_id is not None:
            data["proxyNetworkId"] = proxy_network_id
        if proxy_bridge_id is not None:
            data["proxyBridgeId"] = proxy_bridge_id
        if enable_proxy is not None:
            data["enableProxy"] = enable_proxy
        if enable_override_port is not None:
            data["enableOverridePort"] = enable_override_port
        if override_port is not None:
            data["overridePort"] = override_port
        if auto_node_delete is not None:
            data["autoNodeDelete"] = auto_node_delete
        if auto_node_delete_minutes is not None:
            data["autoNodeDeleteMinutes"] = auto_node_delete_minutes
        if system_flavor is not None:
            data["systemFlavor"] = system_flavor
        if tags is not None:
            data["tags"] = tags
        return self._request("POST", self.BASE_ENDPOINT, json=data)

    def delete_system(self, id: str) -> dict[str, Any] | list[Any] | str:
        """Delete a system by ID.

        Args:
            id: The ID of the system to delete.

        Returns:
            The API response.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}"
        return self._request("DELETE", api_endpoint)
