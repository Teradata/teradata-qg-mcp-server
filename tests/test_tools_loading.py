import importlib
import pkgutil

import pytest

import tools


@pytest.mark.unit
def test_import_all_tool_modules():
    """Ensure all modules under `tools` can be imported without errors.

    This helps catch syntax errors and missing dependencies introduced by
    refactors or merges.
    """
    failures = []
    for finder, name, ispkg in pkgutil.iter_modules(tools.__path__):
        module_name = f"tools.{name}"
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            failures.append((module_name, exc))

    if failures:
        msgs = [f"{m}: {e!r}" for m, e in failures]
        raise AssertionError("Failed to import some tool modules:\n" + "\n".join(msgs))

    # Also ensure the tools package exposes the expected accessors
    assert hasattr(tools, "get_qg_manager")
    assert hasattr(tools, "set_qg_manager")
