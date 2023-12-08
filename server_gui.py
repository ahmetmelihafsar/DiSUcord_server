from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext


class ServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("DiSUcord Server")

        # Server Log
        self.log = scrolledtext.ScrolledText(master, height=10, width=70)
        self.log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Connected Clients
        self.clients_list = scrolledtext.ScrolledText(master, height=10, width=35)
        self.clients_list.grid(row=1, column=0, padx=10, pady=10)
        self.clients_list.insert(tk.END, "Connected Clients:\n")

        # IF 100 Channel Subscribers
        self.if_100_list = scrolledtext.ScrolledText(master, height=10, width=35)
        self.if_100_list.grid(row=1, column=1, padx=10, pady=10)
        self.if_100_list.insert(tk.END, "IF 100 Subscribers:\n")

        # SPS 101 Channel Subscribers
        self.sps_101_list = scrolledtext.ScrolledText(master, height=10, width=35)
        self.sps_101_list.grid(row=2, column=0, padx=10, pady=10)
        self.sps_101_list.insert(tk.END, "SPS 101 Subscribers:\n")

        # Entry for server host and port
        self.host_entry = tk.Entry(master, width=15)
        self.host_entry.grid(row=3, column=0, padx=5)
        self.host_entry.insert(0, "127.0.0.1")

        self.port_entry = tk.Entry(master, width=5)
        self.port_entry.grid(row=3, column=1, padx=5)
        self.port_entry.insert(0, "8080")

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
