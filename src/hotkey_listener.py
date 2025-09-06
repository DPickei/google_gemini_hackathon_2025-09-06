"""
Global hotkey listener for cmd+g to trigger command completion
"""

import logging
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from rich.console import Console
from src import terminal_interface
from src import gemini_client
from src import command_logger

console = Console()
logger = logging.getLogger(__name__)

class HotkeyService:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.terminal = terminal_interface.TerminalInterface()
        self.gemini = gemini_client.GeminiClient()
        self.logger = command_logger.CommandLogger()
        self.pressed_keys = set()
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
    
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            self.pressed_keys.add(key)
            
            # Check for cmd+g combination
            if (Key.cmd in self.pressed_keys and 
                (hasattr(key, 'char') and key.char == 'g')):
                self._handle_completion_request()
                
        except AttributeError:
            # Special keys (ctrl, alt, etc.) might not have char attribute
            pass
    
    def on_key_release(self, key):
        """Handle key release events"""
        try:
            self.pressed_keys.discard(key)
        except KeyError:
            pass
    
    def _handle_completion_request(self):
        """Handle the cmd+g hotkey press"""
        try:
            if self.debug:
                console.print("[cyan]🔍 Hotkey detected! Getting current command...[/cyan]")
            
            # Get current command from terminal
            current_command = self.terminal.get_current_command()
            
            if not current_command or not current_command.strip():
                if self.debug:
                    console.print("[yellow]No command found in terminal[/yellow]")
                return
            
            if self.debug:
                console.print(f"[blue]Current command: '{current_command}'[/blue]")
            
            # Get completion from Gemini
            completed_command = self.gemini.complete_command(current_command)
            
            if completed_command and completed_command != current_command:
                # Replace the command in terminal
                self.terminal.replace_current_command(completed_command)
                
                # Log the completion
                self.logger.log_completion(current_command, completed_command)
                
                if self.debug:
                    console.print(f"[green]✨ Completed to: '{completed_command}'[/green]")
            else:
                if self.debug:
                    console.print("[yellow]No completion suggestion available[/yellow]")
                    
        except Exception as e:
            if self.debug:
                console.print(f"[red]Error during completion: {e}[/red]")
            logger.error(f"Error handling completion request: {e}")
    
    def start(self):
        """Start the hotkey listener service"""
        console.print("[green]🎯 Hotkey listener active - Press Cmd+G to complete commands[/green]")
        console.print("[dim]Press Ctrl+C to stop[/dim]")
        
        with keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release) as listener:
            listener.join()
