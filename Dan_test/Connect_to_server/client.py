import logging
import select
import socket
import time
from typing import TypedDict


class ServerDict(TypedDict):
    """Type definition for server configuration."""
    
    detector: str
    output_dir: str
    port: int
    ip: str
    enabled: bool

class ConvertTime:
    """Utility class for time conversions."""

    @staticmethod
    def min_to_sec(minutes: float) -> float:
        return minutes * 60
    @staticmethod
    def hour_to_sec(hours: float) -> float:
        return hours * 60 * 60
    @staticmethod
    def day_to_sec(days: float) -> float:
        return days * 24 * 60 * 60

class Logger:
    """Handles logging with timestamps and multiple output streams."""
    
    def __init__(self, name: str, log_level=logging.INFO, log_path: str = "Dan_test/Connect_to_server/log.log", console_output: bool = True):
        self.name = name
        # Add custom success level
        logging.addLevelName(25, "SUCCESS")  # 25 is between INFO (20) and WARNING (30)
        
        # Configure logging
        # logging.basicConfig(
        #     level=log_level,
        #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        #     datefmt='%Y-%m-%d %H:%M:%S',
        #     handlers=[logging.FileHandler(log_path)]
        # )
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
        
        # File handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler (optional)
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)
    
    def success(self, message: str):
        self.logger.log(25, message)
    
    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)


class Command:
    """Represents a command to be sent to the detector."""
    
    def __init__(
        self, command_type: str,
        run_number: int, unix_time: int, run_type: int,
        detector: str
        ):

        self.logger: Logger = Logger("Command")
        self.command: str = command_type  # "START" or "STOP" a run
        self.run_number: int = run_number
        self.unix_time: int = unix_time
        self.run_type: int = run_type
        self.detector: str = detector
    
    def to_bytes(self):
        """
        Convert command to byte array for network transmission. 
        
        According to the command-syntax specified in NuclearInstruments/dt5550w-remote-client ReadMe.
        """
        data = [0xFF, 0x80, 0x00, 0x8]  # 4-byte header 
        # 2-byte run number (RN1, RN0):
        data.append( (self.run_number >> 8) & 0xFF )  
        data.append( (self.run_number >> 0) & 0xFF )
        # 2-byte run type (RT1, RT0):
        data.append( (self.run_type >> 8) & 0xFF )  
        data.append( (self.run_type >> 0) & 0xFF )

        if self.command:
            # 3-byte command type prefix:
            data.append(0xEE)  
            data.append(0x0)
            data.append(0x0)
            if self.command == "START":
                data.append(0x1)
            elif self.command == "STOP":
                data.append(0x0)
            else:
                msg = f"Unexpected command type, expected 'START' or 'STOP', got {self.command}" 
                raise ValueError(msg)
        
        # 4-byte start time (T3-T0)
        data.append( (self.unix_time >> 24) & 0xFF )
        data.append( (self.unix_time >> 16) & 0xFF )
        data.append( (self.unix_time >> 8) & 0xFF )
        data.append( (self.unix_time >> 0) & 0xFF )

        return data

    def encode(self):
        return bytearray(self.to_bytes())


class Client:
    """Handle TCP connection to the detector server."""

    def __init__(self, ip: str, port: int):
        """Initialise client."""
        timeout_connect = 10
        self.logger = Logger("Client")
        self.ip = ip
        self.port = port
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(timeout_connect)
            self.client.connect((ip, port))
            self.client.setblocking(0)

        except socket.error:
            msg = f"Unable to connect to server {self.ip}: {self.port}. Error: {socket.error}"
            self.logger.error(msg)
            raise ConnectionError(msg)

    def send_command(self, command: Command):
        self.client.send(command.encode())

    def receive_response(self):
        return self.client.recv(16)
    
    def close(self):
        self.client.close()


def send_command_to_server(client: Client, command: Command, timeout_response: float = 10):
    """Send command to server and wait for response."""
    try:
        command.logger.info(f"Sending {command.command} to Detector {command.detector} at server {client.ip}: {client.port}")
        client.send_command(command)
        ready, _, _= select.select([client.client], [], [], timeout_response)
        if ready:
            response = client.receive_response()
            client.logger.info(f"Server {client.ip}: {client.port}. Response: {response.hex()}")
            client.close()
            return True
    
        return False

    except socket.error:
        client.logger.error(f"Unable to connect to server {client.ip}: {client.port}. Error: {socket.error}")
        return False


if __name__ == "__main__":
    # Server configuration
    server: ServerDict = {
        'detector': 'Det',
        'output_dir': 'path_to_dir',
        'port': 1000,
        'ip': '0.0.0.0',
        'enabled': True
    }

    # Run parameters
    run_duration = ConvertTime.min_to_sec(1)  # run duration should be in seconds
    current_run_number: int = 2
    current_run_type:   int = 1
    start_unix_time: int = int(time.time())

    # Initialise connection and start-command
    client: Client = Client(ip=server['ip'], port=server['port'])
    start_run_command: Command = Command(
        'START', current_run_number,
        start_unix_time, current_run_type,
        server['detector'])
    
    # Attempt to start the run
    sent_start = send_command_to_server(client, start_run_command, time_response=10)
    if sent_start is True:
        client.logger.info(f'Detector is ready, starting run number {current_run_number}')

        # Wait for run duration
        time.sleep(run_duration)
        stop_unix_time: int = int(time.time())

        # Send stop command
        client_stop: Client = Client(ip=server['ip'], port=server['port'])
        
        stop_run_command: Command = Command(
        'STOP', current_run_number,
        stop_unix_time, current_run_type,
        server['detector'])

        sent_stop = send_command_to_server(client_stop, stop_run_command, time_response=10)
        
        if sent_stop is True:
            client.logger.success(f'Run {current_run_number} completed successfully - Duration: {run_duration} seconds')
        
        else:
            msg = 'Failed to stop data acquisition!'
            client.logger.error(msg)
            raise ConnectionError(msg)
    
    else:
        client.logger.warning(f"Detector {server['detector']} is not ready, server {server['ip']}: {server['port']} is unobtainable")


    
    



