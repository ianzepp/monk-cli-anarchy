"""
DEPARTMENT REGISTRY MODULE
Multi-Tenant Vault Management Interface
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Label, Static, Input

from widgets.vault_container import VaultContainer
from api.monk_client import monk


class DepartmentRegistryScreen(Screen):
    """Department Registry - Multi-Tenant Vault Management"""
    
    CSS = """
    .registry-header {
        dock: top;
        height: 4;
        background: #1a1a1a;
        color: #00ff00;
    }
    
    .vault-info {
        text-align: left;
        color: #00ff00;
        text-style: bold;
        margin: 1 0 0 2;
    }
    
    .registry-motto {
        text-align: center;
        color: #1e3a8a;
        text-style: italic;
        margin: 1 0;
    }
    
    .stats-bar {
        height: 3;
        margin: 1 2;
        background: #1a1a1a;
        color: #ffb000;
    }
    
    .management-section {
        height: 18;
        margin: 1 2;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        padding: 0 2;
    }
    
    .section-tabs {
        height: 3;
        margin: 0 2;
    }
    
    .tab-button {
        margin: 1 1 0 0;
    }
    
    .table-container {
        height: 12;
        margin: 1 0;
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
        Binding("escape", "back_to_overseer", "Back", show=True),
        Binding("f", "find_items", "Find", show=True),      # Standard: Find/refresh data
        Binding("c", "create_item", "Create", show=True),   # Standard: Create new
        Binding("d", "delete_item", "Delete", show=True),   # Standard: Delete selected
        Binding("u", "use_selected", "Use", show=True),     # Standard: Update/Use selected
        Binding("s", "toggle_servers", "Servers", show=True),
        Binding("t", "toggle_tenants", "Tenants", show=True), 
        Binding("r", "refresh", "Refresh", show=True),
        Binding("p", "ping_item", "Ping", show=True),
        Binding("enter", "use_selected", "Use Selected", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.current_view = "servers"  # "servers" or "tenants"
        self.selected_item = None
        self.servers_data = []
        self.tenants_data = []

    def compose(self) -> ComposeResult:
        """Build the department registry interface"""
        # Header with vault info
        with Container(classes="registry-header"):
            yield Label(f"Current Vault: {self.app.current_vault}", classes="vault-info")
            yield Label('"Managing vault network connections and tenant databases"', classes="registry-motto")
        
        # Statistics bar
        with Container(classes="stats-bar"):
            yield Label("Connected Vaults: Loading... | Active Tenants: Loading...", id="network_stats")
            
        # Tab buttons
        with Horizontal(classes="section-tabs"):
            yield Button("● SERVERS", variant="primary" if self.current_view == "servers" else "default", 
                        id="servers_tab", classes="tab-button")
            yield Button("◉ TENANTS", variant="primary" if self.current_view == "tenants" else "default", 
                        id="tenants_tab", classes="tab-button")
            
        # Management section with table
        with Container(classes="management-section") as container:
            container.border_title = "VAULT NETWORK ADMINISTRATION"
            
            with Container(classes="table-container"):
                # Server/Tenant table
                table = DataTable(id="management_table")
                yield table
                
        # Status message
        yield Static("Ready for network operations", id="status_message", classes="status-message")

        # Action buttons
        with Container(classes="action-bar"):
            with Horizontal(classes="action-buttons"):
                yield Button("[f] FIND", variant="default", id="find_btn")
                yield Button("[c] CREATE", variant="primary", id="create_btn")
                yield Button("[d] DELETE", variant="default", id="delete_btn")
                yield Button("[u] USE", variant="default", id="use_btn")
                yield Button("[p] PING", variant="default", id="ping_btn")
                
        yield Footer()

    def on_mount(self) -> None:
        """Load initial data"""
        self.setup_table()
        self.load_servers()

    def setup_table(self) -> None:
        """Setup table columns based on current view"""
        table = self.query_one("#management_table", DataTable)
        table.clear(columns=True)
        
        if self.current_view == "servers":
            table.add_columns("NAME", "URL", "STATUS", "DESCRIPTION")
            table.border_title = "SERVER REGISTRY"
        else:  # tenants
            table.add_columns("NAME", "STATUS", "RECORDS", "LAST_ACCESSED")
            table.border_title = "TENANT DATABASE REGISTRY"

    def load_servers(self) -> None:
        """Load server list from monk CLI"""
        self.update_status("Loading server registry...")
        
        result = monk.server_list()
        
        if result.success:
            try:
                # Parse JSON response from monk server list --json
                if isinstance(result.data, dict) and "servers" in result.data:
                    # Extract servers array from JSON response
                    raw_servers = result.data["servers"]
                    
                    # Convert to UI format with proper status mapping
                    self.servers_data = []
                    for server in raw_servers:
                        # Map monk status to UI status indicators
                        status = server.get("status", "unknown")
                        if status == "up":
                            ui_status = "●ONLINE"
                        elif status == "down":
                            ui_status = "◐OFFLINE"
                        else:
                            ui_status = "⚠UNKNOWN"
                        
                        # Mark current server
                        if server.get("is_current", False):
                            ui_status += " *"
                        
                        self.servers_data.append({
                            "name": server.get("name", "unknown"),
                            "url": server.get("endpoint", "unknown"),
                            "status": ui_status,
                            "description": server.get("description", ""),
                            "raw": server  # Keep original data for operations
                        })
                else:
                    self.servers_data = []
                
                self.populate_servers_table()
                
                # Get current server
                current_result = monk.server_current()
                current_server = current_result.data if current_result.success else "None"
                
                self.update_status(f"Loaded {len(self.servers_data)} servers. Current: {current_server}")
                self.update_stats()
                
            except Exception as e:
                self.update_status(f"Error parsing server data: {str(e)}")
                self.servers_data = []
        else:
            self.update_status(f"Failed to load servers: {result.error}")
            # Create some mock data for demonstration
            self.servers_data = [
                {"name": "local", "url": "http://localhost:9001", "status": "●ONLINE", "description": "Development server"},
                {"name": "staging", "url": "https://staging.example.com", "status": "⚠TIMEOUT", "description": "Staging environment"},
                {"name": "prod", "url": "https://api.example.com", "status": "◐OFFLINE", "description": "Production server"},
            ]
            self.populate_servers_table()
            self.update_status("Using demo data - monk CLI not available")

    def populate_servers_table(self) -> None:
        """Populate table with server data"""
        table = self.query_one("#management_table", DataTable)
        table.clear()
        
        for server in self.servers_data:
            # Handle both monk CLI output format and demo format
            name = server.get("name", "unknown")
            url = server.get("url", server.get("endpoint", "unknown"))
            status = server.get("status", "◐UNKNOWN")
            description = server.get("description", server.get("desc", ""))
            
            table.add_row(name, url, status, description)

    def load_tenants(self) -> None:
        """Load tenant list from monk CLI"""
        self.update_status("Loading tenant databases...")
        
        # For now, use demo data since monk tenant list --json doesn't exist yet
        # TODO: Replace with real monk tenant list --json when implemented
        self.tenants_data = [
            {"name": "test-1756112139", "status": "●ACTIVE", "records": "2,847", "last_accessed": "2025-08-28"},
            {"name": "production", "status": "●ACTIVE", "records": "156,332", "last_accessed": "2025-08-28"},
            {"name": "development", "status": "⚠MAINTENANCE", "records": "45", "last_accessed": "2025-08-27"},
            {"name": "staging", "status": "●ACTIVE", "records": "12,456", "last_accessed": "2025-08-27"},
        ]
        self.populate_tenants_table()
        self.update_status(f"Loaded {len(self.tenants_data)} tenant databases (demo data)")
        self.update_stats()

    def populate_tenants_table(self) -> None:
        """Populate table with tenant data"""
        table = self.query_one("#management_table", DataTable)
        table.clear()
        
        for tenant in self.tenants_data:
            name = tenant.get("name", "unknown")
            status = tenant.get("status", "◐UNKNOWN")
            records = tenant.get("records", tenant.get("record_count", "0"))
            last_accessed = tenant.get("last_accessed", tenant.get("last_access", "Unknown"))
            
            table.add_row(name, status, records, last_accessed)

    def update_stats(self) -> None:
        """Update statistics bar"""
        server_count = len(self.servers_data)
        online_servers = len([s for s in self.servers_data if "ONLINE" in str(s.get("status", ""))])
        tenant_count = len(self.tenants_data) 
        active_tenants = len([t for t in self.tenants_data if "ACTIVE" in str(t.get("status", ""))])
        
        stats_text = f"Connected Vaults: {online_servers}/{server_count} | Active Tenants: {active_tenants}/{tenant_count}"
        self.query_one("#network_stats", Label).update(stats_text)

    def update_status(self, message: str) -> None:
        """Update status message"""
        self.query_one("#status_message", Static).update(message)

    def action_back_to_overseer(self) -> None:
        """Return to the overseer console"""
        self.app.pop_screen()
        
    def action_toggle_servers(self) -> None:
        """Switch to servers view"""
        if self.current_view != "servers":
            self.current_view = "servers"
            self.setup_table()
            self.load_servers()
            self.update_tab_buttons()
        
    def action_toggle_tenants(self) -> None:
        """Switch to tenants view"""
        if self.current_view != "tenants":
            self.current_view = "tenants"
            self.setup_table()
            self.load_tenants()
            self.update_tab_buttons()
            
    def update_tab_buttons(self) -> None:
        """Update tab button styling"""
        servers_btn = self.query_one("#servers_tab", Button)
        tenants_btn = self.query_one("#tenants_tab", Button)
        
        if self.current_view == "servers":
            servers_btn.variant = "primary"
            tenants_btn.variant = "default"
        else:
            servers_btn.variant = "default"
            tenants_btn.variant = "primary"

    def action_refresh(self) -> None:
        """Refresh current view"""
        if self.current_view == "servers":
            self.load_servers()
        else:
            self.load_tenants()

    def action_find_items(self) -> None:
        """Find/refresh current items"""
        self.action_refresh()
        
    def action_create_item(self) -> None:
        """Create new server or tenant"""
        if self.current_view == "servers":
            from screens.new_server_screen import NewServerScreen
            self.app.push_screen(NewServerScreen())
        else:
            self.app.bell()
            self.update_status("Tenant creation not yet implemented")
            
    def action_add_item(self) -> None:
        """Legacy method - redirect to create"""
        self.action_create_item()

    def action_delete_item(self) -> None:
        """Delete selected item"""
        table = self.query_one("#management_table", DataTable)
        if table.cursor_row >= 0:
            self.app.bell()
            self.update_status("Deletion not yet implemented")

    def action_ping_item(self) -> None:
        """Ping selected server"""
        if self.current_view == "servers":
            table = self.query_one("#management_table", DataTable)
            if table.cursor_row >= 0:
                row_data = table.get_row_at(table.cursor_row)
                server_name = str(row_data[0])
                self.update_status(f"Pinging {server_name}...")
                
                result = monk.server_ping(server_name)
                if result.success:
                    self.update_status(f"Ping successful: {server_name}")
                else:
                    self.update_status(f"Ping failed: {result.error}")
        else:
            self.update_status("Ping not available for tenants")

    def action_use_selected(self) -> None:
        """Use/switch to selected item"""
        table = self.query_one("#management_table", DataTable)
        if table.cursor_row >= 0:
            row_data = table.get_row_at(table.cursor_row)
            item_name = str(row_data[0])
            
            if self.current_view == "servers":
                self.update_status(f"Switching to server: {item_name}")
                result = monk.server_use(item_name)
                if result.success:
                    self.update_status(f"Now using server: {item_name}")
                else:
                    self.update_status(f"Failed to switch server: {result.error}")
            else:
                self.update_status(f"Switching to tenant: {item_name}")
                result = monk.tenant_use(item_name)
                if result.success:
                    self.update_status(f"Now using tenant: {item_name}")
                else:
                    self.update_status(f"Failed to switch tenant: {result.error}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "servers_tab":
            self.action_toggle_servers()
        elif event.button.id == "tenants_tab":
            self.action_toggle_tenants()
        elif event.button.id == "find_btn":
            self.action_find_items()
        elif event.button.id == "create_btn":
            self.action_create_item()
        elif event.button.id == "delete_btn":
            self.action_delete_item()
        elif event.button.id == "use_btn":
            self.action_use_selected()
        elif event.button.id == "ping_btn":
            self.action_ping_item()