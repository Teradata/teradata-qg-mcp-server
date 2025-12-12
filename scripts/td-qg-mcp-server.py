#!/usr/bin/env python3
import subprocess
import sys
import os
import logging
import argparse
import platform
import json
import warnings
import signal
import time
import socket
from datetime import datetime
from typing import Optional, Dict, List

# Configure logging with simple format (no logger name prefix)
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Suppress all warnings
warnings.filterwarnings("ignore")


def is_port_in_use(host: str, port: int) -> bool:
    """Check if a port is already in use.

    Args:
        host: The host address to check
        port: The port number to check

    Returns:
        True if the port is in use, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True


def get_process_using_port(port: int) -> Optional[str]:
    """Get information about the process using a specific port.

    Args:
        port: The port number to check

    Returns:
        String with process information or None if not found
    """
    try:
        system = platform.system().lower()
        if system == "windows":
            result = subprocess.run(
                ["netstat", "-ano"], capture_output=True, text=True, check=False
            )
            for line in result.stdout.split("\n"):
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    if parts:
                        pid = parts[-1]
                        return f"PID {pid}"
        else:
            # Unix-like systems (Linux, macOS)
            result = subprocess.run(
                ["lsof", "-i", f":{port}"], capture_output=True, text=True, check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split("\n")
                if len(lines) > 1:
                    # Parse the output to get process info
                    process_info = []
                    for line in lines[1:]:  # Skip header
                        parts = line.split()
                        if len(parts) >= 2:
                            process_info.append(f"{parts[0]} (PID {parts[1]})")
                    return ", ".join(process_info)
    except Exception as e:
        logger.debug(f"Error checking process on port {port}: {e}")

    return None


def setup_log_file(log_dir: Optional[str] = None) -> str:
    """Set up and return the log file path.

    Uses a daily log file pattern: qg_server_YYYYMMDD.log
    """
    if log_dir is None:
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Create log file with date pattern (one file per day)
    today = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"qg_server_{today}.log")

    return log_file


def setup_environment(
    log_file: str,
    log_level: str,
    qgm_host: Optional[str] = None,
    qgm_port: Optional[int] = None,
    qgm_username: Optional[str] = None,
    qgm_password: Optional[str] = None,
    qgm_verify_ssl: Optional[bool] = None,
) -> Dict[str, str]:
    """Set up environment variables for the server."""
    env = os.environ.copy()
    env["QG_MCP_SERVER_LOG_FILE"] = log_file
    env["QG_MCP_SERVER_LOG_LEVEL"] = log_level
    if qgm_host:
        env["QG_MANAGER_HOST"] = qgm_host
    if qgm_port:
        env["QG_MANAGER_PORT"] = str(qgm_port)
    if qgm_username:
        env["QG_MANAGER_USERNAME"] = qgm_username
    if qgm_password:
        env["QG_MANAGER_PASSWORD"] = qgm_password
    if qgm_verify_ssl is not None:
        env["QG_MANAGER_VERIFY_SSL"] = "true" if qgm_verify_ssl else "false"
    return env


def get_uvicorn_cli_args(
    log_level: str, host: str = "0.0.0.0", port: int = 8000
) -> List[str]:
    """Get uvicorn command line arguments for subprocess."""
    # Use the Python executable from the current environment
    # This ensures we use the venv Python if available
    python_exe = sys.executable

    return [
        python_exe,
        "-m",
        "uvicorn",
        "src.server:app",
        "--host",
        host,
        "--port",
        str(port),
        "--log-level",
        log_level.lower(),
    ]


def start_server(
    log_dir: Optional[str] = None,
    log_level: str = "INFO",
    foreground: bool = False,
    reload_mode: bool = False,
    host: str = "0.0.0.0",
    port: int = 8000,
    qgm_host: Optional[str] = None,
    qgm_port: Optional[int] = None,
    qgm_username: Optional[str] = None,
    qgm_password: Optional[str] = None,
    qgm_verify_ssl: Optional[bool] = None,
) -> None:
    script_dir = os.path.dirname(__file__)
    project_dir = os.path.dirname(script_dir)

    # Check if port is already in use before starting
    if is_port_in_use(host if host != "0.0.0.0" else "127.0.0.1", port):
        process_info = get_process_using_port(port)
        error_msg = f"ERROR: Port {port} is already in use"
        if process_info:
            error_msg += f" by {process_info}"
        logger.error(error_msg)
        logger.error(
            f"Please stop the process using port {port} or use a different port with --port"
        )
        logger.error(f"To kill the process: lsof -ti :{port} | xargs kill -9")
        sys.exit(1)

    # Add project directory to Python path so src.server can be imported
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)

    # Set up logging level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.getLogger().setLevel(numeric_level)

    logger.debug(f"Using Python executable: {sys.executable}")
    logger.debug(f"Current working directory: {os.getcwd()}")
    logger.debug(f"Project directory: {project_dir}")
    logger.debug(f"Python path: {sys.path}")

    # Set up log file path
    log_file = setup_log_file(log_dir)

    src_dir = os.path.join(project_dir, "src")
    server_script = os.path.join(src_dir, "server.py")

    logger.debug(f"Server script path: {server_script}")
    logger.debug(f"Source directory: {src_dir}")

    if foreground:
        # Run server directly in foreground
        logger.info("Starting server in foreground mode")

        # Set environment variables for logging and QueryGrid
        env = setup_environment(
            log_file,
            log_level,
            qgm_host,
            qgm_port,
            qgm_username,
            qgm_password,
            qgm_verify_ssl,
        )
        os.environ.update(env)

        # Use uvicorn directly for consistent server behavior
        import uvicorn

        if reload_mode:
            # For reload mode, add src directory to Python path so uvicorn can import "server"
            logger.info("Hot reload enabled - watching for file changes")
            if src_dir not in sys.path:
                sys.path.insert(0, src_dir)
            uvicorn.run(
                "src.server:app",
                host=host,
                port=port,
                reload=True,
                reload_dirs=[src_dir],
                log_level=log_level.lower(),
            )
        else:
            # For non-reload mode, add src directory to Python path so uvicorn can import "server"
            if src_dir not in sys.path:
                sys.path.insert(0, src_dir)
            uvicorn.run(
                "src.server:app", host=host, port=port, log_level=log_level.lower()
            )
    else:
        # Use uvicorn directly in background mode for consistency and performance
        logger.info("Starting server in background mode")

        # Set environment variables for logging and QueryGrid (background)
        env = setup_environment(
            log_file,
            log_level,
            qgm_host,
            qgm_port,
            qgm_username,
            qgm_password,
            qgm_verify_ssl,
        )

        # Add project directory and src directory to PYTHONPATH for proper imports
        src_dir = os.path.join(project_dir, "src")
        env["PYTHONPATH"] = f"{project_dir}{os.pathsep}{src_dir}"

        # Run uvicorn directly in background
        uvicorn_cli_args = get_uvicorn_cli_args(log_level, host, port)

        # Open log file for uvicorn output
        log_file_handle = open(log_file, "a")

        # Start process in background with stdout/stderr redirected to log file
        process = subprocess.Popen(
            uvicorn_cli_args,
            cwd=project_dir,  # Run from project root, not src_dir
            env=env,
            stdout=log_file_handle,
            stderr=subprocess.STDOUT,  # Merge stderr into stdout
            start_new_session=True,  # Detach from terminal
            close_fds=True,  # Close file descriptors
        )

        # Save PID to file for later stopping
        pid_dir = os.path.join(project_dir, "run")
        os.makedirs(pid_dir, exist_ok=True)
        pid_file = os.path.join(pid_dir, "server.pid")
        try:
            with open(pid_file, "w") as f:
                f.write(str(process.pid))
            logger.info(f"Server PID saved to {pid_file}")
        except Exception as e:
            logger.error(f"Failed to save PID file: {e}")
            # Terminate the server process since we cannot track it
            try:
                process.terminate()
                logger.info("Server process terminated due to PID file error.")
            except Exception as term_e:
                logger.error(f"Failed to terminate server process: {term_e}")
            return

        logger.info(f"Server started in background (logs: {log_file})")


def is_process_running(pid: int) -> bool:
    """Check if a process with the given PID is running."""
    try:
        system = platform.system().lower()
        if system == "windows":
            # Use tasklist to check if process exists
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True,
                text=True,
                check=False,
            )
            return str(pid) in result.stdout
        else:
            # On Unix-like systems, send signal 0 to check if process exists
            os.kill(pid, 0)
            return True
    except (OSError, ProcessLookupError):
        return False


def get_server_status(host: str = "0.0.0.0", port: int = 8000) -> bool:
    """Check and display the server status."""
    script_dir = os.path.dirname(__file__)
    project_dir = os.path.dirname(script_dir)
    pid_file = os.path.join(project_dir, "run", "server.pid")

    if not os.path.exists(pid_file):
        logger.info("Server is not running (no PID file found)")
        return False

    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        if is_process_running(pid):
            logger.info(f"Server is running (PID: {pid})")

            # Try to get health check information
            import urllib.request
            import urllib.error
            import contextlib

            try:
                # Temporarily redirect stderr to suppress server-side warnings
                with open(os.devnull, "w") as devnull:
                    with contextlib.redirect_stderr(devnull):
                        # Temporarily suppress uvicorn access logs during health check
                        uvicorn_logger = logging.getLogger("uvicorn.access")
                        original_level = uvicorn_logger.level
                        uvicorn_logger.setLevel(logging.WARNING)

                        # Determine the correct URL based on host
                        health_url = (
                            f"http://localhost:{port}/health"
                            if host == "0.0.0.0"
                            else f"http://{host}:{port}/health"
                        )

                        # Load health check timeout from config
                        try:
                            import sys

                            sys.path.insert(0, os.path.join(project_dir, "src"))
                            from src.utils import load_config

                            config = load_config()
                            health_timeout = config.get("server", {}).get(
                                "health_check_timeout", 5
                            )
                        except Exception:
                            health_timeout = 5

                        req = urllib.request.Request(health_url)
                        with urllib.request.urlopen(
                            req, timeout=health_timeout
                        ) as response:
                            health_data = json.loads(response.read().decode())

                        # Restore original log level
                        uvicorn_logger.setLevel(original_level)

                # Display results after restoring stderr
                logger.info("Health Check Results:")
                logger.info(f"  Application: {health_data.get('app', 'unknown')}")
                logger.info(f"  QueryGrid: {health_data.get('querygrid', 'unknown')}")
                if health_data.get("querygrid_version"):
                    logger.info(
                        f"  QueryGrid Version: {health_data.get('querygrid_version')}"
                    )

            except urllib.error.URLError as e:
                logger.warning(f"Could not connect to health endpoint: {e}")
            except Exception as e:
                logger.warning(f"Error fetching health check: {e}")

            return True
        else:
            logger.info(f"Server is not running (stale PID file found: {pid})")
            # Clean up stale PID file
            try:
                os.remove(pid_file)
                logger.info("Removed stale PID file")
            except Exception as e:
                logger.warning(f"Failed to remove stale PID file: {e}")
            return False
    except Exception as e:
        logger.error(f"Error checking server status: {e}")
        return False


def _pid_file_path() -> str:
    script_dir = os.path.dirname(__file__)
    project_dir = os.path.dirname(script_dir)
    return os.path.join(project_dir, "run", "server.pid")


def _read_pid() -> Optional[int]:
    pid_file = _pid_file_path()
    try:
        if os.path.exists(pid_file):
            with open(pid_file, "r") as f:
                return int(f.read().strip())
    except Exception:
        logger.warning("Failed to read PID file")
    return None


def _delete_pid() -> None:
    pid_file = _pid_file_path()
    try:
        if os.path.exists(pid_file):
            os.remove(pid_file)
            logger.info("PID file removed")
    except Exception as e:
        logger.warning(f"Failed to remove PID file: {e}")


def _kill_process_tree(pid: int) -> None:
    """Kill a process and all its children."""
    try:
        # Get all child processes
        result = subprocess.run(
            ["pgrep", "-P", str(pid)],
            capture_output=True,
            text=True,
            check=False,
        )
        child_pids = [int(p) for p in result.stdout.strip().split() if p.strip()]

        # Kill children first
        for child_pid in child_pids:
            try:
                os.kill(child_pid, signal.SIGTERM)
                logger.info(f"Sent SIGTERM to child process {child_pid}")
            except ProcessLookupError:
                pass

        # Kill parent
        try:
            os.kill(pid, signal.SIGTERM)
            logger.info(f"Sent SIGTERM to parent process {pid}")
        except ProcessLookupError:
            pass

        # Wait and force kill if needed
        time.sleep(2)

        # Force kill any survivors
        for child_pid in child_pids:
            try:
                os.kill(child_pid, 0)  # Check if still alive
                os.kill(child_pid, signal.SIGKILL)
                logger.info(f"Sent SIGKILL to child process {child_pid}")
            except ProcessLookupError:
                pass

        try:
            os.kill(pid, 0)  # Check if still alive
            os.kill(pid, signal.SIGKILL)
            logger.info(f"Sent SIGKILL to parent process {pid}")
        except ProcessLookupError:
            pass

    except Exception as e:
        logger.warning(f"Error killing process tree: {e}")


def stop_server() -> None:
    """
    Stop the running server. Prefer PID file if available, else fallback to process search.
    Works for both daemon and foreground modes. Handles child processes (e.g., reload mode).
    Only kills the server associated with the PID file to avoid affecting other instances.
    """
    pid = _read_pid()
    if pid is not None:
        logger.info(f"Stopping server using PID from file: {pid}")
        try:
            if platform.system() != "Windows":
                # Verify the process is actually our server before killing
                try:
                    # Get process command to verify it's our server
                    result = subprocess.run(
                        ["ps", "-p", str(pid), "-o", "command="],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    if result.returncode == 0 and "src.server:app" in result.stdout:
                        logger.info(
                            f"Confirmed PID {pid} is our server, killing process tree"
                        )
                        _kill_process_tree(pid)
                    else:
                        logger.warning(
                            f"PID {pid} is not our server or already stopped"
                        )
                except Exception as e:
                    logger.warning(f"Could not verify process: {e}")
                    # Try killing anyway
                    _kill_process_tree(pid)
            else:
                # On Windows, /T flag kills the process tree
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], check=False)
                logger.info(f"Sent taskkill to process tree {pid}")
        except ProcessLookupError:
            logger.warning(f"Process {pid} not found. Cleaning up PID file.")
        finally:
            # Clean up PID file regardless
            _delete_pid()
        return

    # Fallback: try finding foreground process by command pattern
    # This searches for processes running our specific server
    logger.info("PID file missing; attempting process search fallback")
    try:
        result = subprocess.run(
            [
                "pgrep",
                "-f",
                "src.server:app",  # Only match our specific server
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        pids = [int(p) for p in result.stdout.strip().split() if p.strip()]
        if not pids:
            logger.error("No running server process found")
            return

        # For each found PID, kill its entire process tree
        for p in pids:
            logger.info(f"Found server process {p}, killing process tree")
            _kill_process_tree(p)

    except Exception as e:
        logger.error(f"Fallback process search failed: {e}")
        return


def main() -> None:
    # Load configuration from config.yaml for defaults
    try:
        script_dir = os.path.dirname(__file__)
        project_dir = os.path.dirname(script_dir)
        sys.path.insert(0, os.path.join(project_dir, "src"))
        from src.utils import load_config

        config = load_config()
        server_config = config.get("server", {})
        default_host = server_config.get("host", "0.0.0.0")
        default_port = server_config.get("port", 8000)
    except Exception:
        # Fallback to hardcoded defaults if config loading fails
        default_host = "0.0.0.0"
        default_port = 8000

    parser = argparse.ArgumentParser(
        description="Teradata QueryGrid MCP Server Manager", prog="td-qg-mcp-server.py"
    )
    parser.add_argument(
        "action",
        choices=["start", "stop", "status"],
        help="Action to perform: start, stop, or status the server",
    )
    parser.add_argument(
        "--log-dir",
        help="Directory to write server logs to (default: ./logs)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level for the management script (default: INFO)",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("QG_MCP_SERVER_HOST", default_host),
        help=f"Host to bind the server to (default: {default_host} from config.yaml, or QG_MCP_SERVER_HOST env var)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("QG_MCP_SERVER_PORT", str(default_port))),
        help=f"Port to bind the server to (default: {default_port} from config.yaml, or QG_MCP_SERVER_PORT env var)",
    )
    parser.add_argument(
        "--foreground",
        action="store_true",
        help="Run server in foreground mode (for development/debugging)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable hot reloading (automatically restart on code changes) - only works with --foreground",
    )
    parser.add_argument(
        "--qgm-host", help="QueryGrid Manager host (default: localhost)"
    )
    parser.add_argument(
        "--qgm-port", type=int, help="QueryGrid Manager port (default: 8080)"
    )
    parser.add_argument(
        "--qgm-username", help="QueryGrid Manager username (default: admin)"
    )
    parser.add_argument(
        "--qgm-password", help="QueryGrid Manager password (default: password)"
    )
    parser.add_argument(
        "--qgm-verify-ssl",
        type=lambda x: x.lower() in ["true", "1", "yes"],
        default=None,
        help="Verify SSL certificates when connecting to QueryGrid Manager (default: true). "
        'Use "false", "0", or "no" to disable SSL verification',
    )

    args = parser.parse_args()

    # Validate arguments
    if args.reload and not args.foreground:
        parser.error("--reload can only be used with --foreground")

    if args.action == "start":
        start_server(
            args.log_dir,
            args.log_level,
            args.foreground,
            args.reload,
            args.host,
            args.port,
            args.qgm_host,
            args.qgm_port,
            args.qgm_username,
            args.qgm_password,
            args.qgm_verify_ssl,
        )
    elif args.action == "stop":
        stop_server()
    elif args.action == "status":
        get_server_status(args.host, args.port)


if __name__ == "__main__":
    main()
