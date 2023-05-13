import asyncio
from typing import List


async def create_tasks(
        tasks: List[dict],
        task_queue: asyncio.Queue,
        producer_completed: asyncio.Event) -> None:
    """
    This function is responsible for producing tasks asynchronously and putting them into the task queue.
    :param tasks: the tasks to produce
    :param task_queue: the work queue to put the task into
    :param producer_completed: an event to signal that the producer is done producing tasks
    :return: None
    """
    for task in tasks:
        # We use an async queue here so that we are able to limit the size of the queue. This allows us to control
        # how many tasks are in the queue at any given time. This is useful if we want to limit the amount of memory
        # used by the queue, and so that the producer doesn't produce tasks faster than the consumer can consume them.
        # If the queue is full, the producer will wait until there is space in the queue before putting the task in.
        await task_queue.put(task)

    # Once we are done producing tasks, we set the event to signal that the producer is done.
    producer_completed.set()
