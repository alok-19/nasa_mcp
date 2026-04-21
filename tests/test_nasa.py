import unittest
from unittest.mock import Mock

import requests

from api.nasa import (
    NasaApiError,
    get_nasa_apod,
    make_api_request,
    search_nasa_images,
)


class MakeApiRequestTests(unittest.TestCase):
    def test_returns_json_payload_on_success(self) -> None:
        response = Mock()
        response.json.return_value = {"ok": True}
        response.raise_for_status.return_value = None

        session = Mock()
        session.get.return_value = response

        payload = make_api_request(
            "https://example.test",
            {"q": "moon"},
            timeout=5,
            session=session,
        )

        self.assertEqual(payload, {"ok": True})
        session.get.assert_called_once_with(
            "https://example.test",
            params={"q": "moon"},
            timeout=5,
        )

    def test_wraps_request_failures(self) -> None:
        session = Mock()
        session.get.side_effect = requests.exceptions.ConnectionError("boom")

        with self.assertRaises(NasaApiError) as context:
            make_api_request("https://example.test", {"q": "moon"}, session=session)

        self.assertIn("NASA API request failed", str(context.exception))


class ApodTests(unittest.TestCase):
    def test_rejects_invalid_date_format(self) -> None:
        with self.assertRaises(ValueError):
            get_nasa_apod("2026/01/01")

    def test_rejects_dates_before_apod_launch(self) -> None:
        with self.assertRaises(ValueError):
            get_nasa_apod("1995-06-15")


class SearchNasaImagesTests(unittest.TestCase):
    def test_rejects_blank_queries(self) -> None:
        with self.assertRaises(ValueError):
            search_nasa_images("   ")

    def test_rejects_invalid_page_size(self) -> None:
        with self.assertRaises(ValueError):
            search_nasa_images("mars", size=0)

    def test_normalizes_search_results(self) -> None:
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "collection": {
                "items": [
                    {
                        "data": [
                            {
                                "title": "Mars Rover",
                                "description": "A rover on Mars",
                                "date_created": "2020-01-01T00:00:00Z",
                                "nasa_id": "mars-rover",
                            }
                        ],
                        "links": [
                            {
                                "href": "https://images.test/mars.jpg",
                                "render": "image",
                            }
                        ],
                    }
                ]
            }
        }
        session = Mock()
        session.get.return_value = response

        payload = search_nasa_images("mars", size=1, session=session)

        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["items"][0]["title"], "Mars Rover")
        self.assertEqual(payload["items"][0]["image_url"], "https://images.test/mars.jpg")


if __name__ == "__main__":
    unittest.main()
