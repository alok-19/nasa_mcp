from mcp.server.fastmcp import FastMCP
from api.nasa import get_nasa_apod, search_nasa_images

mcp = FastMCP(
    name="NASA MCP",
    instructions=(
        "Provides NASA Astronomy Picture of the Day data and NASA image search "
        "results as structured tool responses."
    ),
)


@mcp.tool(name="get_nasa_apod", description="Fetch NASA APOD metadata for a given date.")
def get_apod_data(date: str | None = None) -> dict:
    """Get NASA's Astronomy Picture of the Day (APOD).

    Retrieves the featured astronomy image or video for a specific date,
    along with its title, explanation, and metadata from NASA's APOD service.

    Args:
        date: Optional date in YYYY-MM-DD format. If not provided, returns today's APOD.
              Must be between 1995-06-16 (first APOD) and today's date.

    Returns:
        JSON object containing APOD data including title, explanation, image URL,
        date, and other metadata, or error message if request fails.
    """
    try:
        return get_nasa_apod(date)
    except Exception as exc:
        return {"error": str(exc)}


@mcp.tool(
    name="search_images_data",
    description="Search NASA's image library and return compact image metadata.",
)
def search_images_data(q: str, size: int = 3) -> dict:
    """Search NASA's image and video library.

    Searches through NASA's extensive collection of images, videos, and audio files
    using keywords. Returns metadata and links to matching media assets.

    Args:
        q: Search query string. Can include keywords like mission names, celestial objects,
           astronauts, space phenomena, etc. (e.g., "Mars rover", "International Space Station")
        size: Number of results to return (default: 3). Recommended range: 1-20.

    Returns:
        JSON array containing search results with titles, descriptions, image URLs,
        dates, and other metadata for each matching item, or error message if search fails.
    """
    try:
        return search_nasa_images(query=q, size=size)
    except Exception as exc:
        return {"error": str(exc)}


def main():
    mcp.run()


if __name__ == "__main__":
    main()
