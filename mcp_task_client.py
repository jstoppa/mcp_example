from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python", 
    args=["mcp_task_server.py"], 
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            print("✓ Connected to server successfully!")
            print("\n" + "="*50 + "\n")

            # List available prompts
            prompts = await session.list_prompts()
            print("Available prompts:")
            if hasattr(prompts, 'prompts'):
                for prompt in prompts.prompts:
                    print(f"- {prompt.name}")
            print("\n" + "="*50 + "\n")

            # Get a prompt
            prompt = await session.get_prompt("task_description", {"task_title": "Plan lunch"})
            print("Task Description Prompt:")
            if hasattr(prompt, 'messages'):
                for msg in prompt.messages:
                    if hasattr(msg.content, 'text'):
                        print(msg.content.text)
            print("\n" + "="*50 + "\n")

            # List available resources
            resources = await session.list_resources()
            print("Available resources:")
            if hasattr(resources, 'resources'):
                for resource in resources.resources:
                    print(f"- {resource.name}")
            print("\n" + "="*50 + "\n")

            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            if hasattr(tools, 'tools'):
                for tool in tools.tools:
                    print(f"- {tool.name}")
            print("\n" + "="*50 + "\n")

            # Read current tasks
            content, mime_type = await session.read_resource("tasks://list")
            print("Current tasks:")
            tasks_data = format_task_list(content)
            if tasks_data and 'tasks' in tasks_data:
                for task in tasks_data['tasks']:
                    print(f"• {task['title']}: {task['description']}")
            print("\n" + "="*50 + "\n")

            # Add a new task
            new_task = await session.call_tool("add_task", {"params": {"task_title": "Order food"}})
            print("Added new task:")
            if hasattr(new_task, 'content'):
                for content in new_task.content:
                    if hasattr(content, 'text'):
                        task_info = json.loads(content.text)
                        if 'task' in task_info:
                            print(f"• {task_info['task']['title']}: {task_info['task']['description']}")
            print("\n" + "="*50 + "\n")

            # Show updated task list
            updated_content, _ = await session.read_resource("tasks://list")
            print("Updated task list:")
            updated_tasks = format_task_list(updated_content)
            if updated_tasks and 'tasks' in updated_tasks:
                for task in updated_tasks['tasks']:
                    print(f"• {task['title']}: {task['description']}")

def format_task_list(content):
    try:
        if isinstance(content, tuple):
            # Handle the case where content is a tuple
            for item in content[1]:
                if hasattr(item, 'text'):
                    data = json.loads(item.text)
                    return data
        else:
            # Try to parse as JSON string directly
            return json.loads(content)
    except:
        return content


if __name__ == "__main__":
    import asyncio
    asyncio.run(run())