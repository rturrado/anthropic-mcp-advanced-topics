def text_from_message(message):
    """Return the concatenated text of all `text` blocks in `message.content`.
    Works on anything with that shape (e.g., Anthropic `Message` or MCP `CallToolResult`).
    """
    return "".join(block.text for block in message.content if block.type == "text")


def text_from_block(block):
    """Return the text of a content block, falling back to `str()` if no `.text` attribute."""
    return block.text if hasattr(block, "text") else str(block)
