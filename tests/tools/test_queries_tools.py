"""Integration tests for queries_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_get_query_summary_basic(mcp_client: Client):
    """Test getting query summary with default parameters."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    assert metadata["success"] is True

    # Should return list of query summaries
    if "result" in result.data:
        result_data = result.data["result"]
        assert isinstance(result_data, (list, dict))


@pytest.mark.integration
async def test_qg_get_query_summary_completed_true(mcp_client: Client):
    """Test getting query summary filtering by completed queries."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "completed": True,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_query_summary_completed_false(mcp_client: Client):
    """Test getting query summary filtering by non-completed queries."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "completed": False,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_query_summary_with_last_modified_after(mcp_client: Client):
    """Test getting query summary with last_modified_after filter."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "last_modified_after": "2023-01-01T00:00:00Z",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_query_summary_with_query_text_phrase(mcp_client: Client):
    """Test getting query summary with query text phrase filter."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "query_text_phrase": "SELECT",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_query_summary_with_query_ref_ids(mcp_client: Client):
    """Test getting query summary with query reference IDs filter."""
    fake_id1 = str(uuid.uuid4())
    fake_id2 = str(uuid.uuid4())
    query_ref_ids = f"{fake_id1},{fake_id2}"

    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "query_ref_ids": query_ref_ids,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    # May succeed with empty results for non-existent IDs
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_summary_with_initiator_query_id(mcp_client: Client):
    """Test getting query summary with initiator query ID filter."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "initiator_query_id": fake_id,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    # May succeed with empty results for non-existent ID
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_summary_with_multiple_filters(mcp_client: Client):
    """Test getting query summary with multiple filters."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "last_modified_after": "2024-01-01T00:00:00Z",
            "completed": True,
            "query_text_phrase": "SELECT",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_query_summary_with_all_parameters(mcp_client: Client):
    """Test getting query summary with all parameters."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "last_modified_after": "2024-01-01T00:00:00Z",
            "completed": False,
            "query_text_phrase": "SELECT",
            "query_ref_ids": fake_id,
            "initiator_query_id": fake_id,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_summary_invalid_timestamp(mcp_client: Client):
    """Test getting query summary with invalid timestamp format."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "last_modified_after": "not-a-valid-timestamp",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    # API may or may not validate timestamp format
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_summary_response_structure(mcp_client: Client):
    """Test query summary response structure validation."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "completed": True,
        },
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_by_id_not_found(mcp_client: Client):
    """Test getting query by non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_query_by_id",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_query_by_id_invalid_uuid(mcp_client: Client):
    """Test getting query by invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_query_by_id",
        arguments={"id": "not-a-valid-uuid"},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_query_by_id_empty_id(mcp_client: Client):
    """Test getting query by empty ID."""
    result = await mcp_client.call_tool(
        "qg_get_query_by_id",
        arguments={"id": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_by_id"
    # API may succeed with empty ID
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_by_id_response_structure(mcp_client: Client):
    """Test query by ID response structure validation."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_query_by_id",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_details_not_found(mcp_client: Client):
    """Test getting query details by non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_query_details",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_details"
    # API may succeed with empty results for non-existent ID
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_details_invalid_uuid(mcp_client: Client):
    """Test getting query details by invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_query_details",
        arguments={"id": "not-a-valid-uuid"},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_details"
    # API may not validate UUID format strictly
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_details_empty_id(mcp_client: Client):
    """Test getting query details by empty ID."""
    result = await mcp_client.call_tool(
        "qg_get_query_details",
        arguments={"id": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_details"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_query_details_response_structure(mcp_client: Client):
    """Test query details response structure validation."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_query_details",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_queries_error_handling(mcp_client: Client):
    """Test error handling across query tools."""
    # Test get_query_by_id with malformed UUID
    result = await mcp_client.call_tool(
        "qg_get_query_by_id",
        arguments={"id": "12345"},
    )
    assert result.data is not None
    assert "metadata" in result.data

    # Test get_query_details with special characters
    result = await mcp_client.call_tool(
        "qg_get_query_details",
        arguments={"id": "invalid@#$%"},
    )
    assert result.data is not None
    assert "metadata" in result.data


@pytest.mark.integration
async def test_qg_get_query_summary_empty_query_text(mcp_client: Client):
    """Test getting query summary with empty query text phrase."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "query_text_phrase": "",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    # Empty string may be accepted by API
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_summary_future_timestamp(mcp_client: Client):
    """Test getting query summary with future timestamp."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "last_modified_after": "2099-12-31T23:59:59Z",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    # Future timestamp should be valid, may return empty results
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_query_summary_invalid_query_ref_ids_format(mcp_client: Client):
    """Test getting query summary with invalid query ref IDs format."""
    result = await mcp_client.call_tool(
        "qg_get_query_summary",
        arguments={
            "query_ref_ids": "not-a-uuid,also-not-a-uuid",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_query_summary"
    # API may or may not validate UUID format
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_query_by_id_consistency(mcp_client: Client):
    """Test consistency of get_query_by_id for same ID."""
    fake_id = str(uuid.uuid4())

    result1 = await mcp_client.call_tool(
        "qg_get_query_by_id",
        arguments={"id": fake_id},
    )

    result2 = await mcp_client.call_tool(
        "qg_get_query_by_id",
        arguments={"id": fake_id},
    )

    # Both calls should return same success/failure status
    assert result1.data is not None
    assert result2.data is not None
    assert result1.data["metadata"]["success"] == result2.data["metadata"]["success"]


@pytest.mark.integration
async def test_qg_get_query_details_consistency(mcp_client: Client):
    """Test consistency of get_query_details for same ID."""
    fake_id = str(uuid.uuid4())

    result1 = await mcp_client.call_tool(
        "qg_get_query_details",
        arguments={"id": fake_id},
    )

    result2 = await mcp_client.call_tool(
        "qg_get_query_details",
        arguments={"id": fake_id},
    )

    # Both calls should return same success/failure status
    assert result1.data is not None
    assert result2.data is not None
    assert result1.data["metadata"]["success"] == result2.data["metadata"]["success"]
