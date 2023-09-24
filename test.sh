#!/bin/bash

# Specify the JSON file path
json_file="r.json"

# Define the repository name you want to search for
search_repo="Test"

# Use jq to search for the repository and extract its domain
domain=$(jq -r --arg search_repo "$search_repo" '.[] | select(.REPO == $search_repo) | .DOMAIN' "$json_file")

# Check if the domain is not null
if [ ! -z "$domain" ]; then
    echo "Domain for $search_repo: $domain"
else
    echo "Repository not found: $search_repo"
fi