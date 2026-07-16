from abc import ABC
from abc import abstractmethod
from datetime import datetime, date

from typing import Sequence

import polars
import pandas

from ...types.enums import Frequency

from ...clients.async_client import BCChAsyncClient

from .sdk import BaseSDK

class BaseAsyncSDK(BaseSDK[BCChAsyncClient], ABC):
    @abstractmethod
    async def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: bool = True,
    ) -> Sequence[pandas.DataFrame | polars.DataFrame]: ...

    @abstractmethod
    async def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: bool = True,
    ) -> Sequence[pandas.DataFrame | polars.DataFrame]: ...
