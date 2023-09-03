"""
Unit tests for oficinas category
"""
import unittest

import requests

from tests.load_env import config


class TestOficinas(unittest.TestCase):
    """Tests for oficinas category"""

    def test_get_domicilios(self):
        """Test GET method for domicilios"""
        response = requests.get(
            f"{config['api_base_url']}/domicilios",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_oficinas(self):
        """Test GET method for oficinas"""
        response = requests.get(
            f"{config['api_base_url']}/oficinas",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
