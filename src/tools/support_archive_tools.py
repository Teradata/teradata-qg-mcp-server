"""
Support Archive Tools for QueryGrid Manager MCP Server.

TOOL USAGE GUIDE:
=================

🔗 qg_get_support_archive_* tools (Return API URLs):
-----------------------------------------------------
Use these tools when you want to DOWNLOAD A FILE:
- qg_get_support_archive_manager()
- qg_get_support_archive_query()
- qg_get_support_archive_config()
- qg_get_support_archive_node()
- qg_get_support_archive_diagnostic_check()

These tools return API URL and connection details.
The AGENT must then:
1. Ask the user for QueryGrid Manager credentials
2. Write a Python script that calls the API URL
3. Download the zip file using the Python script
4. Save the file to disk

📦 qg_download_support_archive_* tools (Download and Create Zip File):
----------------------------------------------------------------------
Use these tools when you need to download and create a zip file:
- qg_download_support_archive_config()

These tools:
1. Automatically download using pre-configured credentials
2. Return base64-encoded content
3. Agent must use bash or Python to decode content and create zip file

DEFAULT BEHAVIOR:
- User asks to "download support archive" → Use qg_get_* (agent writes Python script)
- User asks for "content" or "base64" → Use qg_download_* (agent creates zip from base64)
"""

from __future__ import annotations

import logging
from typing import Any

from src.mcp_server import qg_mcp_server as mcp
from src.utils import run_tool
from src import tools

logger = logging.getLogger(__name__)


@mcp.tool
def qg_get_support_archive_manager(
    start_time: str | None = None,
    end_time: str | None = None,
    days: str | None = None,
    hours: str | None = None,
) -> dict[str, Any]:
    """
    Get download information for QueryGrid Manager support archive.
    
    ⚠️ THIS TOOL RETURNS API URL - NOT FILE CONTENT
    Use this tool when user wants to DOWNLOAD A FILE.
    For base64-encoded content, use qg_download_support_archive_config() instead.

    🚨 CRITICAL INSTRUCTIONS FOR AI AGENTS - READ CAREFULLY:
    ========================================================
    This tool ONLY returns the API URL and connection details.
    It does NOT download the file - you must ask the user for credentials.
    
    ⛔ DO NOT use credentials from:
    - get_qg_manager() or any pre-configured session
    - Environment variables
    - Configuration files
    - Any stored/cached credentials
    
    ✅ YOU MUST ASK THE USER:
    Before downloading, explicitly ask the user:
    - "What is your QueryGrid Manager username?"
    - "What is your QueryGrid Manager password?"
    
    If the user provided credentials in their original request, use those.
    Otherwise, ASK THE USER before proceeding.

    AGENT WORKFLOW:
    ==============
    1. Call this tool to get API URL and connection details
    2. Ask user for QueryGrid Manager username and password
    3. Write a Python script that:
       - Uses the returned API URL (not this tool)
       - Authenticates with user-provided credentials
       - Downloads the zip file from QueryGrid Manager
       - Saves it to disk
    4. Execute the Python script to download the file

    PYTHON SCRIPT EXAMPLE (for agent to write):
    ```python
    import requests
    from pathlib import Path

    # API details from tool response
    api_url = "https://qgm-host:9443/api/support-archive/manager?days=7"
    verify_ssl = False
    
    # Credentials from user
    username = "<user_provided_username>"
    password = "<user_provided_password>"
    
    # Download the file
    response = requests.get(
        api_url,
        auth=(username, password),
        verify=verify_ssl,
        headers={"Accept": "application/zip"},
        stream=True
    )
    response.raise_for_status()
    
    # Save to file
    output_path = Path.home() / "Downloads" / "qgm_manager_archive.zip"
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"Downloaded to: {output_path}")
    ```

    FILE SAVE LOCATIONS (OS-specific defaults):
    - Linux: /tmp/qgm_manager_archive.zip
    - macOS: ~/Downloads/qgm_manager_archive.zip  
    - Windows: C:\\Users\\<username>\\Downloads\\qgm_manager_archive.zip

    WHAT THIS ARCHIVE CONTAINS:
    - Manager logs and configuration
    - System health information
    - Typically small (<50MB)

    ALL PARAMETERS ARE OPTIONAL. If not provided, defaults will be used.

    Args:
        start_time (str | None): [OPTIONAL] Start of time range in ISO8601 format.
            e.g., '2024-01-01T00:00:00Z'
        end_time (str | None): [OPTIONAL] End of time range in ISO8601 format.
            e.g., '2024-01-31T23:59:59Z'
        days (str | None): [OPTIONAL] Number of days back to include. Defaults to 7.
            e.g., '7', '14', '30'
        hours (str | None): [OPTIONAL] Number of hours back to include.
            e.g., '24', '48', '72'

    Returns:
        dict: Download information including:
            - full_url: Complete API endpoint with parameters
            - verify_ssl: Whether to verify SSL certificates
            - method: HTTP method (GET)
            - headers: Required headers dict
            - instructions: Download steps
            - credential_note: Reminder to ask user for credentials
    """

    def _call() -> dict[str, Any]:
        from src.qgm.support_archive import SupportArchiveClient

        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        client = SupportArchiveClient(qg_manager.session, qg_manager.base_url)

        # Build query parameters
        params = {}
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        if days:
            params["days"] = days
        if hours:
            params["hours"] = hours

        # Construct full URL
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        full_url = f"{client.base_url}/api/support-archive/manager"
        if query_string:
            full_url += f"?{query_string}"

        # Determine SSL verification
        verify_ssl = client.session.verify if hasattr(client.session, "verify") else True

        return {
            "full_url": full_url,
            "verify_ssl": verify_ssl,
            "method": "GET",
            "headers": {
                "Accept": "application/zip",
            },
            "instructions": [
                "1. ASK THE USER for QueryGrid Manager username",
                "2. ASK THE USER for QueryGrid Manager password",
                "3. Use requests.get() with auth=(username, password)",
                "4. Set headers: Accept: application/zip",
                "5. Save response content (binary) to a .zip file",
                "6. Extract the zip file to view logs and configuration",
            ],
            "credential_note": "🚨 MANDATORY: You MUST ask the user for username and password. DO NOT use get_qg_manager() credentials, environment variables, or any pre-configured credentials. If user provided credentials in their request, use those. Otherwise ASK THE USER explicitly.",
            "notes": [
                "This endpoint returns a zip file stream",
                f"SSL verification is {'enabled' if verify_ssl else 'disabled'}",
                "Use 'stream=True' in requests.get() for large files",
                "Default filename suggestion: qgm_manager_archive.zip",
            ],
        }

    return run_tool("qg_get_support_archive_manager", _call)


