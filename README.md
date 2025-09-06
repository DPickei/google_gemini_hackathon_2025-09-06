# Gemini Command Helper 🚀

An AI-powered natural language to shell command converter using Google Gemini CLI. Describe what you want in plain English and get the perfect command back!

## Features

- **Natural Language Input**: "find all python files" → `find . -name '*.py'`
- **Auto-Clipboard**: Commands are automatically copied to your clipboard
- **Clean Output**: Just returns the command, nothing else
- **AI-Powered**: Uses Google Gemini CLI for intelligent translation
- **Universal**: Works in any terminal, anywhere, anytime  
- **Safe**: Never auto-executes, just suggests
- **Learning**: Tracks your usage patterns
- **No Background Service**: Simple standalone tool, no daemon required

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


3. **Ready to use!** 

You can now use the `g` command in two ways:

**Option A - From project directory:**
```bash
cd /Users/david/dev/google_gemini_hackathon_2025-09-06
./g pnpm run     # → suggests: pnpm run dev
```

**Option B - Add to PATH for global use:**
```bash
echo 'export PATH="$PATH:/Users/david/dev/google_gemini_hackathon_2025-09-06"' >> ~/.zshrc
source ~/.zshrc
g ls             # → works from anywhere!
```

## Usage

Use natural language or partial commands with the `g` command:

### Natural Language Examples:
```bash
g find a file named test.py        # → find . -name 'test.py'
g list all python files            # → find . -name '*.py'  
g search for hello in files        # → grep -r 'hello' .
g show running processes           # → ps aux
g check disk usage                 # → df -h
g git add all files               # → git add .
g install packages                # → npm install
```

### Traditional Completion:
```bash
g pnpm run          # → pnpm run dev
g git               # → git status  
g ls                # → ls -la
```

**That's it!** Describe what you want in plain English, get the perfect command, and it's automatically copied to your clipboard ready to paste! ✨

### View Statistics
```bash
uv run gemini-helper stats
```

## Examples

### Natural Language (The Magic! ✨)
```bash
# File operations
g find all javascript files       # → find . -name '*.js'
g copy file to backup folder      # → cp file backup/
g delete all log files            # → rm *.log

# Text searching  
g search for TODO in python files # → grep -r 'TODO' --include='*.py' .
g find lines containing error     # → grep -i 'error' *

# System monitoring
g show disk space                  # → df -h
g list running docker containers   # → docker ps
g check memory usage              # → free -h

# Git operations
g add all changes to git          # → git add .
g show git commit history         # → git log --oneline
g create new branch               # → git checkout -b
```

### Traditional Completion
```bash
g pnpm run          # → pnpm run dev
g git               # → git status
g ls                # → ls -la
```

## Architecture

- **Shell Integration**: Lightweight shell function that intercepts `-gf` flag
- **AI Completion**: Uses Google Gemini CLI for intelligent suggestions
- **Command Logging**: Tracks usage patterns and learns your habits
- **Zero Background**: No daemon, service, or background process required

## Requirements

- Python 3.10+
- Google Gemini CLI installed and configured
- Bash or Zsh shell
