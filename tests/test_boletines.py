"""
Unit tests for boletines category
"""
import unittest

import requests

from tests.load_env import config


class TestBoletines(unittest.TestCase):
    """Tests for boletines category"""

    def test_get_boletines(self):
        """Test GET method for boletines"""
        response = requests.get(
            f"{config['api_base_url']}/boletines",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_boletines_with_estado(self):
        """Test GET method for boletines with estado BORRADOR"""
        response = requests.get(
            f"{config['api_base_url']}/boletines",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
            params={"estado": "BORRADOR"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["estado"], "BORRADOR")


if __name__ == "__main__":
    unittest.main()
