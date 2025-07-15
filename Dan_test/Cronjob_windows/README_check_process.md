# Windows Process Check Script

This directory contains a PowerShell script (`check_process.ps1`) that checks if a file is currently in use by another process.

## Running the Script

### 1. Open PowerShell as Administrator

- Press `Windows + X` on your keyboard
- Select "Windows PowerShell (Admin)" or "Windows Terminal (Admin)"
- Click "Yes" if prompted by User Account Control (UAC)

### 2. Set Execution Policy

In the admin PowerShell window, run:

```powershell
Set-ExecutionPolicy RemoteSigned
```

- Type "Y" when prompted to confirm
- This allows local scripts to run while maintaining security for downloaded scripts

### 3. Run the Script

Navigate to the script directory and run:

```powershell
cd "path\to\Cronjob_windows"
.\check_process.ps1 -FilePath "path\to\your\file"
```

Example:

```powershell
.\check_process.ps1 -FilePath "C:\Users\USER\Desktop\Igor\Runs\DT\Liam_test\test_detector_data\154.data"
```

### 4. (Optional) Reset Execution Policy

If you want to change the execution policy back to its default restricted state:

```powershell
Set-ExecutionPolicy Restricted
```

## Script Output

- If the file is not in use: "File '[path]' is not in use and safe to process."
- If the file is in use: "File '[path]' is currently in use."
- If the file doesn't exist: "Error: File '[path]' does not exist."

## Notes

- The script requires PowerShell 3.0 or later
- You only need to set the execution policy once
- The execution policy can be changed back to Restricted at any time
- Make sure to use the full path to the file you want to check
