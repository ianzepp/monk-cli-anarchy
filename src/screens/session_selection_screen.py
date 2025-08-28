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
from api.monk_client import monk


class SessionSelectionScreen(Screen):
    """Step 3: Select authentication session"""
    
    CSS = """
    .centering-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .session-container {
        width: 80;
        height: auto;
        max-height: 85%;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        overflow-y: auto;
        padding: 0 2;
    }
    
    .step-indicator {
        color: #ffb000;
        text-style: bold;
        text-align: center;
        margin: 1 0;
    }
    
    .connection-info {
        color: #22c55e;
        text-align: center;
        margin: 1 0;
    }
    
    .auth-section {
        background: #1a1a1a;
        margin: 1 0;
        padding: 1;
        height: 8;
    }
    
    .field-label {
        color: #00ff00;
        margin: 1 0 0 0;
    }
    
    .field-input {
        margin: 0 0 1 0;
        width: 100%;
    }
    
    .action-buttons {
        height: 1;
        margin: 2 0;
        align: center middle;
    }
    
    .status-message {
        height: 1;
        margin: 1 0;
        text-align: center;
        color: #ffb000;
    }
    """
    
    BINDINGS = [
        Binding("escape", "back_to_tenants", "Back", show=True),
        Binding("enter", "authenticate", "Authenticate", show=True),
        Binding("s", "use_existing", "Use Existing", show=True),
    ]

    def __init__(self, server_name: str, tenant_name: str):
        super().__init__()
        self.server_name = server_name
        self.tenant_name = tenant_name
        self.existing_session = None

    def compose(self) -> ComposeResult:
        """Build the session selection interface"""
        with Container(classes="centering-container"):
            with Container(classes="session-container") as container:
                container.border_title = "VAULT ACCESS SESSION SELECTION"
                
                with Vertical():
                    yield Label("STEP 3 of 3: Vault Access Authentication", classes="step-indicator")
                    
                    yield Static(
                        '"Security clearance protocols ensure only authorized personnel access vault facilities."',
                        classes="connection-info"
                    )
                    
                    # Server and tenant info (read-only, already selected)
                    yield Label(f"Server: {self.server_name}", classes="field-label", id="server_info")
                    yield Label(f"Tenant: {self.tenant_name}", classes="field-label", id="tenant_info") 
                    yield Label("", id="session_status", classes="connection-info")
                    
                    # Authentication form (similar to original)
                    yield Label("Username:", classes="field-label")
                    yield Input(
                        value="root",
                        id="username_input",
                        classes="field-input"
                    )
                    
                    yield Label("Password:", classes="field-label")
                    yield Input(
                        password=True,
                        placeholder="Security key required",
                        id="password_input",
                        classes="field-input"
                    )
                    
                    # Status message
                    yield Static("Ready for authentication", id="status_message", classes="status-message")
                    
                    # Action buttons with killbox notation
                    with Horizontal(classes="action-buttons"):
                        yield Button("[ENTER] AUTHENTICATE", variant="primary", id="auth_btn")
                        yield Button("[s] USE EXISTING", variant="default", id="existing_btn")
                        yield Button("[ESC] BACK", variant="default", id="back_btn")

    def on_mount(self) -> None:
        """Check for existing authentication on startup"""
        self.check_existing_session()

    def check_existing_session(self) -> None:
        """Check if user is already authenticated for this tenant"""
        self.update_status("Checking for existing authentication...")
        
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
                            self.update_status("Using existing authenticated session...")
                            self.set_timer(2.0, lambda: self.proceed_to_vault(user_data))
                            return
        
        # No existing session
        session_widget = self.query_one("#session_status", Static) 
        session_widget.update("⚠ No existing session - authentication required")
        self.update_status("Enter username and password to authenticate")
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
            self.update_status("No existing session available")
            self.app.bell()
            
    def action_authenticate(self) -> None:
        """Authenticate with new credentials"""
        username = self.query_one("#username_input", Input).value.strip()
        password = self.query_one("#password_input", Input).value.strip()
        
        if not username:
            self.update_status("Username required")
            self.query_one("#username_input", Input).focus()
            return
            
        if not password:
            self.update_status("Password required")
            self.query_one("#password_input", Input).focus()
            return
            
        # Authenticate via monk CLI
        self.update_status("Authenticating...")
        auth_result = monk.auth_login(self.tenant_name, username, password)
        
        if auth_result.success:
            self.update_status("✅ Authentication successful")
            user_data = {
                "username": username,
                "vault_id": self.tenant_name,
                "server": self.server_name
            }
            self.proceed_to_vault(user_data)
        else:
            error_msg = auth_result.error or "Authentication failed"
            self.update_status(f"❌ Authentication failed: {error_msg}")
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