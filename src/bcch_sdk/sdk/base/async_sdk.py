from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from datetime import datetime, date

from typing import TYPE_CHECKING, Literal, Sequence, overload

if TYPE_CHECKING:
    import pandas
    import polars

from ...types.enums import Frequency

from ...clients.async_client import BCChAsyncClient

from .sdk import BaseSDK


class BaseAsyncSDK(BaseSDK[BCChAsyncClient], ABC):
    @overload
    async def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: Literal[True] = True,
    ) -> Sequence[polars.DataFrame]: ...

    @overload
    async def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: Literal[False],
    ) -> Sequence[pandas.DataFrame]: ...

    @abstractmethod
    async def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: bool = True,
    ) -> Sequence[pandas.DataFrame | polars.DataFrame]: ...

    @overload
    async def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: Literal[True] = True,
    ) -> polars.DataFrame: ...

    @overload
    async def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: Literal[False],
    ) -> pandas.DataFrame: ...

    @abstractmethod
    async def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: bool = True,
    ) -> pandas.DataFrame | polars.DataFrame: ...
