"""
QUIT CONFIRMATION SCREEN
Safety confirmation before exiting vault operations
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Label, Static

from screens.base_screen import BaseVaultScreen


class QuitConfirmationScreen(BaseVaultScreen):
    """Confirmation screen for vault exit"""
    
    CSS = """
    .quit-warning {
        text-style: bold;
        text-align: center;
        margin: 2 0;
    }
    
    .quit-message {
        text-align: center;
        margin: 1 0;
    }
    
    .quit-instructions {
        text-align: center;
        margin: 2 0;
    }
    """
    
    BINDINGS = BaseVaultScreen.BINDINGS + [
        Binding("escape", "cancel_quit", "ESC Cancel", show=True),
        Binding("q", "confirm_quit", "Q Confirm Quit", show=True),
        Binding("y", "confirm_quit", "Y Yes", show=True),
        Binding("n", "cancel_quit", "N No", show=True),
    ]

    def compose_content(self) -> ComposeResult:
        """Define quit confirmation content"""
        with Vertical():
            yield Label("⚠ VAULT EXIT CONFIRMATION ⚠", classes="quit-warning amber-alert-text")
            
            yield Label("Are you sure you want to exit the Vault-Tec Enterprise Suite?", classes="quit-message vault-green-text")
            yield Label("Any unsaved work or active sessions will remain intact.", classes="quit-message vault-green-text")
            
            yield Label("Press [Q] or [Y] to confirm exit", classes="quit-instructions offline-gray-text")
            yield Label("Press [ESC] or [N] to cancel and return", classes="quit-instructions offline-gray-text")
            
    def compose_status(self) -> str:
        """Define status message"""
        return "Confirm vault exit - Press Q/Y to quit or ESC/N to cancel"

    def action_confirm_quit(self) -> None:
        """Confirm and exit the application"""
        self.status_update("Exiting Vault-Tec Enterprise Suite...")
        self.app.exit()
        
    def action_cancel_quit(self) -> None:
        """Cancel quit and return to previous screen"""
        self.status_update("Exit cancelled - Returning to vault operations")
        self.app.pop_screen()