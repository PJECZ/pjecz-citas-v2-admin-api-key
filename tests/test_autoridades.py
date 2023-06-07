"""
Unit tests for autoridades category
"""
import os
import unittest

from dotenv import load_dotenv
import requests

load_dotenv()


class TestAutoridades(unittest.TestCase):
    """Tests for autoridades category"""

    def setUp(self) -> None:
        """Initialize the test case"""
        # Load environment variables
        self.api_key = os.getenv("API_KEY", "")
        self.host = os.getenv("HOST", "")
        self.timeout = int(os.getenv("TIMEOUT", "20"))
        # If any of the environment variables is empty, raise an error
        if not self.api_key:
            raise ValueError("API_KEY environment variable is empty")
        if not self.host:
            raise ValueError("HOST environment variable is empty")
        if not self.timeout:
            raise ValueError("TIMEOUT environment variable is empty")
        # Return super
        return super().setUp()

    def test_get_autoridades(self):
        """Test GET method for autoridades"""
        response = requests.get(f"{self.host}/v3/autoridades", headers={"X-Api-Key": self.api_key}, timeout=self.timeout)
        self.assertEqual(response.status_code, 200)

    def test_get_autoridades_by_es_jurisdiccional(self):
        """Test GET method for autoridades by es_jurisdiccional"""
        response = requests.get(f"{self.host}/v3/autoridades", headers={"X-Api-Key": self.api_key}, params={"es_jurisdiccional": 1}, timeout=self.timeout)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        result = data["result"]
        self.assertGreater(result["total"], 0)  # Total of es_jurisdiccional is greater than 0

    def test_get_autoridades_by_es_organo_especializado(self):
        """Test GET method for autoridades by es_organo_especializado"""
        response = requests.get(f"{self.host}/v3/autoridades", headers={"X-Api-Key": self.api_key}, params={"es_organo_especializado": 1}, timeout=self.timeout)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)
        result = data["result"]
        self.assertGreater(result["total"], 0)  # Total of es_organo_especializado is greater than 0


if __name__ == "__main__":
    unittest.main()
