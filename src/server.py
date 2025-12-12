from __future__ import annotations

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenv not installed, continue without .env support
    pass

from src.mcp_server import qg_mcp_server, lifespan as mcp_lifespan
from fastapi import APIRouter, Response, FastAPI
import logging
from src.utils import configure_logging
from typing import Any, cast, AsyncIterator
from contextlib import asynccontextmanager

configure_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Combined lifespan handler for Teradata QueryGrid MCP Server."""
    logger.info("Teradata QueryGrid MCP Server starting up")
    # Initialize QueryGrid Manager and inject into tools
    async with mcp_lifespan():
        # Initialize FastMCP's internal task group via its lifespan
        async with mcp_http_app.lifespan(app):
            yield
    logger.info("Teradata QueryGrid MCP Server shutting down")


# Create the MCP HTTP app once at module level
mcp_http_app = qg_mcp_server.http_app()

# Create a FastAPI app with lifespan
app = FastAPI(lifespan=app_lifespan)

# Health endpoint
router = APIRouter()


@router.get("/health")
def health(response: Response) -> dict[str, Any]:
    """Basic health endpoint. Returns JSON with application and optional
    QueryGrid Manager status. This endpoint is intentionally lightweight and
    does not block on long network calls.
    """
    status: dict[str, Any] = {"app": "ok"}

    # Prefer the injected qg_manager instance if available in the tools
    # package (it is injected during application startup). Fall back to
    # a best-effort initialization when environment variables are present.
    try:
        from src import tools

        injected_qg = tools.get_qg_manager()

        # Only use an injected manager; do not initialize a transient client here.
        if injected_qg is not None:
            try:
                info = injected_qg.api_info_client.get_api_info()
                status["querygrid"] = "ok"
                status["querygrid_version"] = (
                    cast(dict[str, Any], info).get("appVersion")
                    if isinstance(info, dict)
                    else None
                )
            except Exception:
                status["querygrid"] = "unreachable"
        else:
            # Explicitly report that QueryGrid is not configured in this process.
            status["querygrid"] = "not-configured"
    except Exception:
        # If importing tools unexpectedly fails, report nothing about QGM
        pass

    # Normalize HTTP status codes based on QueryGrid result:
    # - 200 OK: querygrid is ok or not-configured
    # - 503 Service Unavailable: querygrid is configured but unreachable
    if status.get("querygrid") == "unreachable":
        response.status_code = 503
    else:
        response.status_code = 200

    return status


# Register health routes on the main application
app.include_router(router)

# Mount the MCP app at root
app.mount("/", mcp_http_app)  # type: ignore[arg-type]

# For uvicorn to import the ASGI app, expose it at module level
asgi_app = app

if __name__ == "__main__":
    import uvicorn
    import os
    import signal
    import sys
    import subprocess
    from pathlib import Path
    from src.utils import load_config

    # Load configuration from config.yaml
    config = load_config()
    server_config = config.get("server", {})

    # Get host and port with priority: env var > config.yaml > hardcoded default
    host = os.getenv("QG_MCP_SERVER_HOST", server_config.get("host", "0.0.0.0"))
    port = int(os.getenv("QG_MCP_SERVER_PORT", str(server_config.get("port", 8000))))

    pid = os.getpid()
    logger.info(
        "Starting Teradata QueryGrid MCP Server on %s:%d (PID: %d)", host, port, pid
    )

    # Write PID file for CLI stop support
    pid_dir = Path("run")
    pid_dir.mkdir(parents=True, exist_ok=True)
    pid_file = pid_dir / "server.pid"
    try:
        pid_file.write_text(str(pid))
        logger.info("Wrote PID file at %s", pid_file)
    except Exception:
        logger.warning("Failed to write PID file at %s", pid_file)

    def kill_process_tree_and_exit(code: int = 0) -> None:
        """Kill this process and all children, then clean up and exit."""
        try:
            # Find and kill all child processes
            try:
                result = subprocess.run(
                    ["pgrep", "-P", str(pid)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                child_pids = [
                    int(p) for p in result.stdout.strip().split() if p.strip()
                ]

                for child_pid in child_pids:
                    try:
                        os.kill(child_pid, signal.SIGKILL)
                        logger.info("Killed child process %d", child_pid)
                    except ProcessLookupError:
                        pass
            except Exception as e:
                logger.warning("Error killing child processes: %s", e)

            # Remove PID file
            if pid_file.exists():
                pid_file.unlink()
                logger.info("Removed PID file %s", pid_file)
        except Exception as e:
            logger.warning("Failed to clean up: %s", e)
        finally:
            # Force exit this process
            os._exit(code)

    # Custom signal handlers to force shutdown of entire process tree
    def handle_sigint(sig, frame):
        logger.info("SIGINT received for PID %d. Shutting down process tree now.", pid)
        kill_process_tree_and_exit(0)

    def handle_sigterm(sig, frame):
        logger.info("SIGTERM received for PID %d. Shutting down process tree now.", pid)
        kill_process_tree_and_exit(0)

    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigterm)

    # Run uvicorn (it may also install handlers, but our handlers ensure cleanup)
    try:
        uvicorn.run(app, host=host, port=port, log_config=None)
    finally:
        # Ensure PID file is cleaned up if uvicorn exits normally
        try:
            if pid_file.exists():
                pid_file.unlink()
        except Exception:
            pass
