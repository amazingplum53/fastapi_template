#!/bin/bash

# File containing the environment variables (you can pass it as an argument or set here)
env_file="$1"

# Check if the file exists
if [[ ! -f "$env_file" ]]; then
  echo "File not found: $env_file"
  exit 1
fi

# Read the file line by line and export the variables
while IFS='=' read -r key value; do
  if [[ -n "$key" && -n "$value" ]]; then
    export "$key"="$value"
    echo "Exported: $key=$value"
  fi
done < "$env_file"