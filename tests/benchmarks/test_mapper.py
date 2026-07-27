from typing import cast

import pytest

from pytest_benchmark.fixture import BenchmarkFixture

from bcch_sdk.mappers.credentials import CredentialsMapper
from bcch_sdk.mappers.web_service import WebServiceResponseMapper
from bcch_sdk.builders.parameters import ParameterBuilder
from bcch_sdk.dto.web_service import WebServiceResponseDTO
from bcch_sdk.models.web_service import WebServiceResponse

from bcch_sdk.types.auth import QueryCredentials
from bcch_sdk.types.parameters import GetSeriesParams

from tests.factories import DUMMY_CREDENTIALS, build_api_series_payload


@pytest.mark.benchmark
def test_credentials_mapper_performance(benchmark: BenchmarkFixture) -> None:
    mapper = CredentialsMapper()

    result = cast(
        QueryCredentials,
        benchmark(mapper.to_query_credentials, DUMMY_CREDENTIALS),
    )
    assert result["user"] == DUMMY_CREDENTIALS["username"]
    assert result["pass"] == DUMMY_CREDENTIALS["password"]


@pytest.mark.benchmark
def test_parameter_builder_performance(benchmark: BenchmarkFixture) -> None:
    result = cast(
        GetSeriesParams,
        benchmark(
            ParameterBuilder.build_get_series_params,
            DUMMY_CREDENTIALS,
            "SF43718",
            "2023-01-01",
            "2023-12-31",
        ),
    )
    assert result["timeseries"] == "SF43718"


@pytest.mark.benchmark
def test_web_service_response_mapper_performance(
    benchmark: BenchmarkFixture,
) -> None:
    payload = build_api_series_payload()
    observations = payload["Series"]["Obs"]
    payload["Series"]["Obs"] = observations * 10_000
    dto = WebServiceResponseDTO.model_validate(payload)

    result = benchmark(WebServiceResponseMapper.from_api_to_domain, dto)

    assert result.series is not None
    assert len(result.series.observations) == 10_000


@pytest.mark.benchmark
def test_direct_domain_model_performance(benchmark: BenchmarkFixture) -> None:
    payload = build_api_series_payload()
    observations = payload["Series"]["Obs"]
    payload["Series"]["Obs"] = observations * 10_000

    result = benchmark(WebServiceResponse.model_validate, payload)

    assert result.series is not None
    assert len(result.series.observations) == 10_000
