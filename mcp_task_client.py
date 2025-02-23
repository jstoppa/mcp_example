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
        if isinstance(content, tuple) and len(content) == 2:
            meta, contents = content
            if isinstance(contents, list) and len(contents) > 0:
                content_item = contents[0]
                if hasattr(content_item, 'text'):
                    return json.loads(content_item.text)
        return None
    except Exception as e:
        print(f"Error parsing tasks: {e}")
        return None

def print_section(title):
    print(f"\n{title}")
    print("=" * 30)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✓ Connected to server")

            # Show current tasks
            print_section("Current Tasks")
            content, _ = await session.read_resource("tasks://list")
            tasks = get_tasks_from_content(content)
            if tasks and 'tasks' in tasks:
                for task in tasks['tasks']:
                    print(f"• {task['title']}")
                    print(f"  {task['description']}")
                print(f"\nTotal tasks: {tasks['count']}")
            else:
                print("No tasks found")

            # Add a new task
            print_section("Adding New Task")
            new_task = await session.call_tool("add_task", {
                "params": {
                    "task_title": "Order food",
                    "description": "Order lunch from the local restaurant"
                }
            })
            print("✓ Task added successfully")

            # Show updated task list
            print_section("Updated Tasks")
            content, _ = await session.read_resource("tasks://list")
            tasks = get_tasks_from_content(content)
            if tasks and 'tasks' in tasks:
                for task in tasks['tasks']:
                    print(f"• {task['title']}")
                    print(f"  {task['description']}")
                print(f"\nTotal tasks: {tasks['count']}")
            else:
                print("No tasks found")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())