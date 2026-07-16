from collections.abc import Sequence
from datetime import date, datetime
from typing import Self, cast

import pandas
import polars
import pytest

from src.clients.async_client import BCChAsyncClient
from src.clients.sync_client import BCChSyncClient
from src.exceptions import InvalidConfigurationException, InvalidSeriesException
from src.models.web_service import WebServiceResponse
from src.sdk.async_sdk import BCChAsyncSDK
from src.sdk.sync_sdk import BCChSyncSDK
from src.types.config import BCChConfig
from src.types.enums import Frequency

from tests.factories import (
    DUMMY_CREDENTIALS,
    build_search_response,
    build_series_response,
)


class FakeSyncClient:
    def __init__(self, responses: list[WebServiceResponse] | None = None) -> None:
        self.responses = responses or []
        self.requested_series: list[str] = []

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        return None

    def get_series(
        self,
        time_series: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ) -> WebServiceResponse:
        self.requested_series.append(time_series)
        if self.responses:
            return self.responses.pop(0)
        return build_series_response(series_id=time_series, observations_count=1)

    def search_series(self, frequency: Frequency) -> WebServiceResponse:
        return build_search_response(items_count=2)


class FakeAsyncClient:
    def __init__(self, responses: list[WebServiceResponse] | None = None) -> None:
        self.responses = responses or []

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        return None

    async def get_series(
        self,
        time_series: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ) -> WebServiceResponse:
        if self.responses:
            return self.responses.pop(0)
        return build_series_response(series_id=time_series, observations_count=1)

    async def search_series(self, frequency: Frequency) -> WebServiceResponse:
        return build_search_response(items_count=2)


class FakeSyncSDK(BCChSyncSDK):
    def __init__(self, client: FakeSyncClient | None = None) -> None:
        super().__init__(BCChConfig(credentials=DUMMY_CREDENTIALS))
        self.fake_client = client or FakeSyncClient()

    def client(self) -> BCChSyncClient:
        return cast(BCChSyncClient, self.fake_client)


class FakeAsyncSDK(BCChAsyncSDK):
    def __init__(self, client: FakeAsyncClient | None = None) -> None:
        super().__init__(BCChConfig(credentials=DUMMY_CREDENTIALS))
        self.fake_client = client or FakeAsyncClient()

    def client(self) -> BCChAsyncClient:
        return cast(BCChAsyncClient, self.fake_client)


def test_sync_sdk_get_series_returns_polars_frames() -> None:
    sdk = FakeSyncSDK()

    result = sdk.get_series(["SF1", "SF2"])

    assert len(result) == 2
    assert all(isinstance(frame, polars.DataFrame) for frame in result)


def test_sync_sdk_get_series_returns_pandas_frames() -> None:
    sdk = FakeSyncSDK()

    result = sdk.get_series(["SF1", "SF2"], polars_response=False)

    assert len(result) == 2
    assert all(isinstance(frame, pandas.DataFrame) for frame in result)


def test_sync_sdk_search_series_returns_dataframe() -> None:
    sdk = FakeSyncSDK()

    result = sdk.search_series(Frequency.DAILY)

    assert isinstance(result, polars.DataFrame)
    assert result.height == 2


def test_sync_sdk_without_configuration_raises() -> None:
    sdk = BCChSyncSDK(configuration=None)

    with pytest.raises(InvalidConfigurationException):
        sdk.client()


def test_sync_sdk_empty_series_input_raises() -> None:
    sdk = FakeSyncSDK()

    with pytest.raises(InvalidSeriesException):
        sdk.get_series([])


@pytest.mark.asyncio
async def test_async_sdk_get_series_returns_polars_frames() -> None:
    sdk = FakeAsyncSDK()

    result = await sdk.get_series(["SF1", "SF2"])

    assert len(result) == 2
    assert all(isinstance(frame, polars.DataFrame) for frame in result)


@pytest.mark.asyncio
async def test_async_sdk_get_series_returns_pandas_frames() -> None:
    sdk = FakeAsyncSDK()

    result = cast(
        Sequence[pandas.DataFrame],
        await sdk.get_series(["SF1", "SF2"], polars_response=False),
    )

    assert len(result) == 2
    assert all(isinstance(frame, pandas.DataFrame) for frame in result)


@pytest.mark.asyncio
async def test_async_sdk_search_series_returns_dataframe() -> None:
    sdk = FakeAsyncSDK()

    result = await sdk.search_series(Frequency.DAILY)

    assert isinstance(result, polars.DataFrame)
    assert result.height == 2


@pytest.mark.asyncio
async def test_async_sdk_without_configuration_raises() -> None:
    sdk = BCChAsyncSDK(configuration=None)

    with pytest.raises(InvalidConfigurationException):
        sdk.client()


@pytest.mark.asyncio
async def test_async_sdk_empty_series_input_raises() -> None:
    sdk = FakeAsyncSDK()

    with pytest.raises(InvalidSeriesException):
        await sdk.get_series([])
