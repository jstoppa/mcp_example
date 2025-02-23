from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

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

                # List available prompts
            prompts = await session.list_prompts()

            # Get a prompt
            prompt = await session.get_prompt("review_task", arguments={"task_title": "Plan meeting"})

            # List available resources
            resources = await session.list_resources()

            # List available tools
            tools = await session.list_tools()

            # Read a resource
            content, mime_type = await session.read_resource("tasks://list")

            # Call a tool
            result = await session.call_tool("generate_description", arguments={"task_title": "Plan meeting"})

            print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())



# async def main():
#     # Initialize the client
#     client = MCPClient()

#     # Discover available servers
#     print("Searching for MCP servers...")
#     servers = await client.discover_servers()
#     if not servers:
#         print("No servers found. Make sure the LLMTaskServer is running!")
#         return

#     # Use the first server
#     server = servers[0]
#     print(f"Found server: {server.name} (ID: {server.id})")

#     # Fetch the task titles resource
#     task_data = await client.request_resource(server.id, "task_titles")
#     print("\nCurrent Task Titles:")
#     print(f"Tasks: {task_data['tasks']}")
#     print(f"Total: {task_data['count']}")

#     # Pick a task and generate a description
#     selected_task = task_data["tasks"][0]  # Take the first task
#     result = await client.invoke_tool(server.id, "generate_description", {"task_title": selected_task})
#     print("\nGenerated Task Description:")
#     print(f"Task: {result['task_title']}")
#     print(f"Description: {result['description']}")

# # Run the client
# asyncio.run(main())