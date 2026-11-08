"""MCP notifications demo (client side).

The server emits two kinds of out-of-band messages while a tool runs:
log notifications (`ctx.info`) and progress updates (`ctx.report_progress`).
This client wires both: `logging_callback` on `ClientSession` catches the logs,
and `progress_callback` on the `call_tool` catches the progress updates.
Both run concurrently with the tool's response.
"""

import asyncio

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import LoggingMessageNotificationParams

from chat_tools import text_from_message

load_dotenv()

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)


async def print_log(params: LoggingMessageNotificationParams):
    print(params.data)


async def print_progress(progress: float, total: float | None, message: str | None):
    if total is not None:
        percentage = (progress / total) * 100
        print(f"Progress: {progress}/{total} ({percentage:.1f}%)")
    else:
        print(f"Progress: {progress}")


async def run():
    async with (
        stdio_client(server_params) as (read, write),
        ClientSession(read, write, logging_callback=print_log) as session,
    ):
        await session.initialize()

        result = await session.call_tool(
            name="add",
            arguments={"a": 1, "b": 3},
            progress_callback=print_progress,
        )
        print(f"Result: {text_from_message(result)}")


if __name__ == "__main__":
    asyncio.run(run())
