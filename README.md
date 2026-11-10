# AnimeAPI MCP server

<img src="icon.png" width="72" align="right" alt="AnimeAPI">

Anime image generation for AI agents at **$0.003 per image**, one of the cheapest anime image APIs. One remote MCP server, no install: `https://animeapi.ai/mcp`. Pay as you go from a prepaid balance (from $5, never expires, no subscription). New accounts get 3 free images, no card.

- **Server URL:** `https://animeapi.ai/mcp` (streamable HTTP, stateless)
- **Sign-in:** OAuth (your agent opens a browser page, you click Allow), or a static header `Authorization: Bearer ank_your_key`
- **Registry name:** `ai.animeapi/mcp` in the [official MCP registry](https://registry.modelcontextprotocol.io)
- **Docs:** https://animeapi.ai/docs/mcp

## Prices

| What | Price |
| --- | --- |
| `anime` image (default; best for characters) | **$0.003** |
| `ultra` image (follows long sentences, renders legible text) | $0.01 |
| `ultra-max` image (highest detail) | $0.02 |
| Video, 480p | $0.016 per second |
| Video, 768p | $0.04 per second |

Any orientation costs the same. Failed generations are refunded.

## Tools

| Tool | What it does | Cost |
| --- | --- | --- |
| `generate_anime_image` | One anime-style image from a text prompt. Returns the image URL, the prompt the model read, the cost and the remaining balance. About 4 seconds on `anime`. | $0.003 / $0.01 / $0.02 per image |
| `generate_anime_video` | One anime clip (MP4, 5 to 15 seconds, with sound) from a text prompt, optionally starting or ending on an image. | $0.016/s (480p), $0.04/s (768p) |
| `get_anime_video` | Checks a video that is still rendering. | Free |

`generate_anime_image` arguments: `prompt` (required, up to 1,000 characters, plain English), `model` (`anime` \| `ultra` \| `ultra-max`, default `anime`), `orientation` (`portrait` \| `square` \| `landscape`, default `portrait`) and `enhance` (default `true`: rewrites plain English into tags for the anime model).

## Install

Get a key at https://animeapi.ai/dashboard/api-keys (keys start with `ank_`), or skip the key and sign in with OAuth where the client supports it.

### Claude Code

```bash
claude mcp add --transport http animeapi https://animeapi.ai/mcp
```

Then run `/mcp`, choose `animeapi` and sign in. With a key instead:

```bash
claude mcp add --transport http animeapi https://animeapi.ai/mcp \
  --header "Authorization: Bearer ank_your_key"
```

### Claude Desktop and claude.ai

Settings → Connectors → **Add custom connector** → URL `https://animeapi.ai/mcp` → sign in when asked.

### Cursor

`~/.cursor/mcp.json` (or `.cursor/mcp.json` in a project):

```json
{
  "mcpServers": {
    "animeapi": { "url": "https://animeapi.ai/mcp" }
  }
}
```

Cursor signs you in on first use. With a key instead:

```json
{
  "mcpServers": {
    "animeapi": {
      "url": "https://animeapi.ai/mcp",
      "headers": { "Authorization": "Bearer ank_your_key" }
    }
  }
}
```

### VS Code (GitHub Copilot)

```bash
code --add-mcp '{"name":"animeapi","type":"http","url":"https://animeapi.ai/mcp"}'
```

or `.vscode/mcp.json`:

```json
{
  "servers": {
    "animeapi": { "type": "http", "url": "https://animeapi.ai/mcp" }
  }
}
```

VS Code signs you in on first use. With a key instead:

```json
{
  "inputs": [
    { "id": "animeapi-key", "type": "promptString", "description": "AnimeAPI key (ank_...)", "password": true }
  ],
  "servers": {
    "animeapi": {
      "type": "http",
      "url": "https://animeapi.ai/mcp",
      "headers": { "Authorization": "Bearer ${input:animeapi-key}" }
    }
  }
}
```

### Windsurf

Open the MCP servers panel in Cascade's settings and add a server, or edit the MCP config file directly:

```json
{
  "mcpServers": {
    "animeapi": {
      "url": "https://animeapi.ai/mcp",
      "transport": "http",
      "headers": { "Authorization": "Bearer ank_your_key" }
    }
  }
}
```

Leave out `headers` to sign in with OAuth instead. Older Windsurf builds keep this file at `~/.codeium/windsurf/mcp_config.json` and name the address `serverUrl` instead of `url`.

### Cline

MCP Servers → Remote Servers → name `animeapi`, URL `https://animeapi.ai/mcp`, transport **Streamable HTTP**. Or in `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "animeapi": {
      "type": "streamableHttp",
      "url": "https://animeapi.ai/mcp",
      "headers": { "Authorization": "Bearer ank_your_key" }
    }
  }
}
```

### OpenAI Codex

`~/.codex/config.toml`:

```toml
[mcp_servers.animeapi]
url = "https://animeapi.ai/mcp"
bearer_token_env_var = "ANIMEAPI_KEY"
```

Export `ANIMEAPI_KEY=ank_your_key` in the shell you start Codex from. Or sign in with OAuth: `codex mcp add animeapi --url https://animeapi.ai/mcp` then `codex mcp login animeapi`.

### ChatGPT (developer mode)

Turn on **Developer mode** in ChatGPT's settings (paid plans; the exact menu has moved between releases), then create a new app (custom connector) with:

- **MCP server URL:** `https://animeapi.ai/mcp`
- **Authentication:** OAuth

ChatGPT registers itself, sends you to the AnimeAPI consent page and receives a key for your account. Enable the app in a chat from the tools menu.

### Anything else

Any client that speaks streamable HTTP works: give it the URL, and either let it run OAuth (the server supports discovery, dynamic client registration and PKCE) or set the `Authorization: Bearer ank_your_key` header. Clients that only speak stdio can bridge with `npx mcp-remote https://animeapi.ai/mcp --header "Authorization: Bearer ank_your_key"`.

### LangChain

Use [`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters) with transport `streamable_http`, URL `https://animeapi.ai/mcp` and the header `Authorization: Bearer ank_your_key`. Or skip MCP and use the plain tool in [`examples/langchain_tool.py`](examples/langchain_tool.py).

## Try it

Ask your agent:

> Draw a knight cat drinking tea in a sunflower field, landscape.

The agent calls `generate_anime_image` and gets back the image URL, the cost ($0.003) and the balance left.

## Good to know

- Every image and video is charged to the connected account's balance. The server tells agents to make one image and ask before making many, and to quote the price before long videos; it cannot enforce that, so watch your usage page.
- Signing in with OAuth creates a key named `MCP · <app name>` in Dashboard → API keys. Revoke it there to disconnect that app.
- Image URLs are on `animeapi.ai/i/...` and are not permanent storage. Download images you want to keep.
- AnimeAPI does not generate adult content. Explicit prompts are refused and not charged.

## This repository

The server itself runs at animeapi.ai; this repository holds its registry entry (`server.json`), install instructions and the place to report problems. Open an issue here or write to contact@animeapi.ai.

## Licence

MIT