@mcp.tool
def qg_get_support_archive_query(
    all: bool = False,
    last_modified_after: str | None = None,
    completed: bool = False,
) -> dict[str, Any]:
    """
    Get download information for QueryGrid query support archive.
    
    ⚠️ THIS TOOL RETURNS API URL - NOT FILE CONTENT
    Use this tool when user wants to DOWNLOAD A FILE.

    🚨 CRITICAL INSTRUCTIONS FOR AI AGENTS - READ CAREFULLY:
    ========================================================
    This tool ONLY returns the API URL. You MUST ask the user for credentials.
    
    ⛔ DO NOT use any pre-configured credentials from get_qg_manager(), environment variables, or config files.
    ✅ ASK THE USER: "What is your QueryGrid Manager username?" and "What is your password?"
    
    If credentials were in the original user request, use those. Otherwise, ASK EXPLICITLY.

    PYTHON SCRIPT EXAMPLE (for agent to write):
    ```python
    import requests
    
    # API details from tool response
    api_url = "https://qgm-host:9443/api/support-archive/query?all=true"
    verify_ssl = False
    
    # Credentials from user
    username = "<user_provided_username>"
    password = "<user_provided_password>"
    
    # Download
    response = requests.get(
        api_url,
        auth=(username, password),
        verify=verify_ssl,
        headers={"Accept": "application/zip"},
        stream=True
    )
    response.raise_for_status()
    
    # Save to file
    with open('qgm_query_archive.zip', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    ```

    WHAT THIS ARCHIVE CONTAINS:
    - Query execution logs
    - Can be VERY LARGE if all=True (hundreds of MB)
    - Use filters to reduce size

    Args:
        all (bool): [OPTIONAL] Include all queries (default: False)
        last_modified_after (str | None): [OPTIONAL] Modified since timestamp
        completed (bool): [OPTIONAL] Include completed queries only

    Returns:
        dict: Download information
    """

    def _call() -> dict[str, Any]:
        from src.qgm.support_archive import SupportArchiveClient

        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        client = SupportArchiveClient(qg_manager.session, qg_manager.base_url)

        params = {}
        if all:
            params["all"] = "true"
        if last_modified_after:
            params["lastModifiedAfter"] = last_modified_after
        if completed:
            params["completed"] = "true"

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        full_url = f"{client.base_url}/api/support-archive/query"
        if query_string:
            full_url += f"?{query_string}"

        verify_ssl = client.session.verify if hasattr(client.session, "verify") else True

        return {
            "full_url": full_url,
            "verify_ssl": verify_ssl,
            "method": "GET",
            "headers": {"Accept": "application/zip"},
            "instructions": [
                "1. ASK USER for username and password",
                "2. Use requests.get() with auth=(username, password)",
                "3. Set stream=True for large files",
                "4. Save binary content to qgm_query_archive.zip",
                "5. Extract to view query logs",
            ],
            "credential_note": "🚨 MANDATORY: You MUST ask the user for username and password. DO NOT use get_qg_manager() credentials, environment variables, or any pre-configured credentials. If user provided credentials in their request, use those. Otherwise ASK THE USER explicitly.",
            "notes": [
                "⚠️ WARNING: all=True can produce very large archives (>500MB)",
                "Use last_modified_after to limit size",
                f"SSL verification is {'enabled' if verify_ssl else 'disabled'}",
            ],
        }

    return run_tool("qg_get_support_archive_query", _call)


