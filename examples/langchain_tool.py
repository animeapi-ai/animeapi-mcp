"""AnimeAPI as a LangChain tool: anime images at $0.003 each.

    pip install langchain-core requests
    export ANIMEAPI_KEY=ank_your_key
    python langchain_tool.py

Give `generate_anime_image` to any tool-calling model, for example:

    from langchain.agents import create_agent
    agent = create_agent("your-model", tools=[generate_anime_image])

Agents that speak MCP can skip this file and connect to https://animeapi.ai/mcp
(for LangChain: langchain-mcp-adapters, transport "streamable_http", header
Authorization: Bearer ank_...).
"""
import os
from typing import Literal

import requests
from langchain_core.tools import tool

PRICES = {"anime": 0.003, "ultra": 0.01, "ultra-max": 0.02}


@tool
def generate_anime_image(
    prompt: str,
    orientation: Literal["portrait", "square", "landscape"] = "portrait",
    model: Literal["anime", "ultra", "ultra-max"] = "anime",
) -> str:
    """Generate one anime-style image with AnimeAPI and return its URL.

    Costs $0.003 per image on "anime" (default, best for characters), $0.01 on "ultra"
    (long prompts, legible text) and $0.02 on "ultra-max" (highest detail).
    Make one image unless the user asks for more.

    Args:
        prompt: What to draw, in plain English, up to 1,000 characters.
        orientation: Shape of the image.
        model: Quality tier.
    """
    response = requests.post(
        "https://animeapi.ai/api/generate",
        headers={"Authorization": f"Bearer {os.environ['ANIMEAPI_KEY']}"},
        json={"prompt": prompt[:1000], "model": model, "orientation": orientation},
        timeout=120,
    )
    data = response.json()
    if not response.ok:
        return f"AnimeAPI error ({data.get('code', response.status_code)}): {data.get('error', 'request failed')}"
    return (
        f"Image URL: {data['image_url']} (cost ${PRICES[model]}, balance left ${data['balance_usd']:.2f}). "
        "The link is not permanent storage; download the image to keep it."
    )


if __name__ == "__main__":
    print(generate_anime_image.invoke({"prompt": "a knight cat drinking tea in a sunflower field", "orientation": "landscape"}))
