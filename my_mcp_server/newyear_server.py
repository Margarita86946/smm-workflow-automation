import asyncio
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

app = Server("newyear-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_newyear_message",
            description="Get a New Year congratulations message",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Optional name to personalize the message"
                    }
                },
                "required": []
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_newyear_message":
        recipient_name = arguments.get("name", "")
        
        if recipient_name:
            message = f"🎉 Happy New Year, {recipient_name}! 🎊\n\nWishing you a year filled with joy, success, and wonderful moments!"
        else:
            message = "🎉 Happy New Year! 🎊\n\nWishing you a year filled with joy, success, and wonderful moments!"
        
        return [TextContent(type="text", text=message)]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    except Exception as e:
        print(f"Error running server: {e}", file=sys.stderr)
        raise

if __name__ == "__main__":
    asyncio.run(main())