@mcp.tool
def qg_get_support_archive_config() -> dict[str, Any]:
    """
    Get download information for QueryGrid configuration archive.
    
    ⚠️ THIS TOOL RETURNS API URL - NOT FILE CONTENT
    Use this tool when user wants to DOWNLOAD A FILE.
    
    💡 ALTERNATIVE: If user asks for BASE64-ENCODED CONTENT or "the content" directly,
    use qg_download_support_archive_config() instead - it returns base64-encoded content.

    🚨 CRITICAL INSTRUCTIONS FOR AI AGENTS - READ CAREFULLY:
    ========================================================
    This tool ONLY returns the API URL. You MUST ask the user for credentials.
    
    ⛔ DO NOT use credentials from get_qg_manager() or any other source.
    ✅ ASK THE USER: "What is your QueryGrid Manager username and password?"
    
    NOTE: Use qg_download_support_archive_config() if you want automatic download with pre-configured credentials.

    WHAT THIS ARCHIVE CONTAINS:
    - All QueryGrid configurations
    - Links, fabrics, connectors, systems
    - Usually small (<10MB)

    Returns:
        dict: Download information
    """

    def _call() -> dict[str, Any]:
        from src.qgm.support_archive import SupportArchiveClient

        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        client = SupportArchiveClient(qg_manager.session, qg_manager.base_url)

        full_url = f"{client.base_url}/api/support-archive/config"
        verify_ssl = client.session.verify if hasattr(client.session, "verify") else True

        return {
            "full_url": full_url,
            "verify_ssl": verify_ssl,
            "method": "GET",
            "headers": {"Accept": "application/zip"},
            "instructions": [
                "1. ASK USER for username and password",
                "2. Use requests.get() with auth",
                "3. Save to qgm_config_archive.zip",
                "4. Extract to view configuration JSON files",
            ],
            "credential_note": "🚨 MANDATORY: You MUST ask the user for username and password. DO NOT use get_qg_manager() credentials, environment variables, or any pre-configured credentials. If user provided credentials in their request, use those. Otherwise ASK THE USER explicitly.",
            "notes": [
                "Configuration archives are typically small (<10MB)",
                f"SSL verification is {'enabled' if verify_ssl else 'disabled'}",
            ],
        }

    return run_tool("qg_get_support_archive_config", _call)


