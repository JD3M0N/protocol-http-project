import socket
from src.protocol.http_protocol import HTTPProtocol

class HTTPClient:
    def __init__(self):
        self.protocol = HTTPProtocol()
        self.timeout = 10  # segundos
    
    def get(self, url):
        """Realiza una solicitud GET básica a una URL"""
        host, path = self._parse_url(url)
        request = self.protocol.create_get_request(host, path)
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((host, 80))
                s.sendall(request.encode())
                response = self._receive_all(s)
                return response
        except Exception as e:
            return f"Error: {str(e)}"
    
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