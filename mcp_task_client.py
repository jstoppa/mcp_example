from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python", 
    args=["mcp_task_server.py"], 
)

def get_tasks_from_content(content):
    try:
        # Extract tasks data from nested JSON response
        content_item = content.contents[0]
        outer_json = json.loads(content_item.text)
        inner_json = json.loads(outer_json['contents'][0]['text'])
        return inner_json
    except Exception as e:
        print(f"Error parsing tasks: {e}")
        return None

def display_tasks(tasks):
    if not tasks or 'tasks' not in tasks:
        print("No tasks found")
        return
        
    for task in tasks['tasks']:
        print(f"• {task['title']}")
        print(f"  {task['description']}")
    print(f"\nTotal tasks: {tasks['count']}")

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✓ Connected to server")

            # Show current tasks
            print("\nCurrent Tasks\n" + "=" * 30)
            tasks = get_tasks_from_content(await session.read_resource("tasks://list"))
            display_tasks(tasks)

            # Add a new task
            print("\nAdding New Task\n" + "=" * 30)
            await session.call_tool("add_task", {
                "params": {
                    "task_title": "Order food",
                    "description": "Order lunch from the local restaurant"
                }
            })
            print("✓ Task added successfully")

            # Show updated task list
            print("\nUpdated Tasks\n" + "=" * 30)
            tasks = get_tasks_from_content(await session.read_resource("tasks://list"))
            display_tasks(tasks)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())