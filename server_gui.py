from __future__ import annotations

import tkinter as tk
import socket
import threading
from tkinter import scrolledtext


class ServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("DiSUcord Server")

        # Server Log Frame
        self.log_frame = tk.LabelFrame(master, text="Server Log")
        self.log_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.log = scrolledtext.ScrolledText(self.log_frame, height=10, width=70)
        self.log.pack()
        self.log.bind(
            "<Key>", lambda e: "break"
        )  # this is done to ensure input from user is disabled

        # Connected Clients Frame
        self.clients_frame = tk.LabelFrame(master, text="Connected Clients")
        self.clients_frame.grid(row=1, column=0, padx=10, pady=10)

        self.clients_list = scrolledtext.ScrolledText(
            self.clients_frame, height=10, width=35
        )
        self.clients_list.pack()
        self.clients_list.bind(
            "<Key>", lambda e: "break"
        )  # this is done to ensure input from user is disabled

        # IF 100 Channel Subscribers Frame
        self.if_100_frame = tk.LabelFrame(master, text="IF 100 Channel Subscribers")
        self.if_100_frame.grid(row=1, column=1, padx=10, pady=10)

        self.if_100_list = scrolledtext.ScrolledText(
            self.if_100_frame, height=10, width=35
        )
        self.if_100_list.pack()
        self.if_100_list.bind(
            "<Key>", lambda e: "break"
        )  # this is done to ensure input from user is disabled

        # SPS 101 Channel Subscribers Frame
        self.sps_101_frame = tk.LabelFrame(master, text="SPS 101 Channel Subscribers")
        self.sps_101_frame.grid(row=2, column=0, padx=10, pady=10)

        self.sps_101_list = scrolledtext.ScrolledText(
            self.sps_101_frame, height=10, width=35
        )
        self.sps_101_list.pack()
        self.sps_101_list.bind(
            "<Key>", lambda e: "break"
        )  # this is done to ensure input from user is disabled

        # Entry for server host and port Frame
        self.entry_frame = tk.LabelFrame(master, text="Server Host and Port")
        self.entry_frame.grid(row=3, column=0, columnspan=2, padx=5)

        self.host_entry = tk.Entry(self.entry_frame, width=15)
        # insert a default value
        self.host_entry.insert(0, "127.0.0.1")

        self.host_entry.pack(side=tk.LEFT)
        self.port_entry = tk.Entry(self.entry_frame, width=5)
        self.port_entry.pack(side=tk.LEFT)
        # insert a default value
        self.port_entry.insert(0, "8080")

        # Start Button
        self.start_button = tk.Button(master, text="Start", command=self.start_server)
        self.start_button.grid(row=4, column=0, padx=10, pady=10)

        # Stop Button
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_server)
        self.stop_button.grid(row=4, column=1, padx=10, pady=10)

        # set running to false, but in tkinter variable
        self.running = tk.BooleanVar()
        self.running.set(False)

    def get_server_details(self):
        """
        Return the host and port from the GUI entries.
        """
        return self.host_entry.get(), int(self.port_entry.get())

    def append_server_log(self, message):
        """
        Update the server log with a new message.
        """
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)  # Auto-scroll to the bottom

    def update_clients_list(self, clients):
        """
        Update the list of connected clients.
        """
        self.clients_list.delete(1.0, tk.END)
        self.clients_list.insert(tk.END, "Connected Clients:\n")
        for client in clients:
            self.clients_list.insert(tk.END, client + "\n")

    def update_channel_subscribers(self, channel, subscribers):
        """
        Update the subscriber list for a specific channel.
        """
        if channel == "IF 100":
            self.if_100_list.delete(1.0, tk.END)
            self.if_100_list.insert(tk.END, "IF 100 Subscribers:\n")
            for subscriber in subscribers:
                self.if_100_list.insert(tk.END, subscriber + "\n")
        elif channel == "SPS 101":
            self.sps_101_list.delete(1.0, tk.END)
            self.sps_101_list.insert(tk.END, "SPS 101 Subscribers:\n")
            for subscriber in subscribers:
                self.sps_101_list.insert(tk.END, subscriber + "\n")
        else:
            # Popup error
            pass

    def stop_server(self):
        self.running.set(False)

        # set button disabled
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

        self.append_server_log("Server stopped.")

    def start_server(self):
        self.running.set(True)

        # set buttons
        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

        self.append_server_log("Server started.")
