from urllib import response
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv("../.env")

# Create an MCP server
mcp = FastMCP(
    name="Bot",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8050,  # only used for SSE transport (set this to any port)
    stateless_http=True,
)


# Add a simple calculator tool
@mcp.tool()
async def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
async def sub(a: int, b: int) -> int:
    """Substraction of two numbers"""
    return a - b

@mcp.tool()
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def ask_question(question: str) -> str:
    """Ask a question and return a response with Ollama.

    Args:
        question: The question to ask.

    Returns:
        A response string.
    """
    def chat_with_ollama(message):
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'mistral',  # or llama3, gemma, deepseek-coder, etc.
                'prompt': message,
                'stream': False
            }
        )
        return response.json()['response']

    reply = chat_with_ollama(question)
    return f"You asked: {reply}"
    



# Run the server
if __name__ == "__main__":
    transport = "stdio"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    elif transport == "streamable-http":
        print("Running server with Streamable HTTP transport")
        mcp.run(transport="streamable-http")
    else:
        raise ValueError(f"Unknown transport: {transport}")
