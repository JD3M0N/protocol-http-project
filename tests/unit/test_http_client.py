import unittest
from src.client.http_client import HTTPClient

class TestHTTPClient(unittest.TestCase):
    def test_get_request(self):
        client = HTTPClient()
        response = client.get("http://httpbin.org/get")
        self.assertIn("HTTP/1.1 200 OK", response)
        self.assertIn('"Host": "httpbin.org"', response)