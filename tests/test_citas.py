"""
Unit tests for the citas category
"""
import unittest

import requests

from tests.load_env import config


class TestCitas(unittest.TestCase):
    """Tests for citas category"""

    def test_get_cit_dias_inhabiles(self):
        """Test GET method for cit_dias_inhabiles"""
        response = requests.get(
            f"{config['host']}/v4/cit_dias_inhabiles",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
