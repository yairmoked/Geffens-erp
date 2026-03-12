import importlib.util


def test_project_package_namespace_exists() -> None:
    assert importlib.util.find_spec("geffens_erp") is not None
