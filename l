#!/bin/bash
# Learning Command Helper - Convert shell commands to quiz questions
# Usage: l <command>
# Output: creates a quiz question and stores it for later practice
# Examples: 
#   l find . -name '*main*'
#   l grep -r "hello" .
#   l pnpm run dev

if [[ $# -eq 0 ]]; then
    echo "Usage: l <command>"
    echo "Examples:"
    echo "  l find . -name '*main*'"
    echo "  l grep -r 'hello' ."
    echo "  l pnpm run dev"
    echo "  l docker ps"
    echo "  l git status"
    exit 1
fi

# Get the project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the learning integration
cd "$SCRIPT_DIR" && uv run python -m src.learning_integration "$*" -l
