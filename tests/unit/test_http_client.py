import unittest
from src.client.http_client import HTTPClient

class TestHTTPClient(unittest.TestCase):
    def test_post_request(self):
        client = HTTPClient()
        response = client.post(
            "http://httpbin.org/post",
            body="test=123",
            headers={"X-Custom-Header": "Hello"}
        )
        self.assertIn("HTTP/1.1 200 OK", response)
        self.assertIn('"test": "123"', response)
        self.assertIn('"X-Custom-Header": "Hello"', response)

    def test_delete_request(self):
        client = HTTPClient()
        response = client.delete("http://httpbin.org/delete")
        self.assertIn("HTTP/1.1 200 OK", response)