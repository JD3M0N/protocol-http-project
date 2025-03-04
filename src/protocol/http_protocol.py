class HTTPProtocol:
    @staticmethod
    def create_request(method, host, path="/", headers=None, body=""):
        """
        Crea una solicitud HTTP completa según RFC 7230.
        
        Args:
            method (str): Método HTTP (GET, POST, etc.)
            host (str): Servidor objetivo
            path (str): Ruta del recurso
            headers (dict): Headers personalizados
            body (str): Cuerpo de la solicitud (para POST/PUT)
        """
        # Headers básicos (RFC 7230)
        default_headers = {
            "Host": host,
            "Connection": "close",
            "User-Agent": "PythonHTTPClient/1.0"
        }
        
        # Merge con headers personalizados
        final_headers = {**default_headers, **(headers or {})}
        
        # Manejo de cuerpo (RFC 7230)
        # Convertir el cuerpo a bytes siempre
        body_bytes = body.encode("utf-8")
        if body_bytes:
            if "Content-Length" not in final_headers:
                final_headers["Content-Length"] = str(len(body_bytes))
            if "Content-Type" not in final_headers:
                final_headers["Content-Type"] = "application/x-www-form-urlencoded"
                
        # Forzamos un orden fijo para los headers
        fixed_order = ["Host", "Connection", "User-Agent", "Content-Length", "Content-Type"]
        headers_lines = []
        for key in fixed_order:
            if key in final_headers:
                headers_lines.append(f"{key}: {final_headers[key]}")
        # Agregar cualquier otro header que no esté en el orden fijo
        for key, value in final_headers.items():
            if key not in fixed_order:
                headers_lines.append(f"{key}: {value}")
        headers_section = "\r\n".join(headers_lines)
        
        # Construcción del mensaje (RFC 7230)
        request_line = f"{method} {path} HTTP/1.1\r\n"
        return f"{request_line}{headers_section}\r\n\r\n{body_bytes.decode('utf-8')}"

    # Métodos específicos para conveniencia
    @staticmethod
    def create_get_request(host, path="/", headers=None):
        return HTTPProtocol.create_request("GET", host, path, headers)
    
    @staticmethod
    def create_post_request(host, path="/", body="", headers=None):
        return HTTPProtocol.create_request("POST", host, path, headers, body)
    
    @staticmethod
    def create_put_request(host, path="/", body="", headers=None):
        return HTTPProtocol.create_request("PUT", host, path, headers, body)
    
    @staticmethod
    def create_delete_request(host, path="/", headers=None):
        return HTTPProtocol.create_request("DELETE", host, path, headers)
    
    @staticmethod
    def create_head_request(host, path="/", headers=None):
        return HTTPProtocol.create_request("HEAD", host, path, headers)