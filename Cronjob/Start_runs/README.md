# Muon Tomography: Scheduling Runs on Windows

This guide explains how to schedule and control data acquisition runs for the Muon Tomography project on Windows. It covers the directory structure, the purpose and usage of each script, and how to use PowerShell to automate sending `START` and `STOP` commands to your detector server.

---

## Directory Structure

All relevant files should be placed in the same directory. For example:

```directory
Connect_to_server/
        ├── client.py
        ├── start_stop_run.py
        ├── run_specs.json
        └── send_command.bat
```

- **client.py**: Core logic for TCP communication and command formatting.
- **start_stop_run.py**: Script to send a `START` or `STOP` command to the server.
- **run_specs.json**: Stores run configuration and the current run number.
- **send_command.bat**: Batch script to automate sending consecutive `STOP` and `START` commands.

---

## Usage

Before running or scheduling scripts, make sure to update the following paths in your files:

- **client.py**:  
  In the `Logger` class, change the default `log_path` to your desired log file directory if needed:

  ```python
  Logger(..., log_path="D:\Above_the_spring_filtered\logs\log_run.log", ...)
  ```

  Replace `log_path` with your preferred path.

- **start_stop_run.py**:  
  Update the path to your JSON file:

  ```python
  json_path: str = r'C:\Users\Jerusalem2\Desktop\Cronjob_code\Start_runs\run_specs.json'
  ```

  Change to the correct path if your JSON file is named or located differently.

- **send_command.bat**:  
  Set the full path to your Python script:

  ```bat
  $PYTHON_SCRIPT = "C:\full\path\to\start_stop_run.py"
  ```

  Replace with the absolute path to `start_stop_run.py` on your system.

---

## Script Descriptions

### `client.py`

This script contains the main classes and functions for communicating with the detector server.

#### Classes

- **ServerDict**  
  A type definition for the server configuration dictionary, specifying keys like `detector`, `output_dir`, `port`, `ip`, and `enabled`.

- **ConvertTime**  
  Utility class for converting time units:
  - `min_to_sec(minutes)`: Converts minutes to seconds.
  - `hour_to_sec(hours)`: Converts hours to seconds.
  - `day_to_sec(days)`: Converts days to seconds.

- **Logger**  
  Handles logging messages to both file and console, with support for different log levels (debug, info, success, warning, error).

- **Command**  
  Represents a command (`START` or `STOP`) to be sent to the detector.  
  - Stores command type, run number, Unix time, run type, and detector name.
  - `to_bytes()`: Converts the command to a byte array for network transmission.
  - `encode()`: Returns the byte array as a `bytearray`.

- **Client**  
  Manages the TCP connection to the detector server.
  - `send_command(command)`: Sends a command to the server.
  - `receive_response()`: Receives a response from the server.
  - `close()`: Closes the connection.

#### Functions

- **send_command_to_server(client, command, timeout_response=10)**  
  Sends a command to the server and waits for a response, logging the result.

---

### `start_stop_run.py`

This script is used to send either a `START` or `STOP` command to the server. It reads the current run number from `run_specs.json`, sends the command, and updates the run number if the command was `STOP`.

**Workflow:**

1. Parses the `--command` argument (`START` or `STOP`).
2. Loads server configuration and the current run number from `run_specs.json`.
3. Creates a `Client` and `Command` instance.
4. Sends the command to the server.
5. If the command was `STOP`, increments the run number in `run_specs.json`.

---

### `run_specs.json`

A JSON file that stores the server configuration and the current run number.  
Example:

```json
{
    "server": {
        "detector": "Det",
        "output_dir": "path_to_dir",
        "port": 1000,
        "ip": "192.168.1.101",
        "enabled": true
    },
    "run_number": 0,
    "run_type": 1
}
```

---

### `send_command.bat`

A Batch script to automate sending consecutive `STOP` and `START` commands.  

## Summary

- Place all files in the same directory.
- Use `start_stop_run.py` to send commands.
- Use `send_command.bat` to automate the process.
- Schedule the PowerShell script with Windows Task Scheduler for automated runs, as explained in the main `READEME.md` file.
