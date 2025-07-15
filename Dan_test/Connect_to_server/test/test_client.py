import select
import socket
import sys


class Client:
    """Handle TCP connection to the detector server."""

    def __init__(self, ip: str, port: int):
        """Initialise client."""
        timeout_connect = 10
        self.ip = ip
        self.port = port
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(timeout_connect)
            self.client.connect((ip, port))
            # Remove non-blocking mode as it's not needed for this simple client
            # self.client.setblocking(0)

        except socket.error as e:
            msg = f"Unable to connect to server {self.ip}: {self.port}. Error: {e}"
            print(f"ERROR: {msg}")
            raise ConnectionError(msg)

    def fileno(self):
        return self.client.fileno()
    
    def on_read(self):
        msg = self.client.recv(1024).decode()
        print(msg)

    def send(self, msg):
        self.client.send(msg)

    def send_command(self, command: str):
        self.client.send(command.encode())

    def receive_response(self):
        return self.client.recv(1024).decode()
    
    def close(self):
        self.client.close()

class Input:
    def __init__(self, sender):
        self.sender = sender
    def fileno(self):
        return sys.stdin.fileno()
    def on_read(self):
        msg = sys.stdin.readline().encode()
        print(msg)
        self.sender.send(msg)

class EventLoop:
    def __init__(self):
        self.readers = []
    
    def __add__(self, reader):
        self.readers.append(reader)
    
    def run_loop(self):
        while True:
            readers, _, _ = select.select(self.readers, [], [])
            for reader in readers:
                reader.on_read()


if __name__ == '__main__':
    client = Client('127.0.0.1', 12345)
    input_reader = Input(client)
    event_loop = EventLoop()
    event_loop + client 
    event_loop + input_reader
    event_loop.run_loop()
    