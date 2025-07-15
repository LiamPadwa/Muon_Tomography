import argparse
import json
import time

from client import Client, Command, ServerDict, send_command_to_server

parser = argparse.ArgumentParser(description='sending START/STOP command to server')
parser.add_argument('--command', type=str, choices=['START', 'STOP'], help='choose a command, either START or STOP')
args = parser.parse_args()
command_type: str = args.command

server: ServerDict = {
        "detector": "Det",
        "output_dir": "",
        "port": 990,
        "ip": "192.168.1.101",
        "enabled": True
        }
run_type: int = 1

json_path: str = r'C:\Users\Jerusalem2\Desktop\Cronjob_code\Start_runs\run_specs.json'
with open(json_path, 'r') as f:
    run_specs: dict = json.load(f)
    run_number: int = run_specs['run_number']

unix_time: int = int(time.time())

client: Client = Client(ip=server['ip'], port=server['port'])
command: Command = Command(command_type, run_number, unix_time, run_type, server['detector'])
command.logger.info(f'Creating {command.command} command for run number {command.run_number}')

if command.command == 'STOP':
    run_specs['run_number'] = run_number + 1

sent_command: bool = send_command_to_server(client, command)

if sent_command:
    client.logger.info(f'Command {command_type} was sucsessfully sent')

    with open(json_path, 'w') as f:
        json.dump(run_specs, f, indent=4)
    
else:
    client.logger.error(f"Detector {server['detector']} is not ready, server {server['ip']}: {server['port']} is unobtainable")

