import select
import socket
import sys

from test_client import EventLoop, Input


class ClientHandler:
    def __init__(self, client, addr):
        self.client = client
        self.addr = addr
    
    def fileno(self):
        return self.client.fileno()
    
    def on_read(self):
        msg = self.client.recv(1024)
        if msg:
            print(f"Message from {self.addr}: {msg.decode().strip()}")


class Server:
    """A server example."""

    def __init__(self, ip: str = '127.0.0.1', port: int = 12345) -> None:
        """Initialise server."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip  # or 'localhost'
        self.port = port 
        self.server.bind((self.ip, self.port))
        self.server.listen()
        self.clients = []
        self.event_loop = None  # Will be set when added to event loop
    
    def fileno(self):
        return self.server.fileno()
    
    def on_read(self):
        client, addr = self.server.accept()
        print(f"New connection from {addr}")
        client_handler = ClientHandler(client, addr)
        self.clients.append(client_handler)
        if self.event_loop:
            self.event_loop + client_handler
        return client_handler
    
    def send(self, msg):
        for client in self.clients[:]:  # Create a copy of the list to safely remove items
            client.client.send(msg)


class Input:
    def __init__(self, sender):
        self.sender = sender
    
    def fileno(self):
        return sys.stdin.fileno()
    
    def on_read(self):
        msg = sys.stdin.readline().encode()
        print(f"Server sending: {msg.decode().strip()}")
        self.sender.send(msg)

class EventLoop:
    def __init__(self):
        self.readers = []
    
    def __add__(self, reader):
        self.readers.append(reader)
        if isinstance(reader, Server):
            reader.event_loop = self
        return self
    
    def run_loop(self):
        while True:
            readers, _, _ = select.select(self.readers, [], [])
            for reader in readers:
                try:
                    reader.on_read()
                except (socket.error, ConnectionError):
                    self.readers.remove(reader)

if __name__ == '__main__':
    server = Server()
    input_reader = Input(server)
    event_loop = EventLoop()
    event_loop + server
    event_loop + input_reader
    event_loop.run_loop()

            


