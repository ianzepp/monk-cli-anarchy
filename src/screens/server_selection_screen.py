"""
VAULT FACILITY SERVER SELECTION (Step 1)
Choose server connection for vault operations
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Label, Static

from widgets.vault_container import VaultContainer
from screens.base_screen import BaseVaultScreen
from api.monk_client import monk


class ServerSelectionScreen(BaseVaultScreen):
    """Step 1: Select server connection"""
    
    CSS = """
    .step-indicator {
        text-style: bold;
        text-align: center;
        margin: 1 0;
    }
    
    .server-list {
        margin: 2 0;
        width: 100%;
    }
    """
    
    BINDINGS = BaseVaultScreen.BINDINGS + [
        Binding("escape", "back_to_welcome", "ESC Back", show=True),
        Binding("c", "create_server", "Create", show=True),
        Binding("1", "select_server_1", "1-9 Select", show=True),
        Binding("2", "select_server_2", "\u200b", show=False),
        Binding("3", "select_server_3", "\u200b", show=False),
        Binding("4", "select_server_4", "\u200b", show=False),
        Binding("5", "select_server_5", "\u200b", show=False),
        Binding("6", "select_server_6", "\u200b", show=False),
        Binding("7", "select_server_7", "\u200b", show=False),
        Binding("8", "select_server_8", "\u200b", show=False),
        Binding("9", "select_server_9", "\u200b", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.servers_data = []
        self.selected_server = None

    def compose_content(self) -> ComposeResult:
        """Define server selection content"""
        with Vertical():
            yield Label("STEP 1 of 3: Choose Server Connection", classes="step-indicator amber-alert-text")
            
            # Server selection list with killboxes
            yield Static("", id="server_list", classes="server-list vault-green-text")
                
    def compose_commands(self) -> list[str]:
        """Define local killbox commands"""
        return ["[ESC] Back", "[c] Create"]
        
    def compose_status(self) -> str:
        """Define default status message"""
        return "Select a vault facility server to connect to"

    def on_mount(self) -> None:
        """Load server data on startup"""
        super().on_mount()
        self.load_servers()

    def load_servers(self) -> None:
        """Load server list from monk CLI"""
        self.status_update("Loading vault facility servers...")
        
        result = monk.server_list()
        if result.success and isinstance(result.data, dict):
            servers = result.data.get("servers", [])
            self.servers_data = servers
            
            if not servers:
                self.status_update("No servers configured. Use [c] CREATE SERVER to add one.")
                return
                
            self.populate_server_table()
            self.update_dynamic_bindings()
            self.status_update(f"Found {len(servers)} vault facility servers. Press [1-{len(servers)}] to select.")
        else:
            # No demo data - show proper error
            self.servers_data = []
            self.populate_server_table()  # Shows "No servers configured"
            error_msg = result.error if result.error else "monk CLI unavailable"
            self.status_update(f"⚠ Overseer resource list not found! {error_msg}. Use [c] CREATE SERVER.")

    def populate_server_table(self) -> None:
        """Populate server list with killbox notation"""
        server_list = self.query_one("#server_list", Static)
        
        if not self.servers_data:
            server_list.update("No servers configured.")
            return
            
        lines = []
        for i, server in enumerate(self.servers_data[:9]):  # Max 9 servers
            name = server.get("name", "unknown")
            endpoint = server.get("endpoint", "unknown")
            status = "●ONLINE" if server.get("status") == "up" else "◐OFFLINE"
            auth_sessions = server.get("auth_sessions", 0)
            current_marker = " *" if server.get("is_current", False) else ""
            
            killbox = f"[{i+1}]"
            line = f"{killbox} {name:12} {endpoint:25} {status:10} {auth_sessions} sessions{current_marker}"
            lines.append(line)
            
        server_list.update("\n".join(lines))


    def update_dynamic_bindings(self) -> None:
        """Update status to show available server range"""
        # Just indicate the range in status message - keep footer simple
        pass

    def action_back_to_welcome(self) -> None:
        """Return to welcome screen"""
        self.app.pop_screen()
        
    def select_server_by_index(self, index: int) -> None:
        """Select server by index and proceed to tenant selection"""
        if 0 <= index < len(self.servers_data):
            server_data = self.servers_data[index]
            server_name = server_data["name"]
            
            # Switch to selected server
            self.status_update(f"Switching to server: {server_name}")
            switch_result = monk.server_use(server_name)
            
            if switch_result.success:
                # Proceed to tenant selection
                from screens.tenant_selection_screen import TenantSelectionScreen
                self.app.push_screen(TenantSelectionScreen(server_name))
            else:
                self.status_update(f"Failed to switch server: {switch_result.error}")
        else:
            self.status_update("Invalid server selection")

    # Individual server selection methods
    def action_select_server_1(self) -> None: self.select_server_by_index(0)
    def action_select_server_2(self) -> None: self.select_server_by_index(1)
    def action_select_server_3(self) -> None: self.select_server_by_index(2)
    def action_select_server_4(self) -> None: self.select_server_by_index(3)
    def action_select_server_5(self) -> None: self.select_server_by_index(4)
    def action_select_server_6(self) -> None: self.select_server_by_index(5)
    def action_select_server_7(self) -> None: self.select_server_by_index(6)
    def action_select_server_8(self) -> None: self.select_server_by_index(7)
    def action_select_server_9(self) -> None: self.select_server_by_index(8)

    def action_create_server(self) -> None:
        """Create new server"""
        from screens.new_server_screen import NewServerScreen
        self.app.push_screen(NewServerScreen())

    def action_ping_server(self) -> None:
        """Ping selected server"""
        table = self.query_one("#server_table", DataTable)
        if table.cursor_row >= 0:
            server_data = self.servers_data[table.cursor_row]
            server_name = server_data["name"]
            
            self.update_status(f"Pinging {server_name}...")
            ping_result = monk.server_ping(server_name)
            
            if ping_result.success:
                self.update_status(f"Ping successful: {server_name}")
                self.load_servers()  # Refresh to update status
            else:
                self.update_status(f"Ping failed: {ping_result.error}")
        else:
            self.update_status("Please select a server first")

