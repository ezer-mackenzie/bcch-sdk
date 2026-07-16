from typing import cast

import pytest

from pytest_benchmark.fixture import BenchmarkFixture

from bcch_sdk.mappers.credentials import CredentialsMapper
from bcch_sdk.builders.parameters import ParameterBuilder

from bcch_sdk.types.auth import QueryCredentials
from bcch_sdk.types.parameters import GetSeriesParams

from tests.factories import DUMMY_CREDENTIALS


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
