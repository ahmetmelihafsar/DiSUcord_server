# main.py
from __future__ import annotations

import socket
import threading
from tkinter import Tk
from server_gui import ServerGUI
from client_handler import ClientHandler
from disucord_server import Server


def start_server(host, port, server, gui):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = ClientHandler(client_socket, client_address, server, gui)
            threading.Thread(target=client_handler.handle_client).start()


if __name__ == "__main__":
    # Assuming you have a method in ServerGUI to get server details
    root = Tk()
    server_gui = ServerGUI(root)
    host, port = server_gui.get_server_details()

    server = Server(server_gui)  # Create an instance of the Server class

    # Start the server in a separate thread
    threading.Thread(target=start_server, args=(host, port, server, server_gui)).start()

    root.mainloop()  # Start the Tkinter event loop
