# Muon Tomography Data Acquisition & Filtering: Windows Project Guide

This project automates data acquisition and filtering for muon tomography experiments on Windows. It is organized into two main directories:

```text
Data_filter/
    filtering_loop.ps1
    check_process.ps1
    data_file_filter_windows.pl
    send_to_drive.ps1
    run_filter.bat

Start_run/
    client.py
    start_stop_run.py
    run_specs.json
    send_command.bat
```

---

## Code Config

Before running the system, you must configure all scripts with the correct file and directory paths for your environment.

### Data_filter

- **filtering_loop.ps1**
  - Set the following variables at the top of the script:

    ```powershell
    $INPUT_DIR = "C:\Path\To\RawData"                # Directory containing raw .data files
    $OUTPUT_DIR = "C:\Path\To\FilteredOutput"        # Directory for filtered output files (Auto Created)
    $PERL_SCRIPT = "C:\Path\To\data_file_filter_windows.pl"  # Full path to the Perl filter script
    $SEND_TO_DRIVE_SCRIPT = "C:\Path\To\send_to_drive.ps1"   # Full path to the upload script (optional)
    ```
  - All scripts should be inside the `Data_filter` directory

- **check_process.ps1**
  - No path changes needed.

- **data_file_filter_windows.pl**
  - No path changes needed.

- **send_to_drive.ps1**
  - No path changes needed

- **run_filter.bat**
  - Update the path to the logs directory (The directory is automatically created):

    ```bat
    set LOG_DIR=C:\Path\To\Logs
    ```
  - Update the path to `filtering_loop.ps1`:

    ```bat
    powershell.exe -ExecutionPolicy Bypass -File "C:\Path\To\filtering_loop.ps1" >> "%LOG_FILE%" 2>&1
    ```

### Start_run

- **client.py**
  - In the `Logger` class, set the `log_path` parameter to your desired log file location:

    ```python
    Logger(..., log_path="C:/Path/To/log.log", ...)
    ```

- **start_stop_run.py**
  - Set the path to your JSON run configuration file:

    ```python
    json_path: str = 'C:/Path/To/run_specs.json'
    ```

- **run_specs.json**
  - No path changes needed, but ensure this file is present and updated with your detector/server settings.

- **send_command.bat**
  - Set the full path to your Python script:

    ```bat
    set PYTHON_SCRIPT= C:\Path\To\Start_run\start_stop_run.py
    ```
  - Update `LOG_DIR` and `LOG_FILE` as needed.

---

## Installations

You must have **Python**, **Perl** and **Rclone** installed and available in your system PATH.

### Python

1. **Download & Install:**
   - Install from website
        - Download Python from [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
        - Run the installer and **check the box "Add Python to PATH"** during installation.
   - Install from Terminal

        ```cmd
        winget install Python.Python.3
        ```
        - Make sure to restart your terminal after installation so the `python` command is available.

2. **Verify Installation:**
   - Open Command Prompt and run:

     ```cmd
     python --version
     ```
   - You should see the installed Python version.

3. **Add Python to PATH (if not already added):**
   - Open the Start Menu and search for "Environment Variables".
   - Click "Edit the system environment variables".
   - In the System Properties window, click "Environment Variables".
   - Under "System variables", find and select the `Path` variable, then click "Edit".
   - Click "New" and add the path to your Python installation (e.g., `C:\Users\YourUser\AppData\Local\Programs\Python\Python311\`).
   - Also add the `Scripts` subfolder (e.g., `C:\Users\YourUser\AppData\Local\Programs\Python\Python311\Scripts\`).
   - Click OK to save and restart your terminal.

### Perl

1. **Download & Install:**
   - Download Strawberry Perl from [https://strawberryperl.com/](https://strawberryperl.com/)
   - Run the installer and follow the prompts (it will add Perl to your PATH by default).

2. **Verify Installation:**
   - Open Command Prompt and run:

     ```cmd
     perl --version
     ```
   - You should see the installed Perl version.

3. **Add Perl to PATH (if not already added):**
   - Strawberry Perl usually adds itself to PATH automatically.
   - To check, open Command Prompt and run:

     ```cmd
     perl --version
     ```
   - If not found, add the Perl `bin` directory (e.g., `C:\Strawberry\perl\bin`) to your PATH using the steps above.

### Rclone

See detailed instructions in `RCLONE.md`

---

**Next Steps:**  
Once all paths are configured and dependencies installed, you can proceed to run and schedule the scripts for automated data acquisition and filtering.

(More instructions will be added in the next steps.)

## Setting Up the Scheduled Tasks

### Creating the Tasks

Setting up the two scheduled tasks for filtering data and for executing runs, using the Task Scheduler GUI.

1. Open Task Scheduler:
   - Press `Windows + R`
   - Type `taskschd.msc` and press Enter

2. Create new task:
   - Click "Create Basic Task"
   - Name: "Data Filter Daily Task"
   - Description: "Runs the data filtering script every day"

3. Set trigger:
   - Choose "Daily"
   - Set start time

4. Set action:
   - Choose "Start a program"
   - Program/script: Browse to `run_filter.bat`
   - Start in: Leave empty

5. Final settings:
   - Check "Open Properties dialog"
   - In Properties:
     - Go to "Settings" tab
     - Check "Run task as soon as possible after a scheduled start is missed"
     - Check "If the task is already running, then the following rule applies: Do not start a new instance"
   - For Testing:
     - In Triggers:
       - Go to Edit
         - Check "Repeat task every"
         - Choose: "for a duration of"

Repeat for the `send_command.bat` script.

Note: Make sure to initilise `send_command.bat` some 5 minutes **earlier** than `run_filter.bat`.

### Managing the Task

Note: In Task Scheduler GUI, you may need to click the "Refresh" button (located in the right panel) to see newly created tasks.

#### To Stop the Task

1. Open Task Scheduler
2. Find "DataFilterHourly" in the task list
3. Right-click and select "Disable" or "Delete"

#### To Modify Schedule

1. Open Task Scheduler
2. Find "Data Filter Daily Task"
3. Right-click and select "Properties"
4. Modify the trigger settings as needed

#### Managing Task State with PowerShell

##### Finding Tasks

To find existing tasks using PowerShell:

```powershell
# List all tasks containing "Data" or "Filter" in their name
Get-ScheduledTask | Where-Object {$_.TaskName -like '*Data*' -or $_.TaskName -like '*Filter*'} | Format-Table -Property TaskName,State,LastRunTime,LastTaskResult
```

To enable, disable, or start a task using PowerShell:

```powershell
# Enable a disabled task
Enable-ScheduledTask -TaskName "YourTaskName"

# Disable a task
Disable-ScheduledTask -TaskName "YourTaskName"

# Start a task immediately
Start-ScheduledTask -TaskName "YourTaskName"

# Stop a running task
Stop-ScheduledTask -TaskName "YourTaskName"

# Check task state
Get-ScheduledTask -TaskName "YourTaskName" | Select-Object TaskName,State
```

Replace "YourTaskName" with your actual task name.

Note: If you get an error "The task is disabled" when trying to start a task, you need to enable it first using `Enable-ScheduledTask`.

### Troubleshooting

1. If scripts don't run:
   - Check execution policy: `Get-ExecutionPolicy`
   - Ensure all paths are correct in scripts
   - Check Task Scheduler history for errors

2. If files aren't being processed:
   - Verify input directory contains .data files
   - Check if files are locked by other processes
   - Ensure output directory exists and is writable

3. To reset execution policy:
   - Run PowerShell as Administrator
   - Execute: `Set-ExecutionPolicy Restricted`
