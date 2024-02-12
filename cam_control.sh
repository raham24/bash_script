#!/bin/bash

# Function to handle Ctrl+C
function cleanup {
    echo "Ctrl+C pressed. Stopping scripts..."
    # Add any cleanup tasks here if needed
    kill 0  # Kill all child processes
    exit 1
}

# Register cleanup function for Ctrl+C
trap cleanup SIGINT

# List of Python programs to run concurrently
python_scripts=("rpi_camera.py" "servo_test.py")

# Infinite loop to run the scripts
while true; do
    for script in "${python_scripts[@]}"; do
        echo "Running $script"
        python3 "$script" &
    done

    # Wait for all background processes to finish
    wait
done

