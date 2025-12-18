"""
Manager for QueryGrid connectors.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class ConnectorClient(BaseClient):
    """Manager for QueryGrid connectors."""

    BASE_ENDPOINT = "/api/config/connectors"

    def get_connectors(
        self,
        flatten: bool = False,
        extra_info: bool = False,
        fabric_version: str | None = None,
        filter_by_name: str | None = None,
        filter_by_tag: str | None = None,
    ) -> Any:
        """Get all connectors."""
        params: dict[str, Any] = {}
        if flatten:
            params["flatten"] = flatten
        if extra_info:
            params["extraInfo"] = extra_info
        if self._is_valid_param(filter_by_name):
            params["filterByName"] = filter_by_name
        if self._is_valid_param(filter_by_tag):
            params["filterByTag"] = filter_by_tag
        if self._is_valid_param(fabric_version):
            params["fabricVersion"] = fabric_version
        return self._request("GET", self.BASE_ENDPOINT, params=params)

    def get_connector_by_id(self, id: str, extra_info: bool = False) -> Any:
        """Get a connector by ID."""
        params = {}
        if extra_info:
            params["extraInfo"] = extra_info
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}", params=params)

    def get_connector_active(self, id: str) -> Any:
        """Get the active version of a connector."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/active")

    def get_connector_pending(self, id: str) -> Any:
        """Get the pending version of a connector."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/pending")

    def get_connector_previous(self, id: str) -> Any:
        """Get the previous version of a connector."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/previous")

    def delete_connector(self, id: str) -> Any:
        """Delete a connector by ID."""
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}")

    def get_connector_drivers(self, id: str, version_id: str) -> Any:
        """Get drivers for a connector version."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/versions/{version_id}/drivers")

    def create_connector(
        self,
        name: str,
        software_name: str,
        software_version: str,
        fabric_id: str,
        system_id: str,
        description: str | None = None,
        driver_nodes: list[str] | None = None,
        properties: dict[str, Any] | None = None,
        overrideable_properties: list[str] | None = None,
        allowed_os_users: list[str] | None = None,
        tags: dict[str, str] | None = None,
    ) -> Any:
        """
        Create a new connector in QueryGrid Manager. Ask for missing parameters if needed. Do not fill in dummy values.
        Always confirm with the user before creating resources.

        Args:
            name (str): The name of the connector.
            software_name (str): The name of the software package to use for this connector.
            software_version (str): The version of the software package to use for this connector.
            fabric_id (str): The ID of the fabric this connector belongs to.
            system_id (str): The ID of the system this connector belongs to.
            description (str | None): Optional description of the connector.
            driver_nodes (list[str] | None): Optional list of node IDs where drivers should be installed.
            properties (dict | None): Optional properties to configure the connector.
            overrideable_properties (list[str] | None): Optional list of property names that can be
                overridden at runtime.
            allowed_os_users (list[str] | None): Optional list of OS users allowed to access this connector.
            tags (dict | None): Optional string key/value pairs for associating some context with the connector.

        Returns:
            dict[str, Any]: The response from the API.
        """
        data: dict[str, Any] = {
            "name": name,
            "softwareName": software_name,
            "softwareVersion": software_version,
            "fabricId": fabric_id,
            "systemId": system_id,
        }
        if description is not None:
            data["description"] = description
        if driver_nodes is not None:
            data["driverNodes"] = driver_nodes
        if properties is not None:
            data["properties"] = properties
        if overrideable_properties is not None:
            data["overrideableProperties"] = overrideable_properties
        if allowed_os_users is not None:
            data["allowedOSUsers"] = allowed_os_users
        if tags is not None:
            data["tags"] = tags
        return self._request("POST", self.BASE_ENDPOINT, json=data)

    def update_connector(
        self,
        id: str,
        name: str | None = None,
        description: str | None = None,
    ) -> Any:
        """
        Update Connector name or description using PATCH (partial update).

        Args:
            id (str): The ID of the connector to update.
            name (str | None): The name of the connector.
            description (str | None): Description of the connector.

        Returns:
            dict[str, Any]: The response from the API.
        """
        data: dict[str, Any] = {}
        if self._is_valid_param(name):
            data["name"] = name
        if self._is_valid_param(description):
            data["description"] = description

        return self._request("PATCH", f"{self.BASE_ENDPOINT}/{id}", json=data)

    def update_connector_active(
        self,
        id: str,
        version_id: str,
    ) -> Any:
        """
        Activate a specific version (pending or previous) of a connector using PATCH.

        NOTE FOR LLMs: When a connector is created, the response contains:
        - 'id': The connector wrapper ID (remains constant across versions)
        - 'versionId': The specific version ID (unique for each active/pending/previous version)
        
        To activate a pending or previous version:
        1. Get the pending/previous version using get_connector_pending() or get_connector_previous()
        2. Extract the 'versionId' from that response
        3. Call this method with the connector 'id' and the 'versionId' to activate

        Args:
            id (str): The connector wrapper ID (constant across all versions).
            version_id (str): The specific version ID to activate (from pending or previous version).

        Returns:
            dict[str, Any]: The response from the API.
        """
        return self._request(
            "PATCH", f"{self.BASE_ENDPOINT}/{id}/active", data=version_id
        )

    def put_connector_active(
        self,
        id: str,
        software_name: str,
        software_version: str,
        fabric_id: str,
        system_id: str,
        description: str | None = None,
        driver_nodes: list[str] | None = None,
        properties: dict[str, Any] | None = None,
        overrideable_properties: list[str] | None = None,
        allowed_os_users: list[str] | None = None,
        tags: dict[str, str] | None = None,
    ) -> Any:
        """
        Update the active version of a connector using PUT (full replacement).

        Args:
            id (str): The ID of the connector.
            software_name (str): The name of the software package.
            software_version (str): The version of the software package.
            fabric_id (str): The ID of the fabric this connector belongs to.
            system_id (str): The ID of the system this connector belongs to.
            description (str | None): Description of the connector.
            driver_nodes (list[str] | None): List of node IDs where drivers should be installed.
            properties (dict | None): Properties to configure the connector.
            overrideable_properties (list[str] | None): Property names that can be overridden at runtime.
            allowed_os_users (list[str] | None): OS users allowed to access this connector.
            tags (dict | None): String key/value pairs for context.

        Returns:
            dict[str, Any]: The response from the API.
        """
        data: dict[str, Any] = {
            "softwareName": software_name,
            "softwareVersion": software_version,
            "fabricId": fabric_id,
            "systemId": system_id,
        }
        if description is not None:
            data["description"] = description
        if driver_nodes is not None:
            data["driverNodes"] = driver_nodes
        if properties is not None:
            data["properties"] = properties
        if overrideable_properties is not None:
            data["overrideableProperties"] = overrideable_properties
        if allowed_os_users is not None:
            data["allowedOSUsers"] = allowed_os_users
        if tags is not None:
            data["tags"] = tags

        return self._request("PUT", f"{self.BASE_ENDPOINT}/{id}/active", json=data)

    def put_connector_pending(
        self,
        id: str,
        software_name: str,
        software_version: str,
        fabric_id: str,
        system_id: str,
        description: str | None = None,
        driver_nodes: list[str] | None = None,
        properties: dict[str, Any] | None = None,
        overrideable_properties: list[str] | None = None,
        allowed_os_users: list[str] | None = None,
        tags: dict[str, str] | None = None,
    ) -> Any:
        """
        Create or replace the pending version of a connector using PUT.

        Args:
            id (str): The ID of the connector.
            software_name (str): The name of the software package.
            software_version (str): The version of the software package.
            fabric_id (str): The ID of the fabric this connector belongs to.
            system_id (str): The ID of the system this connector belongs to.
            description (str | None): Description of the connector.
            driver_nodes (list[str] | None): List of node IDs where drivers should be installed.
            properties (dict | None): Properties to configure the connector.
            overrideable_properties (list[str] | None): Property names that can be overridden at runtime.
            allowed_os_users (list[str] | None): OS users allowed to access this connector.
            tags (dict | None): String key/value pairs for context.

        Returns:
            dict[str, Any]: The response from the API.
        """
        data: dict[str, Any] = {
            "softwareName": software_name,
            "softwareVersion": software_version,
            "fabricId": fabric_id,
            "systemId": system_id,
        }
        if description is not None:
            data["description"] = description
        if driver_nodes is not None:
            data["driverNodes"] = driver_nodes
        if properties is not None:
            data["properties"] = properties
        if overrideable_properties is not None:
            data["overrideableProperties"] = overrideable_properties
        if allowed_os_users is not None:
            data["allowedOSUsers"] = allowed_os_users
        if tags is not None:
            data["tags"] = tags

        return self._request("PUT", f"{self.BASE_ENDPOINT}/{id}/pending", json=data)

    def delete_connector_pending(self, id: str) -> Any:
        """
        Delete the pending version of a connector.

        Args:
            id (str): The ID of the connector.

        Returns:
            dict[str, Any]: The response from the API.
        """
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}/pending")

    def delete_connector_previous(self, id: str) -> Any:
        """
        Delete the previous version of a connector.

        Args:
            id (str): The ID of the connector.

        Returns:
            dict[str, Any]: The response from the API.
        """
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}/previous")
