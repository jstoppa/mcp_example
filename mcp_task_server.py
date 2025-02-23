from mcp.server.fastmcp import FastMCP
import sys
import json

# Sample tasks with titles and descriptions
tasks = [
    {"title": "Plan meeting", "description": "Schedule team sync meeting"},
    {"title": "Write report", "description": "Complete quarterly report"},
    {"title": "Call client", "description": "Follow up on project requirements"}
]

# Create a FastMCP server instance
mcp = FastMCP(name="TaskServer")

# Define a prompt: template for task creation
@mcp.prompt("task_description")
def task_description(task_title="Unnamed task"):
    return f"Based on the task title '{task_title}', generate a detailed description"

# Define a tool: add a new task to the list
@mcp.tool("add_task")
def add_task(params):
    print(f"Adding task with params: {params}", file=sys.stderr)
    task_title = params.get("task_title", "Unnamed task")
    task_description = params.get("description", "No description provided")
    new_task = {"title": task_title, "description": task_description}
    tasks.append(new_task)
    print(f"Current tasks after adding: {tasks}", file=sys.stderr)
    return {"task": new_task, "success": True}

# Define a resource: expose a list of task titles to the client
@mcp.resource("tasks://list")
def get_task_titles():
    print(f"Getting tasks, current list: {tasks}", file=sys.stderr)
    return {
        "meta": None,
        "contents": [{
            "uri": "tasks://list",
            "mime_type": "application/json",
            "text": json.dumps({"tasks": tasks, "count": len(tasks)})
        }]
    }

if __name__ == "__main__":
    print("Starting TaskServer...", file=sys.stderr)
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\nShutting down server...", file=sys.stderr)
    except Exception as e:
        print(f"Error occurred: {e}", file=sys.stderr)
    finally:
        print("Server stopped", file=sys.stderr)