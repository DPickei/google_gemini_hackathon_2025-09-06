"""
Interface for interacting with the terminal application
"""

import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class TerminalInterface:
    """Handles interaction with the active terminal application"""
    
    def __init__(self):
        self.supported_terminals = ['Ghostty', 'Terminal', 'iTerm2', 'iTerm']
    
    def get_current_command(self) -> Optional[str]:
        """Get the current command line input from the active terminal"""
        try:
            # Try to get from Ghostty first (user's preferred terminal)
            command = self._get_ghostty_command()
            if command:
                return command
            
            # Fallback to other terminals
            for terminal in self.supported_terminals:
                command = self._get_terminal_command(terminal)
                if command:
                    return command
                    
            return None
            
        except Exception as e:
            logger.error(f"Error getting current command: {e}")
            return None
    
    def replace_current_command(self, new_command: str) -> bool:
        """Replace the current command in the terminal with a new one"""
        try:
            # Try Ghostty first
            if self._replace_ghostty_command(new_command):
                return True
            
            # Fallback to other terminals
            for terminal in self.supported_terminals:
                if self._replace_terminal_command(terminal, new_command):
                    return True
                    
            return False
            
        except Exception as e:
            logger.error(f"Error replacing command: {e}")
            return False
    
    def _get_ghostty_command(self) -> Optional[str]:
        """Get command from Ghostty terminal"""
        applescript = '''
        tell application "System Events"
            tell process "Ghostty"
                if exists then
                    tell window 1
                        set currentLine to value of text field 1
                        return currentLine
                    end tell
                end if
            end tell
        end tell
        '''
        return self._run_applescript(applescript)
    
    def _get_terminal_command(self, terminal_name: str) -> Optional[str]:
        """Get command from specified terminal application"""
        if terminal_name == "Terminal":
            applescript = f'''
            tell application "{terminal_name}"
                if (count of windows) > 0 then
                    tell window 1
                        tell tab 1
                            set currentLine to contents of text field 1
                            return currentLine
                        end tell
                    end tell
                end if
            end tell
            '''
        else:  # iTerm variants
            applescript = f'''
            tell application "{terminal_name}"
                if (count of windows) > 0 then
                    tell current session of current tab of current window
                        set currentLine to contents of text field 1
                        return currentLine
                    end tell
                end if
            end tell
            '''
        
        return self._run_applescript(applescript)
    
    def _replace_ghostty_command(self, new_command: str) -> bool:
        """Replace command in Ghostty terminal"""
        applescript = f'''
        tell application "System Events"
            tell process "Ghostty"
                if exists then
                    tell window 1
                        keystroke "a" using command down
                        keystroke "{new_command}"
                        return true
                    end tell
                end if
            end tell
        end tell
        '''
        result = self._run_applescript(applescript)
        return result == "true"
    
    def _replace_terminal_command(self, terminal_name: str, new_command: str) -> bool:
        """Replace command in specified terminal"""
        applescript = f'''
        tell application "System Events"
            tell process "{terminal_name}"
                if exists then
                    keystroke "a" using command down
                    keystroke "{new_command}"
                    return true
                end if
            end tell
        end tell
        '''
        result = self._run_applescript(applescript)
        return result == "true"
    
    def _run_applescript(self, script: str) -> Optional[str]:
        """Execute AppleScript and return the result"""
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.warning(f"AppleScript error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("AppleScript execution timed out")
            return None
        except Exception as e:
            logger.error(f"Error running AppleScript: {e}")
            return None
