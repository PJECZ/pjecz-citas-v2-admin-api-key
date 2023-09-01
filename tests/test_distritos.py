"""
Unit tests for distritos category
"""
import unittest

import requests

from tests.load_env import config


class TestDistritos(unittest.TestCase):
    """Tests for distritos category"""

    def test_get_distritos(self):
        """Test GET method for distritos"""
        response = requests.get(
            f"{config['host']}/v4/distritos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_distritos_by_es_distrito_judicial(self):
        """Test GET method for distritos by es_distrito_judicial"""
        response = requests.get(
            f"{config['host']}/v4/distritos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
            params={"es_distrito_judicial": 1},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)

    def test_get_distritos_by_es_distrito(self):
        """Test GET method for distritos by es_distrito"""
        response = requests.get(
            f"{config['host']}/v4/distritos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
            params={"es_distrito": 1},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)

    def test_get_distritos_by_es_jurisdiccional(self):
        """Test GET method for distritos by es_jurisdiccional"""
        response = requests.get(
            f"{config['host']}/v4/distritos",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
            params={"es_jurisdiccional": 1},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)


if __name__ == "__main__":
    unittest.main()
