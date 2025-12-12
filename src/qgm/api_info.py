"""API Info client for QueryGrid Manager API.

This module provides a small client for obtaining API metadata from the
QueryGrid Manager.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class ApiInfoClient(BaseClient):
    """Client for API info operations.

    This client wraps the simple API-info endpoint.
    """

    BASE_ENDPOINT = "/api/"

    def get_api_info(self) -> Any:
        """Get information about the API version and features.

        Returns a mapping containing API metadata. Keys are strings and
        values can be any JSON-serializable type.
        """
        api_endpoint = self.BASE_ENDPOINT
        return self._request("GET", api_endpoint)
