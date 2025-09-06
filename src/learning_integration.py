#!/usr/bin/env python3
"""
Learning integration for converting shell commands to quiz questions using -l flag
"""

import sys
from typing import Optional
from rich.console import Console
from src import learning

console = Console()

def create_learning_question(args: list[str]) -> int:
    """Create a learning question from a shell command"""
    
    # Check if -l flag is present
    if '-l' not in args:
        console.print("[red]Error: -l flag not found[/red]", file=sys.stderr)
        return 1
    
    # Remove -l flag and reconstruct command
    command_parts = [arg for arg in args if arg != '-l']
    shell_command = ' '.join(command_parts)
    
    if not shell_command.strip():
        console.print("[red]Error: No command provided[/red]", file=sys.stderr)
        return 1
    
    try:
        # Create learning manager and store the question
        learning_manager = learning.LearningManager()
        
        console.print(f"[blue]📚 Creating quiz question for:[/blue] [yellow]{shell_command}[/yellow]")
        
        success = learning_manager.store_question(shell_command)
        
        if success:
            console.print(f"[green]✅ Successfully created quiz question![/green]")
            console.print(f"[dim]Run 'uv run python -m src.quiz' to practice your questions[/dim]")
            return 0
        else:
            console.print(f"[red]❌ Failed to create quiz question[/red]", file=sys.stderr)
            return 1
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]", file=sys.stderr)
        return 1

def main():
    """Main entry point for learning integration"""
    if len(sys.argv) < 2:
        console.print("[red]Usage: learning-integration <command> -l[/red]", file=sys.stderr)
        return 1
    
    # Remove script name from args
    args = sys.argv[1:]
    return create_learning_question(args)

if __name__ == "__main__":
    sys.exit(main())
