from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_estimate_shared_memory(
    query_concurrency: float,
    link_buffer_size: float,
    link_buffer_count: float,
    workers_per_node: float,
) -> dict[str, Any]:
    """
    Estimate the shared memory required.

    Args:
        query_concurrency (float): Expected maximum number of QueryGrid queries to run at the same time.
        link_buffer_size (float): The maximum buffer size in bytes.
        link_buffer_count (float): The maximum number of buffers.
        workers_per_node (float): Number of threads that participate in a query on a given node.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_estimate_shared_memory called")

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.shared_memory_estimator_client.estimate_shared_memory(
            query_concurrency=query_concurrency,
            link_buffer_size=link_buffer_size,
            link_buffer_count=link_buffer_count,
            workers_per_node=workers_per_node,
        )

    return run_tool("qg_estimate_shared_memory", _call)
