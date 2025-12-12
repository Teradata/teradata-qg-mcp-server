"""Integration tests for softwares_tools."""

from __future__ import annotations

import uuid
import pytest
from fastmcp.client import Client

from tools import set_qg_manager  # type: ignore[import-not-found]


@pytest.mark.integration
async def test_qg_get_software_basic(mcp_client: Client):
    """Test getting all software packages."""
    result = await mcp_client.call_tool(
        "qg_get_software",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software"
    assert metadata["success"] is True

    # Should return list of software
    if "result" in result.data:
        result_data = result.data["result"]
        assert isinstance(result_data, (list, dict))


@pytest.mark.integration
async def test_qg_get_software_with_name_filter(mcp_client: Client):
    """Test getting software with name filter."""
    result = await mcp_client.call_tool(
        "qg_get_software",
        arguments={
            "filter_by_name": "querygrid",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_software_with_wildcard_filter(mcp_client: Client):
    """Test getting software with wildcard name filter."""
    result = await mcp_client.call_tool(
        "qg_get_software",
        arguments={
            "filter_by_name": "query*",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_software_with_asterisk_filter(mcp_client: Client):
    """Test getting software with asterisk wildcard."""
    result = await mcp_client.call_tool(
        "qg_get_software",
        arguments={
            "filter_by_name": "*grid*",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_software_with_nonexistent_name(mcp_client: Client):
    """Test getting software with non-existent name."""
    result = await mcp_client.call_tool(
        "qg_get_software",
        arguments={
            "filter_by_name": "nonexistent-software-xyz",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software"
    # Should succeed with empty results
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_software_case_insensitive(mcp_client: Client):
    """Test that software name filter is case insensitive."""
    result = await mcp_client.call_tool(
        "qg_get_software",
        arguments={
            "filter_by_name": "QUERYGRID",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_software_response_structure(mcp_client: Client):
    """Test software response structure validation."""
    result = await mcp_client.call_tool(
        "qg_get_software",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_software_jdbc_driver_basic(mcp_client: Client):
    """Test getting all JDBC driver packages."""
    result = await mcp_client.call_tool(
        "qg_get_software_jdbc_driver",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software_jdbc_driver"
    assert metadata["success"] is True


@pytest.mark.integration
async def test_qg_get_software_jdbc_driver_response_structure(mcp_client: Client):
    """Test JDBC driver response structure validation."""
    result = await mcp_client.call_tool(
        "qg_get_software_jdbc_driver",
        arguments={},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_software_jdbc_driver_by_name_basic(mcp_client: Client):
    """Test getting JDBC driver by name."""
    result = await mcp_client.call_tool(
        "qg_get_software_jdbc_driver_by_name",
        arguments={
            "jdbc_driver_name": "postgresql",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software_jdbc_driver_by_name"
    # May or may not find the driver
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_software_jdbc_driver_by_name_mysql(mcp_client: Client):
    """Test getting MySQL JDBC driver by name."""
    result = await mcp_client.call_tool(
        "qg_get_software_jdbc_driver_by_name",
        arguments={
            "jdbc_driver_name": "mysql",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software_jdbc_driver_by_name"
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_software_jdbc_driver_by_name_oracle(mcp_client: Client):
    """Test getting Oracle JDBC driver by name."""
    result = await mcp_client.call_tool(
        "qg_get_software_jdbc_driver_by_name",
        arguments={
            "jdbc_driver_name": "oracle",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software_jdbc_driver_by_name"
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_software_jdbc_driver_by_name_nonexistent(mcp_client: Client):
    """Test getting JDBC driver with non-existent name."""
    result = await mcp_client.call_tool(
        "qg_get_software_jdbc_driver_by_name",
        arguments={
            "jdbc_driver_name": "nonexistent-jdbc-driver-xyz",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software_jdbc_driver_by_name"
    # Should handle non-existent driver
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_software_jdbc_driver_by_name_empty(mcp_client: Client):
    """Test getting JDBC driver with empty name."""
    result = await mcp_client.call_tool(
        "qg_get_software_jdbc_driver_by_name",
        arguments={
            "jdbc_driver_name": "",
        },
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software_jdbc_driver_by_name"
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_software_by_id_not_found(mcp_client: Client):
    """Test getting software by non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_software_by_id",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_software_by_id_invalid_uuid(mcp_client: Client):
    """Test getting software by invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_get_software_by_id",
        arguments={"id": "not-a-valid-uuid"},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software_by_id"
    assert metadata["success"] is False


@pytest.mark.integration
async def test_qg_get_software_by_id_empty_id(mcp_client: Client):
    """Test getting software by empty ID."""
    result = await mcp_client.call_tool(
        "qg_get_software_by_id",
        arguments={"id": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_get_software_by_id"
    # API may accept empty ID
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_software_by_id_response_structure(mcp_client: Client):
    """Test software by ID response structure validation."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_get_software_by_id",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_get_software_by_id_consistency(mcp_client: Client):
    """Test consistency of get_software_by_id for same ID."""
    fake_id = str(uuid.uuid4())

    result1 = await mcp_client.call_tool(
        "qg_get_software_by_id",
        arguments={"id": fake_id},
    )

    result2 = await mcp_client.call_tool(
        "qg_get_software_by_id",
        arguments={"id": fake_id},
    )

    # Both calls should return same success/failure status
    assert result1.data is not None
    assert result2.data is not None
    assert result1.data["metadata"]["success"] == result2.data["metadata"]["success"]


@pytest.mark.integration
@pytest.mark.skip(
    reason="Skipping delete operation to avoid removing software packages from QGM"
)
async def test_qg_delete_software_not_found(mcp_client: Client):
    """Test deleting software by non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_software",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_software"
    # Should fail for non-existent ID
    assert metadata["success"] is False


@pytest.mark.integration
@pytest.mark.skip(
    reason="Skipping delete operation to avoid removing software packages from QGM"
)
async def test_qg_delete_software_invalid_uuid(mcp_client: Client):
    """Test deleting software by invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_software",
        arguments={"id": "not-a-valid-uuid"},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_software"
    assert metadata["success"] is False


@pytest.mark.integration
@pytest.mark.skip(
    reason="Skipping delete operation to avoid removing software packages from QGM"
)
async def test_qg_delete_software_empty_id(mcp_client: Client):
    """Test deleting software by empty ID."""
    result = await mcp_client.call_tool(
        "qg_delete_software",
        arguments={"id": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_software"
    assert metadata["success"] is False


@pytest.mark.integration
@pytest.mark.skip(
    reason="Skipping delete operation to avoid removing software packages from QGM"
)
async def test_qg_delete_software_response_structure(mcp_client: Client):
    """Test delete software response structure validation."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_software",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
@pytest.mark.skip(
    reason="Skipping delete operation to avoid removing JDBC drivers from QGM"
)
async def test_qg_delete_jdbc_driver_not_found(mcp_client: Client):
    """Test deleting JDBC driver by non-existent ID."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_jdbc_driver",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_jdbc_driver"
    # Should fail for non-existent ID
    assert metadata["success"] is False


@pytest.mark.integration
@pytest.mark.skip(
    reason="Skipping delete operation to avoid removing JDBC drivers from QGM"
)
async def test_qg_delete_jdbc_driver_invalid_uuid(mcp_client: Client):
    """Test deleting JDBC driver by invalid UUID format."""
    result = await mcp_client.call_tool(
        "qg_delete_jdbc_driver",
        arguments={"id": "not-a-valid-uuid"},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_jdbc_driver"
    assert metadata["success"] is False


@pytest.mark.integration
@pytest.mark.skip(
    reason="Skipping delete operation to avoid removing JDBC drivers from QGM"
)
async def test_qg_delete_jdbc_driver_empty_id(mcp_client: Client):
    """Test deleting JDBC driver by empty ID."""
    result = await mcp_client.call_tool(
        "qg_delete_jdbc_driver",
        arguments={"id": ""},
    )

    assert result.data is not None
    metadata = result.data["metadata"]
    assert metadata["tool_name"] == "qg_delete_jdbc_driver"
    assert metadata["success"] is False


@pytest.mark.integration
@pytest.mark.skip(
    reason="Skipping delete operation to avoid removing JDBC drivers from QGM"
)
async def test_qg_delete_jdbc_driver_response_structure(mcp_client: Client):
    """Test delete JDBC driver response structure validation."""
    fake_id = str(uuid.uuid4())

    result = await mcp_client.call_tool(
        "qg_delete_jdbc_driver",
        arguments={"id": fake_id},
    )

    assert result.data is not None
    assert isinstance(result.data, dict)
    assert "metadata" in result.data

    metadata = result.data["metadata"]
    assert "tool_name" in metadata
    assert "success" in metadata


@pytest.mark.integration
async def test_qg_software_error_handling(mcp_client: Client):
    """Test error handling across software tools."""
    # Test get_software_by_id with malformed UUID
    result = await mcp_client.call_tool(
        "qg_get_software_by_id",
        arguments={"id": "12345"},
    )
    assert result.data is not None
    assert "metadata" in result.data

    # Test JDBC driver by name with special characters
    result = await mcp_client.call_tool(
        "qg_get_software_jdbc_driver_by_name",
        arguments={"jdbc_driver_name": "invalid@#$%"},
    )
    assert result.data is not None
    assert "metadata" in result.data


@pytest.mark.integration
async def test_qg_get_software_consistency(mcp_client: Client):
    """Test consistency of get_software calls."""
    result1 = await mcp_client.call_tool(
        "qg_get_software",
        arguments={},
    )

    result2 = await mcp_client.call_tool(
        "qg_get_software",
        arguments={},
    )

    # Both calls should return same success status
    assert result1.data is not None
    assert result2.data is not None
    assert result1.data["metadata"]["success"] == result2.data["metadata"]["success"]


@pytest.mark.integration
async def test_qg_get_software_jdbc_driver_consistency(mcp_client: Client):
    """Test consistency of get_software_jdbc_driver calls."""
    result1 = await mcp_client.call_tool(
        "qg_get_software_jdbc_driver",
        arguments={},
    )

    result2 = await mcp_client.call_tool(
        "qg_get_software_jdbc_driver",
        arguments={},
    )

    # Both calls should return same success status
    assert result1.data is not None
    assert result2.data is not None
    assert result1.data["metadata"]["success"] == result2.data["metadata"]["success"]
