# <div align="center">NASA MCP</div>

<div align="center">

**A polished Model Context Protocol server for NASA's Astronomy Picture of the Day and image search APIs.**

Small enough to understand in minutes. Clean enough to ship. Structured enough for real MCP clients.

[![Python](https://img.shields.io/badge/python-3.11%2B-0b3d91?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-FastMCP-1f6feb?style=for-the-badge)](https://github.com/modelcontextprotocol)
[![NASA](https://img.shields.io/badge/API-NASA-d61f26?style=for-the-badge)](https://api.nasa.gov/)
[![CI](https://img.shields.io/github/actions/workflow/status/alok-19/nasa_mcp/ci.yml?branch=main&style=for-the-badge&label=CI)](https://github.com/alok-19/nasa_mcp/actions)
[![License](https://img.shields.io/badge/license-MIT-111827?style=for-the-badge)](./LICENSE)

[Quick Start](#quick-start) •
[Why This Exists](#why-this-exists) •
[Tools](#tools) •
[Project Layout](#project-layout)

</div>

---

## Why This Exists

Most NASA API demos stop at a notebook or a thin script. That is fine for exploration, but weak for reuse.

This project turns the same idea into a production-friendly MCP server:

- structured tool outputs instead of stringified JSON blobs
- validated inputs for dates, queries, and result sizes
- consistent upstream error handling
- clean packaging with a runnable CLI entrypoint
- unit tests for both the NASA client and MCP tool layer
- GitHub Actions CI for repeatable verification

If you want a compact reference implementation for an external-data MCP server, this repo is that.

## What You Get

| Tool | Purpose | Output |
| --- | --- | --- |
| `get_nasa_apod` | Fetch NASA's Astronomy Picture of the Day for a specific date or the latest day | Raw APOD metadata from NASA |
| `search_images_data` | Search NASA's image library with a keyword query | Normalized image metadata with compact fields |

## Quick Start

Run the server locally in a few commands:

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
cp .env.example .env
```

Set your NASA key in `.env`:

```bash
NASA_API_KEY=your_nasa_api_key_here
```

Then start the MCP server:

```bash
nasa-mcp
```

You can use `DEMO_KEY`, but it is rate-limited and not appropriate for sustained use.

## Tools

### `get_nasa_apod`

Returns Astronomy Picture of the Day metadata from NASA's APOD API.

**Input**

```json
{
  "date": "2024-10-05"
}
```

**Behavior**

- accepts `YYYY-MM-DD`
- rejects dates before `1995-06-16`
- rejects future dates
- returns a structured error payload when validation or the upstream API fails

**Example shape**

```json
{
  "date": "2024-10-05",
  "title": "Example Title",
  "explanation": "NASA APOD explanation...",
  "url": "https://apod.nasa.gov/..."
}
```

### `search_images_data`

Searches NASA's image library and returns compact result objects.

**Input**

```json
{
  "q": "mars rover",
  "size": 3
}
```

**Behavior**

- trims and validates the query
- restricts `size` to a safe range
- extracts a useful image URL when present
- returns normalized items instead of the full upstream payload

**Example shape**

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

## Why It Feels Production-Ready

- **Typed, small surface area**: easy to audit and maintain.
- **Validated request boundaries**: bad inputs fail fast.
- **Structured MCP responses**: better client interoperability.
- **No unnecessary runtime dependencies**: only the essentials.
- **CI-backed**: tests run on multiple Python versions.

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
├── .env.example
├── nasa_mcp_server.py
├── pyproject.toml
└── README.md
```

## Local Development

Install and run verification locally:

```bash
python -m py_compile nasa_mcp_server.py api/nasa.py tests/test_nasa.py tests/test_server.py
python -m unittest discover -s tests -v
```

Install as a package:

```bash
pip install .
```

## Design Principles

- **Keep the server thin**: NASA-specific logic stays in `api/nasa.py`.
- **Normalize where it helps**: image search returns useful compact fields.
- **Fail clearly**: validation and upstream failures become explicit errors.
- **Prefer boring deployability**: simple packaging and predictable startup.

## Production Notes

- Use a real NASA API key instead of `DEMO_KEY`.
- Expect upstream availability and rate limits to shape reliability.
- Add caching at the edge if you expect repeated APOD or search traffic.
- Run behind a process manager if you depend on long-lived server uptime.

## Roadmap

- response caching for repeated APOD and search requests
- richer media support beyond image-only search
- deployment examples for common MCP host setups
