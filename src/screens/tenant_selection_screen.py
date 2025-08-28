"""
VAULT DATABASE TENANT SELECTION (Step 2)  
Choose tenant database for vault operations
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Label, Static
from typing import Dict, Any

from widgets.vault_container import VaultContainer
from widgets.killbox_table import KillboxTable
from screens.base_screen import BaseVaultScreen
from api.monk_client import monk


class TenantSelectionScreen(BaseVaultScreen):
    """Step 2: Select tenant database"""
    
    CSS = """
    .step-indicator {
        text-style: bold;
        text-align: center;
        margin: 1 0;
    }
    
    .server-info {
        text-align: center;
        margin: 1 0;
    }
    
    .tenant-list {
        margin: 2 0;
        width: 100%;
    }
    """
    
    BINDINGS = BaseVaultScreen.BINDINGS + [
        Binding("escape", "back_to_servers", "Back", show=True),
        Binding("c", "create_tenant", "Create", show=True),
        Binding("1", "select_tenant_1", "Select", show=True),
        Binding("2", "select_tenant_2", "\u200b", show=False),
        Binding("3", "select_tenant_3", "\u200b", show=False),
        Binding("4", "select_tenant_4", "\u200b", show=False),
        Binding("5", "select_tenant_5", "\u200b", show=False),
        Binding("6", "select_tenant_6", "\u200b", show=False),
        Binding("7", "select_tenant_7", "\u200b", show=False),
        Binding("8", "select_tenant_8", "\u200b", show=False),
        Binding("9", "select_tenant_9", "\u200b", show=False),
    ]

    def __init__(self, server_name: str):
        super().__init__()
        self.server_name = server_name
        self.tenants_data = []
        self.selected_tenant = None

    def compose_content(self) -> ComposeResult:
        """Define tenant selection content"""
        with Vertical():
            yield Label("STEP 2 of 3: Choose Tenant Database", classes="step-indicator amber-alert-text")
            yield Label(f"Server: {self.server_name}", classes="server-info healthy-green-text")
            
            # Tenant selection table with killboxes
            table = DataTable(id="tenant_table", classes="tenant-list")
            table.add_columns("", "NAME", "DISPLAY_NAME", "AUTH_STATUS")
            table.show_header = False
            table.cursor_type = "row"
            table.can_focus = True
            yield table
            
    def compose_status(self) -> str:
        """Define default status message"""
        return "Select a tenant database to access"

    def on_mount(self) -> None:
        """Load tenant data on startup"""
        super().on_mount()
        self.load_tenants()
        # Focus the table so arrow keys and Enter work
        self.call_later(self.focus_table)
        
    def focus_table(self) -> None:
        """Focus the tenant table for navigation"""
        try:
            table = self.query_one("#tenant_table", DataTable)
            table.focus()
        except:
            pass

    def load_tenants(self) -> None:
        """Load tenant list from monk CLI"""
        self.status_update("Loading available tenant databases...")
        
        # Use real monk tenant list --json command
        result = monk.tenant_list()
        if result.success and isinstance(result.data, dict):
            tenants = result.data.get("tenants", [])
            self.tenants_data = tenants
            
            if not tenants:
                self.status_update("No tenants configured. Use [c] CREATE TENANT to add one.")
                return
                
            self.populate_tenant_table()
            self.status_update(f"Found {len(tenants)} tenant databases for server '{self.server_name}'. Press [1-{len(tenants)}] to select.")
        else:
            # No demo data - show proper error
            self.tenants_data = []
            self.populate_tenant_table()  # Shows "No tenants available"
            error_msg = result.error if result.error else "monk CLI unavailable"
            self.status_update(f"⚠ Tenant registry not found! {error_msg}. Use [c] CREATE TENANT.")

    def populate_tenant_table(self) -> None:
        """Populate tenant table with killbox notation"""
        table = self.query_one("#tenant_table", DataTable)
        table.clear()
        
        if not self.tenants_data:
            table.add_row("", "No tenants available.", "", "")
            return
            
        for i, tenant in enumerate(self.tenants_data[:9]):  # Max 9 tenants
            name = tenant.get("name", "unknown")
            display_name = tenant.get("display_name", name)
            authenticated = "✅ AUTH" if tenant.get("authenticated", False) else "❌ NO_AUTH"
            current_marker = " *" if tenant.get("is_current", False) else ""
            
            killbox = f"[{i+1}]"
            auth_status = f"{authenticated}{current_marker}"
            
            table.add_row(killbox, name, display_name, auth_status)
        
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle ENTER key or row selection in tenant table"""
        if event.data_table.id == "tenant_table":
            # Get the row that was selected
            row_index = event.cursor_row
            if 0 <= row_index < len(self.tenants_data):
                self.select_tenant_by_index(row_index)


    def action_back_to_servers(self) -> None:
        """Return to server selection"""
        self.app.pop_screen()
        
    def select_tenant_by_index(self, index: int) -> None:
        """Select tenant by index and proceed to session selection"""
        if 0 <= index < len(self.tenants_data):
            tenant_data = self.tenants_data[index]
            tenant_name = tenant_data["name"]
            
            # Switch to selected tenant
            self.status_update(f"Switching to tenant: {tenant_name}")
            switch_result = monk.tenant_use(tenant_name)
            
            if switch_result.success:
                # Proceed to session selection
                from screens.session_selection_screen import SessionSelectionScreen
                self.app.push_screen(SessionSelectionScreen(self.server_name, tenant_name))
            else:
                self.status_update(f"Failed to switch tenant: {switch_result.error}")
        else:
            self.status_update("Invalid tenant selection")

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
            self.status_update(f"Switching to tenant: {tenant_name}")
            switch_result = monk.tenant_use(tenant_name)
            
            if switch_result.success:
                # Proceed to session selection
                from screens.session_selection_screen import SessionSelectionScreen
                self.app.push_screen(SessionSelectionScreen(self.server_name, tenant_name))
            else:
                self.status_update(f"Failed to switch tenant: {switch_result.error}")
        else:
            self.status_update("Invalid tenant selection")

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
        self.status_update("Tenant creation not yet implemented")