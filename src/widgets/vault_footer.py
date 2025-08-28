"""
Enhanced Vault-Tec Footer with Command Traces
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widget import Widget
from textual.widgets import Static
import json


class VaultFooter(Widget):
    """Footer with integrated command/response traces"""
    
    CSS = """
    VaultFooter {
        dock: bottom;
        height: 3;
        background: #1a1a1a;
    }
    
    .send-trace {
        height: 1;
        background: #0a0a0a;
        color: #ffb000;
        border-top: solid #1a1a1a;
        text-style: bold;
    }
    
    .recv-trace {
        height: 1;
        background: #0a0a0a;  
        color: #22c55e;
        text-style: dim;
    }
    
    .key-bindings {
        height: 1;
        background: #1a1a1a;
        color: #00ff00;
        text-align: center;
    }
    """

    def compose(self) -> ComposeResult:
        """Build the enhanced footer"""
        with Vertical():
            yield Static("CMD: Vault-Tec send_trace ready...", id="send_trace_text", classes="send-trace")
            yield Static("RSP: Vault-Tec recv_trace ready...", id="recv_trace_text", classes="recv-trace") 
            yield Static("CTRL+C Quit | H Help | ⏎ Execute | ESC Back", id="key_bindings", classes="key-bindings")

    def show_send_trace(self, command: str, data: dict = None) -> None:
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
        send_trace = self.query_one("#send_trace_text", Static)
        send_trace.update(f"CMD: {display_text}")
        
        # Clear after brief delay
        self.set_timer(2.0, self.clear_send_trace)
    
    def show_recv_trace(self, data: any) -> None:
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
            recv_trace = self.query_one("#recv_trace_text", Static)
            recv_trace.update(f"RSP: {json_str}")
            
            # Clear after brief delay
            self.set_timer(1.5, self.clear_recv_trace)
            
        except Exception:
            # Fallback for unparseable data
            recv_trace = self.query_one("#recv_trace_text", Static)
            recv_trace.update("RSP: [unparseable response]")
            self.set_timer(1.5, self.clear_recv_trace)
    
    def clear_send_trace(self) -> None:
        """Clear the send trace display"""
        send_trace = self.query_one("#send_trace_text", Static)
        send_trace.update("CMD: Ready...")
    
    def clear_recv_trace(self) -> None:
        """Clear the recv trace display"""
        recv_trace = self.query_one("#recv_trace_text", Static)
        recv_trace.update("RSP: Ready...")
        
    def update_key_bindings(self, bindings: str) -> None:
        """Update the key bindings display"""
        key_bindings = self.query_one("#key_bindings", Static)
        key_bindings.update(bindings)