# Test: pass May 21st 2025
Write-Output "Starting data filter script..."

# Define all paths
$INPUT_DIR = "C:\Users\USER\Desktop\Igor\Runs\DT\Liam_test\test_input_data"
$OUTPUT_DIR = "C:\Users\USER\Desktop\Igor\Runs\DT\Liam_test\Code\output_filtered"
$PERL_SCRIPT = "C:\Users\USER\Desktop\Igor\Runs\DT\Liam_test\Code\data_file_filter_windows.pl"
$SEND_TO_DRIVE_SCRIPT = "C:\Users\USER\Desktop\Igor\Runs\DT\Liam_test\Code\send_to_drive.ps1"

# Create output directory if it doesn't exist
if (-not (Test-Path -Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
}

# Flag to track if any new files were found
$newFilesFound = $false

# Get all .data files from input directory
Get-ChildItem -Path $INPUT_DIR -Filter "*.data" | ForEach-Object {
    $file = $_.FullName
    # Extract filename without extension and create filtered output path
    # Example: input.data -> output_filtered/input_filtered.data
    $filename = [System.IO.Path]::GetFileNameWithoutExtension($file)
    $output_file = Join-Path -Path $OUTPUT_DIR -ChildPath "${filename}_filtered.data"

    # Only process if output doesn't already exist
    if (-not (Test-Path -Path $output_file)) {
        $newFilesFound = $true
        Write-Output "New file found: $file"
        # Check if file is in use
        $scriptPath = Join-Path -Path $PSScriptRoot -ChildPath "check_process.ps1"
        $checkResult = & $scriptPath -FilePath $file
        Write-Output $checkResult
        
        if ($LASTEXITCODE -eq 0) {
            # Run the Perl script
            & perl $PERL_SCRIPT $file $output_file
            
            # If Perl script was successful, send the filtered file to Google Drive
            if ($LASTEXITCODE -eq 0) {
                Write-Output "Sending filtered file to Google Drive: $output_file"
                & $SEND_TO_DRIVE_SCRIPT -FilePath $output_file
            }
        }
    }
}

if (-not $newFilesFound) {
    Write-Output "No new files spotted"
} 