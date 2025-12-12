"""
Manager for QueryGrid managers.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class ManagerClient(BaseClient):
    """Manager for QueryGrid managers."""

    BASE_ENDPOINT = "/api/managers"

    def get_managers(self, extra_info: bool = False, filter_by_name: str | None = None) -> dict[str, Any]:
        """
        Retrieve the list of QueryGrid manager objects from the API.

        Args:
            extra_info (bool): If True, includes additional detailed information
                      about each manager in the response. Defaults to False.
            filter_by_name (str | None): If provided, filters the managers by name.
                          Defaults to None.

        Returns:
            dict[str, Any]: A dictionary containing the list of managers and
                   any additional metadata from the API response.
        """
        params: dict[str, Any] = {}
        if extra_info:
            params["extraInfo"] = extra_info
        if self._is_valid_param(filter_by_name):
            params["filterByName"] = filter_by_name
        return self._request("GET", self.BASE_ENDPOINT, params=params)

    def get_manager_by_id(self, id: str) -> dict[str, Any]:
        """
        Retrieve a specific QueryGrid manager object by its ID.

        Args:
            id (str): The unique identifier of the manager.

        Returns:
            dict[str, Any]: A dictionary containing the manager details.
        """
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}"
        return self._request("GET", api_endpoint)
