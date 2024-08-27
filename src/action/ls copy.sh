#!/bin/bash

# Check if a directory was provided as an argument, otherwise use the current directory
DIR=${1:-.}

# Use 'ls' to list files and 'awk' to convert size to MB
ls -lhS --block-size=M "$DIR" | awk '{print $9 ": " $5}'
