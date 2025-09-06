#!/usr/bin/env python3
"""
Gemini Command Helper - AI-powered command line completion
"""

import click
from rich.console import Console
from rich.table import Table
from src import hotkey_listener
from src import terminal_interface
from src import command_logger

console = Console()

@click.group()
def cli():
    """Gemini Command Helper - AI-powered command line completion"""
    pass

@cli.command()
@click.option('--debug', is_flag=True, help='Enable debug mode')
def start(debug: bool):
    """Start the Gemini Command Helper service."""
    console.print("[bold green]🚀 Starting Gemini Command Helper...[/bold green]")
    
    if debug:
        console.print("[yellow]Debug mode enabled[/yellow]")
    
    try:
        # Start the hotkey listener service
        service = hotkey_listener.HotkeyService(debug=debug)
        service.start()
    except KeyboardInterrupt:
        console.print("\n[bold red]Shutting down Gemini Command Helper...[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

@cli.command()
def stats():
    """Show usage statistics and patterns."""
    logger = command_logger.CommandLogger()
    stats_data = logger.get_stats()
    
    if not stats_data:
        console.print("[yellow]No usage data yet. Start using the tool to see statistics![/yellow]")
        return
    
    console.print("\n[bold blue]📊 Gemini Command Helper Statistics[/bold blue]\n")
    
    # Overall stats
    console.print(f"Total completions: [green]{stats_data.get('total_completions', 0)}[/green]")
    
    # Most common prefixes
    if stats_data.get('most_common_prefixes'):
        table = Table(title="Most Used Command Prefixes")
        table.add_column("Command Prefix", style="cyan")
        table.add_column("Count", style="green")
        
        for prefix, count in stats_data['most_common_prefixes'].items():
            table.add_row(prefix, str(count))
        
        console.print(table)
    
    # Most forgotten commands
    if stats_data.get('most_forgotten_commands'):
        table = Table(title="Most Frequently Completed Commands")
        table.add_column("Partial Command", style="yellow") 
        table.add_column("Times Completed", style="green")
        
        for cmd, count in stats_data['most_forgotten_commands'].items():
            table.add_row(cmd, str(count))
        
        console.print(table)
    
    # Recent completions
    recent = logger.get_recent_completions(5)
    if recent:
        table = Table(title="Recent Completions")
        table.add_column("Original", style="yellow")
        table.add_column("Completed", style="green")
        table.add_column("Time", style="dim")
        
        for entry in recent:
            timestamp = entry['timestamp'][:19].replace('T', ' ')  # Format timestamp
            table.add_row(entry['original'], entry['completed'], timestamp)
        
        console.print(table)

def main():
    """Entry point for the CLI"""
    cli()

if __name__ == "__main__":
    main()
