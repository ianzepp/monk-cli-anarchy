#!/bin/bash

# DEVELOPMENT TESTING SCRIPT
# Jump directly to specific screens for testing

SCREEN=${1:-"welcome"}

echo "Starting Vault-Tec Enterprise Suite in DEV MODE..."
echo "Target screen: $SCREEN"

# Set development environment variables
export DEV_START_SCREEN="$SCREEN"
export DEV_MOCK_AUTH="true"
export DEBUG="true"

# Use the existing run script but with dev settings
./run.sh