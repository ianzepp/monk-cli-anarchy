"""
VAULT-TEC NETWORK ACCESS TERMINAL
Authentication Screen Implementation
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Static
from textual.message import Message

from widgets.vault_container import VaultContainer
from config import config


class AuthScreen(Screen):
    """Vault-Tec Network Access Terminal Authentication"""
    
    CSS = """
    .auth-container {
        width: 70;
        height: 25;
        margin: 2;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
    }
    
    .auth-form {
        padding: 1 2;
        height: 100%;
    }
    
    .field-label {
        color: #00ff00;
        margin: 1 0 0 0;
    }
    
    .auth-input {
        margin: 0 0 1 0;
        width: 100%;
    }
    
    .button-row {
        height: auto;
        margin: 2 0 0 0;
        align: center middle;
    }
    
    .system-message {
        color: #1e3a8a;
        text-style: italic;
        text-align: center;
        margin: 1 0;
    }
    
    .status-message {
        height: 3;
        margin: 1 0;
        text-align: center;
    }
    """
    
    BINDINGS = [
        Binding("enter", "authenticate", "Authenticate", show=True),
        Binding("escape", "cancel", "Cancel", show=True),
        Binding("tab", "focus_next", "Next Field", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.server_name = "dev"  # Default server
        self.hostname = "localhost:9001"
        self.status_message = ""

    def compose(self) -> ComposeResult:
        """Build the authentication interface"""
        yield Header(show_clock=True)
        
        with Container(classes="auth-container") as container:
            container.border_title = "VAULT-TEC NETWORK ACCESS TERMINAL"
            
            with Vertical(classes="auth-form"):
                yield Static(
                    '"Security clearance protocols ensure only authorized personnel access vault facilities."',
                    classes="system-message"
                )
                
                # Server info display
                yield Label(f"Server: {self.server_name} ({self.hostname})", classes="field-label")
                yield Label("Status: ●ONLINE | Last ping: 14:32:07", classes="field-label status-ok")
                
                # Authentication form
                yield Label("Tenant (Vault):", classes="field-label")
                yield Input(
                    placeholder="test-1756112139",
                    id="tenant_input",
                    classes="auth-input"
                )
                
                yield Label("Username:", classes="field-label") 
                yield Input(
                    placeholder="root",
                    value="root",
                    id="username_input",
                    classes="auth-input"
                )
                
                yield Label("Password:", classes="field-label")
                yield Input(
                    placeholder="Security key required",
                    password=True,
                    id="password_input", 
                    classes="auth-input"
                )
                
                # Status display
                with Container(classes="status-message"):
                    yield Static("Ready for authentication", id="status_display")
                
                # Action buttons
                with Horizontal(classes="button-row"):
                    yield Button("▶ REQUEST ACCESS", variant="primary", id="auth_button")
                    yield Button("◉ SERVER SETUP", variant="default", id="setup_button")
                    
        yield Footer()

    def on_mount(self) -> None:
        """Focus the tenant input on startup or auto-authenticate in overseer mode"""
        if config.is_overseer_mode:
            # Auto-authenticate in overseer mode
            self.call_later(self.auto_authenticate)
        else:
            self.query_one("#tenant_input", Input).focus()

    def auto_authenticate(self) -> None:
        """Auto-authenticate in overseer mode"""
        self.update_status("🔓 OVERSEER MODE: Auto-authenticating...", "info")
        
        # Use default values from config
        tenant = config.default_tenant
        username = config.default_username
        
        # Fill in the form visually
        self.query_one("#tenant_input", Input).value = tenant
        self.query_one("#username_input", Input).value = username
        self.query_one("#password_input", Input).value = "overseer-access"
        
        # Authenticate after a brief delay
        self.set_timer(1.0, lambda: self.authenticate_success(tenant, username))

    def action_authenticate(self) -> None:
        """Handle authentication attempt"""
        tenant = self.query_one("#tenant_input", Input).value.strip()
        username = self.query_one("#username_input", Input).value.strip()
        password = self.query_one("#password_input", Input).value.strip()
        
        if config.is_overseer_mode:
            # In overseer mode, accept any credentials
            tenant = tenant or config.default_tenant
            username = username or config.default_username
            self.update_status("🔓 OVERSEER MODE: Access granted", "success")
            self.authenticate_success(tenant, username)
            return
        
        if not tenant:
            self.update_status("⚠ Vault identifier required", "warning")
            self.query_one("#tenant_input", Input).focus()
            return
            
        if not username:
            self.update_status("⚠ Username required", "warning") 
            self.query_one("#username_input", Input).focus()
            return
            
        if not password:
            self.update_status("⚠ Password required", "warning")
            self.query_one("#password_input", Input).focus()
            return
            
        # Show authentication in progress
        self.update_status("🔄 Validating security clearance...", "info")
        
        # TODO: Actual API authentication
        # For now, simulate successful authentication
        self.authenticate_success(tenant, username)
        
    def authenticate_success(self, vault_id: str, username: str) -> None:
        """Handle successful authentication"""
        user_data = {
            "vault_id": vault_id,
            "username": username,
            "server": self.server_name,
            "hostname": self.hostname
        }
        
        self.update_status("✅ Security clearance confirmed", "success")
        
        # Notify the main app of successful authentication
        self.app.authenticate_user(user_data)
        
    def update_status(self, message: str, status_type: str = "info") -> None:
        """Update the status message display"""
        status_display = self.query_one("#status_display", Static)
        status_display.update(message)
        
        # Apply appropriate styling based on status type
        status_display.remove_class("status-ok", "status-warning", "status-error")
        if status_type == "success":
            status_display.add_class("status-ok")
        elif status_type == "warning":
            status_display.add_class("status-warning")
        elif status_type == "error":
            status_display.add_class("status-error")

    def action_cancel(self) -> None:
        """Cancel authentication and exit"""
        self.app.exit()
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "auth_button":
            self.action_authenticate()
        elif event.button.id == "setup_button":
            self.update_status("Server setup not yet implemented", "info")