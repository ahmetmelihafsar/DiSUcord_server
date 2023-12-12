# main.py
from __future__ import annotations

from tkinter import Tk
from server_gui import ServerGUI
from disucord_server import Server

if __name__ == "__main__":
    root = Tk()
    server_gui = ServerGUI(root)

    server = Server(server_gui)  # Create an instance of the Server class

    root.mainloop()  # Start the Tkinter event loop
