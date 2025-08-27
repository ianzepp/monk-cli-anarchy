"""
System Status Panel Widget
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from .vault_container import VaultContainer, StatusIndicator


class SystemStatusPanel(Widget):
    """System status monitoring panel"""
    
    CSS = """
    SystemStatusPanel {
        width: 1fr;
        margin: 0 1;
    }
    
    .status-container {
        height: 100%;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
    }
    
    .status-item {
        margin: 0 1;
        height: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Build the system status panel"""
        with VaultContainer(title="SYSTEM STATUS", classes="status-container"):
            with Vertical():
                yield StatusIndicator("ok", "● DATABASE: OK", classes="status-item")
                yield StatusIndicator("ok", "● API: ONLINE", classes="status-item") 
                yield StatusIndicator("ok", "● OBSERVERS: OK", classes="status-item")
                yield StatusIndicator("ok", "● SECURITY: OK", classes="status-item")

    def update_system_status(self, status_data: dict):
        """Update system status from API data"""
        status_items = self.query(StatusIndicator)
        
        # Map status to display text and status
        status_mapping = {
            "database": ("● DATABASE", 0),
            "api": ("● API", 1), 
            "observers": ("● OBSERVERS", 2),
            "security": ("● SECURITY", 3)
        }
        
        for system, data in status_data.items():
            if system in status_mapping:
                label, index = status_mapping[system]
                status_text = data.upper()
                
                try:
                    status_item = status_items[index]
                    status_item.update(f"{label}: {status_text}")
                    status_item.update_status(data)
                except (IndexError, AttributeError):
                    pass  # Widget might not be available