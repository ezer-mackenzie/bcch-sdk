import multiprocessing
import resource
import sys
from collections.abc import Callable
from multiprocessing.queues import Queue
from typing import Any

import pytest

from bcch_sdk.mappers.dataframe import DataFrameMapper
from tests.factories import build_search_response, build_series_response

ROWS = 10_000
MAX_PEAK_MIB = 1024


def _measure_peak_rss(case: str, queue: Queue[tuple[int, float]]) -> None:
    operations: dict[str, Callable[[], Any]] = {
        "get-pandas": lambda: DataFrameMapper.get_series(
            build_series_response(observations_count=ROWS),
            polars_response=False,
        ),
        "get-polars": lambda: DataFrameMapper.get_series(
            build_series_response(observations_count=ROWS)
        ),
        "search-pandas": lambda: DataFrameMapper.search_series(
            build_search_response(items_count=ROWS),
            polars_response=False,
        ),
        "search-polars": lambda: DataFrameMapper.search_series(
            build_search_response(items_count=ROWS)
        ),
    }
    result = operations[case]()
    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mib = max_rss / (1024 * 1024 if sys.platform == "darwin" else 1024)
    queue.put((len(result), peak_mib))


@pytest.mark.benchmark
@pytest.mark.parametrize(
    "case",
    ["get-pandas", "get-polars", "search-pandas", "search-polars"],
)
def test_native_peak_memory_in_isolated_process(case: str) -> None:
    context = multiprocessing.get_context("spawn")
    queue: Queue[tuple[int, float]] = context.Queue()
    process = context.Process(target=_measure_peak_rss, args=(case, queue))
    process.start()
    process.join(timeout=30)

    assert process.exitcode == 0
    rows, peak_mib = queue.get(timeout=1)
    print(f"{case}: native peak RSS {peak_mib:.2f} MiB")
    assert rows == ROWS
    assert peak_mib < MAX_PEAK_MIB
