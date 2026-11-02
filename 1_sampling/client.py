"""MCP sampling demo (client side).

The server exposes a `summarize` tool that needs an LLM to run. Instead of calling Claude itself,
the server asks the client (via a sampling request) to invoke the LLM and return the result.
This client supplies the LLM through `sampling_callback`, which is wired into `ClientSession`.
"""

import asyncio
from pathlib import Path

from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.session import RequestContext
from mcp.client.stdio import stdio_client
from mcp.types import (
    CreateMessageRequestParams,
    CreateMessageResult,
    SamplingMessage,
    TextContent,
)

from chat_tools import text_from_block, text_from_message
from models import MODEL_SONNET

load_dotenv()

anthropic_client = AsyncAnthropic()
model = MODEL_SONNET

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
)


async def chat(input_messages: list[SamplingMessage], max_tokens=4000):
    messages = []
    for msg in input_messages:
        if msg.role in ("user", "assistant") and msg.content.type == "text":
            messages.append({"role": msg.role, "content": text_from_block(msg.content)})

    response = await anthropic_client.messages.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )

    return text_from_message(response)


async def call_claude(_context: RequestContext, params: CreateMessageRequestParams):
    text = await chat(params.messages)

    return CreateMessageResult(
        role="assistant",
        model=model,
        content=TextContent(type="text", text=text),
    )


async def run():
    async with (
        stdio_client(server_params) as (read, write),
        ClientSession(read, write, sampling_callback=call_claude) as session,
    ):
        await session.initialize()

        text_to_summarize = Path(__file__).parent.joinpath("the_black_cat.txt").read_text()
        result = await session.call_tool(
            name="summarize",
            arguments={"text_to_summarize": text_to_summarize},
        )
        print(text_from_message(result))


if __name__ == "__main__":
    asyncio.run(run())
