import pytest
from fastapi.testclient import TestClient
import types

# Import from src package
from src.server import app


class DummyQGManager:
    def __init__(self, reachable: bool = True) -> None:
        self.reachable: bool = reachable
        api_info = {"version": "1.2.3"}
        self.api_info_client = types.SimpleNamespace(get_api_info=lambda: api_info)

    def is_reachable(self):
        return self.reachable


@pytest.fixture(autouse=True)
def inject_dummy_qg_manager(monkeypatch):
    # Use central setter to inject qg_manager for tests
    from src import tools

    prev_manager = tools.get_qg_manager()  # Save previous manager
    dummy = DummyQGManager(reachable=True)
    tools.set_qg_manager(dummy)
    yield
    # Restore previous manager to avoid test leakage
    tools.set_qg_manager(prev_manager)


@pytest.mark.unit
def test_health_ok():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("querygrid") == "ok"
