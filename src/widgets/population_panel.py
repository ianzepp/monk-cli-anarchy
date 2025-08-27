"""
Vault Population Panel Widget
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from .vault_container import VaultContainer


class PopulationPanel(Widget):
    """Vault population statistics panel"""
    
    CSS = """
    PopulationPanel {
        width: 1fr;
        margin: 0 1;
    }
    
    .population-container {
        height: 100%;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
    }
    
    .pop-stat {
        margin: 0 1;
        height: 1;
        color: #00ff00;
    }
    """

    def compose(self) -> ComposeResult:
        """Build the population panel"""
        with VaultContainer(title="VAULT POPULATION", classes="population-container"):
            with Vertical():
                yield Static("Total Records: 847", classes="pop-stat", id="total_records")
                yield Static("Active: 834", classes="pop-stat", id="active_records")
                yield Static("Offline: 13", classes="pop-stat", id="offline_records")  
                yield Static("Last Update: 14:32", classes="pop-stat", id="last_update")

    def update_population_stats(self, stats: dict):
        """Update population statistics"""
        self.query_one("#total_records", Static).update(f"Total Records: {stats.get('total', 0)}")
        self.query_one("#active_records", Static).update(f"Active: {stats.get('active', 0)}")
        self.query_one("#offline_records", Static).update(f"Offline: {stats.get('offline', 0)}")
        self.query_one("#last_update", Static).update(f"Last Update: {stats.get('timestamp', 'Unknown')}")