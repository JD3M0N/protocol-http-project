class HTTPProtocol:
    @staticmethod
    def create_get_request(host, path="/"):
        """Crea una solicitud GET básica según RFC 7230"""
        request_line = f"GET {path} HTTP/1.1\r\n"
        headers = f"Host: {host}\r\nConnection: close\r\n\r\n"
        return request_line + headers