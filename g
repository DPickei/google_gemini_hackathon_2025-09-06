#!/bin/bash
# Gemini Command Helper - Natural language to shell command converter
# Usage: g <description or partial command>
# Output: displays command and copies it to clipboard
# Examples: 
#   g pnpm run
#   g find a file named test.py
#   g list all python files

if [[ $# -eq 0 ]]; then
    echo "Usage: g <description or partial command>"
    echo "Examples:"
    echo "  g pnpm run"
    echo "  g find a file named test.py"
    echo "  g list all python files"
    echo "  g search for 'hello' in files"
    echo "  g show running processes"
    exit 1
fi

# Get the project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


# Run the completion
cd "$SCRIPT_DIR" && uv run python -m src.shell_integration "$*" -g
