from unittest import TestCase
from unittest.mock import patch

from presentation import get_new_client_data


class PresentationTest(TestCase):
    def test_get_new_bookmark_data(self):
        with patch("builtins.input", side_effect=["mock_title", "mock_url", "mock_notes"]):
            result = get_new_client_data()
            self.assertEqual(
                result,
                {
                    "client_name": "mock_title",
                    "url": "mock_url",
                    "notes": "mock_notes"
                }
            )
