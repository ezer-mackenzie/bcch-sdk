from bcch_sdk.dto.web_service import WebServiceResponseDTO
from bcch_sdk.mappers.web_service import WebServiceResponseMapper


def test_web_service_response_dto_allows_series_only_payloads() -> None:
    dto = WebServiceResponseDTO.model_validate(
        {
            "Codigo": 0,
            "Descripcion": "Success",
            "Series": {
                "seriesId": "SF1",
                "descripEsp": "Serie de prueba",
                "descripIng": "Test series",
                "Obs": [
                    {
                        "indexDateString": "01-01-2024",
                        "value": "10.5",
                        "statusCode": "OK",
                    }
                ],
            },
        }
    )

    response = WebServiceResponseMapper.from_api_to_domain(dto)

    assert response.series is not None
    assert response.series.id == "SF1"
    assert response.series_information is None


def test_web_service_response_dto_allows_search_only_payloads() -> None:
    dto = WebServiceResponseDTO.model_validate(
        {
            "Codigo": 0,
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
    )

    response = WebServiceResponseMapper.from_api_to_domain(dto)

    assert response.series is None
    assert response.series_information is not None
    assert response.series_information[0].id == "SF1"
