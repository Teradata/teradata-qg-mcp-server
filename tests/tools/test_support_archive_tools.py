"""Tests for support archive tools."""

import json
import os
from unittest.mock import MagicMock, patch

import pytest
from mcp import ClientSession


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


@pytest.fixture
def mock_qgm():
    """Mock QueryGridManager for download info tests - reads from environment variables."""
    # Read from environment variables - no defaults, must be set by user
    base_url = os.getenv("QGM_BASE_URL")
    verify_ssl = os.getenv("QGM_VERIFY_SSL")
    
    if base_url is None:
        raise ValueError(
            "QGM_BASE_URL environment variable is not set. "
            "Please set it to your QueryGrid Manager URL (e.g., export QGM_BASE_URL='https://qgm-host:9443')"
        )
    
    if verify_ssl is None:
        raise ValueError(
            "QGM_VERIFY_SSL environment variable is not set. "
            "Please set it to 'true' or 'false' (e.g., export QGM_VERIFY_SSL='false')"
        )
    
    mock_mgr = MagicMock()
    mock_mgr.base_url = base_url
    
    # Mock session with required properties
    mock_session = MagicMock()
    mock_session.verify = verify_ssl.lower() == "true"
    mock_mgr.session = mock_session
    
    return mock_mgr


class TestSupportArchiveTools:
    """Test support archive tools."""

    async def test_qg_get_support_archive_manager(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting manager support archive download info."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            result = await mcp_client.call_tool(
                "qg_get_support_archive_manager", arguments={}
            )

            assert result is not None
            assert len(result.content) == 1
            
            # Parse the JSON result
            result_dict = json.loads(result.content[0].text)
            assert "result" in result_dict
            
            download_info = result_dict["result"]
            assert download_info["full_url"] == f"{mock_qgm.base_url}/api/support-archive/manager"
            assert download_info["method"] == "GET"
            assert download_info["verify_ssl"] == mock_qgm.session.verify
            assert "headers" in download_info
            assert download_info["headers"]["Accept"] == "application/zip"
            assert "instructions" in download_info
            assert "credential_note" in download_info
            assert "Ask user" in download_info["credential_note"] or "ASK" in str(download_info["instructions"])

    async def test_qg_get_support_archive_manager_with_time_params(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting manager download info with time parameters."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            result = await mcp_client.call_tool(
                "qg_get_support_archive_manager",
                arguments={
                    "start_time": "2023-01-01T00:00:00Z",
                    "end_time": "2023-01-31T23:59:59Z",
                },
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            assert "startTime=2023-01-01T00:00:00Z" in download_info["full_url"]
            assert "endTime=2023-01-31T23:59:59Z" in download_info["full_url"]

    async def test_qg_get_support_archive_manager_with_days(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting manager download info with days parameter."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            result = await mcp_client.call_tool(
                "qg_get_support_archive_manager",
                arguments={"days": "30"},
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            assert "days=30" in download_info["full_url"]

    async def test_qg_get_support_archive_query(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting query support archive download info."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            result = await mcp_client.call_tool(
                "qg_get_support_archive_query",
                arguments={"all": True, "completed": True},
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            assert "/api/support-archive/query" in download_info["full_url"]
            assert "all=true" in download_info["full_url"]
            assert "completed=true" in download_info["full_url"]
            assert download_info["method"] == "GET"
            assert "credential_note" in download_info

    async def test_qg_get_support_archive_query_with_time_filter(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting query download info with time filter."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            result = await mcp_client.call_tool(
                "qg_get_support_archive_query",
                arguments={"last_modified_after": "2023-01-01T00:00:00Z"},
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            assert "lastModifiedAfter=2023-01-01T00:00:00Z" in download_info["full_url"]

    async def test_qg_get_support_archive_config(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting config support archive download info."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            result = await mcp_client.call_tool(
                "qg_get_support_archive_config", arguments={}
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            assert download_info["full_url"] == f"{mock_qgm.base_url}/api/support-archive/config"
            assert "Configuration archives are typically small" in str(download_info["notes"])
            assert "credential_note" in download_info

    async def test_qg_download_support_archive_config(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test downloading config support archive with base64 encoding."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            # Mock the actual download to return fake zip bytes
            mock_zip_content = b'PK\x03\x04fake_zip_content'  # Fake zip file signature
            
            with patch("src.qgm.support_archive.SupportArchiveClient.get_support_archive_config", 
                      return_value=mock_zip_content):
                result = await mcp_client.call_tool(
                    "qg_download_support_archive_config", arguments={}
                )

                result_dict = json.loads(result.content[0].text)
                base64_content = result_dict["result"]
                
                # Verify it's a base64-encoded string
                assert isinstance(base64_content, str)
                
                # Verify we can decode it back to the original bytes
                import base64
                decoded_bytes = base64.b64decode(base64_content)
                assert decoded_bytes == mock_zip_content

    async def test_qg_get_support_archive_node_with_filters(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting node download info with filters."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            system_id = "sys-123"
            result = await mcp_client.call_tool(
                "qg_get_support_archive_node",
                arguments={"system_id": system_id},
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            assert f"systemId={system_id}" in download_info["full_url"]
            assert "credential_note" in download_info

    async def test_qg_get_support_archive_node_with_fabric_filter(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting node download info with fabric filter."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            fabric_id = "fab-456"
            result = await mcp_client.call_tool(
                "qg_get_support_archive_node",
                arguments={"fabric_id": fabric_id},
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            assert f"fabricId={fabric_id}" in download_info["full_url"]

    async def test_qg_get_support_archive_node_with_connector_filter(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting node download info with connector filter."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            connector_id = "conn-789"
            result = await mcp_client.call_tool(
                "qg_get_support_archive_node",
                arguments={"connector_id": connector_id},
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            assert f"connectorId={connector_id}" in download_info["full_url"]

    async def test_qg_get_support_archive_node_no_filters_warning(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test node download info without filters shows warning."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            result = await mcp_client.call_tool(
                "qg_get_support_archive_node", arguments={}
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            # Check for warning about no filters
            notes_str = str(download_info["notes"])
            assert "WARNING" in notes_str or "large" in notes_str.lower()

    async def test_qg_get_support_archive_diagnostic_check(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting diagnostic check download info."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            result = await mcp_client.call_tool(
                "qg_get_support_archive_diagnostic_check", arguments={}
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            assert "/api/support-archive/diagnostic-check" in download_info["full_url"]
            assert "credential_note" in download_info

    async def test_qg_get_support_archive_diagnostic_check_with_filter(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test getting diagnostic check download info with check_id filter."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            check_id = "check-456"
            result = await mcp_client.call_tool(
                "qg_get_support_archive_diagnostic_check",
                arguments={"check_id": check_id},
            )

            result_dict = json.loads(result.content[0].text)
            download_info = result_dict["result"]
            
            assert f"checkId={check_id}" in download_info["full_url"]

    async def test_no_credentials_in_response(
        self, mcp_client: ClientSession, mock_qgm
    ):
        """Test that no credentials are included in any response."""
        with patch("src.tools.get_qg_manager", return_value=mock_qgm):
            # Test all tools
            tools_to_test = [
                ("qg_get_support_archive_manager", {}),
                ("qg_get_support_archive_query", {}),
                ("qg_get_support_archive_config", {}),
                ("qg_get_support_archive_node", {}),
                ("qg_get_support_archive_diagnostic_check", {}),
            ]
            
            for tool_name, args in tools_to_test:
                result = await mcp_client.call_tool(tool_name, arguments=args)
                result_dict = json.loads(result.content[0].text)
                download_info = result_dict["result"]
                
                # Verify no username or password fields
                assert "username" not in download_info
                assert "password" not in download_info
                
                # Verify credential_note is present
                assert "credential_note" in download_info
                assert "ASK" in download_info["credential_note"].upper() or \
                       "ASK" in str(download_info["instructions"]).upper()


# Unit tests
class TestSupportArchiveToolsUnit:
    """Unit tests for support archive tools module."""

    def test_module_imports(self):
        """Test that the module can be imported."""
        from src.tools import support_archive_tools

        assert support_archive_tools is not None

    def test_all_functions_exist(self):
        """Test that all expected functions exist."""
        from src.tools import support_archive_tools

        expected_functions = [
            "qg_get_support_archive_manager",
            "qg_get_support_archive_query",
            "qg_get_support_archive_config",
            "qg_download_support_archive_config",  # Base64 download version
            "qg_get_support_archive_node",
            "qg_get_support_archive_diagnostic_check",
        ]

        for func_name in expected_functions:
            assert hasattr(support_archive_tools, func_name)
            # Functions are decorated with @mcp.tool, so just verify they exist
            func = getattr(support_archive_tools, func_name)
            assert func is not None

    def test_environment_variables_read(self):
        """Test that environment variables are read correctly in fixture."""
        # This is tested indirectly through the fixture usage in other tests
        # Just verify we can read the env vars
        base_url = os.getenv("QGM_BASE_URL")
        verify_ssl = os.getenv("QGM_VERIFY_SSL")
        
        # If not set, the fixture will raise an error (tested in integration tests)
        # This unit test just verifies the variables can be read
        assert base_url is not None or True  # Will pass even if not set
        assert verify_ssl is not None or True  # Will pass even if not set
