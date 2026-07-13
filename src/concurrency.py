from collections.abc import Callable, Coroutine, Sequence

from concurrent.futures import ThreadPoolExecutor

from typing import TypeVar

import logging
import asyncio

ResultT = TypeVar("ResultT")
logger = logging.getLogger(__name__)


def run_in_threads(
    tasks: Sequence[Callable[[], ResultT]],
    max_workers: int | None = None,
) -> list[ResultT]:
    """Run a collection of callables concurrently in threads."""
    logger.debug("Executing %s threaded tasks", len(tasks))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task) for task in tasks]
        return [future.result() for future in futures]


async def gather_async_tasks(
    tasks: Sequence[Coroutine[None, None, ResultT]],
) -> list[ResultT]:
    """Gather multiple async tasks and return their results."""
    logger.debug("Gathering %s async tasks", len(tasks))
    return await asyncio.gather(*tasks)
