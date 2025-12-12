import logging
import logging.handlers
import os
import glob
import time
import warnings
from pathlib import Path
from typing import Any, Callable, cast

import yaml

# Suppress urllib3 SSL warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")
try:
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    pass  # urllib3 might not be imported yet


def load_config() -> dict[str, Any]:
    """Load complete configuration from config.yaml file.

    Returns:
        dict[str, Any]: Complete configuration dictionary with default values if file not found
    """
    default_config = {
        "server": {
            "host": "0.0.0.0",
            "port": 8000,
            "health_check_timeout": 5,
        },
        "querygrid": {
            "request_timeout": 10,
            "verify_ssl": True,
        },
        "logging": {
            "max_file_size_mb": 100,
            "retention_days": 30,
            "backup_count": 10,
            "log_level": "INFO",
            "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "date_format": "%Y-%m-%d %H:%M:%S",
        },
    }

    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        return default_config

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            # Merge with defaults to ensure all keys exist
            for section, defaults in default_config.items():
                if section not in config:
                    config[section] = defaults
                else:
                    # Merge section defaults with loaded values
                    config[section] = {**defaults, **config[section]}
            return config
    except Exception as e:
        logging.warning("Failed to load config.yaml, using defaults: %s", e)
        return default_config


def load_logging_config() -> dict[str, Any]:
    """Load logging configuration from config.yaml file.

    Returns:
        dict[str, Any]: Logging configuration dictionary with default values if file not found
    """
    default_config = {
        "max_file_size_mb": 100,
        "retention_days": 30,
        "backup_count": 10,
        "log_level": "INFO",
        "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "date_format": "%Y-%m-%d %H:%M:%S",
    }

    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        return default_config

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            return config.get("logging", default_config)
    except Exception as e:
        logging.warning("Failed to load config.yaml, using defaults: %s", e)
        return default_config


def cleanup_old_logs(log_file: str, retention_days: int) -> None:
    """Remove log files older than retention_days.

    Args:
        log_file: Path to the current log file
        retention_days: Number of days to retain log files
    """
    try:
        log_dir = os.path.dirname(log_file)
        log_basename = os.path.basename(log_file)
        # Pattern matches both rotated files (*.log.1, *.log.2) and dated files
        pattern = os.path.join(log_dir, "*")

        current_time = time.time()
        retention_seconds = retention_days * 24 * 60 * 60

        for file_path in glob.glob(pattern):
            if os.path.isfile(file_path) and file_path.endswith(".log"):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > retention_seconds:
                    try:
                        os.remove(file_path)
                        logging.debug("Removed old log file: %s", file_path)
                    except Exception as e:
                        logging.warning(
                            "Failed to remove old log file %s: %s", file_path, e
                        )
    except Exception as e:
        logging.warning("Error during log cleanup: %s", e)


def configure_logging() -> None:
    """Configure logging with rotation from environment variables and config.yaml.

    This standardizes logging setup across modules with automatic log rotation
    and retention management.
    """
    log_file = os.getenv("QG_MCP_SERVER_LOG_FILE")
    log_level = os.getenv("QG_MCP_SERVER_LOG_LEVEL")

    # Load configuration from config.toml
    config = load_logging_config()

    # Use config values or environment variables
    if log_level is None:
        log_level = config.get("log_level", "INFO")

    max_file_size_mb = config.get("max_file_size_mb", 100)
    retention_days = config.get("retention_days", 30)
    backup_count = config.get("backup_count", 10)
    log_format = config.get(
        "log_format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    date_format = config.get("date_format", "%Y-%m-%d %H:%M:%S")

    max_bytes = max_file_size_mb * 1024 * 1024  # Convert MB to bytes

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create formatter
    formatter = logging.Formatter(log_format, datefmt=date_format)

    handlers: list[logging.Handler] = []

    if log_file:
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Use RotatingFileHandler for log rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

        # Clean up old log files based on retention policy
        cleanup_old_logs(log_file, retention_days)

    # Always add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
        force=True,
    )


def extract_error_message(e: Exception) -> str:
    """Extract detailed error message from HTTP response or return string representation.

    Args:
        e: The exception that occurred

    Returns:
        str: The detailed error message
    """
    error_message = str(e)
    response = getattr(e, "response", None)
    if response is not None:
        try:
            error_details: Any = response.json()
            if isinstance(error_details, dict):
                error_dict = cast(dict[str, Any], error_details)
                msg: Any = (
                    error_dict.get("message")
                    or error_dict.get("error")
                    or cast(Any, error_details)
                )
                error_message = str(msg)
        except (ValueError, TypeError, AttributeError):
            text = getattr(response, "text", None)
            if text:
                error_message = str(text)
    return error_message


def create_response(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    """Create a formatted response with result and metadata.

    Args:
        result: The operation result
        metadata: Metadata about the operation

    Returns:
        dict[str, Any]: Formatted response
    """
    return {
        "result": result,
        "metadata": metadata,
    }


def run_tool(tool_name: str, func: Callable[[], Any]) -> dict[str, Any]:
    """Run a callable representing a tool operation and return a standardized response.

    Args:
        tool_name: Logical name of the tool (used in metadata)
        func: Zero-argument callable that performs the operation and returns a result

    Returns:
        dict[str, Any]: Formatted response produced by `create_response`.
    """
    logger = logging.getLogger(__name__)
    try:
        result = func()
        metadata: dict[str, Any] = {"tool_name": tool_name, "success": True}
        return create_response(result, metadata)
    except Exception as e:
        logger.error("Error in %s: %s", tool_name, e)
        error_message = extract_error_message(e)
        error_result = f"❌ Error in QueryGrid {tool_name} operation: {error_message}"
        error_metadata: dict[str, Any] = {
            "tool_name": tool_name,
            "error": error_message,
            "success": False,
        }
        return create_response(error_result, error_metadata)
