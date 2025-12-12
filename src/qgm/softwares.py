"""
Manager for QueryGrid software versions.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class SoftwareClient(BaseClient):
    """Manager for QueryGrid software."""

    BASE_ENDPOINT = "/api/software"

    def get_software(self, filter_by_name: str | None = None) -> dict[str, Any]:
        """Get all software packages."""
        params = {}
        if self._is_valid_param(filter_by_name):
            params["filterByName"] = filter_by_name
        return self._request("GET", self.BASE_ENDPOINT, params=params)

    def get_software_jdbc_driver(self) -> dict[str, Any]:
        """Find all JDBC driver related software."""
        api_endpoint = f"{self.BASE_ENDPOINT}/jdbc-driver"
        return self._request("GET", api_endpoint)  # No extraInfo for software

    def get_software_jdbc_driver_by_name(self, jdbc_driver_name: str) -> dict[str, Any]:
        """Find JDBC driver software by name."""
        api_endpoint = f"{self.BASE_ENDPOINT}/jdbc-driver/{jdbc_driver_name}"
        return self._request("GET", api_endpoint)

    def get_software_by_id(self, id: str) -> dict[str, Any]:
        """Get software by ID."""
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}"
        return self._request("GET", api_endpoint)

    def get_software_package(self, id: str) -> dict[str, Any]:
        """Download software package by ID."""
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}/package"
        return self._request("GET", api_endpoint)

    def get_software_resource_bundle(self, id: str, locale: str | None = None) -> dict[str, Any]:
        """Download software resource bundle by ID."""
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}/resource-bundle"
        params = {}
        if self._is_valid_param(locale):
            params["locale"] = locale
        return self._request("GET", api_endpoint, params=params)

    def delete_software(self, id: str) -> dict[str, Any]:
        """Delete software by ID.

        Args:
            id: The ID of the software to delete.

        Returns:
            The API response.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}"
        return self._request("DELETE", api_endpoint)

    def delete_jdbc_driver(self, id: str) -> dict[str, Any]:
        """Delete JDBC driver software by ID.

        Args:
            id: The ID of the JDBC driver software to delete.

        Returns:
            The API response.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/jdbc-driver/{id}"
        return self._request("DELETE", api_endpoint)
