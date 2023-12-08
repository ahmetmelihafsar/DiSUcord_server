# client_handler.py
from __future__ import annotations

import socket
import disucord_server
import server_gui


class ClientHandler:
    def __init__(self, client_socket: socket.socket, client_address, server, gui):
        self.client_socket = client_socket
        self.client_address = client_address
        self.server: disucord_server.Server = server
        self.gui: server_gui.ServerGUI = gui
        self.username = ""
        self.running = True

    def handle_client(self):
        """
        Main loop for handling client interactions.
        """
        try:
            while self.running:
                message = self.client_socket.recv(1024).decode("utf-8")
                if message:
                    print(f"Received message from {self.username}: {message}")
                    self.process_message(message)
                else:
                    print(f"Client {self.username} disconnected")
                    self.disconnect_client()
        except socket.error as e:
            print(f"Socket error: {e}")
        finally:
            self.disconnect_client()

    def process_message(self, message: str):
        """
        Process incoming messages from the client.
        """
        if message.startswith("SETNAME"):
            self.username = message.removeprefix("SETNAME ")
            is_added = self.server.add_client(self.username, self)
            if not is_added:
                self.disconnect_client()
                return
        elif message.startswith("SUBSCRIBE"):
            channel = message.removeprefix("SUBSCRIBE ")
            self.server.subscribe_client_to_channel(self.username, channel)
        elif message.startswith("UNSUBSCRIBE"):
            channel = message.removeprefix("UNSUBSCRIBE ")
            self.server.unsubscribe_client_from_channel(self.username, channel)
        elif message.startswith("MESSAGE"):
            channel, content = message.split(" ", 2)[1:]
            self.server.broadcast_message(channel, self.username, content)
        # Add other message processing as needed

    def send_message(self, message: str):
        """
        Send a message to the client.
        """
        try:
            self.client_socket.send(message.encode("utf-8"))
        except socket.error as e:
            print(f"Error sending message to {self.username}: {e}")

    def disconnect_client(self):
        """
        Disconnect the client.
        """
        self.running = False
        self.server.remove_client(self.username)
        self.client_socket.close()
        print(f"Client {self.username} disconnected")
