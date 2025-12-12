"""
Manager for QueryGrid shared memory estimator.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class SharedMemoryEstimatorClient(BaseClient):
    """Manager for QueryGrid shared memory estimator operations."""

    BASE_ENDPOINT = "/api/shared-memory-estimator"

    def estimate_shared_memory(
        self,
        query_concurrency: float,
        link_buffer_size: float,
        link_buffer_count: float,
        workers_per_node: float,
    ) -> dict[str, Any]:
        """Estimate the shared memory required.

        Args:
            query_concurrency: Expected maximum number of QueryGrid queries to run at the same time.
            link_buffer_size: The maximum buffer size in bytes.
            link_buffer_count: The maximum number of buffers.
            workers_per_node: Number of threads that participate in a query on a given node.

        Returns:
            The estimated shared memory in bytes.
        """
        data = {
            "queryConcurrency": query_concurrency,
            "linkBufferSize": link_buffer_size,
            "linkBufferCount": link_buffer_count,
            "workersPerNode": workers_per_node,
        }
        return self._request("POST", self.BASE_ENDPOINT, json=data)
