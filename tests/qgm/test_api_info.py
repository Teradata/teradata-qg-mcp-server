"""Integration tests for API info client."""

from __future__ import annotations

import pytest


@pytest.mark.integration
def test_qg_get_api_info(qg_manager):
    """Test getting API information from QueryGrid Manager."""
    result = qg_manager.api_info_client.get_api_info()

    # Verify response structure
    assert isinstance(result, dict), "API info should return a dictionary"
    assert "appVersion" in result, "API info should contain appVersion"
    assert "apiVersion" in result, "API info should contain apiVersion"
    assert "features" in result, "API info should contain features"

    # Verify types
    assert isinstance(result["appVersion"], str), "appVersion should be a string"
    assert isinstance(result["apiVersion"], int), "apiVersion should be an integer"
    assert isinstance(result["features"], dict), "features should be a dictionary"
