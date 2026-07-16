import tracemalloc

import pytest

from src.mappers.dataframe import DataFrameMapper

from tests.factories import build_search_response, build_series_response


@pytest.mark.benchmark
def test_memory_usage_large_get_series_pandas() -> None:
    tracemalloc.start()

    response = build_series_response(observations_count=10000)

    df = DataFrameMapper.get_series(response, polars_response=False)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Memory usage: {current / 10**6:.2f} MB")
    print(f"Peak memory: {peak / 10**6:.2f} MB")
    assert len(df) == 10000


@pytest.mark.benchmark
def test_memory_usage_large_get_series_polars() -> None:
    tracemalloc.start()

    response = build_series_response(observations_count=10000)

    df = DataFrameMapper.get_series(response)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Polars Get Series - Memory usage: {current / 10**6:.2f} MB")
    print(f"Polars Get Series - Peak memory: {peak / 10**6:.2f} MB")
    assert len(df) == 10000


@pytest.mark.benchmark
def test_memory_usage_large_search_series_pandas() -> None:
    tracemalloc.start()

    response = build_search_response(items_count=10000)

    df = DataFrameMapper.search_series(response, polars_response=False)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Pandas Search Series - Memory usage: {current / 10**6:.2f} MB")
    print(f"Pandas Search Series - Peak memory: {peak / 10**6:.2f} MB")
    assert len(df) == 10000


@pytest.mark.benchmark
def test_memory_usage_large_search_series_polars() -> None:
    tracemalloc.start()

    response = build_search_response(items_count=10000)

    df = DataFrameMapper.search_series(response)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Polars Search Series - Memory usage: {current / 10**6:.2f} MB")
    print(f"Polars Search Series - Peak memory: {peak / 10**6:.2f} MB")
    assert len(df) == 10000
