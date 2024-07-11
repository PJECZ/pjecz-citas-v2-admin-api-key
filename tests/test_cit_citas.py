"""
Unit tests for the cit citas category
"""
import unittest

import requests

from tests.load_env import config


class TestCitCitas(unittest.TestCase):
    """Tests for cit citas category"""

    def test_get_cit_citas(self):
        """Test GET method for cit_citas"""
        response = requests.get(
            url=f"{config['api_base_url']}/cit_citas",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
