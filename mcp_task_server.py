from mcp.server.fastmcp import FastMCP
from transformers import pipeline

# Sample task titles
tasks = ["Plan meeting", "Write report", "Call client"]

# Set up the LLM pipeline (using GPT-2)
generator = pipeline("text-generation", model="gpt2")

# Create a FastMCP server instance
mcp = FastMCP(name="LLMTaskServer")

# Define a prompt: template for the LLM to generate a task description
@mcp.prompt("task_description")
def task_description(params):
    return f"Based on the task title '{params.get('task_title', 'Unnamed task')}', generate a detailed description"

# Define a tool: generate a task description using the LLM
@mcp.tool("generate_description")
def generate_description(params):
    task_title = params.get("task_title", "Unnamed task")
    # Use the LLM to generate a description
    prompt = f"Describe the task: {task_title}"
    result = generator(prompt, max_length=50, num_return_sequences=1)[0]["generated_text"]
    return {"task_title": task_title, "description": result.strip()}
    

# Define a resource: expose a list of task titles to the client
@mcp.resource("tasks://list")
def get_task_titles():
    return {"tasks": tasks, "count": len(tasks)}




if __name__ == "__main__":
    print("Starting LLMTaskServer...")
    try:
        # Run directly without asyncio.run()
        mcp.run()  
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Server stopped")