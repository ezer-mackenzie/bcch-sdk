import json
import asyncio
from typing import cast

from httpx import AsyncClient, Client, MockTransport, Request, Response
import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from bcch_sdk.clients.async_client import BCChAsyncClient
from bcch_sdk.clients.sync_client import BCChSyncClient
from bcch_sdk.models.web_service import WebServiceResponse

from tests.factories import DUMMY_CREDENTIALS, build_api_series_payload


def build_response(_: Request) -> Response:
    return Response(
        200,
        content=json.dumps(build_api_series_payload()).encode("iso-8859-1"),
        headers={"content-type": "application/json; charset=iso-8859-1"},
    )


@pytest.mark.benchmark
def test_sync_client_request_performance(benchmark: BenchmarkFixture) -> None:
    transport = MockTransport(build_response)
    client = BCChSyncClient(
        credentials=DUMMY_CREDENTIALS,
        session=Client(transport=transport),
    )

    with client:
        result = cast(WebServiceResponse, benchmark(client.get_series, "SF1"))

    assert result.series is not None
    assert result.series.id == "SF1"


@pytest.mark.benchmark
def test_async_client_request_performance(benchmark: BenchmarkFixture) -> None:
    transport = MockTransport(build_response)

    async def get_series() -> WebServiceResponse:
        client = BCChAsyncClient(
            credentials=DUMMY_CREDENTIALS,
            session=AsyncClient(transport=transport),
        )
        async with client:
            return await client.get_series("SF1")

    result = cast(WebServiceResponse, benchmark(lambda: asyncio.run(get_series())))

    assert result.series is not None
    assert result.series.id == "SF1"
