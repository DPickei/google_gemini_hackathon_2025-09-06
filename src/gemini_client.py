"""
Client for interacting with Google Gemini CLI
"""

import subprocess
import logging
import os
from typing import Optional
import json
import re

logger = logging.getLogger(__name__)

class GeminiClient:
    """Handles interaction with the Gemini CLI for command completion"""
    
    def __init__(self):
        self.gemini_command = "gemini"
        self._test_gemini_availability()
    
    def _test_gemini_availability(self):
        """Test if Gemini CLI is available"""
        try:
            result = subprocess.run(
                [self.gemini_command, '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                logger.warning("Gemini CLI may not be properly configured")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.error("Gemini CLI not found. Please ensure it's installed and in PATH")
    
    def complete_command(self, partial_command: str) -> Optional[str]:
        """Get command completion from Gemini AI"""
        try:
            # Create a focused prompt for command completion
            prompt = self._create_completion_prompt(partial_command)
            
            # Call Gemini CLI - use list format to avoid shell escaping issues
            result = subprocess.run(
                [self.gemini_command, '-p', prompt],
                capture_output=True,
                text=True,
                timeout=30,
                env=dict(os.environ)  # Inherit environment
            )
            
            if result.returncode == 0:
                completion = self._parse_completion_response(result.stdout.strip())
                return completion
            else:
                logger.error(f"Gemini CLI error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("Gemini CLI request timed out")
            return None
        except Exception as e:
            logger.error(f"Error calling Gemini CLI: {e}")
            return None
    
    def _create_completion_prompt(self, partial_command: str) -> str:
        """Create a focused prompt for command completion"""
        return f'''Convert this to a shell command. Return only the command, nothing else.

Input: {partial_command}

Examples:
- "pnpm run" → "pnpm run dev"
- "git status" → "git status"
- "list files" → "ls -la"
- "find a file named script.py" → "find . -name 'script.py'"
- "search for text in files" → "grep -r 'text' ."
- "show running processes" → "ps aux"
- "check disk usage" → "df -h"
- "install package" → "npm install"
- "git add all files" → "git add ."

Command:'''
    
    def _parse_completion_response(self, response: str) -> Optional[str]:
        """Parse the Gemini response to extract the completed command"""
        try:
            # Clean up the response
            response = response.strip()
            
            if not response:
                return None
            
            # Split into lines and find the most likely command
            lines = [line.strip() for line in response.split('\n') if line.strip()]
            
            if not lines:
                return None
            
            # Look for the first line that looks like a command
            for line in lines:
                # Skip obvious explanatory text
                if any(skip in line.lower() for skip in ['here', 'the completed', 'command:', 'output:', 'result:']):
                    continue
                
                # Clean the line but preserve quotes if they're balanced
                line = line.strip()
                
                # If it looks like a command, return it (don't strip quotes if they're balanced)
                if line and not line.endswith(':') and not line.startswith(('Note:', 'Example:', 'Usage:')):
                    # Fix common quote issues
                    line = self._fix_quotes(line)
                    return line
            
            # Fallback: return the first non-empty line
            first_line = lines[0].strip()
            return self._fix_quotes(first_line)
            
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {e}")
            return None
    
    def _fix_quotes(self, command: str) -> str:
        """Fix unbalanced quotes in commands"""
        try:
            # Count quotes
            single_quotes = command.count("'")
            double_quotes = command.count('"')
            
            # Fix unbalanced single quotes
            if single_quotes % 2 == 1:
                # Find the last single quote and add a closing one
                command = command + "'"
            
            # Fix unbalanced double quotes  
            if double_quotes % 2 == 1:
                # Find the last double quote and add a closing one
                command = command + '"'
            
            return command
            
        except Exception as e:
            logger.error(f"Error fixing quotes: {e}")
            return command
    
    def log_completion(self, original_command: str, completed_command: str):
        """Log the completion for future learning (placeholder for now)"""
        # TODO: Implement logging to a file for tracking patterns
        logger.info(f"Completion: '{original_command}' → '{completed_command}'")
