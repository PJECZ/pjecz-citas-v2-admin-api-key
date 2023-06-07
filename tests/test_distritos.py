"""
Unit tests for distritos category
"""
import os
import unittest

from dotenv import load_dotenv
import requests

load_dotenv()


class TestDistritos(unittest.TestCase):
    """Tests for distritos category"""

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

    def test_get_distritos(self):
        """Test GET method for distritos"""
        response = requests.get(f"{self.host}/v3/distritos", headers={"X-Api-Key": self.api_key}, timeout=self.timeout)
        self.assertEqual(response.status_code, 200)

    def test_get_distritos_by_es_distrito_judicial(self):
        """Test GET method for distritos by es_distrito_judicial"""
        response = requests.get(f"{self.host}/v3/distritos", headers={"X-Api-Key": self.api_key}, params={"es_distrito_judicial": 1}, timeout=self.timeout)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)

    def test_get_distritos_by_es_distrito(self):
        """Test GET method for distritos by es_distrito"""
        response = requests.get(f"{self.host}/v3/distritos", headers={"X-Api-Key": self.api_key}, params={"es_distrito": 1}, timeout=self.timeout)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)

    def test_get_distritos_by_es_jurisdiccional(self):
        """Test GET method for distritos by es_jurisdiccional"""
        response = requests.get(f"{self.host}/v3/distritos", headers={"X-Api-Key": self.api_key}, params={"es_jurisdiccional": 1}, timeout=self.timeout)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["success"], True)


if __name__ == "__main__":
    unittest.main()
