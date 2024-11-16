from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
from example_workflow import *

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="your-task-queue",
        workflows=[ExampleWorkflow],
        activities=[example_activity],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())