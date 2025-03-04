import unittest
from src.protocol.http_protocol import HTTPProtocol

class TestHTTPProtocol(unittest.TestCase):
    def test_create_get_request(self):
        expected = "GET / HTTP/1.1\r\nHost: ejemplo.com\r\nConnection: close\r\n\r\n"
        self.assertEqual(HTTPProtocol.create_get_request("ejemplo.com"), expected)