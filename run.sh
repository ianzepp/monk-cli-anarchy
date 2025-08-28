#!/bin/bash

# Function to reset terminal (less aggressive - preserve text selection)
reset_terminal() {
    # Only disable problematic mouse modes, keep text selection working
    printf '\e[?1003l\e[?1015l\e[?1006l\e[?25h'
    tput rmcup 2>/dev/null || true
    clear
}

# Function to cleanup on exit
cleanup() {
    reset_terminal
    exit 0
}

# Set up signal handlers
trap cleanup EXIT INT TERM

# Initial terminal reset
reset_terminal

echo "Starting Vault-Tec Enterprise Suite..."
echo "Activating virtual environment..."

# Set development monk executable path
export MONK_EXECUTABLE="/Users/ianzepp/Workspaces/monk-cli/monk"
echo "Using monk executable: $MONK_EXECUTABLE"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate" 
    echo "  python3 -m pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment and set Python executable
source venv/bin/activate

# Function to use venv Python executable
python_exec() {
    ./venv/bin/python "$@"
}

if ! python_exec -c "import textual" 2>/dev/null; then
    echo "Error: Textual not installed. Installing dependencies..."
    python_exec -m pip install -r requirements.txt
fi

echo "Launching application..."
python_exec main.py

# Cleanup happens automatically via trap