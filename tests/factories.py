from datetime import date, timedelta
from typing import Any

from bcch_sdk.models.observation_series import ObservationSeries
from bcch_sdk.models.series import Series
from bcch_sdk.models.series_information import SerieInformation
from bcch_sdk.models.web_service import WebServiceResponse
from bcch_sdk.types.auth import InternalCredentials
from bcch_sdk.types.enums import Frequency


DUMMY_CREDENTIALS: InternalCredentials = {
    "username": "test-user",
    "password": "test-password",
}


def build_series_response(
    *,
    series_id: str = "SF1",
    observations_count: int = 3,
) -> WebServiceResponse:
    base_date = date(2024, 1, 1)

    return WebServiceResponse(
        code=0,
        description="Success",
        series=Series(
            id=series_id,
            spanish_description="Test Series",
            english_description="Test Series",
            observations=[
                ObservationSeries(
                    index_date=base_date + timedelta(days=index),
                    value=float(index),
                    status_code="OK",
                )
                for index in range(observations_count)
            ],
        ),
        series_information=None,
    )


def build_search_response(*, items_count: int = 3) -> WebServiceResponse:
    base_date = date(2024, 1, 1)
    frequencies = list(Frequency)

    return WebServiceResponse(
        code=0,
        description="Success",
        series=None,
        series_information=[
            SerieInformation(
                id=f"SF{index}",
                frequency=frequencies[index % len(frequencies)],
                spanish_title=f"Test {index}",
                english_title=f"Test {index}",
                first_observation=base_date - timedelta(days=index + 30),
                last_observation=base_date - timedelta(days=index),
                updated_at=base_date,
                created_at=base_date - timedelta(days=365),
            )
            for index in range(items_count)
        ],
    )


def build_api_series_payload(*, series_id: str = "SF1") -> dict[str, Any]:
    return {
        "Codigo": 0,
        "Descripcion": "Success",
        "Series": {
            "seriesId": series_id,
            "descripEsp": "Test Series",
            "descripIng": "Test Series",
            "Obs": [
                {
                    "indexDateString": "01-01-2024",
                    "value": "10.5",
                    "statusCode": "OK",
                }
            ],
        },
        "SeriesInfos": [],
    }
