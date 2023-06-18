"""
Unit tests for boletines category
"""
import os
import unittest

from dotenv import load_dotenv
import requests

load_dotenv()


class TestBoletines(unittest.TestCase):
    """Tests for boletines category"""

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

    def test_get_boletines(self):
        """Test GET method for boletines"""
        response = requests.get(f"{self.host}/v3/boletines", headers={"X-Api-Key": self.api_key}, timeout=self.timeout)
        self.assertEqual(response.status_code, 200)

    def test_get_boletines_with_estado(self):
        """Test GET method for boletines with estado BORRADOR"""
        params = {"estado": "BORRADOR"}
        response = requests.get(f"{self.host}/v3/boletines", headers={"X-Api-Key": self.api_key}, params=params, timeout=self.timeout)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
