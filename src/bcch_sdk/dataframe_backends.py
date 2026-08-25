from importlib import import_module
from types import ModuleType

from .exceptions import MissingDataFrameDependencyException


def load_pandas() -> ModuleType:
    return _load_backend("pandas", "pandas")


def load_polars() -> ModuleType:
    return _load_backend("polars", "polars")


def _load_backend(module_name: str, extra_name: str) -> ModuleType:
    try:
        return import_module(module_name)
    except ImportError:
        raise MissingDataFrameDependencyException(
            f"The {module_name} backend is not installed. "
            f"Install it with 'pip install bcch-sdk[{extra_name}]'."
        ) from None
