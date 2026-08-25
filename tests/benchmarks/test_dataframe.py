from typing import cast

from pytest_benchmark.fixture import BenchmarkFixture

import pytest
import polars
import pandas

from bcch_sdk.mappers.dataframe import DataFrameMapper

from tests.factories import build_search_response, build_series_response


@pytest.mark.benchmark
@pytest.mark.parametrize("rows", [100, 10_000])
def test_dataframe_mapper_get_series_pandas(
    benchmark: BenchmarkFixture, rows: int
) -> None:
    response = build_series_response(observations_count=rows)

    result = cast(
        pandas.DataFrame,
        benchmark(DataFrameMapper.get_series, response, polars_response=False),
    )
    assert len(result) == rows


@pytest.mark.benchmark
@pytest.mark.parametrize("rows", [100, 10_000])
def test_dataframe_mapper_get_series_polars(
    benchmark: BenchmarkFixture, rows: int
) -> None:
    response = build_series_response(observations_count=rows)

    result = cast(
        polars.DataFrame,
        benchmark(DataFrameMapper.get_series, response, polars_response=True),
    )
    assert len(result) == rows


@pytest.mark.benchmark
@pytest.mark.parametrize("rows", [100, 10_000])
def test_dataframe_mapper_search_series_pandas(
    benchmark: BenchmarkFixture, rows: int
) -> None:
    response = build_search_response(items_count=rows)

    result = cast(
        pandas.DataFrame,
        benchmark(DataFrameMapper.search_series, response, polars_response=False),
    )
    assert len(result) == rows


@pytest.mark.benchmark
@pytest.mark.parametrize("rows", [100, 10_000])
def test_dataframe_mapper_search_series_polars(
    benchmark: BenchmarkFixture, rows: int
) -> None:
    response = build_search_response(items_count=rows)

    result = cast(
        polars.DataFrame,
        benchmark(DataFrameMapper.search_series, response, polars_response=True),
    )
    assert len(result) == rows
