"""
Manager for QueryGrid datasource registration operations.
"""

from __future__ import annotations

from .base import BaseClient
from typing import Any


class DatasourceRegistrationClient(BaseClient):
    """Manager for QueryGrid datasource registration operations."""

    BASE_ENDPOINT = "/api/operations"

    def get_datasource_registration(self, datasource_type: str, system_id: str) -> Any:
        """
        Generate node registration zip file for a given data source.

        Args:
            datasource_type (str): Name of the data source type.
                E.g. emr, dataproc, hdinsight, genericjdbc, cdp, bigquery, onpremtd
            system_id (str): ID of the system.

        Returns:
            Any: The API response. This may be a dict, list, str, or raw bytes
            depending on the underlying client implementation.
        """
        params: dict[str, str] = {}
        params["datasourceType"] = datasource_type
        params["systemId"] = system_id
        return self._request("GET", f"{self.BASE_ENDPOINT}/datasource-registration", params=params)
