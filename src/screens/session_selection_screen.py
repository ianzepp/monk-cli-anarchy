"""
VAULT ACCESS SESSION SELECTION (Step 3)
Choose authentication session or create new login
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Input, Label, Static

from widgets.vault_container import VaultContainer
from screens.base_screen import BaseVaultScreen
from api.monk_client import monk


class SessionSelectionScreen(BaseVaultScreen):
    """Step 3: Select authentication session"""
    
    CSS = """
    .step-indicator {
        text-style: bold;
        text-align: center;
        margin: 1 0;
    }
    
    .connection-info {
        text-align: center;
        margin: 1 0;
    }
    
    .auth-section {
        margin: 2 0;
        padding: 1;
    }
    
    .field-label {
        margin: 1 0 0 0;
    }
    
    .field-input {
        margin: 0 0 1 0;
        width: 100%;
    }
    """
    
    BINDINGS = BaseVaultScreen.BINDINGS + [
        Binding("escape", "back_to_tenants", "Back", show=True),
        Binding("enter", "authenticate", "Authenticate", show=True),
        Binding("s", "use_existing", "Use Existing", show=True),
    ]

    def __init__(self, server_name: str, tenant_name: str):
        super().__init__()
        self.server_name = server_name
        self.tenant_name = tenant_name
        self.existing_session = None

    def compose_content(self) -> ComposeResult:
        """Define session selection content"""
        with Vertical():
            yield Label("STEP 3 of 3: Vault Access Authentication", classes="step-indicator amber-alert-text")
            
            yield Static(
                '"Security clearance protocols ensure only authorized personnel access vault facilities."',
                classes="connection-info steel-blue-text"
            )
            
            yield Label(f"Server: {self.server_name} • Tenant: {self.tenant_name}", classes="connection-info healthy-green-text")
            yield Static("", id="session_status", classes="connection-info")
            
            # Authentication form
            with Container(classes="auth-section"):
                yield Label("Username:", classes="field-label vault-green-text")
                yield Input(
                    value="root",
                    id="username_input",
                    classes="field-input"
                )
                
                yield Label("Password:", classes="field-label vault-green-text")
                yield Input(
                    password=True,
                    placeholder="Security key required",
                    id="password_input",
                    classes="field-input"
                )
                
    def compose_status(self) -> str:
        """Define default status message"""
        return "Ready for authentication"

    def on_mount(self) -> None:
        """Check for existing authentication on startup"""
        super().on_mount()
        self.check_existing_session()

    def check_existing_session(self) -> None:
        """Check if user is already authenticated for this tenant"""
        self.status_update("Checking for existing authentication...")
        
        # Check auth status
        status_result = monk.auth_status()
        if status_result.success and isinstance(status_result.data, dict):
            auth_data = status_result.data
            
            if auth_data.get("authenticated", False):
                # Check if token is expired
                expired_result = monk.auth_expired()
                if expired_result.success:  # Not expired
                    # Get auth info
                    info_result = monk.auth_info()
                    if info_result.success and isinstance(info_result.data, dict):
                        user_info = info_result.data
                        current_tenant = user_info.get("tenant", "")
                        username = user_info.get("name", "unknown")
                        
                        if current_tenant == self.tenant_name:
                            # Already authenticated to this tenant - auto-proceed
                            self.existing_session = user_info
                            session_widget = self.query_one("#session_status", Static)
                            session_widget.update(f"✅ Current session: {username}@{current_tenant}")
                            
                            # Auto-proceed with existing session after brief display
                            user_data = {
                                "username": username,
                                "vault_id": current_tenant,
                                "server": self.server_name
                            }
                            self.status_update("Using existing authenticated session...")
                            self.set_timer(2.0, lambda: self.proceed_to_vault(user_data))
                            return
        
        # No existing session
        session_widget = self.query_one("#session_status", Static) 
        session_widget.update("⚠ No existing session - authentication required")
        self.status_update("Enter username and password to authenticate")
        self.query_one("#username_input", Input).focus()

    def update_status(self, message: str) -> None:
        """Update status message"""
        self.query_one("#status_message", Static).update(message)

    def action_back_to_tenants(self) -> None:
        """Return to tenant selection"""
        self.app.pop_screen()
        
    def action_use_existing(self) -> None:
        """Use existing authentication session"""
        if self.existing_session:
            # Already authenticated - proceed to main app
            user_data = {
                "username": self.existing_session.get("name", "unknown"),
                "vault_id": self.tenant_name,
                "server": self.server_name
            }
            self.proceed_to_vault(user_data)
        else:
            self.status_update("No existing session available")
            self.app.bell()
            
    def action_authenticate(self) -> None:
        """Authenticate with new credentials"""
        username = self.query_one("#username_input", Input).value.strip()
        password = self.query_one("#password_input", Input).value.strip()
        
        if not username:
            self.status_update("Username required")
            self.query_one("#username_input", Input).focus()
            return
            
        if not password:
            self.status_update("Password required")
            self.query_one("#password_input", Input).focus()
            return
            
        # Authenticate via monk CLI
        self.status_update("Authenticating...")
        auth_result = monk.auth_login(self.tenant_name, username, password)
        
        if auth_result.success:
            self.status_update("✅ Authentication successful")
            user_data = {
                "username": username,
                "vault_id": self.tenant_name,
                "server": self.server_name
            }
            self.proceed_to_vault(user_data)
        else:
            error_msg = auth_result.error or "Authentication failed"
            self.status_update(f"❌ Authentication failed: {error_msg}")
            self.query_one("#password_input", Input).focus()

    def proceed_to_vault(self, user_data: dict) -> None:
        """Proceed to main vault application"""
        # Clear all auth screens and go to main app
        while len(self.app.screen_stack) > 1:
            self.app.pop_screen()
            
        # Set app authentication state
        self.app.authenticate_user(user_data)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "auth_btn":
            self.action_authenticate()
        elif event.button.id == "existing_btn":
            self.action_use_existing()
        elif event.button.id == "back_btn":
            self.action_back_to_tenants()