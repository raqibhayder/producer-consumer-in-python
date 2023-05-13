import asyncio
from time import perf_counter
from typing import List, Callable

import consumer
import producer
import result_handler

NUM_WORKERS = 5
TASK_QUEUE_MAX_SIZE = 50

NUM_RESULT_HANDLERS = 5
RESULT_QUEUE_MAX_SIZE = 20


def run_job(
        tasks: List[dict], task_completed_callback:
        Callable[[dict], None],
        job_completed_callback: Callable[[dict], None]) -> None:
    """
    This function is responsible for running a job. It will create the task queue, result queue, and start the workers
    and result handlers. This is not an asynchronous function because we want to wait for the job to finish before
    returning.
    :param tasks: 
    :param task_completed_callback: 
    :param job_completed_callback: 
    :return: 
    """
    async def controller():
        start = perf_counter()

        task_queue = asyncio.Queue(maxsize=TASK_QUEUE_MAX_SIZE)
        result_queue = asyncio.Queue(maxsize=RESULT_QUEUE_MAX_SIZE)

        workers = []

        # We need to know when the producer is done producing tasks
        producer_completed = asyncio.Event()
        # Initially we set the event to false because the producer hasn't started producing tasks yet.
        producer_completed.clear()

        workers.append(
            asyncio.create_task(producer.create_tasks(tasks, task_queue, producer_completed))
        )

        for _ in range(NUM_WORKERS):
            workers.append(
                asyncio.create_task(consumer.process_task(task_queue, result_queue))
            )

        for _ in range(NUM_RESULT_HANDLERS):
            workers.append(
                asyncio.create_task(result_handler.handle_task_result(result_queue, task_completed_callback))
            )

        # We wait for the producer to finish producing tasks before we start the result handlers.
        await producer_completed.wait()

        await task_queue.join()
        await result_queue.join()

        for worker in workers:
            worker.cancel()

        end = perf_counter()
        job_completed_callback({"duration": end - start})

    asyncio.run(controller())
