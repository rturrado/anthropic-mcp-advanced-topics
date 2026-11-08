"""MCP notifications demo (server side).

The `add` tool is contrived (a slow sum) to show that a tool can emit:
- Log messages (`ctx.info`) that reach the client via its `logging_callback`.
- Progress updates (`ctx.report_progress`) that reach the client via `progress_callback`.
Both are pushed by the server during the tool's execution, independent of the final return value.
"""

import asyncio

from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP(name="Demo Server")


@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    await ctx.info(f"Preparing to add {a} and {b}...")
    await ctx.report_progress(20, 100)

    await asyncio.sleep(2)

    await ctx.info(f"OK, adding {a} and {b}...")
    await ctx.report_progress(80, 100)

    return a + b


if __name__ == "__main__":
    mcp.run(transport="stdio")
