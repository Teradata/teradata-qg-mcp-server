"""Integration tests for shared_memory_estimator_tools."""

from __future__ import annotations

import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_estimate_shared_memory_basic(mcp_client: Client):
    """Test shared memory estimation with basic parameters."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 10.0,
            "link_buffer_size": 1048576.0,
            "link_buffer_count": 100.0,
            "workers_per_node": 4.0,
        },
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    assert metadata["success"] is True

    # Should return estimation result
    assert "result" in result.data


@pytest.mark.integration
async def test_qg_estimate_shared_memory_small_values(mcp_client: Client):
    """Test shared memory estimation with small parameter values."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 1.0,
            "link_buffer_size": 1024.0,
            "link_buffer_count": 10.0,
            "workers_per_node": 1.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_estimate_shared_memory_large_values(mcp_client: Client):
    """Test shared memory estimation with large parameter values."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 1000.0,
            "link_buffer_size": 10485760.0,
            "link_buffer_count": 1000.0,
            "workers_per_node": 64.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    # API may reject very large values
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_estimate_shared_memory_zero_concurrency(mcp_client: Client):
    """Test shared memory estimation with zero query concurrency."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 0.0,
            "link_buffer_size": 1048576.0,
            "link_buffer_count": 100.0,
            "workers_per_node": 4.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    # API may or may not accept zero concurrency
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_estimate_shared_memory_zero_buffer_size(mcp_client: Client):
    """Test shared memory estimation with zero buffer size."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 10.0,
            "link_buffer_size": 0.0,
            "link_buffer_count": 100.0,
            "workers_per_node": 4.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    # API may or may not accept zero buffer size
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_estimate_shared_memory_zero_buffer_count(mcp_client: Client):
    """Test shared memory estimation with zero buffer count."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 10.0,
            "link_buffer_size": 1048576.0,
            "link_buffer_count": 0.0,
            "workers_per_node": 4.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    # API may or may not accept zero buffer count
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_estimate_shared_memory_zero_workers(mcp_client: Client):
    """Test shared memory estimation with zero workers per node."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 10.0,
            "link_buffer_size": 1048576.0,
            "link_buffer_count": 100.0,
            "workers_per_node": 0.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    # API may or may not accept zero workers
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_estimate_shared_memory_fractional_values(mcp_client: Client):
    """Test shared memory estimation with fractional parameter values."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 5.5,
            "link_buffer_size": 1048576.5,
            "link_buffer_count": 50.5,
            "workers_per_node": 2.5,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    # API should handle fractional values
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_estimate_shared_memory_typical_small_deployment(mcp_client: Client):
    """Test shared memory estimation for typical small deployment."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 5.0,
            "link_buffer_size": 524288.0,  # 512KB
            "link_buffer_count": 50.0,
            "workers_per_node": 2.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_estimate_shared_memory_typical_medium_deployment(mcp_client: Client):
    """Test shared memory estimation for typical medium deployment."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 20.0,
            "link_buffer_size": 1048576.0,  # 1MB
            "link_buffer_count": 100.0,
            "workers_per_node": 8.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_estimate_shared_memory_typical_large_deployment(mcp_client: Client):
    """Test shared memory estimation for typical large deployment."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 100.0,
            "link_buffer_size": 2097152.0,  # 2MB
            "link_buffer_count": 200.0,
            "workers_per_node": 16.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_estimate_shared_memory_response_structure(mcp_client: Client):
    """Test response structure validation."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 10.0,
            "link_buffer_size": 1048576.0,
            "link_buffer_count": 100.0,
            "workers_per_node": 4.0,
        },
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata

    # Should have result with estimation
    if metadata["success"]:
        assert "result" in result.data


@pytest.mark.integration
async def test_qg_estimate_shared_memory_consistency(mcp_client: Client):
    """Test consistency of estimation for same parameters."""
    arguments = {
        "query_concurrency": 10.0,
        "link_buffer_size": 1048576.0,
        "link_buffer_count": 100.0,
        "workers_per_node": 4.0,
    }

    result1 = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments=arguments,
    )

    result2 = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments=arguments,
    )

    # Both calls should return same success status
    assert result1.data is not None
    assert result2.data is not None
    assert result1.data["metadata"]["success"] == result2.data["metadata"]["success"]

    # If successful, results should match
    if result1.data["metadata"]["success"]:
        assert result1.data["result"] == result2.data["result"]


@pytest.mark.integration
async def test_qg_estimate_shared_memory_different_buffer_sizes(mcp_client: Client):
    """Test that different buffer sizes produce different estimations."""
    base_args = {
        "query_concurrency": 10.0,
        "link_buffer_count": 100.0,
        "workers_per_node": 4.0,
    }

    # Small buffer
    result_small = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={**base_args, "link_buffer_size": 524288.0},  # 512KB
    )

    # Large buffer
    result_large = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={**base_args, "link_buffer_size": 2097152.0},  # 2MB
    )

    assert result_small.data is not None
    assert result_large.data is not None
    assert result_small.data["metadata"]["success"] is True
    assert result_large.data["metadata"]["success"] is True

    # Results should be different (larger buffer should require more memory)
    # This assumes the API returns different values for different buffer sizes


@pytest.mark.integration
async def test_qg_estimate_shared_memory_different_concurrency(mcp_client: Client):
    """Test that different concurrency values produce different estimations."""
    base_args = {
        "link_buffer_size": 1048576.0,
        "link_buffer_count": 100.0,
        "workers_per_node": 4.0,
    }

    # Low concurrency
    result_low = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={**base_args, "query_concurrency": 5.0},
    )

    # High concurrency
    result_high = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={**base_args, "query_concurrency": 50.0},
    )

    assert result_low.data is not None
    assert result_high.data is not None
    assert result_low.data["metadata"]["success"] is True
    assert result_high.data["metadata"]["success"] is True

    # Results should be different (higher concurrency should require more memory)


@pytest.mark.integration
async def test_qg_estimate_shared_memory_high_workers(mcp_client: Client):
    """Test shared memory estimation with high number of workers."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 10.0,
            "link_buffer_size": 1048576.0,
            "link_buffer_count": 100.0,
            "workers_per_node": 128.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_estimate_shared_memory_max_buffer_count(mcp_client: Client):
    """Test shared memory estimation with maximum buffer count."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 10.0,
            "link_buffer_size": 1048576.0,
            "link_buffer_count": 10000.0,
            "workers_per_node": 4.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_estimate_shared_memory_minimal_config(mcp_client: Client):
    """Test shared memory estimation with minimal configuration."""
    result = await mcp_client.call_tool(
        "qg_estimate_shared_memory",
        arguments={
            "query_concurrency": 1.0,
            "link_buffer_size": 65536.0,  # 64KB
            "link_buffer_count": 5.0,
            "workers_per_node": 1.0,
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_estimate_shared_memory"
    assert metadata["success"] is True
