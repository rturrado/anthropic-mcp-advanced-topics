"""MCP sampling demo (server side).

The `summarize` tool needs an LLM but the server doesn't talk to one directly.
It uses `ctx.session.create_message(...)` to send a sampling request back to the client,
which must handle it via its `sampling_callback` and return the model's response.
This inverts the usual direction: the server consumes the client's LLM.
"""

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP(name="Demo Server")


@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
    prompt = f"""
        Please summarize the following text:
        {text_to_summarize}
    """

    result = await ctx.session.create_message(
        messages=[SamplingMessage(role="user", content=TextContent(type="text", text=prompt))],
        max_tokens=4000,
        system_prompt="You are a helpful research assistant.",
    )

    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")


if __name__ == "__main__":
    mcp.run(transport="stdio")
