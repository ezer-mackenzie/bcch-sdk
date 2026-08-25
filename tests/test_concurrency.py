import asyncio
import threading
import time

import pytest

from bcch_sdk.concurrency import gather_async_tasks, run_in_threads


def test_run_in_threads_limits_concurrency() -> None:
    active = 0
    maximum = 0
    lock = threading.Lock()

    def task() -> int:
        nonlocal active, maximum
        with lock:
            active += 1
            maximum = max(maximum, active)
        time.sleep(0.01)
        with lock:
            active -= 1
        return 1

    assert run_in_threads([task] * 8, max_workers=3) == [1] * 8
    assert maximum == 3


@pytest.mark.asyncio
async def test_gather_async_tasks_limits_concurrency() -> None:
    active = 0
    maximum = 0

    async def task() -> int:
        nonlocal active, maximum
        active += 1
        maximum = max(maximum, active)
        await asyncio.sleep(0.01)
        active -= 1
        return 1

    assert (
        await gather_async_tasks([task() for _ in range(8)], max_concurrency=3)
        == [1] * 8
    )
    assert maximum == 3


@pytest.mark.asyncio
async def test_gather_async_tasks_rejects_invalid_limit() -> None:
    coroutine = asyncio.sleep(0, result=1)
    try:
        with pytest.raises(ValueError, match="greater than zero"):
            await gather_async_tasks([coroutine], max_concurrency=0)
    finally:
        coroutine.close()
