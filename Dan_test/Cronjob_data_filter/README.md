# Automated Data Filtering with Cron

This project provides a cron-based automation pipeline for filtering `.data` files using a Perl script. It monitors a specified input directory, checks if new data files are ready and not currently in use, and then filters them into an output directory.

## Main Script: `filtering_loop.sh`

This is the core script executed by the cronjob.

### Functionality

- Checks the `INPUT_DIR` for new `.data` files.
- Skips files that have already been processed.
- Uses `check_process.sh` to determine if a file is currently in use.
- If available and not filtered, runs the Perl filter script to generate the processed file in `OUTPUT_DIR`.

### Path Configuration

```bash
INPUT_DIR="/Users/liam/Documents/Muon_tomography/Dan_test/Cronjob_data_filter/test_input_data"
OUTPUT_DIR="/Users/liam/Documents/Muon_tomography/Dan_test/Cronjob_data_filter/output_filtered"
```

### Output Naming

Each output file is named after the input and suffixed with `_filtered`.

Example:

```text
input:    testfile.data
output:   testfile_filtered.data
```

---

## Helper Script: `check_process.sh`

This script uses `lsof` to check if a given file is currently being used (e.g., written to or open by another process).

### Functionality

- Takes one argument: the full path to the input `.data` file.
- Returns a successful exit code (0) if the file is **not in use**.
- Returns a failure exit code (1) if the file **is currently being used**.

### Example Use

```bash
/bin/bash check_process.sh /path/to/file.data
```

---

## Directory Structure

Ensure the input directory exist:

- **Input Directory:**  
  `/Users/liam/Documents/Muon_tomography/Dan_test/Cronjob_data_filter/test_input_data`

The script will automatically create the output directory if it does not exist.

---

## Cronjob Setup

To automatically run the script at regular intervals:

### 1. Open your crontab with nano

```bash
EDITOR=nano crontab -e
```

### 2. Add the following cron entry

```cron
* * * * * /bin/bash script.sh >> logfile.log 2>&1
```

In Liam's machine:

```cron
* * * * * /bin/bash /Users/liam/Documents/Muon_tomography/Dan_test/Cronjob_data_filter/filtering_loop.sh >> /Users/liam/Documents/Muon_tomography/Dan_test/Cronjob_data_filter/cron.log 2>&1
```

### Explanation

- `* * * * *` — Runs **every minute**.
- The `>> ... 2>&1` part redirects both standard output and errors to `cron.log`.

### Example log path

```bash
/Users/liam/Documents/Muon_tomography/Dan_test/Cronjob_data_filter/cron.log
```

You can inspect this log to monitor the script's behaviour and debug any issues.
Check logfile:

```bash
cat log_path.log
```

### Example cron schedules

- `0 5 * * *` - Runs every day at 5 A.M.

---

## Final Notes

- Make sure the shell scripts are executable:

  ```bash
  chmod +x filtering_loop.sh check_process.sh
  ```

- Ensure `cron` has the necessary **Full Disk Access** in **System Settings > Privacy & Security** for it to run on macOS.
- The program *is not* built to work on Windows

- All commands and files is use should be written in their *full* path form
- To check the path of a command (e.g perl), run:

```bash
which perl
```

---
