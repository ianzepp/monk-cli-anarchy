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
from api.monk_client import monk
from utils.session_timer import SessionTimer


class AuthScreen(Screen):
    """Vault-Tec Network Access Terminal Authentication"""
    
    CSS = """
    .centering-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .auth-container {
        width: 70;
        height: auto;
        max-height: 90%;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        overflow-y: auto;
    }
    
    .auth-form {
        padding: 1 2;
        height: auto;
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
        self.server_name = "Loading..."
        self.hostname = "Unknown"
        self.status_message = ""

    def compose(self) -> ComposeResult:
        """Build the authentication interface"""
        yield Header(show_clock=True)
        
        # Center the auth container on screen
        with Container(classes="centering-container"):
            with Container(classes="auth-container") as container:
                container.border_title = "VAULT-TEC NETWORK ACCESS TERMINAL"
                
                with Vertical(classes="auth-form"):
                    yield Static(
                        '"Security clearance protocols ensure only authorized personnel access vault facilities."',
                        classes="system-message"
                    )
                    
                    # Server info display (will be updated on mount)
                    yield Label(f"Server: {self.server_name} ({self.hostname})", classes="field-label", id="server_info_label")
                    yield Label("Status: Checking...", classes="field-label", id="server_status_label")
                    
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
        """Focus the tenant input on startup or check existing authentication"""
        # Always check existing auth, but never auto-proceed
        self.call_later(self.check_existing_auth)

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
        
    def check_existing_auth(self) -> None:
        """Check if user is already authenticated via monk CLI"""
        self.update_status("Checking existing authentication...", "info")
        
        # First get current server info
        self.update_server_info()
        
        # Check auth status
        status_result = monk.auth_status()
        if status_result.success and isinstance(status_result.data, dict):
            auth_data = status_result.data
            
            if auth_data.get("authenticated", False):
                # Check if token is actually expired
                expired_result = monk.auth_expired()
                if not expired_result.success:  # auth expired returns error when expired
                    # Token is expired
                    self.update_status("⚠ Previous session expired - Re-authentication required", "warning")
                    self.query_one("#tenant_input", Input).focus()
                    return
                
                # Already authenticated and not expired - get user info
                info_result = monk.auth_info()
                if info_result.success and isinstance(info_result.data, dict):
                    user_info = info_result.data
                    tenant = user_info.get("tenant", "unknown")
                    username = user_info.get("name", "unknown")
                    
                    # Get session time remaining
                    expires_result = monk.auth_expires()
                    session_info = ""
                    if expires_result.success:
                        session_info = f" ({SessionTimer.get_session_display(expires_result.data)})"
                    
                    # Fill form with existing auth info
                    self.query_one("#tenant_input", Input).value = tenant
                    self.query_one("#username_input", Input).value = username
                    self.query_one("#password_input", Input).value = "authenticated"
                    
                    self.update_status(f"✅ Authenticated as {username}@{tenant}{session_info} - Press Enter", "success")
                    return
                    
        # Not authenticated, focus on tenant input for manual auth
        self.update_status("Authentication required", "info")
        self.query_one("#tenant_input", Input).focus()
        
    def update_server_info(self) -> None:
        """Update server info display with current monk server"""
        try:
            # Get server list and find current server
            servers_result = monk.server_list()
            if servers_result.success and isinstance(servers_result.data, dict):
                servers = servers_result.data.get("servers", [])
                
                # Check if no servers are configured
                if not servers:
                    self.handle_no_servers()
                    return
                
                # Find the current server (marked with is_current: true)
                current_server_data = None
                for server in servers:
                    if server.get("is_current", False):
                        current_server_data = server
                        break
                
                if current_server_data:
                    self.server_name = current_server_data.get("name", "unknown")
                    self.hostname = current_server_data.get("endpoint", "unknown")
                    status = current_server_data.get("status", "unknown")
                    
                    # Update UI labels
                    server_info_label = self.query_one("#server_info_label", Label)
                    server_info_label.update(f"Server: {self.server_name} ({self.hostname})")
                    
                    server_status_label = self.query_one("#server_status_label", Label)
                    if status == "up":
                        server_status_label.update("Status: ●ONLINE")
                        server_status_label.add_class("status-ok")
                    elif status == "down":
                        server_status_label.update("Status: ◐OFFLINE") 
                        server_status_label.add_class("status-error")
                    else:
                        server_status_label.update("Status: ⚠UNKNOWN")
                        server_status_label.add_class("status-warning")
                    
                    return
                        
            # Fallback if we can't get server info
            self.server_name = "unknown"
            self.hostname = "unknown"
            server_info_label = self.query_one("#server_info_label", Label)
            server_info_label.update("Server: No server configured")
            
        except Exception as e:
            # Graceful fallback
            pass
            
    def handle_no_servers(self) -> None:
        """Handle case when no servers are configured"""
        self.server_name = "none"
        self.hostname = "none"
        
        # Update UI to show no servers
        server_info_label = self.query_one("#server_info_label", Label)
        server_info_label.update("Server: No servers configured")
        
        server_status_label = self.query_one("#server_status_label", Label)
        server_status_label.update("Click SERVER SETUP to add a server")
        server_status_label.add_class("status-warning")
        
        # Update status to guide user
        self.update_status("⚠ No servers configured - Click SERVER SETUP to add one", "warning")

    def action_authenticate(self) -> None:
        """Handle authentication attempt"""
        tenant = self.query_one("#tenant_input", Input).value.strip()
        username = self.query_one("#username_input", Input).value.strip()
        password = self.query_one("#password_input", Input).value.strip()
        
        if config.is_overseer_mode:
            # In overseer mode, accept any credentials but still require Enter
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
        
        # Use real monk auth login
        auth_result = monk.auth_login(tenant, username, password)
        
        if auth_result.success:
            self.update_status("✅ Authentication successful", "success")
            self.authenticate_success(tenant, username)
        else:
            error_msg = auth_result.error or "Authentication failed"
            self.update_status(f"❌ Authentication failed: {error_msg}", "error")
            self.query_one("#password_input", Input).focus()
        
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
            from screens.server_management_screen import ServerManagementScreen
            self.app.push_screen(ServerManagementScreen())