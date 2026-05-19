<!--
mcp-name: io.github.yubinkim444/ai-first-scraper-mcp
-->

# ai-first-scraper-mcp

> **Plug Claude Desktop, Cursor, or Cline straight into an ad-free web
> scraper + search engine.** Three tools, one line of config.

[![PyPI](https://img.shields.io/pypi/v/ai-first-scraper-mcp)](https://pypi.org/project/ai-first-scraper-mcp/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![MCP](https://img.shields.io/badge/MCP-server-7c3aed)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green)]()

---

## What it does

Adds three tools to any [MCP](https://modelcontextprotocol.io)-compatible
agent:

| Tool | What it does |
|------|--------------|
| `fetch_page` | Fetch one URL → return clean Markdown (HTML or PDF). |
| `fetch_pages_batch` | Fetch up to 25 URLs in parallel → return Markdown for each. |
| `search_web` | Run a web search and return the top-k result pages already converted to Markdown. |

No more "the model called curl and then tried to parse 80kB of ad HTML."
Your agent receives clean Markdown ready to reason about.

Backed by the [ai-first-scraper](https://github.com/yubinkim444/ai-first-scraper)
and [ai-first-search](https://github.com/yubinkim444/ai-first-search) APIs.

---

## Install

### Fastest — `uvx` (no install, runs from PyPI on demand)

```jsonc
// claude_desktop_config.json  /  cline_mcp_settings.json  /  ~/.cursor/mcp.json
{
  "mcpServers": {
    "ai-first-scraper": {
      "command": "uvx",
      "args": ["ai-first-scraper-mcp"]
    }
  }
}
```

Restart your client (Claude Desktop / Cursor / Cline). The three tools above
will appear automatically.

### Alternative — pip install

```bash
pip install ai-first-scraper-mcp
```

```jsonc
{
  "mcpServers": {
    "ai-first-scraper": {
      "command": "ai-first-scraper-mcp"
    }
  }
}
```

---

## Where the config file lives

| Client | Config path |
|--------|-------------|
| **Claude Desktop (macOS)** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Claude Desktop (Windows)** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Cursor** | `~/.cursor/mcp.json` |
| **Cline (VS Code)** | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |

---

## Point at your own backend (optional)

By default this server calls the public `ai-first-scraper.onrender.com` and
`ai-first-search.onrender.com` instances. If you want to self-host, set env
vars in your MCP config:

```jsonc
{
  "mcpServers": {
    "ai-first-scraper": {
      "command": "uvx",
      "args": ["ai-first-scraper-mcp"],
      "env": {
        "SCRAPER_URL": "https://your-scraper.example.com",
        "SEARCH_URL":  "https://your-search.example.com",
        "AFS_TIMEOUT": "60"
      }
    }
  }
}
```

---

## Verify it works

Open your MCP client and ask the agent:

> "Use the search_web tool to find the top 3 recent articles about MCP and
> summarize them in 5 bullets each."

You should see the agent call `search_web`, get back Markdown for each result,
and produce the summary without ever touching raw HTML.

---

## Companion projects

- **[ai-first-scraper](https://github.com/yubinkim444/ai-first-scraper)** — the
  per-URL Markdown cleaner this MCP server fans out to.
- **[ai-first-search](https://github.com/yubinkim444/ai-first-search)** —
  search → scrape → markdown pipeline.
- **[mcp-rec](https://github.com/yubinkim444/mcp-rec)** — record & replay any MCP server's traffic for tests and bug reports.
- **[llm-cache-proxy](https://github.com/yubinkim444/llm-cache-proxy)** — local cache for OpenAI/Anthropic API calls.
- **[promptlocker](https://github.com/yubinkim444/promptlock)** — lockfile for prompts.
- **[context-diff](https://github.com/yubinkim444/context-diff)** — see what blew up your Claude Code context window.
- **[agentwatch](https://github.com/yubinkim444/agentwatch)** — overlay for browser AI agents.

---

## Develop locally

```bash
git clone https://github.com/yubinkim444/ai-first-scraper-mcp.git
cd ai-first-scraper-mcp

uv sync                    # or: pip install -e .
ai-first-scraper-mcp       # speaks MCP over stdio
```

To test against a local client, point its MCP config at the same command.

---

## License

MIT © yubinkim444
