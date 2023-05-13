# Producer Consumer model in Python using Asyncio

In the producer-consumer model, a **producer** pushes tasks to the **queue** and the **consumer** monitors the queue 
for new tasks. When a new task is available, the consumer pulls the task from the queue and executes it until the queue
is empty. Usually, we have many producers submitting tasks to the queue and many consumers monitoring the queue for new 
tasks.
