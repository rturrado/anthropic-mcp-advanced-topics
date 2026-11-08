"""Entry point of the roots demo.

Reads the root paths from argv, constructs an `MCPClient` that advertises them,
wires it to the `Claude` service and a `CliChat` + `CliApp`, and starts the interactive chat loop.
"""

import asyncio
import os
import sys
from contextlib import AsyncExitStack

from core.claude import Claude
from core.cli import CliApp
from core.cli_chat import CliChat
from dotenv import load_dotenv
from mcp_client import MCPClient

from models import MODEL_DEFAULT

load_dotenv()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
assert anthropic_api_key, "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"

claude_model = MODEL_DEFAULT


async def main():
    claude_service = Claude(model=claude_model)

    # Get root directories from command line arguments
    root_paths = sys.argv[1:]
    if not root_paths:
        print("Usage: uv run main.py <root1> [root2] ...")
        print("Example: uv run main.py /path/to/videos /another/path")
        sys.exit(1)

    clients = {}

    async with AsyncExitStack() as stack:
        # Create the MCP client with the provided root directories
        doc_client = await stack.enter_async_context(
            MCPClient(command="uv", args=["run", "mcp_server.py"], roots=root_paths)
        )
        clients["doc_client"] = doc_client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            claude_service=claude_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
