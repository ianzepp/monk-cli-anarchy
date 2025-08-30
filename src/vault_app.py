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
        # App-level bindings are hidden - screens handle their own display
        Binding("ctrl+c", "quit", "Quit", priority=True, show=False),
    ]

    def __init__(self):
        super().__init__()
        self.current_user = None
        self.current_vault = None
        self.authenticated = False
        self.vault_footer = None

    def compose(self) -> ComposeResult:
        """Compose the main application layout"""
        # No app-level widgets - screens fully control their layout
        return []

    def on_mount(self) -> None:
        """Application startup"""
        from config import config
        
        # Check for development mode screen bypass
        if config.dev_start_screen:
            self._start_dev_screen(config.dev_start_screen)
        else:
            # Start with welcome screen to demonstrate 4-row layout
            from screens.welcome_screen import WelcomeScreen
            self.push_screen(WelcomeScreen())

    def action_help(self) -> None:
        """Show help documentation"""
        self.bell()
        # TODO: Implement help system

    def action_ai_assistant(self) -> None:
        """Open global AI assistant"""
        from screens.ai_assistant_screen import AIAssistantScreen
        self.push_screen(AIAssistantScreen())

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
    
    def _start_dev_screen(self, screen_name: str) -> None:
        """Start application at specific screen for development/testing"""
        from config import config
        
        # Set up mock authentication state if needed
        if config.dev_mock_auth:
            self.current_user = config.default_username
            self.current_vault = config.default_tenant
            self.authenticated = True
        
        # Route to specific screens
        screen_name = screen_name.lower()
        
        if screen_name == "overseer":
            self.current_user = self.current_user or "dev-user"
            self.current_vault = self.current_vault or "dev-vault"
            self.authenticated = True
            from screens.overseer_screen import OverseerScreen
            self.push_screen(OverseerScreen())
            
        elif screen_name == "population":
            self.current_user = self.current_user or "dev-user"
            self.current_vault = self.current_vault or "dev-vault"
            self.authenticated = True
            from screens.population_management_screen import PopulationManagementScreen
            self.push_screen(PopulationManagementScreen())
            
        elif screen_name == "department" or screen_name == "registry":
            self.current_user = self.current_user or "dev-user"
            self.current_vault = self.current_vault or "dev-vault"
            self.authenticated = True
            from screens.department_registry_screen import DepartmentRegistryScreen
            self.push_screen(DepartmentRegistryScreen())
            
        elif screen_name == "schema" or screen_name == "lab":
            self.current_user = self.current_user or "dev-user"
            self.current_vault = self.current_vault or "dev-vault"
            self.authenticated = True
            from screens.schema_lab_screen import SchemaLabScreen
            self.push_screen(SchemaLabScreen())
            
        elif screen_name == "schema_wizard_1":
            self.current_user = self.current_user or "dev-user"
            self.current_vault = self.current_vault or "dev-vault"
            self.authenticated = True
            from screens.schema_wizard_screen import SchemaWizardScreen
            self.push_screen(SchemaWizardScreen(mode="create"))
            
        elif screen_name == "server":
            from screens.server_selection_screen import ServerSelectionScreen
            self.push_screen(ServerSelectionScreen())
            
        elif screen_name == "tenant":
            from screens.tenant_selection_screen import TenantSelectionScreen
            self.push_screen(TenantSelectionScreen("dev-server"))
            
        elif screen_name == "session":
            from screens.session_selection_screen import SessionSelectionScreen
            self.push_screen(SessionSelectionScreen("dev-server", "dev-tenant"))
            
        else:
            # Unknown screen, fall back to welcome
            from screens.welcome_screen import WelcomeScreen
            self.push_screen(WelcomeScreen())