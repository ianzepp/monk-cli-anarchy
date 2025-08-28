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
from api.monk_client import monk


class ServerSelectionScreen(Screen):
    """Step 1: Select server connection"""
    
    CSS = """
    .centering-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .server-container {
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
    
    .server-table {
        height: 12;
        margin: 1 0;
    }
    
    .server-table:focus-within {
        border: solid #ffb000;
        border-title-color: #ff3030;
    }
    
    .action-buttons {
        height: 3;
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
        Binding("escape", "quit_app", "Quit", show=True),
        Binding("c", "create_server", "Create Server", show=True),
        Binding("1", "select_server_1", "[1]", show=True),
        Binding("2", "select_server_2", "[2]", show=True),
        Binding("3", "select_server_3", "[3]", show=True),
        Binding("4", "select_server_4", "[4]", show=True),
        Binding("5", "select_server_5", "[5]", show=True),
        Binding("6", "select_server_6", "[6]", show=True),
        Binding("7", "select_server_7", "[7]", show=True),
        Binding("8", "select_server_8", "[8]", show=True),
        Binding("9", "select_server_9", "[9]", show=True),
        Binding("p", "ping_server", "Ping", show=True),
        Binding("left", "focus_previous_button", "◀", show=False),
        Binding("right", "focus_next_button", "▶", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.servers_data = []
        self.selected_server = None

    def compose(self) -> ComposeResult:
        """Build the server selection interface"""
        with Container(classes="centering-container"):
            with Container(classes="server-container") as container:
                container.border_title = "VAULT FACILITY SERVER SELECTION"
                
                with Vertical():
                    yield Label("STEP 1 of 3: Choose Server Connection", classes="step-indicator")
                    
                    # Server selection list with killboxes
                    with Container(classes="server-table"):
                        yield Static("", id="server_list")
                    
                    # Status message
                    yield Static("Select a vault facility server to connect to", id="status_message", classes="status-message")
                    
                    # Action buttons with killbox notation
                    with Horizontal(classes="action-buttons"):
                        yield Button("[c] CREATE SERVER", variant="primary", id="create_btn")
                        yield Button("[ESC] QUIT", variant="default", id="quit_btn")

    def on_mount(self) -> None:
        """Load server data on startup"""
        self.load_servers()

    def load_servers(self) -> None:
        """Load server list from monk CLI"""
        self.update_status("Loading vault facility servers...")
        
        result = monk.server_list()
        if result.success and isinstance(result.data, dict):
            servers = result.data.get("servers", [])
            self.servers_data = servers
            
            if not servers:
                self.update_status("No servers configured. Use [c] CREATE SERVER to add one.")
                return
                
            self.populate_server_table()
            self.update_status(f"Found {len(servers)} vault facility servers. Use [ENTER] to select.")
        else:
            # No demo data - show proper error
            self.servers_data = []
            self.populate_server_table()  # Shows "No servers configured"
            error_msg = result.error if result.error else "monk CLI unavailable"
            self.update_status(f"⚠ Overseer resource list not found! {error_msg}. Use [c] CREATE SERVER to configure connections.")

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

    def update_status(self, message: str) -> None:
        """Update status message"""
        self.query_one("#status_message", Static).update(message)

    def action_quit_app(self) -> None:
        """Quit the application"""
        self.app.exit()
        
    def select_server_by_index(self, index: int) -> None:
        """Select server by index and proceed to tenant selection"""
        if 0 <= index < len(self.servers_data):
            server_data = self.servers_data[index]
            server_name = server_data["name"]
            
            # Switch to selected server
            self.update_status(f"Switching to server: {server_name}")
            switch_result = monk.server_use(server_name)
            
            if switch_result.success:
                # Proceed to tenant selection
                from screens.tenant_selection_screen import TenantSelectionScreen
                self.app.push_screen(TenantSelectionScreen(server_name))
            else:
                self.update_status(f"Failed to switch server: {switch_result.error}")
        else:
            self.update_status("Invalid server selection")

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

    def action_focus_next_button(self) -> None:
        """Focus next button without looping"""
        buttons = self.query("Button")
        if not buttons:
            return
            
        # Find currently focused button
        focused_button = None
        for i, button in enumerate(buttons):
            if button.has_focus:
                focused_button = i
                break
        
        # Move to next button, but stop at last one
        if focused_button is not None and focused_button < len(buttons) - 1:
            buttons[focused_button + 1].focus()
        elif focused_button is None:
            # No button focused, focus first one
            buttons[0].focus()
    
    def action_focus_previous_button(self) -> None:
        """Focus previous button without looping"""
        buttons = self.query("Button")
        if not buttons:
            return
            
        # Find currently focused button
        focused_button = None
        for i, button in enumerate(buttons):
            if button.has_focus:
                focused_button = i
                break
        
        # Move to previous button, but stop at first one
        if focused_button is not None and focused_button > 0:
            buttons[focused_button - 1].focus()
        elif focused_button is None:
            # No button focused, focus last one
            buttons[-1].focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "create_btn":
            self.action_create_server()
        elif event.button.id == "quit_btn":
            self.action_quit_app()