# Muon Tomography: Automated Data Filtering on Windows

This guide explains how to use and configure the data filtering automation scripts for your Muon Tomography project on Windows. It covers the directory structure, the purpose and usage of each script, and how to automate the filtering and upload process.

---

## Directory Structure

All relevant files should be placed in the same directory:

```directory
Data_filter/
    ├── check_process.ps1
    ├── filtering_loop.ps1
    ├── data_file_filter_windows.pl
    ├── send_to_drive.ps1
    ├── run_filter.bat
    └── RCLONE.md
```

- **check_process.ps1**: Checks if a file is currently in use by another process.
- **filtering_loop.ps1**: Main PowerShell script that scans for new raw data files, filters them, and uploads results.
- **data_file_filter_windows.pl**: Perl script that performs the actual data filtering.
- **send_to_drive.ps1**: PowerShell script that uploads filtered files to Google Drive using Rclone.
- **run_filter.bat**: Batch script to execute the programme.
- **RCLONE.md**: Documentation for setting up and using Rclone for Google Drive uploads.

---

## Usage

Before running or scheduling scripts, make sure to update the following paths in your files:

- **filtering_loop.ps1**:  
  Set the following variables at the top of the script to match your environment:

  ```powershell
  $INPUT_DIR = "D:\Above_the_spring_raw_data"
  $OUTPUT_DIR = "D:\Above_the_spring_filtered"
  $PERL_SCRIPT = "C:\Path\To\data_file_filter_windows.pl"
  $SEND_TO_DRIVE_SCRIPT = "C:\Path\To\send_to_drive.ps1"
  ```
  
  Adjust these paths as needed.

- **run_filter.bat**:  
  Update the log directory and the path to `filtering_loop.ps1`:

  ```bat
  set LOG_DIR=D:\Above_the_spring_filtered\logs
  if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
  set LOG_FILE=%LOG_DIR%\filter_log.txt
  powershell.exe -ExecutionPolicy Bypass -File "C:\Path\To\filtering_loop.ps1" >> "%LOG_FILE%" 2>&1
  ```

- **send_to_drive.ps1**:
  Update the output Google Drive directory

  ```bat
  $drive_directory = "Jerusalem_filtered"
  ```

---

## Script Descriptions

### `check_process.ps1`

Checks if a file is currently in use by another process. Used by `filtering_loop.ps1` to avoid processing files that are still being written.

---

### `data_file_filter_windows.pl`

Perl script that performs the actual data filtering. Keeping events detected in all of the detector 4 layers.

- Usage:

  ```cmd
  perl data_file_filter_windows.pl inputFile.data outputFile.data
  ```
- Called automatically by `filtering_loop.ps1`.

---

### `send_to_drive.ps1`

Uploads a specified file to Google Drive using Rclone.  

- Usage:  

  ```powershell
  .\send_to_drive.ps1 -FilePath "C:\Path\To\Your\File.data"
  ```
- Make sure to configure Rclone as described in `RCLONE.md`.

---

### `filtering_loop.ps1`

Main automation script.  
**Workflow:**

1. Scans `$INPUT_DIR` for new `.data` files.
2. For each new file:
   - Checks if the file is in use (`check_process.ps1`).
   - Runs the Perl filter (`data_file_filter_windows.pl`) to create a filtered output in `$OUTPUT_DIR`.
   - If filtering is successful, uploads the filtered file to Google Drive using `send_to_drive.ps1`.

---

### `run_filter.bat`

Batch script to run `filtering_loop.ps1` and log all output to a log file.  

- Ensures the log directory exists.
- Appends a timestamped header for each run.

---

### `RCLONE.md`

Documentation for installing, configuring, and using Rclone to upload files to Google Drive.  
- Follow the instructions in this file to set up your Google Drive remote and test uploads.

---

## Logging

The programme maintains a single log file for all runs:

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

## Summary

- Place all files in the same directory.
- Update all paths in the scripts to match your environment.
- Use `run_filter.bat` to run the filtering and upload process.
- Use Windows Task Scheduler to automate execution, as described in the main project documentation.
