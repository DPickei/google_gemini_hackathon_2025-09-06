#!/bin/bash
# Simple shell integration for Gemini Command Helper

PROJECT_DIR="/Users/david/dev/google_gemini_hackathon_2025-09-06"

# Add to .zshrc
cat >> ~/.zshrc << EOF

# Gemini Command Helper - AI completion with -g flag
# Usage: pnpm run -g, git -g, etc.
_gemini_wrapper() {
    local cmd="\$1"
    shift
    local args=("\$@")
    
    # Check if -g is in the arguments
    if [[ "\${args[-1]}" == "-g" ]]; then
        # Remove -g and complete the command
        args=("\${args[@]:0:\${#args[@]}-1}")
        local partial_command="\$cmd \${args[*]}"
        cd "$PROJECT_DIR" && uv run python -m src.shell_integration \$partial_command -g
    else
        # Execute normally
        command "\$cmd" "\${args[@]}"
    fi
}

# Alias common commands
alias pnpm='_gemini_wrapper pnpm'
alias git='_gemini_wrapper git'
alias npm='_gemini_wrapper npm'
alias docker='_gemini_wrapper docker'
alias ls='_gemini_wrapper ls'

# Direct completion command
gai() {
    if [[ \$# -eq 0 ]]; then
        echo "Usage: gai <partial-command>"
        echo "Example: gai pnpm run"
        return 1
    fi
    cd "$PROJECT_DIR" && uv run python -m src.shell_integration "\$*" -g
}
EOF

echo "✅ Added simple Gemini integration to ~/.zshrc"
echo "Now you can use: pnpm run -g, git -g, ls -g, etc."
echo "Or: gai <partial-command>"