@mcp.tool
def qg_download_support_archive_config() -> dict[str, Any]:
    """
    Download QueryGrid configuration archive directly (returns base64-encoded zip file).
    
    ✅ THIS TOOL RETURNS BASE64-ENCODED CONTENT - NOT API URL
    Use this tool when user asks for:
    - "Get me the config archive content"
    - "Show me the config archive in base64"
    - "Download config archive as base64"
    
    🚫 DO NOT use this tool when user asks to:
    - "Download the config archive" (use qg_get_support_archive_config() instead)
    - "Give me the API to download" (use qg_get_support_archive_config() instead)

    ✅ THIS TOOL USES PRE-CONFIGURED CREDENTIALS: Unlike the qg_get_support_archive_* 
    tools, this tool automatically downloads the file using credentials from get_qg_manager().
    You do NOT need to ask the user for credentials when using this tool.

    ⚠️ RETURNS BASE64 CONTENT: This tool returns base64-encoded zip content.
    The AGENT must create the actual zip file using bash or Python.

    AGENT WORKFLOW:
    ==============
    1. Call this tool to get base64-encoded zip content
    2. Write a bash or Python script to decode and create zip file
    3. Execute the script to create the zip file
    4. Make the zip file available to the user

    PYTHON SCRIPT EXAMPLE (for agent to write):
    ```python
    import base64
    
    # Base64 content from tool response
    base64_content = "<base64_string_from_tool_response>"
    
    # Decode and write to zip file
    zip_bytes = base64.b64decode(base64_content)
    with open('qgm_config_archive.zip', 'wb') as f:
        f.write(zip_bytes)
    
    print("Zip file created: qgm_config_archive.zip")
    ```

    BASH SCRIPT EXAMPLE (for agent to write):
    ```bash
    # Decode base64 and create zip file
    echo "<base64_string_from_tool_response>" | base64 -d > qgm_config_archive.zip
    ```

    FILE SAVE LOCATION:
    - Ask the user where they want to save the file
    - Default suggestions by OS:
      * Linux: /tmp/qgm_config_archive.zip
      * macOS: ~/Downloads/qgm_config_archive.zip
      * Windows: %USERPROFILE%\\Downloads\\qgm_config_archive.zip

    WHAT THIS ARCHIVE CONTAINS:
    - All QueryGrid configurations
    - Links, fabrics, connectors, systems
    - Usually small (<10MB)

    Returns:
        dict: Base64-encoded zip file data in the 'result' field
    """

    def _call() -> str:
        import base64
        from src.qgm.support_archive import SupportArchiveClient

        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        client = SupportArchiveClient(qg_manager.session, qg_manager.base_url)

        # Get the zip file as bytes
        zip_bytes = client.get_support_archive_config()
        
        # Check file size and log warning for large files
        file_size_mb = len(zip_bytes) / (1024 * 1024)
        logger.info(f"Config archive size: {file_size_mb:.2f} MB")
        
        if file_size_mb > 10:
            logger.warning(
                "Config archive is larger than expected: %.2f MB. "
                "Base64 encoding will increase size to ~%.2f MB.",
                file_size_mb, file_size_mb * 1.33
            )
        
        # Convert bytes to base64 string for JSON serialization
        return base64.b64encode(zip_bytes).decode('utf-8')

    return run_tool("qg_download_support_archive_config", _call)


