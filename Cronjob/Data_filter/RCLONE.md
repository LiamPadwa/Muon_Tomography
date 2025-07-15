# RCLONE Google Drive Integration Guide

This guide explains how to configure [Rclone](https://rclone.org/) for Google Drive and how to use the `send_to_drive.ps1` PowerShell script to automate file uploads from your Windows system.

---

## 1. Rclone Installation

1. **Download Rclone:**  
   Go to [https://rclone.org/downloads/](https://rclone.org/downloads/) and download the Windows zip file.

2. **Extract Rclone:**  
   Extract the contents to a directory of your choice, e.g., `C:\Tools\rclone`.

3. **(Optional) Add Rclone to PATH:**  
   - Open System Properties → Environment Variables.
   - Edit the `Path` variable and add the directory where `rclone.exe` is located.
   - This allows you to run `rclone` from any command prompt.

---

## 2. Initial Rclone Configuration for Google Drive

You only need to do this once per machine/account.

1. **Open Command Prompt and navigate to your Rclone directory:**

    ```cmd
    cd C:\Tools\rclone
    ```

2. **Start the configuration wizard:**

    ```cmd
    rclone config
    ```

3. **Create a new remote:**
    - Type `n` and press Enter to create a new remote.
    - **Name:** Enter a name for your remote (e.g., `Jerusalem`). This name will be used in all future commands.
    - **Storage:** Type the number corresponding to `Google Drive` (usually `20`) and press Enter.

4. **Google Drive settings:**
    - Accept the defaults for client ID and secret (just press Enter twice).
    - **Scope:** Type `1` for "Full access" and press Enter.
    - Accept the default root folder ID (press Enter).
    - **Advanced config:** Type `n` for "No".
    - **Use auto config (Web Browser):** Type `y` for "Yes" (recommended).

5. **Authorise Rclone:**
    - A browser window will open. Log in with your Google account (e.g., `jerusalemdetector@gmail.com`).
    - Grant Rclone the requested permissions.
    - After successful authentication, you should see a "Success" message in the browser.

6. **Shared Drive (if applicable):**
    - Select `y` when prompted to configure as a Shared Drive, then choose the Shared Drive you want to use.
    - Select the Shared Drive you want to use.
    - Type `y` for **Keep Jerusalem Remote**

7. **Finish:**
    - Confirm to keep the remote.
    - Type `q` to quit the configuration wizard.

---

## 3. Using Rclone

You can now use Rclone commands to interact with your Google Drive.  
Replace `Jerusalem` with the name you chose for your remote.

- **List directories in your Google Drive:**

    ```cmd
    rclone lsd Jerusalem:
    ```

- **List all files:**

    ```cmd
    rclone ls Jerusalem:
    ```

- **Copy a file to Google Drive:**

    ```cmd
    rclone copy C:\Path\To\Your\File.txt Jerusalem:Target\Folder\on\GoogleDrive
    ```

---

## 4. Automating Uploads with `send_to_drive.ps1`

The `send_to_drive.ps1` PowerShell script automates the process of uploading a file to Google Drive using Rclone.

### Script Overview

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

# Check if the file exists
if (-not (Test-Path $FilePath)) {
    Write-Error "File not found: $FilePath"
    exit 1
}

# Define rclone path (adjust this path according to your rclone installation)
$rclonePath = "C:\Users\USER\Desktop\Igor\Rclone\rclone"
$remote_name = "Jerusalem:"
$drive_directory = "Test"

# Execute rclone copy command
try {
    & $rclonePath copy $FilePath $remote_name$drive_directory
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Successfully copied file to Google Drive"
    } else {
        Write-Error "Failed to copy file. Rclone exit code: $LASTEXITCODE"
    }
} catch {
    Write-Error "An error occurred while copying the file: $_"
    exit 1
}
```

### How It Works

- **Parameters:**  
  The script takes a single parameter: the full path to the file you want to upload.

- **File Check:**  
  It first checks if the file exists. If not, it exits with an error.

- **Rclone Path:**  
  Set `$rclonePath` to the full path of your `rclone.exe`.

- **Remote Name and Directory:**  
  - `$remote_name` should match the name you gave your remote during configuration (e.g., `Jerusalem:`).
  - `$drive_directory` is the folder in your Google Drive where files will be uploaded.

- **Upload:**  
  The script runs the Rclone `copy` command to upload the file. It checks the exit code and prints a success or error message.

### Example Usage

From PowerShell:

```powershell
.\send_to_drive.ps1 -FilePath "C:\Path\To\Your\File.txt"
```

---

## 5. Troubleshooting

- If you get authentication errors, rerun `rclone config` and reauthorize.
- Make sure the paths in `send_to_drive.ps1` are correct for your system.
- If uploading to a Shared Drive, ensure you selected it during Rclone configuration.

---

## References

- [Rclone Documentation](https://rclone.org/docs/)
- [Rclone Google Drive Backend](https://rclone.org/drive/)