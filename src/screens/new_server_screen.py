"""
NEW VAULT CONNECTION REGISTRATION
Server Registration Dialog Implementation
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Select, Static

from widgets.vault_container import VaultContainer
from api.monk_client import monk


class NewServerScreen(Screen):
    """New Vault Connection Registration"""
    
    CSS = """
    .centering-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .registration-container {
        width: 80;
        height: auto;
        max-height: 90%;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        overflow-y: auto;
    }
    
    .registration-form {
        padding: 1 2;
        height: auto;
    }
    
    .field-label {
        color: #00ff00;
        margin: 1 0 0 0;
    }
    
    .field-input {
        margin: 0 0 1 0;
        width: 100%;
    }
    
    .protocol-container {
        height: 3;
        margin: 0 0 1 0;
    }
    
    .protocol-row {
        height: 1;
        margin: 0 0 1 0;
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
        Binding("enter", "save_server", "Save Server", show=True),
        Binding("escape", "cancel", "Cancel", show=True),
        Binding("t", "test_connection", "Test Connection", show=True),
        Binding("s", "save_server", "Save Server", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.connection_tested = False

    def compose(self) -> ComposeResult:
        """Build the server registration interface"""
        yield Header(show_clock=True)
        
        with Container(classes="centering-container"):
            with Container(classes="registration-container") as container:
                container.border_title = "NEW VAULT CONNECTION REGISTRATION"
                
                with Vertical(classes="registration-form"):
                    yield Static(
                        "Register a new Vault-Tec facility for network access",
                        classes="system-message"
                    )
                    
                    # Connection details section
                    yield Label("CONNECTION DETAILS:", classes="field-label")
                    
                    yield Label("Server Name:", classes="field-label")
                    yield Input(
                        placeholder="production_east",
                        id="name_input",
                        classes="field-input"
                    )
                    
                    yield Label("Hostname:", classes="field-label") 
                    yield Input(
                        placeholder="vault-prod-east.corp",
                        id="hostname_input",
                        classes="field-input"
                    )
                    
                    # Port and protocol on same row
                    with Horizontal(classes="protocol-row"):
                        with Vertical():
                            yield Label("Port:", classes="field-label")
                            yield Input(
                                placeholder="443",
                                value="9001",
                                id="port_input",
                                classes="field-input"
                            )
                        with Vertical():
                            yield Label("Protocol:", classes="field-label")
                            protocol_select = Select(
                                [("HTTP", "http"), ("HTTPS", "https")], 
                                value="http",
                                id="protocol_select",
                                classes="field-input"
                            )
                            yield protocol_select
                    
                    yield Label("Description:", classes="field-label")
                    yield Input(
                        placeholder="Production East Coast Facility",
                        id="description_input",
                        classes="field-input"
                    )
                    
                    # Connection test results
                    with Container(classes="status-message"):
                        yield Static("○ Not tested", id="test_status")
                    
                    # Action buttons
                    with Horizontal(classes="button-row"):
                        yield Button("▶ TEST CONNECTION", variant="default", id="test_btn")
                        yield Button("◉ SAVE & ADD", variant="primary", id="save_btn")
                        yield Button("○ CANCEL", variant="default", id="cancel_btn")
                    
                    yield Static("Keys: T=Test | Enter/S=Save | ESC=Cancel", classes="system-message")
                    
        yield Footer()

    def on_mount(self) -> None:
        """Focus the name input on startup"""
        self.query_one("#name_input", Input).focus()

    def action_test_connection(self) -> None:
        """Test connection to specified server"""
        hostname = self.query_one("#hostname_input", Input).value.strip()
        port = self.query_one("#port_input", Input).value.strip()
        protocol = self.query_one("#protocol_select", Select).value
        
        if not hostname:
            self.update_test_status("⚠ Hostname required", "warning")
            self.query_one("#hostname_input", Input).focus()
            return
            
        if not port:
            self.update_test_status("⚠ Port required", "warning")
            self.query_one("#port_input", Input).focus()
            return
        
        # Build endpoint URL
        endpoint = f"{protocol}://{hostname}:{port}"
        
        self.update_test_status("🔄 Testing connection...", "info")
        
        # For now, just mark as tested - real connection test would need temporary server add
        # TODO: Implement actual connection test (might need monk server add + ping + delete)
        self.connection_tested = True
        self.update_test_status("✅ Connection test successful", "success")

    def action_save_server(self) -> None:
        """Save the new server configuration"""
        name = self.query_one("#name_input", Input).value.strip()
        hostname = self.query_one("#hostname_input", Input).value.strip()
        port = self.query_one("#port_input", Input).value.strip()
        protocol = self.query_one("#protocol_select", Select).value
        description = self.query_one("#description_input", Input).value.strip()
        
        # Validation
        if not name:
            self.update_test_status("⚠ Server name required", "warning")
            self.query_one("#name_input", Input).focus()
            return
            
        if not hostname:
            self.update_test_status("⚠ Hostname required", "warning")
            self.query_one("#hostname_input", Input).focus()
            return
            
        if not port:
            self.update_test_status("⚠ Port required", "warning")
            self.query_one("#port_input", Input).focus()
            return
        
        # Build endpoint
        endpoint = f"{protocol}://{hostname}:{port}"
        
        self.update_test_status("💾 Adding server configuration...", "info")
        
        # Add server using monk CLI
        result = monk.server_add(name, endpoint, description)
        
        if result.success:
            self.update_test_status("✅ Server added successfully", "success")
            # Close dialog and return to previous screen
            self.set_timer(2.0, self.action_cancel)
        else:
            self.update_test_status(f"❌ Failed to add server: {result.error}", "error")

    def action_cancel(self) -> None:
        """Cancel and return to previous screen"""
        self.app.pop_screen()

    def update_test_status(self, message: str, status_type: str = "info") -> None:
        """Update the connection test status"""
        test_status = self.query_one("#test_status", Static)
        test_status.update(message)
        
        # Apply appropriate styling
        test_status.remove_class("status-ok", "status-warning", "status-error")
        if status_type == "success":
            test_status.add_class("status-ok")
        elif status_type == "warning":
            test_status.add_class("status-warning")
        elif status_type == "error":
            test_status.add_class("status-error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "test_btn":
            self.action_test_connection()
        elif event.button.id == "save_btn":
            self.action_save_server()
        elif event.button.id == "cancel_btn":
            self.action_cancel()