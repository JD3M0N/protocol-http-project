from src.client.http_client import HTTPClient

class ConsoleInterface:
    def __init__(self):
        self.client = HTTPClient()  # Instancia del cliente HTTP

    def start(self):
        print("Cliente HTTP Avanzado")
        while True:
            try:
                method = input("\nMétodo (GET/POST/PUT/DELETE/HEAD): ").upper()
                url = input("URL: ")

                if method in ["POST", "PUT"]:
                    body = input("Cuerpo (ej: key=value): ")
                    response = getattr(self.client, method.lower())(url, body)
                else:
                    response = getattr(self.client, method.lower())(url)

                print(f"\nRESPUESTA {method}:\n{response.split('\r\n\r\n')[0]}\n[...]")

            except Exception as e:
                print(f"Error: {str(e)}")
