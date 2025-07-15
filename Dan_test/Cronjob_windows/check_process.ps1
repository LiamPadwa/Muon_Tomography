# Test: pass May 20th 2025

param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

# Check if the file exists
if (-not (Test-Path -Path $FilePath -PathType Leaf)) {
    Write-Error "Error: File '$FilePath' does not exist."
    exit 1
}

# Check if the file is currently in use
try {
    $fileStream = [System.IO.File]::Open($FilePath, 'Open', 'Read', 'None')
    $fileStream.Close()
    $fileStream.Dispose()
    Write-Output "File '$FilePath' is not in use and safe to process."
    exit 0
}
catch {
    Write-Output "File '$FilePath' is currently in use."
    exit 1
} 