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
        # First level: Get the contents array from the ReadResourceResult
        if not hasattr(content, 'contents') or not content.contents:
            print("No contents found in response")
            return None
            
        # Get the first content item which contains our text
        content_item = content.contents[0]
        if not hasattr(content_item, 'text'):
            print("Content item does not have text")
            return None
            
        # First JSON parse: Parse the outer JSON structure
        outer_json = json.loads(content_item.text)
        if not isinstance(outer_json, dict) or 'contents' not in outer_json:
            print("Invalid outer JSON structure")
            return None
            
        # Get the inner content item
        inner_contents = outer_json['contents']
        if not isinstance(inner_contents, list) or not inner_contents:
            print("No inner contents found")
            return None
            
        inner_content = inner_contents[0]
        if 'text' not in inner_content:
            print("Inner content does not have text")
            return None
            
        # Second JSON parse: Parse the actual tasks data
        return json.loads(inner_content['text'])
    except Exception as e:
        print(f"Error parsing tasks: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
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
            response = await session.read_resource("tasks://list")
            tasks = get_tasks_from_content(response)  # Pass the response directly
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
            response = await session.read_resource("tasks://list")
            tasks = get_tasks_from_content(response)  # Pass the response directly
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