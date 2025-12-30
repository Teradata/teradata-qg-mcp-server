from __future__ import annotations

"""Tools package for Teradata QueryGrid MCP Server.

Provides a central accessor for the injected qg_manager and imports all tool
submodules so @mcp.tool decorators register with the FastMCP app.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.qgm.querygrid_manager import QueryGridManager

__all__ = ["get_qg_manager", "set_qg_manager"]

qg_manager: QueryGridManager | None = None


def get_qg_manager() -> QueryGridManager | None:
    """Return the injected QueryGridManager instance or None."""
    return qg_manager


def set_qg_manager(manager: QueryGridManager | None) -> None:
    """Set the module-level qg_manager reference."""
    global qg_manager
    qg_manager = manager


# Import tool submodules to trigger decorator registration
from src.tools import (
    api_info_tools,
    bridges_tools,
    comm_policies_tools,
    connectors_tools,
    create_foreign_server_tools,
    datacenters_tools,
    diagnostic_check_tools,
    fabrics_tools,
    issues_tools,
    links_tools,
    managers_tools,
    networks_tools,
    nodes_tools,
    node_virtual_ips_tools,
    operations_tools,
    queries_tools,
    shared_memory_estimator_tools,
    softwares_tools,
    support_archive_tools,
    systems_tools,
    user_mapping_tools,
    users_tools,
)
