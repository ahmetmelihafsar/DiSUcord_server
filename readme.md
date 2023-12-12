# Discord Server

This project is a simple implementation of a Discord-like server in Python. It allows clients to connect, subscribe to channels, and send messages.

## Features

- User Authentication: Users can connect to the server with a unique username.
- Channel Subscription: Users can subscribe to different channels.
- Message Sending: Users can send messages to the channels they are subscribed to.
- GUI Updates: The server GUI is updated in real-time with the list of connected clients and channel subscribers.

## Code Structure

The `discord_server.py` file contains the `Server` class which is the main class for the server. It manages client connections, channel subscriptions, message broadcasting, and interacts with the GUI. It also starts the server and handles client connections in separate threads.

The `client_handler.py` file contains the `ClientHandler` class which is responsible for handling individual client connections. It processes incoming messages from clients, sends messages to clients, and disconnects clients when necessary.

The `server_gui.py` file contains the `ServerGUI` class which is responsible for the graphical user interface of the server. It displays the server log, the list of connected clients, and the list of subscribers for each channel. It also provides methods to start and stop the server.

## Usage

To start the server, run the `discord_server.py` file. Clients can then connect to it and start interacting.

## Dependencies

This project requires Python 3.x and uses the built-in `socket` library for networking.

## Installation and Running

This project requires Python 3.x. If you don't have Python installed, you can download it from [here](https://www.python.org/downloads/).

1. Clone the repository:

    ```bash
    git clone https://github.com/ahmetmelihafsar/DiSUcord_server.git
    ```

2. Navigate to the project directory:

    ```bash
    cd DiSUcord_server
    ```

3. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the server:

    ```bash
    python main.py
    ```

Clients can then connect to the server and start interacting.

Please note that you might need to replace `python` with `python3` in the command above, depending on your system configuration.

## Future Work

- Implement private messaging between users.
- Add more robust error handling and logging.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
