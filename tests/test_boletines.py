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
            f"{config['host']}/v4/boletines",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_boletines_with_estado(self):
        """Test GET method for boletines with estado BORRADOR"""
        params = {"estado": "BORRADOR"}
        response = requests.get(
            f"{config['host']}/v4/boletines",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
            params=params,
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
