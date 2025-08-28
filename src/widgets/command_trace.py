"""
Command Trace Widget
Fast-scrolling command execution display
"""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Static
import json


class SendTrace(Widget):
    """Fast-scrolling command execution trace"""
    
    CSS = """
    SendTrace {
        dock: bottom;
        height: 1;
        background: #0a0a0a;
        color: #ffb000;
        border-top: solid #1a1a1a;
        z-index: 10;
    }
    
    .command-display {
        text-style: bold;
        color: #ffb000;
        width: 100%;
        overflow: hidden;
    }
    """

    def __init__(self):
        super().__init__()
        self.current_command = ""

    def compose(self) -> ComposeResult:
        """Build the command trace"""
        with Horizontal():
            yield Static("CMD: Vault-Tec command trace ready...", id="command_text", classes="command-display")

    def show_command(self, command: str, data: dict = None) -> None:
        """Display a command execution (briefly)"""
        # Format command with optional JSON data
        display_text = f"monk {command}"
        if data:
            json_str = json.dumps(data, separators=(',', ':'))  # Compact JSON
            if len(json_str) > 50:
                json_str = json_str[:47] + "..."
            display_text += f" {json_str}"
        
        # Truncate if too long
        if len(display_text) > 120:
            display_text = display_text[:117] + "..."
        
        # Update display
        self.current_command = display_text
        command_display = self.query_one("#command_text", Static)
        command_display.update(f"CMD: {display_text}")
        
        # Clear after brief delay
        self.set_timer(2.0, self.clear_command)
    
    def clear_command(self) -> None:
        """Clear the command display"""
        command_display = self.query_one("#command_text", Static)
        command_display.update("")


class RecvTrace(Widget):
    """Fast-scrolling JSON response trace"""
    
    CSS = """
    RecvTrace {
        dock: bottom;
        height: 1;
        background: #0a0a0a;
        color: #22c55e;
        border-top: solid #1a1a1a;
        z-index: 11;
    }
    
    .response-display {
        color: #22c55e;
        width: 100%;
        overflow: hidden;
        text-style: dim;
    }
    """

    def compose(self) -> ComposeResult:
        """Build the response trace"""
        with Horizontal():
            yield Static("RSP: Vault-Tec response trace ready...", id="response_text", classes="response-display")

    def show_response(self, data: any) -> None:
        """Display a JSON response (briefly)"""
        try:
            if isinstance(data, (dict, list)):
                # Convert to compact JSON
                json_str = json.dumps(data, separators=(',', ':'))
            else:
                # Raw text response
                json_str = str(data)
            
            # Truncate if too long
            if len(json_str) > 150:
                json_str = json_str[:147] + "..."
                
            # Update display
            response_display = self.query_one("#response_text", Static)
            response_display.update(f"RSP: {json_str}")
            
            # Clear after brief delay
            self.set_timer(1.5, self.clear_response)
            
        except Exception:
            # Fallback for unparseable data
            response_display = self.query_one("#response_text", Static)
            response_display.update("RSP: [unparseable response]")
            self.set_timer(1.5, self.clear_response)
    
    def clear_response(self) -> None:
        """Clear the response display"""
        response_display = self.query_one("#response_text", Static)
        response_display.update("")