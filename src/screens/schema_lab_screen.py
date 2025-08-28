"""
RESEARCH & DEVELOPMENT LAB
Schema Management Interface Implementation
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Label, Static

from widgets.vault_container import VaultContainer
from models.vault_data import vault_data


class SchemaLabScreen(Screen):
    """Research & Development Laboratory - Schema Management"""
    
    CSS = """
    .lab-header {
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
    
    .lab-motto {
        text-align: center;
        color: #1e3a8a;
        text-style: italic;
        margin: 1 0;
    }
    
    .registry-container {
        height: 20;
        margin: 1 2;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        padding: 0 2;
    }
    
    .stats-bar {
        height: 3;
        margin: 1 2;
        background: #1a1a1a;
        color: #ffb000;
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
    """
    
    BINDINGS = [
        Binding("escape", "back_to_overseer", "Back to Overseer", show=True),
        Binding("n", "new_schema", "New Schema", show=True),
        Binding("i", "import_schema", "Import", show=True),
        Binding("e", "export_all", "Export All", show=True),
        Binding("b", "backup", "Backup", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("enter", "edit_selected", "Edit Selected", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.selected_schema = None

    def compose(self) -> ComposeResult:
        """Build the schema laboratory interface"""
        # Header with vault info
        with Container(classes="lab-header"):
            yield Label(f"Current Vault: {self.app.current_vault}", classes="vault-info")
            yield Label('"Schema configurations require precision. Results may vary."', classes="lab-motto")
        
        # Statistics bar with dynamic data
        with Container(classes="stats-bar"):
            schema_data = vault_data.generate_schema_registry_data()
            deployed = len([s for s in schema_data if s["status"] == "●DEPLOYED"])
            testing = len([s for s in schema_data if s["status"] == "⚠TESTING"]) 
            draft = len([s for s in schema_data if s["status"] == "○DRAFT"])
            total = len(schema_data)
            
            yield Label(f"Active Experiments: {total} | Deployed: {deployed} | Under Development: {testing + draft}", id="lab_stats")
            
        # Schema registry table  
        with VaultContainer(title="SCHEMA REGISTRY", classes="registry-container"):
            # Create data table for schemas
            table = DataTable(id="schema_table")
            table.add_columns("NAME", "VER", "RECORDS", "STATUS", "ACTIONS")
            
            # Load dynamic schema data
            schema_data = vault_data.generate_schema_registry_data()
            table.add_rows([
                (schema["name"], schema["version"], schema["records"], 
                 schema["status"], schema["actions"]) 
                for schema in schema_data
            ])
            
            yield table

        # Action buttons
        with Container(classes="action-bar"):
            with Horizontal(classes="action-buttons"):
                yield Button("▶ NEW SCHEMA", variant="primary", id="new_schema_btn")
                yield Button("◉ IMPORT", variant="default", id="import_btn")
                yield Button("○ EXPORT ALL", variant="default", id="export_btn")
                yield Button("⚠ BACKUP", variant="default", id="backup_btn")
                
        yield Footer()

    def on_mount(self) -> None:
        """Focus the data table on startup"""
        table = self.query_one(DataTable)
        table.focus()

    def action_back_to_overseer(self) -> None:
        """Return to the overseer console"""
        self.app.pop_screen()
        
    def action_new_schema(self) -> None:
        """Create a new schema"""
        self.app.bell()
        # TODO: Implement new schema creation wizard
        
    def action_import_schema(self) -> None:
        """Import schema from file"""
        self.app.bell()
        # TODO: Implement schema import functionality
        
    def action_export_all(self) -> None:
        """Export all schemas"""
        self.app.bell()
        # TODO: Implement export all functionality
        
    def action_backup(self) -> None:
        """Backup all schemas"""
        self.app.bell()
        # TODO: Implement backup functionality
        
    def action_refresh(self) -> None:
        """Refresh schema data"""
        self.app.bell()
        # TODO: Refresh schema list from API
        
    def action_edit_selected(self) -> None:
        """Edit the selected schema"""
        table = self.query_one(DataTable)
        if table.cursor_row >= 0:
            row_data = table.get_row_at(table.cursor_row)
            schema_name = str(row_data[0])
            self.app.bell()
            # TODO: Navigate to schema editor for selected schema
            
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "new_schema_btn":
            self.action_new_schema()
        elif event.button.id == "import_btn":
            self.action_import_schema()
        elif event.button.id == "export_btn":
            self.action_export_all()
        elif event.button.id == "backup_btn":
            self.action_backup()
            
    def on_data_table_row_selected(self, event) -> None:
        """Handle schema selection in table"""
        table = self.query_one(DataTable)
        if table.cursor_row >= 0:
            row_data = table.get_row_at(table.cursor_row)
            self.selected_schema = str(row_data[0])
            # Update display or highlight selected schema