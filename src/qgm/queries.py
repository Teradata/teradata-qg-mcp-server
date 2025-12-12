"""
Manager for QueryGrid queries.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class QueryClient(BaseClient):
    """Manager for QueryGrid queries."""

    BASE_ENDPOINT = "/api/queries"

    def get_query_summary(
        self,
        last_modified_after: str | None = None,
        completed: bool = False,
        query_text_phrase: str | None = None,
        query_ref_ids: str | None = None,
        initiator_query_id: str | None = None,
    ) -> dict[str, Any]:
        """Get query summary records."""
        params: dict[str, Any] = {}
        if self._is_valid_param(last_modified_after):
            params["lastModifiedAfter"] = last_modified_after
        if completed:
            params["completed"] = completed
        if self._is_valid_param(query_text_phrase):
            params["queryTextPhrase"] = query_text_phrase
        if self._is_valid_param(query_ref_ids):
            params["queryRefIds"] = query_ref_ids
        if self._is_valid_param(initiator_query_id):
            params["initiatorQueryId"] = initiator_query_id
        return self._request("GET", self.BASE_ENDPOINT, params=params)

    def get_query_by_id(self, id: str) -> dict[str, Any]:
        """Get query summary by ID."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}")

    def get_query_details(self, id: str) -> dict[str, Any]:
        """Get query details by ID."""
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}/details")
