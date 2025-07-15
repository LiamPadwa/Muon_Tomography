#!/bin/bash

FILE="$1"

# Check if a file argument was provided
if [ -z "$FILE" ]; then
    echo "Usage: $0 /full/path/to/file"
    exit 1
fi

# Check if the file actually exists
if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' does not exist."
    exit 1
fi

# Check if the file is currently in use
if lsof "$FILE" > /dev/null 2>&1; then
    echo "File '$FILE' is currently in use."
    exit 1
else
    echo "File '$FILE' is not in use and safe to process."
    exit 0
fi
