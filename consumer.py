import asyncio
from random import random
from time import perf_counter


async def find_number_squared(number: int) -> int:
    """
    This function is responsible for finding the square of a number.
    :param number: the number to find the square of
    :return: the square of the number
    """
    await asyncio.sleep(random() * 2)
    return number ** 2


async def process_task(
        task_queue: asyncio.Queue,
        results_queue: asyncio.Queue) -> None:
    """
    This function is responsible for processing tasks asynchronously. It takes tasks from the task queue, processes
    them, and puts the results into the results queue.
    :param task_queue: the queue to get tasks from
    :param results_queue: the queue to put results into
    :return: None
    """
    # This is an infinite loop that will keep running until the program is terminated. This is because we want the
    # consumer to keep processing tasks until there are no more tasks to process.
    while True:
        # We pull a task from the task queue. If there are no tasks in the queue, the consumer will wait until there
        # is a task in the queue before pulling it out.
        task = await task_queue.get()

        task_id, number = task['task_id'], task['number']

        # print(f"Processing task {task_id}")

        start = perf_counter()
        # We do some work here. In this case, we are just finding the square of the number in the task. This is a
        # blocking operation, so we use await to wait for the result.
        result = await find_number_squared(number)
        end = perf_counter()

        # print(f"Task {task_id} completed in {end - start:.2f}s")

        # We put the result in to the results queue.
        await results_queue.put(
            {
                "task_id": task_id,
                "result": result,
                "duration": end - start
            }
        )

        # We tell the task queue that we are done processing the task. This is important because it allows the task
        # queue to know that it can put another task into the queue if it is full.
        task_queue.task_done()
