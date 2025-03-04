import argparse
from src.ui.console_interface import ConsoleInterface
from src.ui.visual_interface import HTTPClientGUI
import tkinter as tk

def main():
    parser = argparse.ArgumentParser(description="Cliente HTTP")
    parser.add_argument("--gui", action="store_true", help="Ejecutar interfaz gráfica")
    args = parser.parse_args()

    if args.gui:
        root = tk.Tk()
        app = HTTPClientGUI(root)
        app.run()
    else:
        cli = ConsoleInterface()
        cli.start()

if __name__ == "__main__":
    main()