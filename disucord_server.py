# server.py

# Necessary imports
from __future__ import annotations
import socket
import time

# import killable threads and normal threads
from kthread import KThread  # type: ignore
import threading
from typing import Dict
from constants import *


class Server:
    def __init__(self, gui: ServerGUI):
        # Initialize clients and channels dictionaries for managing connections and subscriptions
        self.clients: Dict[str, ClientHandler] = {}
        self.channels: Dict[str, set[str]] = {"IF 100": set(), "SPS 101": set()}
        self.gui = gui  # GUI reference for server

        # Thread locks for ensuring thread safety
        self.clients_lock = threading.Lock()
        self.channels_lock = threading.Lock()

        # Flag for server shutdown status
        self.is_shutting_down = False

        # Start the server control thread
        threading.Thread(target=self.server_thread_controller, daemon=True).start()

    def add_client(self, username, client_handler: ClientHandler) -> bool:
        """
        Add a new client to the server. Ensures unique usernames.
        """
        with self.clients_lock:  # Ensure thread-safe access to clients dictionary
            if username in self.clients:
                client_handler.send_message(
                    f"[{SERVER_ALIAS}]: Username already taken."
                )
                self.gui.append_server_log(
                    f"[{SERVER_ALIAS}]: Connection attempt with taken username `{username}` from {client_handler.client_address[0]}:{client_handler.client_address[1]}"
                )
                return False
            self.clients[username] = client_handler
            client_handler.send_message(f"[{SERVER_ALIAS}]: Connected successfully.")
            self.gui.append_server_log(
                f"[{SERVER_ALIAS}]: New connection from {client_handler.client_address[0]}:{client_handler.client_address[1]} as `{username}`"
            )

        self.update_gui_clients()  # Update GUI with new client list
        return True

    def remove_client(self, username: str):
        """
        Remove a client from the server and all channels they are subscribed to.
        """
        with self.clients_lock:  # Handle client removal
            if username in self.clients:
                del self.clients[username]

        with self.channels_lock:  # Update channel subscriptions
            for channel in self.channels:
                if username in self.channels[channel]:
                    self.channels[channel].remove(username)

        self.gui.append_server_log(f"[{SERVER_ALIAS}]: `{username}` disconnected.")
        self.update_gui_clients_and_channels()  # Update GUI lists

    def subscribe_client_to_channel(self, username, channel):
        """
        Subscribe a client to a specific channel.
        """
        if channel in self.channels and username in self.clients:
            self.channels[channel].add(username)
            self.clients[username].send_message(
                f"[{SERVER_ALIAS}]: Subscribed to {channel}"
            )
            self.gui.append_server_log(
                f"[{SERVER_ALIAS}]: `{username}` subscribed to {channel}"
            )
            self.update_gui_channels()  # Update GUI channel subscribers list

    def unsubscribe_client_from_channel(self, username, channel):
        """
        Unsubscribe a client from a specific channel.
        """
        if channel in self.channels and username in self.clients:
            if username in self.channels[channel]:
                self.channels[channel].remove(username)
                self.clients[username].send_message(
                    f"[{SERVER_ALIAS}]: Unsubscribed from {channel}"
                )
                self.gui.append_server_log(
                    f"[{SERVER_ALIAS}]: `{username}` unsubscribed from {channel}"
                )
                self.update_gui_channels()  # Update GUI channel subscribers list

    def broadcast_message(self, channel, sender_username, message):
        """
        Broadcast a message to all subscribers of a channel.
        """
        if channel in self.channels:
            for username in self.channels[channel]:
                if username in self.clients:
                    prefix = f"[{channel}] {sender_username}: "
                    self.clients[username].send_message(prefix + message)
                    self.gui.append_server_log(prefix + message)  # Log the message

    def _start_server(self, host, port, server, gui: ServerGUI):
        """
        Function to start the server socket and listen for client connections.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self.server_socket = server_socket
            server_socket.settimeout(1)  # Timeout for non-blocking accept call
            server_socket.bind((host, port))
            server_socket.listen()
            self.gui.append_server_log(f"Server listening on {host}:{port}")

            while not self.is_shutting_down:
                try:
                    client_socket, client_address = server_socket.accept()
                    client_handler = ClientHandler(
                        client_socket, client_address, server, gui
                    )
                    threading.Thread(target=client_handler.handle_client).start()
                    self.gui.append_server_log(
                        f"New client handler thread started for {client_address}"
                    )
                except socket.timeout:
                    continue  # Skip iteration on timeout
                except socket.error as e:
                    self.gui.append_server_log(f"Error accepting connection: {e}")

    def server_thread_controller(self):
        """
        Controller thread for managing server start and shutdown.
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
                    self.gui.append_server_log("Server thread started")
            else:
                if hasattr(self, "server_thread"):
                    print(f"Server thread exists, will kill if alive")
                    if self.server_thread.is_alive():
                        print(f"Server thread is alive, will kill")
                        self.server_thread.kill()
                        del self.server_thread
                        print(f"Server thread killed and deleted")

                        # Acquire locks before modifying shared resources
                        print(f"Acquiring locks to modify shared resources")
                        print(
                            f"Setting shutdown flag and acquiring locks to modify shared resources"
                        )
                        self.is_shutting_down = True

                        # Create a list of clients to disconnect
                        clients_to_disconnect = []
                        with self.clients_lock:
                            clients_to_disconnect = list(self.clients.keys())

                        # Disconnect each client
                        for client in clients_to_disconnect:
                            self.clients[client].disconnect_client()

                        with self.clients_lock:
                            self.clients.clear()

                        with self.channels_lock:
                            self.channels = {"IF 100": set(), "SPS 101": set()}

                        print(f"We will update the GUI with cleaning the slate")

                        # Update the GUI
                        self.update_gui_clients()
                        self.update_gui_channels()

                        # Close the socket
                        self.server_socket.close()

                        # Finished shutting down, reset the flag
                        self.is_shutting_down = False

            time.sleep(0.1)

    def update_gui_clients_and_channels(self):
        """
        Update GUI with current clients and channel subscribers.
        """
        self.update_gui_clients()
        self.update_gui_channels()

    def update_gui_clients(self):
        """
        Update the GUI with the current list of clients.
        """
        with self.clients_lock:
            clients_list = [username for username in self.clients]
        self.gui.update_clients_list(clients_list)

    def update_gui_channels(self):
        """
        Update the GUI with the current list of channel subscribers.
        """
        with self.channels_lock:
            for channel in self.channels:
                self.gui.update_channel_subscribers(
                    channel, [username for username in self.channels[channel]]
                )


from server_gui import ServerGUI
from client_handler import ClientHandler
