"""
Unit tests for the cit dias inhabiles category
"""
import unittest

import requests

from tests.load_env import config


class TestCitDiasInhabiles(unittest.TestCase):
    """Tests for cit dias inhabiles category"""

    def test_get_cit_dias_inhabiles(self):
        """Test GET method for cit_dias_inhabiles"""
        response = requests.get(
            f"{config['api_base_url']}/cit_dias_inhabiles",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
