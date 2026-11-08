"""`Chat` subclass that holds a reference to a dedicated "doc client" MCP server.

Adds pass-through helpers for `list_prompts` and `get_prompt` against that client.
In this demo the "doc client" is the roots server itself;
the helpers are scaffolding that future demos (which do expose prompts) can reuse.
"""

from anthropic.types import MessageParam
from mcp.types import Prompt, PromptMessage
from mcp_client import MCPClient

from core.chat import Chat
from core.claude import Claude


class CliChat(Chat):
    def __init__(
        self,
        doc_client: MCPClient,
        clients: dict[str, MCPClient],
        claude_service: Claude,
    ):
        super().__init__(clients=clients, claude_service=claude_service)

        self.doc_client: MCPClient = doc_client

    async def list_prompts(self) -> list[Prompt]:
        return await self.doc_client.list_prompts()

    async def get_prompt(self, command: str, doc_id: str) -> list[PromptMessage]:
        return await self.doc_client.get_prompt(command, {"doc_id": doc_id})

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})


def convert_prompt_message_to_message_param(
    prompt_message: PromptMessage,
) -> MessageParam:
    role = "user" if prompt_message.role == "user" else "assistant"
    content = prompt_message.content
    if getattr(content, "type", None) == "text":
        return {"role": role, "content": getattr(content, "text", "")}
    return {"role": role, "content": ""}


def convert_prompt_messages_to_message_params(
    prompt_messages: list[PromptMessage],
) -> list[MessageParam]:
    return [convert_prompt_message_to_message_param(msg) for msg in prompt_messages]
