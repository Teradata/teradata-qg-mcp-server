"""Test that the MCP server can run in both foreground and background modes."""

import os
import signal
import subprocess
import time
from pathlib import Path

import pytest
import requests

PROJECT_ROOT = Path(__file__).parent.parent
SERVER_SCRIPT = PROJECT_ROOT / "scripts" / "td-qg-mcp-server.py"
PID_FILE = PROJECT_ROOT / "run" / "server.pid"


@pytest.mark.integration
def test_server_background_mode():
    """Test that the server can start and stop in background mode."""
    # Clean up any leftover PID file
    if PID_FILE.exists():
        PID_FILE.unlink()

    # Start server in background
    result = subprocess.run(
        ["python", str(SERVER_SCRIPT), "start", "--port", "8003"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=30,  # Increased timeout
    )

    try:
        assert result.returncode == 0, f"Failed to start server: {result.stderr}"
        assert "Starting server in background mode" in result.stderr  # Logs go to stderr
        assert PID_FILE.exists(), "PID file was not created"

        # Read PID
        pid = int(PID_FILE.read_text().strip())
        assert pid > 0, "Invalid PID in PID file"

        # The fact that the command returned successfully with a PID file
        # confirms background mode works
    finally:
        # Clean up: try to stop the server if it's still running
        if PID_FILE.exists():
            subprocess.run(
                ["python", str(SERVER_SCRIPT), "stop"],
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                timeout=10,
            )


@pytest.mark.integration
def test_server_foreground_mode_starts():
    """Test that the server script can be invoked with foreground flag."""
    # This test verifies the command-line arguments are accepted
    # We'll start it as a subprocess and kill it quickly
    process = subprocess.Popen(
        ["python", str(SERVER_SCRIPT), "start", "--foreground", "--port", "8004"],
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Give it a moment to start or fail
        time.sleep(3)

        # Check if process is still running (not crashed)
        assert process.poll() is None, "Foreground server crashed immediately"

        # If still running, that's a success - foreground mode works
    finally:
        # Stop the server
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

    # Exit code -15 (SIGTERM) is expected since we terminated it
    # Negative return codes indicate signal termination
    assert (
        process.returncode == 0  # Clean shutdown
        or process.returncode == -15  # SIGTERM
        or process.returncode == -signal.SIGTERM  # SIGTERM (alternative representation)
    ), f"Unexpected return code: {process.returncode}"


@pytest.mark.integration
def test_server_reload_flag_requires_foreground():
    """Test that --reload flag requires --foreground."""
    result = subprocess.run(
        ["python", str(SERVER_SCRIPT), "start", "--reload", "--port", "8005"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0, "Should fail when --reload is used without --foreground"
    assert "--reload can only be used with --foreground" in result.stderr
