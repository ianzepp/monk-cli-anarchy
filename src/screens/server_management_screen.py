"""
VAULT CONNECTION MANAGEMENT
Server Management Interface Implementation
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Label, Static

from widgets.vault_container import VaultContainer
from api.monk_client import monk


class ServerManagementScreen(Screen):
    """Vault Connection Management"""
    
    CSS = """
    .management-header {
        dock: top;
        height: 4;
        background: #1a1a1a;
        color: #00ff00;
    }
    
    .header-title {
        text-align: center;
        color: #00ff00;
        text-style: bold;
        margin: 1 0;
    }
    
    .header-subtitle {
        text-align: center;
        color: #1e3a8a;
        text-style: italic;
        margin: 0 0 1 0;
    }
    
    .servers-section {
        height: 18;
        margin: 1 2;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        padding: 0 2;
    }
    
    .server-details {
        height: 6;
        margin: 1 2;
        background: #1a1a1a;
        color: #ffb000;
        padding: 1;
    }
    
    .action-bar {
        dock: bottom;
        height: 3;
        background: #1a1a1a;
        margin: 0 2;
    }
    
    .action-buttons {
        height: 1;
        margin: 1 0;
        align: center middle;
    }
    
    .status-message {
        height: 1;
        margin: 0 2;
        text-align: center;
        color: #ffb000;
    }
    """
    
    BINDINGS = [
        Binding("escape", "back_to_auth", "Back to Auth", show=True),
        Binding("a", "add_server", "Add Server", show=True),
        Binding("e", "edit_server", "Edit", show=True),
        Binding("d", "delete_server", "Delete", show=True),
        Binding("t", "test_connection", "Test", show=True),
        Binding("u", "use_server", "Use Server", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("enter", "use_server", "Use Server", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.selected_server = None
        self.servers_data = []

    def compose(self) -> ComposeResult:
        """Build the server management interface"""
        # Header
        with Container(classes="management-header"):
            yield Label("VAULT CONNECTION MANAGEMENT", classes="header-title")
            yield Label("Manage saved vault facility connections", classes="header-subtitle")
        
        # Server table
        with Container(classes="servers-section") as container:
            container.border_title = "CONFIGURED SERVERS"
            
            table = DataTable(id="servers_table")
            table.add_columns("NAME", "ADDRESS", "STATUS", "AUTHENTICATED", "ACTIONS")
            yield table
            
        # Selected server details
        with Container(classes="server-details"):
            yield Label("SELECTED SERVER DETAILS:", id="details_title")
            yield Label("No server selected", id="server_name_detail")
            yield Label("", id="server_description_detail")
            yield Label("", id="server_added_detail")
            yield Label("", id="server_auth_detail")

        # Status message
        yield Static("Ready for server management operations", id="status_message", classes="status-message")

        # Action buttons
        with Container(classes="action-bar"):
            with Horizontal(classes="action-buttons"):
                yield Button("▶ ADD SERVER", variant="primary", id="add_btn")
                yield Button("◉ AUTHENTICATE", variant="default", id="auth_btn")
                yield Button("○ REMOVE", variant="default", id="remove_btn")
                yield Button("⚠ TEST CONNECTION", variant="default", id="test_btn")
                
        yield Footer()

    def on_mount(self) -> None:
        """Load server data on screen mount"""
        self.load_servers()

    def load_servers(self) -> None:
        """Load server list from monk CLI"""
        self.update_status("Loading server configurations...")
        
        result = monk.server_list()
        if result.success and isinstance(result.data, dict):
            servers = result.data.get("servers", [])
            self.servers_data = servers
            self.populate_servers_table()
            self.update_status(f"Loaded {len(servers)} server configurations")
        else:
            self.update_status(f"Failed to load servers: {result.error}")
            self.servers_data = []

    def populate_servers_table(self) -> None:
        """Populate table with server data"""
        table = self.query_one("#servers_table", DataTable)
        table.clear()
        
        for server in self.servers_data:
            name = server.get("name", "unknown")
            endpoint = server.get("endpoint", "unknown")
            
            # Status mapping
            status = server.get("status", "unknown")
            if status == "up":
                ui_status = "●UP"
            elif status == "down":
                ui_status = "◐DOWN"
            else:
                ui_status = "⚠UNKNOWN"
            
            # Mark current server
            if server.get("is_current", False):
                ui_status += " *"
            
            # Authentication status
            auth_sessions = server.get("auth_sessions", 0)
            if auth_sessions > 0:
                auth_status = f"✅ VALID ({auth_sessions})"
            else:
                auth_status = "❌ NONE"
            
            # Actions
            actions = "[E][T][X]"  # Edit, Test, Remove
            
            table.add_row(name, endpoint, ui_status, auth_status, actions)

    def update_server_details(self, server_data: dict) -> None:
        """Update the server details panel"""
        name = server_data.get("name", "Unknown")
        description = server_data.get("description", "No description")
        added_at = server_data.get("added_at", "Unknown")
        last_ping = server_data.get("last_ping", "Never")
        auth_sessions = server_data.get("auth_sessions", 0)
        
        self.query_one("#details_title", Label).update(f"SELECTED SERVER DETAILS: {name}")
        self.query_one("#server_name_detail", Label).update(f"Description: {description}")
        self.query_one("#server_description_detail", Label).update(f"Added: {added_at}")
        self.query_one("#server_added_detail", Label).update(f"Last Ping: {last_ping}")
        self.query_one("#server_auth_detail", Label).update(f"Auth Sessions: {auth_sessions}")

    def update_status(self, message: str) -> None:
        """Update status message"""
        self.query_one("#status_message", Static).update(message)

    def action_back_to_auth(self) -> None:
        """Return to authentication screen"""
        self.app.pop_screen()
        
    def action_add_server(self) -> None:
        """Add new server"""
        from screens.new_server_screen import NewServerScreen
        self.app.push_screen(NewServerScreen())
        
    def action_edit_server(self) -> None:
        """Edit selected server"""
        table = self.query_one("#servers_table", DataTable)
        if table.cursor_row >= 0:
            server_data = self.servers_data[table.cursor_row]
            self.update_status(f"Edit server '{server_data['name']}' not yet implemented")
        else:
            self.update_status("No server selected")

    def action_delete_server(self) -> None:
        """Delete selected server"""
        table = self.query_one("#servers_table", DataTable)
        if table.cursor_row >= 0:
            server_data = self.servers_data[table.cursor_row]
            server_name = server_data["name"]
            
            self.update_status(f"Deleting server '{server_name}'...")
            result = monk.server_delete(server_name)
            
            if result.success:
                self.update_status(f"Server '{server_name}' deleted successfully")
                self.load_servers()  # Refresh list
            else:
                self.update_status(f"Failed to delete server: {result.error}")
        else:
            self.update_status("No server selected")

    def action_test_connection(self) -> None:
        """Test connection to selected server"""
        table = self.query_one("#servers_table", DataTable)
        if table.cursor_row >= 0:
            server_data = self.servers_data[table.cursor_row]
            server_name = server_data["name"]
            
            self.update_status(f"Testing connection to '{server_name}'...")
            result = monk.server_ping(server_name)
            
            if result.success:
                self.update_status(f"Connection test successful: {server_name}")
                self.load_servers()  # Refresh to update status
            else:
                self.update_status(f"Connection test failed: {result.error}")
        else:
            self.update_status("No server selected")

    def action_use_server(self) -> None:
        """Switch to selected server"""
        table = self.query_one("#servers_table", DataTable)
        if table.cursor_row >= 0:
            server_data = self.servers_data[table.cursor_row]
            server_name = server_data["name"]
            
            self.update_status(f"Switching to server '{server_name}'...")
            result = monk.server_use(server_name)
            
            if result.success:
                self.update_status(f"Now using server: {server_name}")
                self.load_servers()  # Refresh to update current indicators
            else:
                self.update_status(f"Failed to switch server: {result.error}")
        else:
            self.update_status("No server selected")

    def action_refresh(self) -> None:
        """Refresh server list"""
        self.load_servers()

    def on_data_table_row_selected(self, event) -> None:
        """Handle server selection in table"""
        table = self.query_one("#servers_table", DataTable)
        if table.cursor_row >= 0 and table.cursor_row < len(self.servers_data):
            server_data = self.servers_data[table.cursor_row]
            self.selected_server = server_data["name"]
            self.update_server_details(server_data)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "add_btn":
            self.action_add_server()
        elif event.button.id == "auth_btn":
            # Return to auth screen for authentication
            self.app.pop_screen()
        elif event.button.id == "remove_btn":
            self.action_delete_server()
        elif event.button.id == "test_btn":
            self.action_test_connection()