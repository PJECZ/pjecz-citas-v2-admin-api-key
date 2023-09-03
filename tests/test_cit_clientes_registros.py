"""
Unit tests for the cit clientes registros category
"""
import unittest

import requests

from tests.load_env import config


class TestCitClientesRegistros(unittest.TestCase):
    """Tests for cit clientes registros category"""

    def test_get_cit_clientes_registros(self):
        """Test GET method for cit_clientes_registros"""
        response = requests.get(
            f"{config['api_base_url']}/cit_clientes_registros",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
