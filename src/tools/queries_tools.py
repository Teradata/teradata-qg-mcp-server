from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool

from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_query_summary(
    last_modified_after: str | None = None,
    completed: bool = False,
    query_text_phrase: str | None = None,
    query_ref_ids: str | None = None,
    initiator_query_id: str | None = None,
) -> dict[str, Any]:
    """
    Get summaries of all the queries run using QueryGrid. Query summaries can be filtered based on various criteria.
    Optional arguments can be ignored if not needed.

    Args:
        last_modified_after (str | None): [Optional] Return all query summary that have been modified since
            the time provided. Time should be provided in ISO8601 format. e.g., '2023-01-01T00:00:00Z'
        completed (bool): Include completed queries. Values are 'true' or 'false'.
        query_text_phrase (str | None): [Optional] Only return queries that contain the supplied phrase in the
            query text.
        query_ref_ids (str | None): [Optional] Filter by comma separated query reference IDs.
            IDs are in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000,223e4567-e89b-12d3-a456-426614174001'.
        initiator_query_id (str | None): [Optional] Filter by initiator query ID.
            ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.
    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug(
        "Tool: handle_qg_get_query_summary: last_modified_after=%s, completed=%s, query_text_phrase=%s, "
        "query_ref_ids=%s, initiator_query_id=%s",
        last_modified_after,
        completed,
        query_text_phrase,
        query_ref_ids,
        initiator_query_id,
    )

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.query_client.get_query_summary(
            last_modified_after=last_modified_after,
            completed=completed,
            query_text_phrase=query_text_phrase,
            query_ref_ids=query_ref_ids,
            initiator_query_id=initiator_query_id,
        )

    return run_tool("qg_get_query_summary", _call)


@mcp.tool
def qg_get_query_by_id(
    id: str,
) -> dict[str, Any]:
    """
    Get a specific QueryGrid query by ID.

    Args:
        id (str): The ID of the query to retrieve. ID is in UUID format. e.g., '123e4567-e89b-12d3-a456-426614174000'.

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_query_by_id called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.query_client.get_query_by_id(id)

    return run_tool("qg_get_query_by_id", _call)


@mcp.tool
def qg_get_query_details(
    id: str,
) -> dict[str, Any]:
    """
    Get detailed information for a specific QueryGrid query.

    Args:
        id (str): The ID of the query to retrieve details for

    Returns:
        ResponseType: formatted response with operation results + metadata
    """
    logger.debug("Tool: qg_get_query_details called with id=%s", id)

    def _call():
        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        return qg_manager.query_client.get_query_details(id)

    return run_tool("qg_get_query_details", _call)
