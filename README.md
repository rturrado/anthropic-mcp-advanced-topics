# MCP: Advanced Topics - exercises

Demos from Anthropic Academy's free [MCP: Advanced Topics](https://anthropic.skilljar.com/model-context-protocol-advanced-topics) course,
collected into a single uv project.
One folder per demo at the project root, all sharing the same dependencies.

## Setup

1.  `uv sync`
2.  `cp .env.example .env`
3.  Edit `.env` and set your real `ANTHROPIC_API_KEY`. See [Getting the key](#getting-the-key) for details.

The `3_roots` demo also requires FFmpeg on your PATH for the video conversion tool
(`brew install ffmpeg` on macOS, `apt install ffmpeg` on Debian/Ubuntu).

### Getting the key

1.  Log in to the [Anthropic Console](https://console.anthropic.com).
2.  Go to *Settings / API Keys* and click *Create Key*.
3.  Give it a name and copy the key; it is shown only once.

New accounts get a small free credit.
Once it runs out, requests fail with `429` until you top up or enable billing on the workspace.

## Demos

1.  **Sampling** — the MCP server asks the client to invoke the LLM (reverses the usual flow).
2.  **Notifications** — the MCP server pushes updates to the client (progress reports for long-running work).
3.  **Roots** — the client exposes a set of filesystem roots the server is allowed to inspect; includes a video conversion tool as a worked example.
