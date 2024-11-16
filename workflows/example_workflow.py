from temporalio import workflow, activity
from datetime import timedelta
from dataclasses import dataclass
from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
from datetime import datetime

@dataclass
class ExampleParams:
    greeting: str
    name: str

@activity.defn(name="example_activity")
async def example_activity(input: ExampleParams) -> str:
    return f"{input.greeting}, {input.name}!"

@workflow.defn(name="ExampleWorkflow")
class ExampleWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        print("Running")
        return await workflow.execute_activity(
            example_activity,
            ExampleParams("Hello", name),
            schedule_to_close_timeout=timedelta(seconds=2),
        )
    
async def main():
    client = await Client.connect("localhost:7233")
    result = await client.execute_workflow(
        ExampleWorkflow.run,
        "test-workflow",
        id=f"your-workflow-id:{datetime.now().strftime('%Y-%m-%d:%H-%M-%S')}",
        task_queue="your-task-queue",
    )
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())