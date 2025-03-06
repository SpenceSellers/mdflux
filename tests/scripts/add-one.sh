#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "No argument provided"
    exit 1
fi

# Add 1 to the argument
result=$(( $1 + 1 ))

# Output the result
echo $result