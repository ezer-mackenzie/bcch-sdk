from typing import cast

from pytest_benchmark.fixture import BenchmarkFixture

import pytest
import polars
import pandas

from bcch_sdk.mappers.dataframe import DataFrameMapper

from tests.factories import build_search_response, build_series_response


@pytest.mark.benchmark
def test_dataframe_mapper_get_series_pandas(benchmark: BenchmarkFixture) -> None:
    response = build_series_response(observations_count=99)

    result = cast(
        pandas.DataFrame,
        benchmark(DataFrameMapper.get_series, response, polars_response=False),
    )
    assert len(result) == 99


@pytest.mark.benchmark
def test_dataframe_mapper_get_series_polars(benchmark: BenchmarkFixture) -> None:
    response = build_series_response(observations_count=99)

    result = cast(
        polars.DataFrame,
        benchmark(DataFrameMapper.get_series, response, polars_response=True),
    )
    assert len(result) == 99


@pytest.mark.benchmark
def test_dataframe_mapper_search_series_pandas(benchmark: BenchmarkFixture) -> None:
    response = build_search_response(items_count=50)

    result = cast(
        pandas.DataFrame,
        benchmark(DataFrameMapper.search_series, response, polars_response=False),
    )
    assert len(result) == 50


@pytest.mark.benchmark
def test_dataframe_mapper_search_series_polars(benchmark: BenchmarkFixture) -> None:
    response = build_search_response(items_count=50)

    result = cast(
        polars.DataFrame,
        benchmark(DataFrameMapper.search_series, response, polars_response=True),
    )
    assert len(result) == 50
