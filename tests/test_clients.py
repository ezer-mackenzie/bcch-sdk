import json
import logging

import pytest
from httpx import AsyncClient, Client, ConnectError, MockTransport, Request, Response

from bcch_sdk.clients.async_client import BCChAsyncClient
from bcch_sdk.clients.sync_client import BCChSyncClient
from bcch_sdk.exceptions import (
    InvalidCredentialsException,
    InvalidDateException,
    InvalidFrequencyException,
    InvalidSeriesException,
    ResponseParseException,
    TransportException,
    WebServiceResponseException,
)
from bcch_sdk.types.enums import Frequency

from tests.factories import DUMMY_CREDENTIALS, build_api_series_payload


def json_response(payload: dict[str, object], status_code: int = 200) -> Response:
    return Response(
        status_code,
        content=json.dumps(payload).encode("iso-8859-1"),
        headers={"content-type": "application/json; charset=iso-8859-1"},
    )


def sync_client_for(response: Response) -> BCChSyncClient:
    transport = MockTransport(lambda _: response)
    return BCChSyncClient(
        credentials=DUMMY_CREDENTIALS,
        session=Client(transport=transport),
    )


def async_client_for(response: Response) -> BCChAsyncClient:
    transport = MockTransport(lambda _: response)
    return BCChAsyncClient(
        credentials=DUMMY_CREDENTIALS,
        session=AsyncClient(transport=transport),
    )


def search_payload(code: int = 0) -> dict[str, object]:
    return {
        "Codigo": code,
        "Descripcion": "Success",
        "SeriesInfos": [
            {
                "seriesId": "SF1",
                "frequencyCode": "DAILY",
                "spanishTitle": "Serie de prueba",
                "englishTitle": "Test series",
                "firstObservation": "01-01-2024",
                "lastObservation": "02-01-2024",
                "updatedAt": "03-01-2024",
                "createdAt": "01-01-2023",
            }
        ],
    }


def test_sync_client_get_series_returns_domain_response() -> None:
    client = sync_client_for(json_response(build_api_series_payload(series_id="SF1")))

    result = client.get_series("SF1")

    assert result.series is not None
    assert result.series.id == "SF1"


def test_sync_client_get_series_maps_invalid_series_code() -> None:
    payload = build_api_series_payload(series_id="SF1")
    payload["Codigo"] = -50
    client = sync_client_for(json_response(payload))

    with pytest.raises(InvalidSeriesException):
        client.get_series("INVALID")


def test_sync_client_get_series_maps_invalid_date_code() -> None:
    payload = build_api_series_payload(series_id="SF1")
    payload["Codigo"] = -1
    client = sync_client_for(json_response(payload))

    with pytest.raises(InvalidDateException):
        client.get_series("SF1", first_date="2024-01-01")


def test_sync_client_search_series_maps_invalid_credentials_code() -> None:
    client = sync_client_for(json_response(search_payload(code=-5)))

    with pytest.raises(InvalidCredentialsException):
        client.search_series(Frequency.DAILY)


def test_sync_client_search_series_maps_invalid_frequency_code() -> None:
    client = sync_client_for(json_response(search_payload(code=-1)))

    with pytest.raises(InvalidFrequencyException):
        client.search_series(Frequency.DAILY)


def test_sync_client_maps_http_status_errors() -> None:
    client = sync_client_for(json_response({"error": "unavailable"}, status_code=503))

    with pytest.raises(WebServiceResponseException):
        client.get_series("SF1")


def test_sync_client_rejects_unknown_api_error() -> None:
    payload = build_api_series_payload()
    payload["Codigo"] = -999
    client = sync_client_for(json_response(payload))

    with pytest.raises(WebServiceResponseException, match="-999"):
        client.get_series("SF1")


@pytest.mark.parametrize(
    "response",
    [
        Response(200, text="not-json"),
        json_response({"unexpected": "schema"}),
    ],
)
def test_sync_client_maps_invalid_payloads(response: Response) -> None:
    with pytest.raises(ResponseParseException):
        sync_client_for(response).get_series("SF1")


