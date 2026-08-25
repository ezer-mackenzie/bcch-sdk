import pytest
from collections.abc import Callable
from types import ModuleType
from typing import NoReturn

import bcch_sdk.dataframe_backends as backends
from bcch_sdk.exceptions import MissingDataFrameDependencyException


@pytest.mark.parametrize(
    "loader, extra",
    [(backends.load_pandas, "pandas"), (backends.load_polars, "polars")],
)
def test_missing_dataframe_backend_has_actionable_error(
    monkeypatch: pytest.MonkeyPatch,
    loader: Callable[[], ModuleType],
    extra: str,
) -> None:
    def missing(_: str) -> NoReturn:
        raise ImportError

    monkeypatch.setattr(backends, "import_module", missing)
    with pytest.raises(
        MissingDataFrameDependencyException,
        match=rf"bcch-sdk\[{extra}\]",
    ):
        loader()


def test_dataframe_backends_load_when_installed() -> None:
    assert backends.load_pandas().__name__ == "pandas"
    assert backends.load_polars().__name__ == "polars"
