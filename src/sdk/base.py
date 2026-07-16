from abc import ABC
from abc import abstractmethod
from datetime import datetime, date

from httpx import Timeout
from typing import Generic, Sequence, Self

from dataclasses import dataclass

import polars
import pandas

from ..types.enums import Frequency
from ..types.core import ClientT
from ..types.config import BCChConfig

from ..clients.async_client import BCChAsyncClient
from ..clients.sync_client import BCChSyncClient


@dataclass(slots=True)
class BaseSDK(Generic[ClientT], ABC):
    configuration: BCChConfig | None = None

    @classmethod
    def from_credentials(
        cls,
        username: str,
        password: str,
        timeout: Timeout | None = None,
    ) -> Self:
        config = BCChConfig(
            credentials={"username": username, "password": password},
            timeout=timeout or Timeout(10.0),
        )
        return cls(configuration=config)

    @abstractmethod
    def client(self) -> ClientT: ...


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


class BaseSyncSDK(BaseSDK[BCChSyncClient]):
    @abstractmethod
    def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: bool = True,
    ) -> Sequence[pandas.DataFrame | polars.DataFrame]: ...

    @abstractmethod
    def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: bool = True,
    ) -> pandas.DataFrame | polars.DataFrame: ...
