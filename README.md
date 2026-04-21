# NASA MCP

An MCP server that exposes two practical NASA tools:

- `get_nasa_apod` for Astronomy Picture of the Day metadata
- `search_images_data` for NASA image-library search

It is intentionally small, typed, and easy to run locally or deploy behind any MCP-compatible client.

## Why This Repo Exists

Many NASA demos stop at a notebook or a thin script. This repository packages the same idea as a reusable MCP server with:

- input validation for dates, queries, and result sizes
- structured error handling around upstream API failures
- compact search responses that are useful inside tool-calling workflows
- unit coverage for the client and MCP tool layer
- GitHub Actions CI for repeatable verification

## Features

| Tool | What it does | Notes |
| --- | --- | --- |
| `get_nasa_apod` | Fetches NASA APOD metadata for a specific date or the latest entry | Validates date format and APOD availability window |
| `search_images_data` | Searches NASA's image library and returns compact image metadata | Limits page size and normalizes response shape |

## Project Layout

```text
nasa_mcp/
├── api/
│   ├── __init__.py
│   └── nasa.py
├── tests/
│   ├── test_nasa.py
│   └── test_server.py
├── .github/workflows/ci.yml
├── nasa_mcp_server.py
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.11+
- A NASA API key for higher rate limits

You can use `DEMO_KEY`, but it is heavily rate-limited and not appropriate for steady production traffic.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
cp .env.example .env
```

Set `NASA_API_KEY` in `.env`, then run:

```bash
nasa-mcp
```

## Tool Examples

### APOD

Input:

```json
{
  "date": "2024-10-05"
}
```

Output shape:

```json
{
  "date": "2024-10-05",
  "title": "Example Title",
  "explanation": "NASA APOD explanation...",
  "url": "https://apod.nasa.gov/..."
}
```

### Image Search

Input:

```json
{
  "q": "mars rover",
  "size": 3
}
```

Output shape:

```json
{
  "query": "mars rover",
  "count": 3,
  "items": [
    {
      "title": "Mars Rover",
      "description": "A rover on Mars",
      "date_created": "2020-01-01T00:00:00Z",
      "nasa_id": "mars-rover",
      "image_url": "https://images-assets.nasa.gov/..."
    }
  ]
}
```

## Verification

Local verification used for this repo:

```bash
python -m py_compile nasa_mcp_server.py api/nasa.py tests/test_nasa.py tests/test_server.py
python -m unittest discover -s tests -v
```

CI runs the same test suite on Python 3.11, 3.12, and 3.13.

## Production Notes

- Use a real NASA API key instead of `DEMO_KEY`.
- Run the server under a process manager in environments where long-lived MCP processes are expected.
- Treat upstream NASA availability and rate limits as an external dependency.
- If you need stronger SLAs, add retry and caching policy at the deployment edge rather than inside the tool layer.

## Roadmap

- optional response caching for APOD and repeated searches
- transport-specific deployment examples
- richer media support beyond image-only search
