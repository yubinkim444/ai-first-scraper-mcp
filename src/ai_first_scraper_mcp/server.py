"""
ai-first-scraper-mcp
====================
A Model Context Protocol (MCP) server that gives Claude Desktop, Cursor,
Cline, and any other MCP-compatible agent three tools:

    fetch_page          single URL  -> clean Markdown
    fetch_pages_batch   many URLs   -> clean Markdown for each
    search_web          query       -> top-N pages already converted to Markdown

Under the hood it calls a deployed ai-first-scraper and ai-first-search
instance. Point at your own deployment with SCRAPER_URL / SEARCH_URL env vars.

Run via:
    uvx ai-first-scraper-mcp
    # or
    pip install ai-first-scraper-mcp && ai-first-scraper-mcp
"""

from __future__ import annotations

import os
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

SCRAPER_URL = os.getenv("SCRAPER_URL", "https://ai-first-scraper.onrender.com").rstrip("/")
SEARCH_URL = os.getenv("SEARCH_URL", "https://ai-first-search.onrender.com").rstrip("/")
DEFAULT_TIMEOUT = float(os.getenv("AFS_TIMEOUT", "45"))

mcp = FastMCP("ai-first-scraper")


@mcp.tool()
async def fetch_page(url: str, max_tokens: Optional[int] = None) -> str:
    """Fetch a single web page or PDF and return its main content as clean,
    ad-free Markdown — ready to drop into an LLM prompt.

    Args:
        url: A fully-qualified http(s) URL.
        max_tokens: Optional soft cap on the returned Markdown (whitespace
            tokens). When exceeded, the body is truncated and a
            `[...truncated]` marker is appended.

    Returns:
        The cleaned Markdown body of the page.
    """
    params: dict[str, str | int] = {"url": url}
    if max_tokens:
        params["max_tokens"] = max_tokens
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        resp = await client.get(f"{SCRAPER_URL}/raw", params=params)
        resp.raise_for_status()
        return resp.text


@mcp.tool()
async def fetch_pages_batch(urls: list[str], max_tokens: Optional[int] = None) -> list[dict]:
    """Fetch many web pages in parallel and return each one's clean Markdown.

    Use this whenever you need to read more than one URL at once — it is far
    faster than calling fetch_page in a loop because the upstream scraper
    handles the concurrency.

    Args:
        urls: Up to 25 URLs.
        max_tokens: Optional per-URL soft cap on the returned Markdown.

    Returns:
        A list of `{url, ok, data?, error?}` objects in the same order as the
        input URLs. `data` is `{title, word_count, markdown, links, ...}` on
        success; `error` contains the failure reason otherwise.
    """
    body: dict = {"urls": urls}
    if max_tokens:
        body["max_tokens"] = max_tokens
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        resp = await client.post(f"{SCRAPER_URL}/batch", json=body)
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def search_web(q: str, k: int = 5, max_tokens: Optional[int] = None) -> list[dict]:
    """Run a web search and return the top-k result pages already converted to
    clean Markdown. Use this whenever you need fresh information from the
    public web — it combines search and read in one call.

    Args:
        q: The user's query (free text).
        k: How many results to fetch (1–10, default 5).
        max_tokens: Optional per-result soft cap on the returned Markdown.

    Returns:
        A list of `{url, title, snippet, ok, markdown, word_count, error?}`
        result objects. Use `title` and `snippet` to decide which results are
        worth citing, then drop the `markdown` field into your prompt.
    """
    params: dict[str, str | int] = {"q": q, "k": k}
    if max_tokens:
        params["max_tokens"] = max_tokens
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        resp = await client.get(f"{SEARCH_URL}/search", params=params)
        resp.raise_for_status()
        return resp.json().get("results", [])


def main() -> None:
    """Console-script entry point — runs the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
