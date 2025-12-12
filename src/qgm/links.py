"""
Manager for QueryGrid links.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class LinkClient(BaseClient):
    """Manager for QueryGrid links."""

    BASE_ENDPOINT = "/api/config/links"

    def get_links(
        self,
        flatten: bool = False,
        extra_info: bool = False,
        filter_by_name: str | None = None,
        filter_by_tag: str | None = None,
    ) -> dict[str, Any]:
        """Get all links."""
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

    def get_link_by_id(self, id: str, extra_info: bool = False) -> dict[str, Any]:
        """Get a link by ID."""
        params = {}
        if extra_info:
            params["extraInfo"] = extra_info
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}", params=params)

    def get_link_active(self, id: str) -> dict[str, Any]:
        """Get the active version of a link."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/active")

    def get_link_pending(self, id: str) -> dict[str, Any]:
        """Get the pending version of a link."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/pending")

    def get_link_previous(self, id: str) -> dict[str, Any]:
        """Get the previous version of a link."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/previous")

    def delete_link(self, id: str) -> dict[str, Any]:
        """Delete a link by ID.

        Args:
            id: The ID of the link to delete.

        Returns:
            The API response.
        """
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}")

    def create_link(
        self,
        name: str,
        fabricId: str,
        initiatorConnectorId: str,
        targetConnectorId: str,
        commPolicyId: str,
        description: str | None = None,
        initiatorProperties: dict[str, Any] | None = None,
        overridableInitiatorPropertyNames: list[str] | None = None,
        initiatorNetworkId: str | None = None,
        initiatorThreadsPerQuery: int | None = None,
        targetProperties: dict[str, Any] | None = None,
        overridableTargetPropertyNames: list[str] | None = None,
        targetNetworkId: str | None = None,
        targetThreadsPerQuery: int | None = None,
        userMappingId: str | None = None,
        usersToTroubleshoot: dict[str, Any] | None = None,
        enableAcks: bool | None = None,
        bridges: list[dict[str, Any]] | None = None,
        tags: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Create a new link in QueryGrid Manager.

        Args:
            name (str): The name of the link.
            fabricId (str): The ID of the fabric the link belongs to.
            initiatorConnectorId (str): The ID of the initiating connector.
            targetConnectorId (str): The ID of the target connector.
            commPolicyId (str): The ID of the communication policy to use.
            description (str | None): Optional description of the link.
            initiatorProperties (dict | None): Optional initiating connector properties.
            overridableInitiatorPropertyNames (list[str] | None): Optional overridable initiator properties.
            initiatorNetworkId (str | None): Optional network ID for initiator.
            initiatorThreadsPerQuery (int | None): Optional threads per query for initiator.
            targetProperties (dict | None): Optional target connector properties.
            overridableTargetPropertyNames (list[str] | None): Optional overridable target properties.
            targetNetworkId (str | None): Optional network ID for target.
            targetThreadsPerQuery (int | None): Optional threads per query for target.
            userMappingId (str | None): Optional user mapping ID.

            enableAcks (bool | None): Optional enable acknowledgments.
            bridges (list[dict] | None): Optional bridges configuration.
            usersToTroubleshoot (dict[str, Any] | None): Optional users to troubleshoot.
            tags (dict[str, str] | None): Optional string key/value pairs for context.

        Returns:
            dict[str, Any]: The response from the API.
        """
        data: dict[str, Any] = {
            "name": name,
            "fabricId": fabricId,
            "initiatorConnectorId": initiatorConnectorId,
            "targetConnectorId": targetConnectorId,
            "commPolicyId": commPolicyId,
            "description": description,
            "initiatorProperties": initiatorProperties,
            "overridableInitiatorPropertyNames": overridableInitiatorPropertyNames,
            "initiatorNetworkId": initiatorNetworkId,
            "initiatorThreadsPerQuery": initiatorThreadsPerQuery,
            "targetProperties": targetProperties,
            "overridableTargetPropertyNames": overridableTargetPropertyNames,
            "targetNetworkId": targetNetworkId,
            "targetThreadsPerQuery": targetThreadsPerQuery,
            "userMappingId": userMappingId,
            "usersToTroubleshoot": usersToTroubleshoot,
            "enableAcks": enableAcks,
            "bridges": bridges,
            "tags": tags,
        }
        return self._request("POST", self.BASE_ENDPOINT, json=data)
