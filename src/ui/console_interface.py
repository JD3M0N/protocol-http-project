from src.client.http_client import HTTPClient

class ConsoleInterface:
    def __init__(self):
        self.client = HTTPClient()
    
    def start(self):
        print("Cliente HTTP Minimalista (Ctrl+C para salir)")
        while True:
            try:
                url = input("\nIngrese URL (ej: http://ejemplo.com): ")
                response = self.client.get(url)
                print("\nRESPUESTA:\n" + response)
            except KeyboardInterrupt:
                print("\nSaliendo...")
                break
            except Exception as e:
                print(f"Error: {str(e)}")