from __future__ import annotations

import os
from typing import AsyncIterator
from fastmcp import FastMCP
import logging
from src.qgm.querygrid_manager import QueryGridManager
from contextlib import asynccontextmanager


logger = logging.getLogger(__name__)

qg_mcp_server = FastMCP("Teradata QueryGrid MCP Server")


@asynccontextmanager
async def lifespan() -> AsyncIterator[None]:
    """ASGI lifespan context.

    Validates required environment variables (QG_MANAGER_*), initializes a
    `QueryGridManager`, injects it into the tools package, and ensures clean
    shutdown on application exit.
    """
    # Startup
    logger.info("MCP Server starting up")

    # Validate required environment variables
    host: str | None = os.getenv("QG_MANAGER_HOST")
    port: str | None = os.getenv("QG_MANAGER_PORT")
    username: str | None = os.getenv("QG_MANAGER_USERNAME")
    password: str | None = os.getenv("QG_MANAGER_PASSWORD")

    if not host or not port:
        raise ValueError(
            "QG_MANAGER_HOST and QG_MANAGER_PORT environment variables are required"
        )
    if not username or not password:
        raise ValueError(
            "QG_MANAGER_USERNAME and QG_MANAGER_PASSWORD environment variables are required"
        )

    # Initialize QueryGridManager and inject into tool modules
    qg_manager: QueryGridManager = QueryGridManager(
        username=username, password=password
    )

    # Import tools and set shared manager; tools package auto-imports its modules
    try:
        from src import tools

        tools.set_qg_manager(qg_manager)
    except Exception:
        logger.exception("Failed to initialize tools package or set qg_manager")

    try:
        yield
    finally:
        # Shutdown
        try:
            qg_manager.close()
        except Exception:
            logger.exception("Error closing QueryGridManager")
        logger.info("MCP Server shutting down")
