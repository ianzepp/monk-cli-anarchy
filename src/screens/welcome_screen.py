"""
VAULT-TEC ENTERPRISE SUITE WELCOME SCREEN
Entry point demonstrating 4-row layout design language
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Label, Static
from datetime import datetime

from widgets.vault_container import VaultContainer
from screens.base_screen import BaseVaultScreen


class WelcomeScreen(BaseVaultScreen):
    """Welcome screen implementing 4-row design language"""
    
    CSS = """
    .welcome-content {
        text-align: center;
        align: center middle;
    }
    
    .vault-logo {
        text-style: bold;
        text-align: center;
        margin: 2 0;
    }
    
    .subtitle {
        text-style: italic;
        text-align: center;
        margin: 1 0;
    }
    
    .instructions {
        text-align: center;
        margin: 2 0;
    }
    """
    
    BINDINGS = BaseVaultScreen.BINDINGS + [
        Binding("o", "open_connection", "Open Connection", show=False),
    ]

    def compose_commands(self) -> list[str]:
        """Define local killbox commands"""
        return ["[o] Open Connection"]
        
    def compose_status(self) -> str:
        """Define default status message"""
        return "System ready - All vault facility modules operational"

    def compose_content(self) -> ComposeResult:
        """Define welcome screen content"""
        with Vertical(classes="welcome-content"):
            yield Static("""
██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗    ████████╗███████╗ ██████╗
██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝    ╚══██╔══╝██╔════╝██╔════╝
██║   ██║███████║██║   ██║██║     ██║          ██║   █████╗  ██║     
╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║          ██║   ██╔══╝  ██║     
 ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║          ██║   ███████╗╚██████╗
  ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝          ╚═╝   ╚══════╝ ╚═════╝
            """, classes="vault-logo amber-alert-text")
            
            yield Label("ENTERPRISE SUITE™", classes="subtitle steel-blue-text")
            yield Label('"Building Tomorrow\'s Business Solutions... Yesterday\'s Way"', classes="subtitle steel-blue-text")
            
            yield Label("Welcome to the Vault-Tec Enterprise Suite™", classes="welcome-content vault-green-text")
            yield Label("Your comprehensive terminal interface for monk-cli operations", classes="welcome-content vault-green-text")
            
            yield Label("Press [o] to open a vault facility connection", classes="instructions offline-gray-text")
            yield Label("Press [?] for AI assistance with vault operations", classes="instructions offline-gray-text")


    def action_open_connection(self) -> None:
        """Open vault facility connection (start authentication flow)"""
        # Update status to show action
        self.status_update("Opening vault facility connection...")
        
        # Start authentication flow
        from screens.server_selection_screen import ServerSelectionScreen
        self.app.push_screen(ServerSelectionScreen())