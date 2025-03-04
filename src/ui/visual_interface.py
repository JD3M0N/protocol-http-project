import tkinter as tk
from tkinter import ttk, scrolledtext
from src.client.http_client import HTTPClient

class HTTPClientGUI:
    def __init__(self, master):
        self.master = master
        self.client = HTTPClient()
        self.headers = {}
        
        master.title("HTTP Client GUI")
        self._create_widgets()
    
    def _create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Método HTTP
        ttk.Label(main_frame, text="Método:").grid(row=0, column=0, sticky="w")
        self.method_var = tk.StringVar(value="GET")
        method_combobox = ttk.Combobox(main_frame, textvariable=self.method_var, 
                                     values=["GET", "POST", "PUT", "DELETE", "HEAD"])
        method_combobox.grid(row=0, column=1, sticky="ew")
        method_combobox.bind("<<ComboboxSelected>>", self._toggle_body_input)

        # URL
        ttk.Label(main_frame, text="URL:").grid(row=1, column=0, sticky="w")
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=1, columnspan=2, sticky="ew")

        # Headers
        ttk.Label(main_frame, text="Headers:").grid(row=2, column=0, sticky="nw")
        self.header_key = ttk.Entry(main_frame, width=15)
        self.header_key.grid(row=2, column=1, sticky="ew")
        self.header_value = ttk.Entry(main_frame, width=25)
        self.header_value.grid(row=2, column=2, sticky="ew")
        ttk.Button(main_frame, text="Agregar", command=self._add_header).grid(row=2, column=3)

        # Cuerpo
        ttk.Label(main_frame, text="Cuerpo:").grid(row=3, column=0, sticky="nw")
        self.body_text = scrolledtext.ScrolledText(main_frame, width=50, height=8)
        self.body_text.grid(row=3, column=1, columnspan=3, sticky="ew")

        # Botón de enviar
        ttk.Button(main_frame, text="Enviar Solicitud", command=self._send_request).grid(row=4, column=1, pady=10)

        # Respuesta
        ttk.Label(main_frame, text="Respuesta:").grid(row=5, column=0, sticky="nw")
        self.response_text = scrolledtext.ScrolledText(main_frame, width=50, height=15)
        self.response_text.grid(row=5, column=1, columnspan=3, sticky="ew")

        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
    
    def _toggle_body_input(self, event=None):
        """Habilita/deshabilita el área de cuerpo según el método"""
        method = self.method_var.get()
        if method in ["POST", "PUT"]:
            self.body_text.config(state=tk.NORMAL)
        else:
            self.body_text.delete("1.0", tk.END)
            self.body_text.config(state=tk.DISABLED)
    
    def _add_header(self):
        """Agrega un header a la lista"""
        key = self.header_key.get().strip()
        value = self.header_value.get().strip()
        if key and value:
            self.headers[key] = value
            self.header_key.delete(0, tk.END)
            self.header_value.delete(0, tk.END)
    
    def _send_request(self):
        """Ejecuta la solicitud y muestra la respuesta"""
        method = self.method_var.get()
        url = self.url_entry.get().strip()
        body = self.body_text.get("1.0", tk.END).strip() if method in ["POST", "PUT"] else ""
        
        try:
            response = self._execute_method(method, url, body)
            self._display_response(response)
        except Exception as e:
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, f"Error: {str(e)}")
    
    def _execute_method(self, method, url, body):
        """Ejecuta el método HTTP correspondiente"""
        methods = {
            "GET": self.client.get,
            "POST": lambda: self.client.post(url, body, self.headers),
            "PUT": lambda: self.client.put(url, body, self.headers),
            "DELETE": lambda: self.client.delete(url, self.headers),
            "HEAD": lambda: self.client.head(url, self.headers)
        }
        return methods[method.upper()]()
    
    def _display_response(self, response):
        """Formatea y muestra la respuesta"""
        self.response_text.delete("1.0", tk.END)
        
        # Separar headers y cuerpo
        parts = response.split("\r\n\r\n", 1)
        headers = parts[0]
        body = parts[1] if len(parts) > 1 else ""
        
        # Mostrar con formato
        self.response_text.insert(tk.END, "=== Headers ===\n")
        self.response_text.insert(tk.END, headers + "\n\n")
        self.response_text.insert(tk.END, "=== Cuerpo ===\n")
        self.response_text.insert(tk.END, body)
    
    def run(self):
        self.master.mainloop()