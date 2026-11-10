# Installing the AnimeAPI MCP server (for AI agents)

AnimeAPI is a remote MCP server. There is nothing to download, build or run.

- URL: `https://animeapi.ai/mcp`
- Transport: streamable HTTP
- Auth: header `Authorization: Bearer <key>` where the key starts with `ank_`, or OAuth if the client supports it.
- Cost: $0.003 per image on the default model. Each generation is charged to the user's prepaid balance.

## Steps

1. Ask the user for their AnimeAPI key. If they do not have one, send them to https://animeapi.ai/dashboard/api-keys (sign-up gives 3 free images, no card). Do not invent a key.
2. Add this entry to the client's MCP settings.

Cline (`cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "animeapi": {
      "type": "streamableHttp",
      "url": "https://animeapi.ai/mcp",
      "headers": { "Authorization": "Bearer ank_your_key" },
      "disabled": false
    }
  }
}
```

Clients that use the common `mcp.json` shape (Cursor and others):

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

3. Verify: the server should list three tools: `generate_anime_image`, `generate_anime_video`, `get_anime_video`.
4. Do not generate a test image without asking: every image costs the user $0.003.

## If something fails

- "AnimeAPI rejected the API key": the key is wrong or revoked. Ask the user for a new one.
- "balance is too low": the user needs to add funds at https://animeapi.ai/dashboard/billing (from $5).
- The client only supports stdio: bridge with `npx mcp-remote https://animeapi.ai/mcp --header "Authorization: Bearer ank_your_key"`.
