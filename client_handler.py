# client_handler.py
from __future__ import annotations

import socket
import re
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
        Special commands are separated by '\\x' and end with '\\e'.
        Double backslash '\\' is used to indicate a single backslash in data parts.
        """

        # Placeholder for a single backslash (choose a string that won't naturally occur in your messages)
        single_backslash_placeholder = "<SINGLE_BACKSLASH>"

        # Replace double backslashes with the placeholder
        message = message.replace('\\\\', single_backslash_placeholder)

        # Check for the end of the message
        if '\\e' in message:
            message = message.split('\\e')[0]

        # Split the message by the special separator '\x'
        parts = re.split(r'\\x+', message)

        # Process each part to replace the placeholder with a single backslash
        parts = [part.replace(single_backslash_placeholder, '\\') for part in parts]

        # Extract the main command and its parameters
        main_command = parts[0]
        parameters = parts[1:]

        # Process the main command
        if main_command == "SETNAME":
            self.username = parameters[0]
            is_added = self.server.add_client(self.username, self)
            if not is_added:
                self.disconnect_client()
                return
        elif main_command == "SUBSCRIBE":
            channel = parameters[0]
            self.server.subscribe_client_to_channel(self.username, channel)
        elif main_command == "UNSUBSCRIBE":
            channel = parameters[0]
            self.server.unsubscribe_client_from_channel(self.username, channel)
        elif main_command == "MESSAGE":
            channel, content = parameters
            self.server.broadcast_message(channel, self.username, content)
        else:
            print(f"Unknown command: {main_command}")

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
