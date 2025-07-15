#!/bin/bash
# Test: pass May 14th
echo "Starting data filter script..."


INPUT_DIR="/Users/liam/Documents/Muon_tomography/Dan_test/Cronjob_data_filter/test_input_data"
OUTPUT_DIR="/Users/liam/Documents/Muon_tomography/Dan_test/Cronjob_data_filter/output_filtered"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.data; do  
    
    filename=$(basename "$file" .data)  # removes .data extension 
    output_file="${OUTPUT_DIR}/${filename}_filtered.data"

    # Only process if output doesn't already exist
    if [ ! -f "$output_file" ]; then

        if /bin/bash /Users/liam/Documents/Muon_tomography/Dan_test/Cronjob_data_filter/check_process.sh "$file"; then

            /usr/bin/perl /Users/liam/Documents/Muon_tomography/Dan_test/Cronjob_data_filter/data_file_filter_linux.pl "$file" "$output_file"
        
        fi  # End of 'check process' if

    fi  # End of 'check if already filtered' if
done
