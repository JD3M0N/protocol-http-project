import socket
from src.protocol.http_protocol import HTTPProtocol

class HTTPClient:
    def __init__(self):
        self.protocol = HTTPProtocol()
        self.timeout = 10
    
    def _send_request(self, host, request):
        """Método común para enviar cualquier tipo de solicitud"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((host, 80))
                s.sendall(request.encode())
                return self._receive_all(s)
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Métodos específicos
    def get(self, url, headers=None):
        host, path = self._parse_url(url)
        request = self.protocol.create_get_request(host, path, headers)
        return self._send_request(host, request)
    
    def post(self, url, body="", headers=None):
        host, path = self._parse_url(url)
        request = self.protocol.create_post_request(host, path, body, headers)
        return self._send_request(host, request)
    
    def put(self, url, body="", headers=None):
        host, path = self._parse_url(url)
        request = self.protocol.create_put_request(host, path, body, headers)
        return self._send_request(host, request)
    
    def delete(self, url, headers=None):
        host, path = self._parse_url(url)
        request = self.protocol.create_delete_request(host, path, headers)
        return self._send_request(host, request)
    
    def head(self, url, headers=None):
        host, path = self._parse_url(url)
        request = self.protocol.create_head_request(host, path, headers)
        return self._send_request(host, request)
    
    def _parse_url(self, url):
        """Extrae host y path de una URL simple (sin soporte para HTTPS o puertos personalizados)"""
        url = url.replace("http://", "")
        parts = url.split("/", 1)
        host = parts[0]
        path = "/" + parts[1] if len(parts) > 1 else "/"
        return host, path
    
    def _receive_all(self, sock):
        """Lee todos los datos de la respuesta hasta que se cierra la conexión"""
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        return response.decode(errors="ignore")