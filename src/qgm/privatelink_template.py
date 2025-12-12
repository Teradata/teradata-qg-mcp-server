"""
Manager for QueryGrid privatelink template operations.
"""

from __future__ import annotations

from .base import BaseClient


class PrivatelinkTemplateClient(BaseClient):
    """Manager for QueryGrid privatelink template operations."""

    BASE_ENDPOINT = "/api/operations"

    def get_privatelink_template(self, cloud_platform: str) -> bytes:
        """
        Generate private link template file for a given cloud platform.

        Args:
            cloud_platform (str): Name of the cloud platform. E.g. aws, azure, gc

        Returns:
            bytes: The template file content.
        """
        params = {"cloud_platform": cloud_platform}
        return self._request("GET", f"{self.BASE_ENDPOINT}/privatelink-template", params=params)