def test_sync_client_maps_transport_errors() -> None:
    def fail(request: Request) -> Response:
        raise ConnectError("offline", request=request)

    client = BCChSyncClient(
        credentials=DUMMY_CREDENTIALS,
        session=Client(transport=MockTransport(fail)),
    )
    with pytest.raises(TransportException):
        client.get_series("SF1")


def test_sync_client_does_not_close_injected_session() -> None:
    session = Client(transport=MockTransport(lambda _: json_response(search_payload())))
    client = BCChSyncClient(credentials=DUMMY_CREDENTIALS, session=session)

    with client:
        pass

    assert not session.is_closed
    session.close()


def test_sync_client_reopens_owned_session() -> None:
    client = BCChSyncClient(credentials=DUMMY_CREDENTIALS)
    with client:
        assert client.session is not None
    assert client.session is None
    with client:
        assert client.session is not None
    assert client.session is None


def test_sync_client_never_logs_credentials(caplog: pytest.LogCaptureFixture) -> None:
    client = sync_client_for(json_response(build_api_series_payload()))
    with caplog.at_level(logging.DEBUG):
        client.get_series("SF1")
    sdk_logs = "\n".join(
        record.getMessage()
        for record in caplog.records
        if record.name.startswith("bcch_sdk")
    )
    assert DUMMY_CREDENTIALS["username"] not in sdk_logs
    assert DUMMY_CREDENTIALS["password"] not in sdk_logs


@pytest.mark.asyncio
async def test_async_client_get_series_returns_domain_response() -> None:
    client = async_client_for(json_response(build_api_series_payload(series_id="SF1")))

    result = await client.get_series("SF1")

    assert result.series is not None
    assert result.series.id == "SF1"


@pytest.mark.asyncio
async def test_async_client_search_series_returns_domain_response() -> None:
    client = async_client_for(json_response(search_payload()))

    result = await client.search_series(Frequency.DAILY)

    assert result.series_information is not None
    assert result.series_information[0].id == "SF1"


@pytest.mark.asyncio
async def test_async_client_search_series_maps_invalid_credentials_code() -> None:
    client = async_client_for(json_response(search_payload(code=-5)))

    with pytest.raises(InvalidCredentialsException):
        await client.search_series(Frequency.DAILY)


@pytest.mark.asyncio
async def test_async_client_maps_http_status_errors() -> None:
    client = async_client_for(json_response({"error": "unavailable"}, status_code=503))

    with pytest.raises(WebServiceResponseException):
        await client.get_series("SF1")


@pytest.mark.asyncio
async def test_async_client_maps_invalid_series_and_date_codes() -> None:
    for code, exception in [(-50, InvalidSeriesException), (-1, InvalidDateException)]:
        payload = build_api_series_payload()
        payload["Codigo"] = code
        with pytest.raises(exception):
            await async_client_for(json_response(payload)).get_series("SF1")


@pytest.mark.asyncio
async def test_async_client_maps_invalid_frequency_code() -> None:
    with pytest.raises(InvalidFrequencyException):
        await async_client_for(json_response(search_payload(code=-1))).search_series(
            Frequency.DAILY
        )


@pytest.mark.asyncio
async def test_async_client_maps_transport_errors() -> None:
    async def fail(request: Request) -> Response:
        raise ConnectError("offline", request=request)

    client = BCChAsyncClient(
        credentials=DUMMY_CREDENTIALS,
        session=AsyncClient(transport=MockTransport(fail)),
    )
    with pytest.raises(TransportException):
        await client.get_series("SF1")


@pytest.mark.asyncio
async def test_async_client_does_not_close_injected_session() -> None:
    session = AsyncClient(
        transport=MockTransport(lambda _: json_response(search_payload()))
    )
    client = BCChAsyncClient(credentials=DUMMY_CREDENTIALS, session=session)
    async with client:
        pass
    assert not session.is_closed
    await session.aclose()


@pytest.mark.asyncio
async def test_async_client_reopens_owned_session() -> None:
    client = BCChAsyncClient(credentials=DUMMY_CREDENTIALS)
    async with client:
        assert client.session is not None
    assert client.session is None
    async with client:
        assert client.session is not None
    assert client.session is None
