"""
VAULT-TEC ENTERPRISE SUITE™
Main Application Class
"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header
from textual.screen import Screen

from screens.auth_screen import AuthScreen
from screens.overseer_screen import OverseerScreen
from theme.vault_theme import VAULT_CSS
from widgets.vault_footer import VaultFooter
from api.monk_client import monk


class VaultApp(App):
    """Main Vault-Tec Enterprise Suite Application"""
    
    TITLE = "VAULT-TEC ENTERPRISE SUITE™ v2.0.0"
    SUB_TITLE = "Building Tomorrow's Business Solutions... Yesterday's Way"
    CSS = VAULT_CSS
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True, show=True),
        Binding("h", "help", "Help", show=True),
        Binding("ctrl+c", "quit", "Quit", priority=True),
    ]

    def __init__(self):
        super().__init__()
        self.current_user = None
        self.current_vault = None
        self.authenticated = False
        self.vault_footer = None

    def compose(self) -> ComposeResult:
        """Compose the main application layout"""
        # Add simple footer for now (traces can be added later)
        yield Footer()

    def on_mount(self) -> None:
        """Application startup"""
        # Start with authentication screen
        self.push_screen(AuthScreen())

    def action_help(self) -> None:
        """Show help documentation"""
        self.bell()
        # TODO: Implement help system

    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()

    def authenticate_user(self, user_data: dict) -> None:
        """Handle successful authentication"""
        self.current_user = user_data.get("username")
        self.current_vault = user_data.get("vault_id") 
        self.authenticated = True
        
        # Switch to main dashboard
        self.pop_screen()  # Remove auth screen
        self.push_screen(OverseerScreen())

    def logout(self) -> None:
        """Handle user logout"""
        self.current_user = None
        self.current_vault = None
        self.authenticated = False
        
        # Return to authentication
        self.pop_screen()  # Remove current screen
        self.push_screen(AuthScreen())