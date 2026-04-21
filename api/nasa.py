from __future__ import annotations

import logging
import os
from datetime import date, datetime
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger(__name__)
APOD_START_DATE = date(1995, 6, 16)
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
NASA_IMAGE_SEARCH_URL = "https://images-api.nasa.gov/search"
NASA_API_KEY = os.getenv("NASA_API_KEY") or "DEMO_KEY"


class NasaApiError(RuntimeError):
    """Raised when a NASA API request cannot be completed successfully."""


def _parse_date(value: str) -> date:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("date must use YYYY-MM-DD format") from exc

    if parsed < APOD_START_DATE:
        raise ValueError("date must be on or after 1995-06-16")
    if parsed > date.today():
        raise ValueError("date cannot be in the future")
    return parsed


def make_api_request(
    url: str,
    params: dict[str, Any],
    timeout: int = 10,
    session: requests.sessions.Session | None = None,
) -> dict[str, Any]:
    """Perform a NASA API GET request and return the decoded JSON payload."""
    requester = session or requests
    try:
        response = requester.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as exc:
        raise NasaApiError(f"NASA API request timed out after {timeout}s") from exc
    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else "unknown"
        raise NasaApiError(f"NASA API returned HTTP {status_code}") from exc
    except requests.exceptions.RequestException as exc:
        raise NasaApiError("NASA API request failed") from exc
    except ValueError as exc:
        raise NasaApiError("NASA API returned invalid JSON") from exc
    except Exception as exc:
        LOGGER.exception("Unexpected NASA API failure for %s", url)
        raise NasaApiError("Unexpected NASA API error") from exc


def get_nasa_apod(
    requested_date: str | None = None,
    session: requests.sessions.Session | None = None,
) -> dict[str, Any]:
    """Retrieve NASA's APOD payload for a specific day or the latest item."""
    params: dict[str, Any] = {"api_key": NASA_API_KEY}
    if requested_date:
        params["date"] = _parse_date(requested_date).isoformat()
    return make_api_request(NASA_APOD_URL, params, timeout=10, session=session)


def _extract_image_url(item: dict[str, Any]) -> str | None:
    for link in item.get("links", []):
        if link.get("render") == "image" and link.get("href"):
            return link["href"]
    return None


def search_nasa_images(
    query: str,
    size: int = 3,
    session: requests.sessions.Session | None = None,
) -> dict[str, Any]:
    """Search NASA's image library and return a compact, MCP-friendly payload."""
    cleaned_query = query.strip()
    if not cleaned_query:
        raise ValueError("query must not be blank")
    if not 1 <= size <= 25:
        raise ValueError("size must be between 1 and 25")

    params = {
        "q": cleaned_query,
        "media_type": "image",
        "page": 1,
        "page_size": size,
    }
    payload = make_api_request(NASA_IMAGE_SEARCH_URL, params, timeout=15, session=session)

    items: list[dict[str, Any]] = []
    for item in payload.get("collection", {}).get("items", []):
        metadata = (item.get("data") or [{}])[0]
        items.append(
            {
                "title": metadata.get("title"),
                "description": metadata.get("description"),
                "date_created": metadata.get("date_created"),
                "nasa_id": metadata.get("nasa_id"),
                "image_url": _extract_image_url(item),
            }
        )

    return {"query": cleaned_query, "count": len(items), "items": items}
