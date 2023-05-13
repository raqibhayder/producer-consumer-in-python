import asyncio
from typing import Callable


async def handle_task_result(result_queue: asyncio.Queue, callback: Callable[[dict], None]) -> None:
    """
    This function is responsible for pulling tasks from the result queue and calling the callback function with the
    result.
    :param result_queue: the queue to pull results from
    :param callback: the callback function to call with the result
    :return: None
    """

    while True:
        result = await result_queue.get()
        callback(result)
        result_queue.task_done()
