import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()  # Needed to run interactive python


async def main():
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",  # The command to run your server
        #args=["server.py"],  # Arguments to the command
        args=["app.py"],  # Arguments to the command
    )

    # Connect to the server
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with await ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call our calculator tool
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            print(f"2 + 3 = {result.content[0].text}")

            result = await session.call_tool("sub", arguments={"a": 2, "b": 3, "c": 4})
            print(f"7 - 3 = {result.content[1].text}")

            result = await session.call_tool("Multiply", arguments={"a": 5, "b": 2})
            print(f"5 * 2 = {result.content[2].text}")

            result = await session.call_tool("ask_question", arguments={"question": "What is the capital of France?"}, timeout=10000000)
            print("Server response:\n", result)
           


if __name__ == "__main__":
    asyncio.run(main())
