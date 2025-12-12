from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_run_diagnostic_check(
    type: str,
    component_id: str | None = None,
    data_flow: str | None = None,
    node_id: str | None = None,
    version: str | None = None,
    bandwidth_mb_per_node: float | None = None,
    properties: str | None = None,
) -> dict[str, Any]:
    """
    Run a diagnostic check or connector install.

    Args:
        type (str): Type of diagnostic check (LINK, LINK_BANDWIDTH, CONNECTOR, CONNECTOR_INSTALL).
        component_id (str | None): Id of the link or connector to check.
        data_flow (str | None): Data flow direction.
        node_id (str | None): Id of the node.
        version (str | None): Version to use.
        bandwidth_mb_per_node (float | None): Bandwidth in MB per node.
        properties (str | None): Additional properties as JSON string.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_run_diagnostic_check called with type=%s", type)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.diagnostic_check_client.run_diagnostic_check(
            type=type,
            component_id=component_id,
            data_flow=data_flow,
            node_id=node_id,
            version=version,
            bandwidth_mb_per_node=bandwidth_mb_per_node,
            properties=properties,
        )

    return run_tool("qg_run_diagnostic_check", _call)


@mcp.tool
def qg_get_diagnostic_check_status(
    id: str,
) -> dict[str, Any]:
    """
    Get the status of a QueryGrid diagnostic check.

    Args:
        id (str): The ID of the diagnostic check. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_diagnostic_check_status called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.diagnostic_check_client.get_diagnostic_check_status(id)

    return run_tool("qg_get_diagnostic_check_status", _call)
