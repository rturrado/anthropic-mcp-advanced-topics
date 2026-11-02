"""MCP transport-over-HTTP demo (server + browser client).

The server exposes an `add` tool and a `GET /` route that serves `index.html`,
a self-contained browser page that acts as the MCP client
— talking to the server over the `streamable-http` transport instead of stdio.

The `FastMCP` flags `stateless_http` and `json_response` are the chapter's main point:
without them, `streamable-http` falls back to session-based SSE streaming,
which plain-JS browser clients can't consume as easily as single JSON responses.
"""

import asyncio
from pathlib import Path

from mcp.server.fastmcp import Context, FastMCP
from starlette.requests import Request
from starlette.responses import Response

mcp = FastMCP(
    name="HTTP Transport Demo",
    # stateless_http=True,
    # json_response=True,

    # Match the trailing slash the browser client (`index.html`) uses,
    # so requests to `/mcp/` land here directly instead of hitting a 307 redirect from Starlette's `redirect_slashes`
    # — browsers do not follow redirects on CORS preflights.
    streamable_http_path="/mcp/",

    # Bind to `localhost` so uvicorn advertises `http://localhost:8000` on startup,
    # matching the hardcoded origin in `index.html`.
    # If uvicorn said `127.0.0.1` instead,
    # a user visiting that URL would make the fetch to `localhost:8000/mcp/` cross-origin and
    # trigger a CORS preflight the server does not answer.
    host="localhost",
)


@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    await ctx.info(f"Preparing to add {a} and {b}...")
    await ctx.report_progress(20, 100)

    await asyncio.sleep(2)

    await ctx.info(f"OK, adding {a} and {b}...")
    await ctx.report_progress(80, 100)

    return a + b


@mcp.custom_route("/", methods=["GET"])
async def serve_index(_request: Request) -> Response:
    html = (Path(__file__).parent / "index.html").read_text()
    return Response(content=html, media_type="text/html")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
