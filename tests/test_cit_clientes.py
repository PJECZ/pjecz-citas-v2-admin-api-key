"""
Unit tests for the cit clientes category
"""
import unittest

import requests

from tests.load_env import config


class TestCitClientes(unittest.TestCase):
    """Tests for cit clientes category"""

    def test_get_cit_clientes(self):
        """Test GET method for cit_clientes"""
        response = requests.get(
            url=f"{config['api_base_url']}/cit_clientes",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
