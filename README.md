# Command 
Gemini CLI powered assistant for making commands. Use natural language OR partial command syntax and it will complete your command! After, you can quiz yourself on the command to improve your command capabilities.

## Features
- **Partial Syntax Completion**: `pnpm run` → `pnpm run dev`
- **Natural Language Input**: "find all python files" → `find . -name '*.py'`
- **Auto-Clipboard**: Commands are automatically copied to your clipboard
- **Learning System**: Convert commands to Duolingo-style quiz questions for practice

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Ensure Gemini CLI is installed**:
   ```bash
   # Test that gemini CLI is available
   gemini --help
   ```

## Usage
Use the `./g` command from the project directory:

```bash
cd /Users/david/dev/google_gemini_hackathon_2025-09-06
./g pnpm run     # → suggests: pnpm run dev
./g find all python files  # → find . -name '*.py'
```

- The `./g` command supports two types of input:

### Syntax Fix / Completion:
```bash
./g pnpm run env      # → pnpm run dev
./g git state         # → git status  
./g docker            # → docker ps
./g find . -name      # → find . -name '*.py'
```

### Natural Language:
```bash
./g find a file named test.py        # → find . -name 'test.py'
./g list all python files           # → find . -name '*.py'  
./g search for hello in files       # → grep -r 'hello' .
./g show running processes          # → ps aux
./g check disk usage                # → df -h
./g git add all files              # → git add .
./g install packages               # → npm install
```

## Syntax Quiz

Create quiz questions from commands you want to remember:
```bash
./l find . -name '*.py'     # Creates a quiz question
uv run python -m src.quiz   # Take the quiz
```

## Requirements

- Python 3.10+
- Google Gemini CLI installed and configured