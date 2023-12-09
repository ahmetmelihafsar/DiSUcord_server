# server.py

from __future__ import annotations
import client_handler
import server_gui

# import dict
from typing import Dict


class Server:
    def __init__(self, gui: server_gui.ServerGUI):
        self.clients: Dict[
            str, client_handler.ClientHandler
        ] = {}  # Dictionary to hold client username and ClientHandler object
        self.channels: Dict[str, set[str]] = {
            "IF 100": set(),
            "SPS 101": set(),
        }  # Channel subscribers
        self.gui = gui

    def add_client(
        self, username, client_handler: client_handler.ClientHandler
    ) -> bool:
        """
        Add a new client to the server.
        """
        if username in self.clients:
            client_handler.send_message("Username already taken.")
            return False
        self.clients[username] = client_handler
        client_handler.send_message("Connected successfully.")

        # Update the GUI
        self.gui.update_clients_list([username for username in self.clients])

        return True

    def remove_client(self, username: str):
        """
        Remove a client from the server.
        """
        if username in self.clients:
            del self.clients[username]
            # Unsubscribe from channels
            for channel in self.channels:
                if username in self.channels[channel]:
                    self.channels[channel].remove(username)

            # Update the GUI
            self.gui.update_clients_list([username for username in self.clients])
            # Update the subscribers in the GUI
            for channel in self.channels:
                self.gui.update_channel_subscribers(
                    channel, [username for username in self.channels[channel]]
                )

    def subscribe_client_to_channel(self, username, channel):
        """
        Subscribe a client to a channel.
        """
        if channel in self.channels and username in self.clients:
            self.channels[channel].add(username)
            self.clients[username].send_message(f"Subscribed to {channel}")

            # Update the GUI
            self.gui.update_channel_subscribers(
                channel, [username for username in self.channels[channel]]
            )

    def unsubscribe_client_from_channel(self, username, channel):
        """
        Unsubscribe a client from a channel.
        """
        if channel in self.channels and username in self.clients:
            if username in self.channels[channel]:
                self.channels[channel].remove(username)
                self.clients[username].send_message(f"Unsubscribed from {channel}")

            # Update the GUI
            self.gui.update_channel_subscribers(
                channel, [username for username in self.channels[channel]]
            )

    def broadcast_message(self, channel, sender_username, message):
        """
        Broadcast a message to all subscribers of a channel.
        """
        if channel in self.channels:
            for username in self.channels[channel]:
                if username in self.clients:
                    prefix = f"[{channel}] {sender_username}: "
                    self.clients[username].send_message(prefix + message)

                # Update the GUI
                self.gui.append_server_log(prefix + message)
