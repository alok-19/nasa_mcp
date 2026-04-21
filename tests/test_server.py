import unittest
from unittest.mock import patch

import nasa_mcp_server


class ServerToolTests(unittest.TestCase):
    @patch("nasa_mcp_server.get_nasa_apod")
    def test_apod_tool_returns_structured_payload(self, mock_get_nasa_apod) -> None:
        mock_get_nasa_apod.return_value = {"title": "The Moon"}

        payload = nasa_mcp_server.get_apod_data("2024-01-01")

        self.assertEqual(payload, {"title": "The Moon"})

    @patch("nasa_mcp_server.search_nasa_images")
    def test_search_tool_returns_structured_payload(self, mock_search_nasa_images) -> None:
        mock_search_nasa_images.return_value = {"items": [], "count": 0}

        payload = nasa_mcp_server.search_images_data("moon", size=2)

        self.assertEqual(payload, {"items": [], "count": 0})

    @patch("nasa_mcp_server.get_nasa_apod")
    def test_apod_tool_surfaces_errors(self, mock_get_nasa_apod) -> None:
        mock_get_nasa_apod.side_effect = ValueError("bad date")

        payload = nasa_mcp_server.get_apod_data("bad")

        self.assertEqual(payload, {"error": "bad date"})


if __name__ == "__main__":
    unittest.main()
