# server.py

from __future__ import annotations

import socket
import time

# import killable threads and normal threads
from kthread import KThread  # type: ignore
import threading

# import dict
from typing import Dict


class Server:
    def __init__(self, gui: ServerGUI):
        self.clients: Dict[
            str, ClientHandler
        ] = {}  # Dictionary to hold client username and ClientHandler object
        self.channels: Dict[str, set[str]] = {
            "IF 100": set(),
            "SPS 101": set(),
        }  # Channel subscribers
        self.gui = gui

        # Adding locks for thread safety
        self.clients_lock = threading.Lock()
        self.channels_lock = threading.Lock()

        # run the controller
        threading.Thread(target=self.server_thread_controller, daemon=True).start()

    def add_client(self, username, client_handler: ClientHandler) -> bool:
        """
        Add a new client to the server.
        """
        with self.clients_lock:  # Acquire lock for clients dictionary
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
        with self.clients_lock:  # Acquire lock for clients dictionary
            if username in self.clients:
                del self.clients[username]

        with self.channels_lock:  # Acquire lock for channels dictionary
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

    def _start_server(self, host, port, server, gui: ServerGUI):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self.server_socket = server_socket
            server_socket.bind((host, port))
            server_socket.listen()
            print(f"Server listening on {host}:{port}")

            while True:
                client_socket, client_address = server_socket.accept()
                client_handler = ClientHandler(
                    client_socket, client_address, server, gui
                )
                threading.Thread(target=client_handler.handle_client).start()

    def server_thread_controller(self):
        """
        This function runs in a thread. Periodically checks for whether
        the gui.running is true or not. If true, runs the start_server
        in a seperate killable thread. If not, checks if the seperate thread
        is running and kills it.
        """
        while True:
            if self.gui.running.get():
                if not hasattr(self, "server_thread"):
                    self.server_thread = KThread(
                        target=self._start_server,
                        args=(
                            self.gui.host_entry.get(),
                            int(self.gui.port_entry.get()),
                            self,
                            self.gui,
                        ),
                        daemon=True,
                    )
                    self.server_thread.start()
            else:
                if hasattr(self, "server_thread"):
                    if self.server_thread.is_alive():
                        self.server_thread.kill()
                        del self.server_thread

                        # Acquire locks before modifying shared resources
                        with self.clients_lock:
                            # Close the connections
                            while self.clients:
                                client = next(iter(self.clients))
                                self.clients[client].disconnect_client()
                            self.clients.clear()

                        with self.channels_lock:
                            self.channels = {"IF 100": set(), "SPS 101": set()}

                        # Update the GUI
                        self.update_gui_clients()
                        self.update_gui_channels()

                        # Close the socket
                        self.server_socket.close()

            time.sleep(0.1)

    def update_gui_clients(self):
        with self.clients_lock:  # Acquire lock for reading clients dictionary
            clients_list = [username for username in self.clients]
        self.gui.update_clients_list(clients_list)

    def update_gui_channels(self):
        with self.channels_lock:  # Acquire lock for reading channels dictionary
            for channel in self.channels:
                self.gui.update_channel_subscribers(
                    channel, [username for username in self.channels[channel]]
                )


from server_gui import ServerGUI
from client_handler import ClientHandler
