from collections.abc import Sequence
import asyncio
from datetime import date, datetime
from typing import Self, cast

import pandas
import polars
import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from bcch_sdk.clients.async_client import BCChAsyncClient
from bcch_sdk.clients.sync_client import BCChSyncClient
from bcch_sdk.models.web_service import WebServiceResponse
from bcch_sdk.sdk.async_sdk import BCChAsyncSDK
from bcch_sdk.sdk.sync_sdk import BCChSyncSDK
from bcch_sdk.types.config import BCChConfig
from bcch_sdk.types.enums import Frequency

from tests.factories import DUMMY_CREDENTIALS, build_series_response

SERIES = [
    "F022.TPM.TIN.D001.NO.Z.D",
    "F032.IMC.IND.Z.Z.EP18.Z.Z.0.M",
    "F032.PIB.FLU.R.CLP.2018.04.10.0.M",
    "F032.PIB.FLU.N.CLP.EP18.04.14.0.T",
    "F032.PIB.FLU.N.CLP.EP18.04.12.1.T",
]


class FakeSyncClient:
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
        return build_series_response(series_id=time_series, observations_count=2)

    def search_series(self, frequency: Frequency) -> WebServiceResponse:
        raise NotImplementedError


class FakeAsyncClient:
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
        return build_series_response(series_id=time_series, observations_count=2)

    async def search_series(self, frequency: Frequency) -> WebServiceResponse:
        raise NotImplementedError


class BenchmarkSyncSDK(BCChSyncSDK):
    def client(self) -> BCChSyncClient:
        return cast(BCChSyncClient, FakeSyncClient())


class BenchmarkAsyncSDK(BCChAsyncSDK):
    def client(self) -> BCChAsyncClient:
        return cast(BCChAsyncClient, FakeAsyncClient())


def create_config() -> BCChConfig:
    return BCChConfig(credentials=DUMMY_CREDENTIALS)


@pytest.mark.benchmark
def test_sync_sdk_polars(benchmark: BenchmarkFixture) -> None:
    sdk = BenchmarkSyncSDK(create_config())

    result = cast(
        Sequence[polars.DataFrame],
        benchmark(sdk.get_series, SERIES, "2024-01-01", "2024-01-02"),
    )

    assert len(result) == len(SERIES)
    assert all(isinstance(frame, polars.DataFrame) for frame in result)


@pytest.mark.benchmark
def test_sync_sdk_pandas(benchmark: BenchmarkFixture) -> None:
    sdk = BenchmarkSyncSDK(create_config())

    result = cast(
        Sequence[pandas.DataFrame],
        benchmark(
            sdk.get_series,
            SERIES,
            "2024-01-01",
            "2024-01-02",
            polars_response=False,
        ),
    )
    assert len(result) == len(SERIES)
    assert all(isinstance(frame, pandas.DataFrame) for frame in result)


@pytest.mark.benchmark
def test_async_sdk_polars(benchmark: BenchmarkFixture) -> None:
    sdk = BenchmarkAsyncSDK(create_config())

    async def get_series() -> Sequence[polars.DataFrame]:
        return await sdk.get_series(SERIES, "2024-01-01", "2024-01-02")

    result = cast(
        Sequence[polars.DataFrame], benchmark(lambda: asyncio.run(get_series()))
    )
    assert len(result) == len(SERIES)
    assert all(isinstance(frame, polars.DataFrame) for frame in result)


@pytest.mark.benchmark
def test_async_sdk_pandas(benchmark: BenchmarkFixture) -> None:
    sdk = BenchmarkAsyncSDK(create_config())

    async def get_series() -> Sequence[pandas.DataFrame]:
        return await sdk.get_series(
            SERIES,
            "2024-01-01",
            "2024-01-02",
            polars_response=False,
        )

    result = cast(
        Sequence[pandas.DataFrame], benchmark(lambda: asyncio.run(get_series()))
    )
    assert len(result) == len(SERIES)
    assert all(isinstance(frame, pandas.DataFrame) for frame in result)
