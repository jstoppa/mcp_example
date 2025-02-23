from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json, asyncio

async def run():
    # Connect to the task server
    async with stdio_client(StdioServerParameters(command="python", args=["mcp_task_server.py"])) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Get task description suggestion using prompt
            prompt_result = await session.get_prompt("task_description", {"task_title": "Do shopping"})
            print(f"\nSuggested description: {prompt_result.messages[0].content.text}")
            
            # Display all tasks
            response = await session.read_resource("tasks://list")
            tasks = json.loads(json.loads(response.contents[0].text)['contents'][0]['text'])
            for task in tasks['tasks']:
                print(f"• {task['title']}: {task['description']}")
            
            # Add a new task
            await session.call_tool("add_task", {
                "params": {
                    "task_title": "Order food",
                    "description": "Order lunch from the local restaurant"
                }
            })

            # Display again all tasks
            response = await session.read_resource("tasks://list")
            tasks = json.loads(json.loads(response.contents[0].text)['contents'][0]['text'])
            for task in tasks['tasks']:
                print(f"• {task['title']}: {task['description']}")

if __name__ == "__main__":
    asyncio.run(run())