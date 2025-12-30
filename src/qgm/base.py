"""
Base client class for QueryGrid Manager API.
"""

from __future__ import annotations

import logging
from typing import Any

import requests


class BaseClient:
    """Base class for QueryGrid Manager API resource clients."""

    def __init__(self, session: requests.Session, base_url: str, timeout: int = 10):
        self.session = session
        self.base_url = base_url
        self.logger = logging.getLogger(self.__class__.__module__)

        # The session is expected to be pre-configured (e.g., with retry strategy) by QueryGridManager.

        # Timeout for requests (seconds) - configurable via config.yaml
        self._timeout = timeout

    @staticmethod
    def _is_valid_param(value: Any) -> bool:
        """Check if a parameter value is valid (not None, empty string, or 'null' string)."""
        return value is not None and value != "" and value != "null"

    def _request(self, method: str, endpoint: str, binary: bool = False, **kwargs: Any) -> Any:
        """Make a request to the QGM API.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint path
            binary: If True, return raw binary content. If False, return JSON or text.
            **kwargs: Additional arguments to pass to requests.Session.request()

        Returns:
            bytes if binary=True, otherwise a parsed JSON object (dict or list) or plain text response.
        """
        url = f"{self.base_url}{endpoint}"
        log_msg = "Making %s request to %s" + (" (binary response expected)" if binary else "")
        self.logger.debug(log_msg, method, url)

        # Ensure a timeout is always set to avoid hanging requests
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            # Include response body in error message for better debugging
            error_details = ""
            try:
                error_body = response.json()
                error_details = f"\nAPI Error: {error_body.get('message', error_body)}"
            except (ValueError, AttributeError):
                if response.text:
                    error_details = f"\nAPI Response: {response.text}"
            
            self.logger.error("HTTP request failed: %s%s", exc, error_details)
            raise requests.exceptions.HTTPError(
                f"{exc}{error_details}", response=response
            ) from exc
        except requests.exceptions.RequestException as exc:
            self.logger.error("HTTP request failed: %s", exc)
            raise

        if binary:
            return response.content
        
        try:
            return response.json()
        except ValueError:
            return response.text