@mcp.tool
def qg_get_support_archive_node(
    system_id: str | None = None,
    fabric_id: str | None = None,
    connector_id: str | None = None,
) -> dict[str, Any]:
    """
    Get download information for QueryGrid node support archive.
    
    ⚠️ THIS TOOL RETURNS API URL - NOT FILE CONTENT
    Use this tool when user wants to DOWNLOAD A FILE.

    🚨 CRITICAL INSTRUCTIONS FOR AI AGENTS - READ CAREFULLY:
    ========================================================
    This tool ONLY returns the API URL. You MUST ask the user for credentials.
    This can produce VERY LARGE archives if no filters are applied.
    
    ⛔ DO NOT use credentials from get_qg_manager(), environment variables, or config.
    ✅ ASK THE USER: "What is your QueryGrid Manager username and password?"

    WHAT THIS ARCHIVE CONTAINS:
    - Node logs from all matching nodes
    - Can be EXTREMELY LARGE (>1GB) without filters
    - ALWAYS use system_id, fabric_id, or connector_id filters

    RECOMMENDED APPROACH:
    1. First, get node count: qg_get_nodes(filter_by_system_id=...)
    2. If many nodes, further filter by fabric or connector
    3. Then download the archive

    Args:
        system_id (str | None): [OPTIONAL] Filter by system ID (UUID)
        fabric_id (str | None): [OPTIONAL] Filter by fabric ID (UUID)
        connector_id (str | None): [OPTIONAL] Filter by connector ID (UUID)

    Returns:
        dict: Download information
    """

    def _call() -> dict[str, Any]:
        from src.qgm.support_archive import SupportArchiveClient

        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        client = SupportArchiveClient(qg_manager.session, qg_manager.base_url)

        params = {}
        if system_id:
            params["systemId"] = system_id
        if fabric_id:
            params["fabricId"] = fabric_id
        if connector_id:
            params["connectorId"] = connector_id

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        full_url = f"{client.base_url}/api/support-archive/node"
        if query_string:
            full_url += f"?{query_string}"

        verify_ssl = client.session.verify if hasattr(client.session, "verify") else True

        notes = [
            "Node archives can be extremely large without filters",
            "Use system_id, fabric_id, or connector_id to reduce size",
            f"SSL verification is {'enabled' if verify_ssl else 'disabled'}",
        ]
        if not system_id and not fabric_id and not connector_id:
            notes.insert(
                0,
                "⚠️ WARNING: No filters applied - archive may be VERY LARGE (>1GB). Consider adding filters.",
            )

        return {
            "full_url": full_url,
            "verify_ssl": verify_ssl,
            "method": "GET",
            "headers": {"Accept": "application/zip"},
            "instructions": [
                "1. ASK USER for username and password",
                "2. Check the notes for size warnings",
                "3. Use requests.get() with stream=True",
                "4. Consider showing download progress for large files",
                "5. Save to qgm_node_archive.zip",
            ],
            "credential_note": "🚨 MANDATORY: You MUST ask the user for username and password. DO NOT use get_qg_manager() credentials, environment variables, or any pre-configured credentials. If user provided credentials in their request, use those. Otherwise ASK THE USER explicitly.",
            "notes": notes,
        }

    return run_tool("qg_get_support_archive_node", _call)


@mcp.tool
def qg_get_support_archive_diagnostic_check(
    check_id: str | None = None,
) -> dict[str, Any]:
    """
    Get download information for diagnostic check support archive.
    
    ⚠️ THIS TOOL RETURNS API URL - NOT FILE CONTENT
    Use this tool when user wants to DOWNLOAD A FILE.

    🚨 CRITICAL INSTRUCTIONS FOR AI AGENTS - READ CAREFULLY:
    ========================================================
    This tool ONLY returns the API URL. You MUST ask the user for credentials.
    
    ⛔ DO NOT use credentials from get_qg_manager() or any pre-configured source.
    ✅ ASK THE USER: "What is your QueryGrid Manager username and password?"

    WHAT THIS ARCHIVE CONTAINS:
    - Diagnostic check results and logs
    - Size varies by check type (usually <100MB)

    Args:
        check_id (str | None): [OPTIONAL] Filter by diagnostic check ID (UUID)

    Returns:
        dict: Download information
    """

    def _call() -> dict[str, Any]:
        from src.qgm.support_archive import SupportArchiveClient

        qg_manager = tools.get_qg_manager()
        if qg_manager is None:
            raise RuntimeError("QueryGridManager is not initialized")
        client = SupportArchiveClient(qg_manager.session, qg_manager.base_url)

        params = {}
        if check_id:
            params["checkId"] = check_id

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        full_url = f"{client.base_url}/api/support-archive/diagnostic-check"
        if query_string:
            full_url += f"?{query_string}"

        verify_ssl = client.session.verify if hasattr(client.session, "verify") else True

        return {
            "full_url": full_url,
            "verify_ssl": verify_ssl,
            "method": "GET",
            "headers": {"Accept": "application/zip"},
            "instructions": [
                "1. ASK USER for username and password",
                "2. Use requests.get() with auth",
                "3. Save to qgm_diagnostic_archive.zip",
                "4. Extract to view diagnostic results",
            ],
            "credential_note": "🚨 MANDATORY: You MUST ask the user for username and password. DO NOT use get_qg_manager() credentials, environment variables, or any pre-configured credentials. If user provided credentials in their request, use those. Otherwise ASK THE USER explicitly.",
            "notes": [
                "Diagnostic archives are typically moderate size (<100MB)",
                f"SSL verification is {'enabled' if verify_ssl else 'disabled'}",
            ],
        }

    return run_tool("qg_get_support_archive_diagnostic_check", _call)
