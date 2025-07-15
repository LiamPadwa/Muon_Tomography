# Setting Up Scheduled Data Filtering Task On Windows

> **Test Status**: All tests passed on May 21st, 2025

> **Last Updated**: May 21st, 2025

This guide explains how to set up an hourly task to run the data filtering script on Windows.

## Prerequisites

1. All scripts are in place:
   - `check_process.ps1`
   - `filtering_loop.ps1`
   - `run_filter.bat`
   - `data_file_filter_windows.pl`
   - `send_to_drive.ps1`

2. PowerShell execution policy is set:

   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```

## Directory Structure

```text
C:\Users\USER\Desktop\Igor\Runs\DT\Liam_test\
├── test_input_data\        # Input .data files
├── Code\
│   ├── output_filtered\    # Filtered output files
│   ├── logs\              # Log files
│   │   └── filter_log.txt # Single log file for all runs
│   ├── filtering_loop.ps1
│   ├── check_process.ps1
│   ├── data_file_filter_windows.pl
│   └── run_filter.bat
│   └── send_to_drive.ps1
```

## Logging

The script maintains a single log file for all runs:

- Log file: `logs/filter_log.txt`
- Each run is separated by a timestamp header
- Log format:

  ```text
  ========================================
  Run started at: [date] [time]
  ========================================
  [script output]
  ```

- Logs include:
  - Script start messages
  - File processing status
  - Files that were skipped (already filtered)
  - Any errors that occurred

## Setting Up the Scheduled Task

### Method 1: Using Task Scheduler GUI

1. Open Task Scheduler:
   - Press `Windows + R`
   - Type `taskschd.msc` and press Enter

2. Create new task:
   - Click "Create Basic Task"
   - Name: "Data Filter Hourly Task"
   - Description: "Runs the data filtering script every hour"

3. Set trigger:
   - Choose "Daily"
   - Set start time to next hour
   - Check "Repeat task every: 1 hour" 
   - Set "for a duration of: 24 hours"

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

   - In Triggers:
     - Go to Edit
       - Check "Repeat task every"
       - Choose: "for a duration of"


### Method 2: Using PowerShell (Run as Administrator)

```powershell
# Create a new scheduled task action that will execute the batch file
# -Execute parameter specifies the full path to the script that will run
$action = New-ScheduledTaskAction -Execute "C:\Users\USER\Desktop\Igor\Runs\DT\Liam_test\Code\run_filter.bat"

# Create a trigger that will run the task:
# -Once: Start the task once
# -At (Get-Date): Start from current time
# -RepetitionInterval: Run every 1 hour
# -RepetitionDuration: Continue for 3650 days (approximately 10 years)
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 3650)

# Configure task settings:
# -StartWhenAvailable: Run task as soon as possible if missed
# -DontStopOnIdleEnd: Continue running even if computer becomes idle
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd

# Register the scheduled task with Windows Task Scheduler:
# -TaskName: Name that will appear in Task Scheduler
# -Action: The action we defined above
# -Trigger: The schedule we defined above
# -Settings: The settings we defined above
# -Description: A description of what the task does
Register-ScheduledTask -TaskName "DataFilterHourly" -Action $action -Trigger $trigger -Settings $settings -Description "Runs the data filtering script every hour"
```

## Managing the Task

### To Stop the Task

1. Open Task Scheduler
2. Find "DataFilterHourly" in the task list
3. Right-click and select "Disable" or "Delete"

### To Modify Schedule

1. Open Task Scheduler
2. Find "DataFilterHourly"
3. Right-click and select "Properties"
4. Modify the trigger settings as needed

### Managing Task State with PowerShell

#### Finding Tasks

To find existing tasks using PowerShell:

```powershell
# List all tasks containing "Data" or "Filter" in their name
Get-ScheduledTask | Where-Object {$_.TaskName -like '*Data*' -or $_.TaskName -like '*Filter*'} | Format-Table -Property TaskName,State,LastRunTime,LastTaskResult
```

Note: In Task Scheduler GUI, you may need to click the "Refresh" button (located in the right panel) to see newly created tasks.

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

Note: If you get an error "The task is disabled" when trying to start a task, you need to enable it first using `Enable-ScheduledTask`. Replace "YourTaskName" with your actual task name.

## Troubleshooting

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
