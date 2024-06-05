#!/bin/bash

# Check if file exists
if [ ! -f "$1" ]; then
    echo "Error: File not found!"
    exit 1
fi

# Count the initial number of lines
initial_line_count=$(wc -l < "$1")
echo "Initial number of lines: $initial_line_count"

# Continuously monitor the file for changes
while true; do
    # Count the current number of lines
    current_line_count=$(wc -l < "$1")
    
    # Calculate the difference in line count
    new_lines=$((current_line_count - initial_line_count))
    
    # If new lines are added, print the count
    if [ "$new_lines" -gt 0 ]; then
        echo "New lines added: $new_lines"
        
        # Update the initial line count
        initial_line_count=$current_line_count
    fi
    
    # Sleep for 1 second before checking again
    sleep 1
done
