"""
VAULT DATABASE TENANT SELECTION (Step 2)  
Choose tenant database for vault operations
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Label, Static

from widgets.vault_container import VaultContainer
from api.monk_client import monk


class TenantSelectionScreen(Screen):
    """Step 2: Select tenant database"""
    
    CSS = """
    .centering-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .tenant-container {
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
    
    .server-info {
        color: #22c55e;
        text-align: center;
        margin: 1 0;
    }
    
    .tenant-table {
        height: 12;
        margin: 1 0;
    }
    
    .tenant-table:focus-within {
        border: solid #ffb000;
        border-title-color: #ff3030;
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
        Binding("escape", "back_to_servers", "Back", show=True),
        Binding("c", "create_tenant", "Create Tenant", show=True),
        Binding("1", "select_tenant_1", "[1]", show=True),
        Binding("2", "select_tenant_2", "[2]", show=True),
        Binding("3", "select_tenant_3", "[3]", show=True),
        Binding("4", "select_tenant_4", "[4]", show=True),
        Binding("5", "select_tenant_5", "[5]", show=True),
        Binding("6", "select_tenant_6", "[6]", show=True),
        Binding("7", "select_tenant_7", "[7]", show=True),
        Binding("8", "select_tenant_8", "[8]", show=True),
        Binding("9", "select_tenant_9", "[9]", show=True),
    ]

    def __init__(self, server_name: str):
        super().__init__()
        self.server_name = server_name
        self.tenants_data = []
        self.selected_tenant = None

    def compose(self) -> ComposeResult:
        """Build the tenant selection interface"""
        with Container(classes="centering-container"):
            with Container(classes="tenant-container") as container:
                container.border_title = "VAULT DATABASE TENANT SELECTION"
                
                with Vertical():
                    yield Label("STEP 2 of 3: Choose Tenant Database", classes="step-indicator")
                    yield Label(f"Server: {self.server_name}", classes="server-info")
                    
                    # Tenant selection list with killboxes
                    with Container(classes="tenant-table"):
                        yield Static("", id="tenant_list")
                    
                    # Status message
                    yield Static("Select a tenant database to access", id="status_message", classes="status-message")
                    
                    # Action buttons with killbox notation
                    with Horizontal(classes="action-buttons"):
                        yield Button("[ENTER] SELECT TENANT", variant="primary", id="select_btn")
                        yield Button("[c] CREATE TENANT", variant="default", id="create_btn")
                        yield Button("[ESC] BACK TO SERVERS", variant="default", id="back_btn")

    def on_mount(self) -> None:
        """Load tenant data on startup"""
        self.load_tenants()

    def load_tenants(self) -> None:
        """Load tenant list from monk CLI"""
        self.update_status("Loading available tenant databases...")
        
        # Use real monk tenant list --json command
        result = monk.tenant_list()
        if result.success and isinstance(result.data, dict):
            tenants = result.data.get("tenants", [])
            self.tenants_data = tenants
            
            if not tenants:
                self.update_status("No tenants configured. Use [c] CREATE TENANT to add one.")
                return
                
            self.populate_tenant_table()
            self.update_status(f"Found {len(tenants)} tenant databases. Press [1-9] to select.")
        else:
            # No demo data - show proper error
            self.tenants_data = []
            self.populate_tenant_table()  # Shows "No tenants available"
            error_msg = result.error if result.error else "monk CLI unavailable"
            self.update_status(f"⚠ Tenant registry not found! {error_msg}. Use [c] CREATE TENANT to configure databases.")

    def populate_tenant_table(self) -> None:
        """Populate tenant list with killbox notation"""
        tenant_list = self.query_one("#tenant_list", Static)
        
        if not self.tenants_data:
            tenant_list.update("No tenants available.")
            return
            
        lines = []
        for i, tenant in enumerate(self.tenants_data[:9]):  # Max 9 tenants
            name = tenant.get("name", "unknown")
            display_name = tenant.get("display_name", name)
            authenticated = "✅ AUTH" if tenant.get("authenticated", False) else "❌ NO_AUTH"
            current_marker = " *" if tenant.get("is_current", False) else ""
            
            killbox = f"[{i+1}]"
            line = f"{killbox} {name:15} {display_name:25} {authenticated:10}{current_marker}"
            lines.append(line)
            
        tenant_list.update("\n".join(lines))

    def update_status(self, message: str) -> None:
        """Update status message"""
        self.query_one("#status_message", Static).update(message)

    def action_back_to_servers(self) -> None:
        """Return to server selection"""
        self.app.pop_screen()
        
    def select_tenant_by_index(self, index: int) -> None:
        """Select tenant by index and proceed to session selection"""
        if 0 <= index < len(self.tenants_data):
            tenant_data = self.tenants_data[index]
            tenant_name = tenant_data["name"]
            
            # Switch to selected tenant
            self.update_status(f"Switching to tenant: {tenant_name}")
            switch_result = monk.tenant_use(tenant_name)
            
            if switch_result.success:
                # Proceed to session selection
                from screens.session_selection_screen import SessionSelectionScreen
                self.app.push_screen(SessionSelectionScreen(self.server_name, tenant_name))
            else:
                self.update_status(f"Failed to switch tenant: {switch_result.error}")
        else:
            self.update_status("Invalid tenant selection")

    # Individual tenant selection methods
    def action_select_tenant_1(self) -> None: self.select_tenant_by_index(0)
    def action_select_tenant_2(self) -> None: self.select_tenant_by_index(1)
    def action_select_tenant_3(self) -> None: self.select_tenant_by_index(2)
    def action_select_tenant_4(self) -> None: self.select_tenant_by_index(3)
    def action_select_tenant_5(self) -> None: self.select_tenant_by_index(4)
    def action_select_tenant_6(self) -> None: self.select_tenant_by_index(5)
    def action_select_tenant_7(self) -> None: self.select_tenant_by_index(6)
    def action_select_tenant_8(self) -> None: self.select_tenant_by_index(7)
    def action_select_tenant_9(self) -> None: self.select_tenant_by_index(8)

    def select_tenant_by_index(self, index: int) -> None:
        """Select tenant by index and proceed to session selection"""
        if 0 <= index < len(self.tenants_data):
            tenant_data = self.tenants_data[index]
            tenant_name = tenant_data["name"]
            
            # Switch to selected tenant
            self.update_status(f"Switching to tenant: {tenant_name}")
            switch_result = monk.tenant_use(tenant_name)
            
            if switch_result.success:
                # Proceed to session selection
                from screens.session_selection_screen import SessionSelectionScreen
                self.app.push_screen(SessionSelectionScreen(self.server_name, tenant_name))
            else:
                self.update_status(f"Failed to switch tenant: {switch_result.error}")
        else:
            self.update_status("Invalid tenant selection")

    # Individual tenant selection methods  
    def action_select_tenant_1(self) -> None: self.select_tenant_by_index(0)
    def action_select_tenant_2(self) -> None: self.select_tenant_by_index(1)
    def action_select_tenant_3(self) -> None: self.select_tenant_by_index(2)
    def action_select_tenant_4(self) -> None: self.select_tenant_by_index(3)
    def action_select_tenant_5(self) -> None: self.select_tenant_by_index(4)
    def action_select_tenant_6(self) -> None: self.select_tenant_by_index(5)
    def action_select_tenant_7(self) -> None: self.select_tenant_by_index(6)
    def action_select_tenant_8(self) -> None: self.select_tenant_by_index(7)
    def action_select_tenant_9(self) -> None: self.select_tenant_by_index(8)

    def action_create_tenant(self) -> None:
        """Create new tenant"""
        self.app.bell()
        # TODO: Implement tenant creation dialog
        self.update_status("Tenant creation not yet implemented")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "select_btn":
            self.action_select_tenant()
        elif event.button.id == "create_btn":
            self.action_create_tenant()
        elif event.button.id == "back_btn":
            self.action_back_to_servers()
        elif event.button.id == "quit_btn":
            self.app.exit()