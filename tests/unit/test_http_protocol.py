import unittest
from src.protocol.http_protocol import HTTPProtocol

class TestHTTPProtocol(unittest.TestCase):
    def test_post_request(self):
        request = HTTPProtocol.create_post_request(
            host="api.example.com",
            path="/data",
            body="name=John&age=30",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        expected = (
            "POST /data HTTP/1.1\r\n"
            "Host: api.example.com\r\n"
            "Connection: close\r\n"
            "User-Agent: PythonHTTPClient/1.0\r\n"
            "Content-Length: 16\r\n"
            "Content-Type: application/x-www-form-urlencoded\r\n\r\n"
            "name=John&age=30"
        )
        self.assertEqual(request, expected)

    def test_head_request(self):
        request = HTTPProtocol.create_head_request("example.com", "/status")
        self.assertIn("HEAD /status HTTP/1.1", request)
        self.assertIn("Host: example.com", request)
        self.assertNotIn("Content-Length", request)