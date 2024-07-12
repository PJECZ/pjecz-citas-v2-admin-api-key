"""
Unit tests for autoridades category
"""
import unittest

import requests

from tests.load_env import config


class TestAutoridades(unittest.TestCase):
    """Tests for autoridades category"""

    def test_get_autoridades(self):
        """Test GET method for autoridades"""
        response = requests.get(
            url=f"{config['api_base_url']}/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
        )
        self.assertEqual(response.status_code, 200)

    def test_get_autoridades_by_es_jurisdiccional(self):
        """Test GET method for autoridades by es_jurisdiccional"""
        response = requests.get(
            url=f"{config['api_base_url']}/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
            params={"es_jurisdiccional": 1},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_jurisdiccional"], 1)

    def test_get_autoridades_by_es_organo_especializado(self):
        """Test GET method for autoridades by es_organo_especializado"""
        response = requests.get(
            f"{config['api_base_url']}/autoridades",
            headers={"X-Api-Key": config["api_key"]},
            timeout=config["timeout"],
            params={"es_organo_especializado": 1},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        for item in data["items"]:
            self.assertEqual(item["es_organo_especializado"], 1)


if __name__ == "__main__":
    unittest.main()
