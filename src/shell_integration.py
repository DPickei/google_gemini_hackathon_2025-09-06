#!/usr/bin/env python3
"""
Shell integration for Gemini command completion using -gf flag
"""

import sys
import subprocess
import json
from typing import Optional
from src import gemini_client
from src import command_logger

def complete_and_execute(args: list[str]) -> int:
    """Complete a command using Gemini and execute it"""
    
    # Check if -g flag is present
    if '-g' not in args:
        print("Error: -g flag not found", file=sys.stderr)
        return 1
    
    # Remove -g flag and reconstruct command
    command_parts = [arg for arg in args if arg != '-g']
    partial_command = ' '.join(command_parts)
    
    if not partial_command.strip():
        print("Error: No command provided", file=sys.stderr)
        return 1
    
    try:
        # Get completion from Gemini
        gemini = gemini_client.GeminiClient()
        completed_command = gemini.complete_command(partial_command)
        
        if not completed_command:
            print(f"No completion found for: {partial_command}", file=sys.stderr)
            return 1
        
        # Log the completion
        logger = command_logger.CommandLogger()
        logger.log_completion(partial_command, completed_command)
        
        # Copy to clipboard (macOS)
        try:
            subprocess.run(['pbcopy'], input=completed_command, text=True, check=True)
        except Exception:
            pass  # Silently fail if pbcopy isn't available
        
        # Just output the command, nothing else
        print(completed_command)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def main():
    """Main entry point for shell integration"""
    if len(sys.argv) < 2:
        print("Usage: gemini-complete <command> -g", file=sys.stderr)
        return 1
    
    # Remove script name from args
    args = sys.argv[1:]
    return complete_and_execute(args)

if __name__ == "__main__":
    sys.exit(main())
