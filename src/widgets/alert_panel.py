"""
Alert Center Panel Widget
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from .vault_container import VaultContainer


class AlertPanel(Widget):
    """System alerts and warnings panel"""
    
    CSS = """
    AlertPanel {
        width: 1fr;
        margin: 0 1;
    }
    
    .alert-container {
        height: 100%;
        border: solid #00ff00;
        border-title-color: #ffb000; 
        border-title-style: bold;
    }
    
    .alert-item {
        margin: 0 1;
        height: 1;
    }
    
    .alert-warning {
        color: #f59e0b;
    }
    
    .alert-critical {
        color: #dc2626;
    }
    
    .alert-info {
        color: #00ff00;
    }
    """

    def compose(self) -> ComposeResult:
        """Build the alert panel"""
        with VaultContainer(title="ALERTS", classes="alert-container"):
            with Vertical():
                yield Static("⚠ 2 Schema", classes="alert-item alert-warning", id="schema_warnings")
                yield Static("  Warnings", classes="alert-item alert-warning")
                yield Static("● 0 Critical", classes="alert-item alert-info", id="critical_alerts")
                yield Static("  Issues", classes="alert-item alert-info")

    def update_alerts(self, alerts: list):
        """Update alert information"""
        schema_warnings = sum(1 for a in alerts if a.get("type") == "schema" and a.get("level") == "warning")
        critical_alerts = sum(1 for a in alerts if a.get("level") == "critical")
        
        self.query_one("#schema_warnings", Static).update(f"⚠ {schema_warnings} Schema")
        self.query_one("#critical_alerts", Static).update(f"● {critical_alerts} Critical")