"""
SCHEMA LABORATORY MODULE
JSON Schema Management and Meta Operations
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DataTable, Label, Static
from typing import Dict, Any, List

from screens.base_screen import BaseVaultScreen
from api.monk_client import monk


class SchemaLabScreen(BaseVaultScreen):
    """Schema Laboratory - Meta schema management and JSON Schema operations"""
    
    CSS = """
    .lab-title {
        text-style: bold;
        text-align: center;
        margin: 1 0;
    }
    
    .lab-motto {
        text-align: center;
        text-style: italic;
        margin: 1 0;
    }
    
    .schema-list {
        margin: 2 0;
        width: 100%;
        height: 1fr;
        min-height: 10;
    }
    
    .stats-summary {
        text-align: center;
        margin: 1 0;
    }
    """
    
    BINDINGS = BaseVaultScreen.BINDINGS + [
        Binding("escape", "back_to_overseer", "Back", show=True),
        Binding("enter", "edit_current", "Edit", show=True),
        Binding("c", "create_schema", "Create", show=True),
        Binding("f", "find_schema", "Find", show=True),
        Binding("u", "update_selected", "Update", show=True),
        Binding("d", "delete_selected", "Delete", show=True),
        Binding("1", "select_schema_1", "1-9 Select + ENTER", show=True),
        Binding("2", "select_schema_2", "\u200b", show=False),
        Binding("3", "select_schema_3", "\u200b", show=False),
        Binding("4", "select_schema_4", "\u200b", show=False),
        Binding("5", "select_schema_5", "\u200b", show=False),
        Binding("6", "select_schema_6", "\u200b", show=False),
        Binding("7", "select_schema_7", "\u200b", show=False),
        Binding("8", "select_schema_8", "\u200b", show=False),
        Binding("9", "select_schema_9", "\u200b", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.schemas_data = []
        self.selected_schema = None

    def compose_content(self) -> ComposeResult:
        """Define schema laboratory content"""
        with Vertical():
            yield Label("SCHEMA LABORATORY", classes="lab-title amber-alert-text")
            yield Label('"JSON Schema definitions require precision. Results may vary."', classes="lab-motto steel-blue-text")
            
            # Stats summary
            yield Static("", id="schema_stats", classes="stats-summary healthy-green-text")
            
            # Schema table with killboxes - responsive column sizing
            table = DataTable(id="schema_table", classes="schema-list")
            # Use explicit column widths for better layout
            table.add_column("", width=4)      # Killbox: [1]
            table.add_column("NAME", width=12)  # Schema name
            table.add_column("STATUS", width=10) # Status indicator
            table.add_column("FIELDS", width=8)  # Field count
            table.add_column("TABLE", width=12)  # Table name
            table.add_column("UPDATED", width=10) # Update date
            table.show_header = False
            table.cursor_type = "row"
            table.can_focus = True
            yield table
            
    def compose_status(self) -> str:
        """Define default status message"""
        return "Ready for schema operations"

    def on_mount(self) -> None:
        """Load schema data on startup"""
        super().on_mount()
        self.load_schemas()
        # Focus the table so arrow keys and Enter work
        self.call_later(self.focus_table)
        
    def focus_table(self) -> None:
        """Focus the schema table for navigation"""
        try:
            table = self.query_one("#schema_table", DataTable)
            table.focus()
        except:
            pass

    def load_schemas(self) -> None:
        """Load schema list from monk CLI using data select schema"""
        self.status_update("Loading schema registry...")
        
        # Use monk data select schema to get all schemas
        result = monk.data_select("schema")
        if result.success and isinstance(result.data, list):
            self.schemas_data = result.data
            
            if not self.schemas_data:
                self.status_update("No schemas found. Use [c] CREATE SCHEMA to add one.")
                # Still populate empty table
                self.call_later(self.populate_schema_table)
                return
                
            # Use call_later to ensure table is ready
            self.call_later(self.populate_schema_table)
            self.call_later(self.update_stats)
            self.status_update(f"Found {len(self.schemas_data)} schemas. Press [1-{min(len(self.schemas_data), 9)}] to select.")
        else:
            # No schemas or error
            self.schemas_data = []
            self.call_later(self.populate_schema_table)
            error_msg = result.error if result.error else "monk CLI unavailable"
            self.status_update(f"⚠ Schema registry not accessible! {error_msg}. Use [c] CREATE SCHEMA.")

    def populate_schema_table(self) -> None:
        """Populate schema table with killbox notation"""
        try:
            table = self.query_one("#schema_table", DataTable)
            table.clear()
            
            if not self.schemas_data:
                table.add_row("", "No schemas available.", "", "", "", "")
                return
                
            for i, schema in enumerate(self.schemas_data[:9]):  # Max 9 schemas
                name = schema.get("name", "unknown")
                status = self.format_status(schema.get("status", "unknown"))
                field_count = schema.get("field_count", "0")
                table_name = schema.get("table_name", "unknown")
                updated = self.format_date(schema.get("updated_at", ""))
                
                killbox = f"[{i+1}]"
                
                # Add row to table
                table.add_row(killbox, name, status, field_count, table_name, updated)
                
        except Exception as e:
            # Fallback - update status with error info
            self.status_update(f"Table population error: {str(e)}")

    def format_status(self, status: str) -> str:
        """Format schema status with visual indicators"""
        status_map = {
            "active": "●ACTIVE",
            "system": "⚙SYSTEM", 
            "pending": "○PENDING",
            "disabled": "◐DISABLED"
        }
        return status_map.get(status, f"?{status.upper()}")

    def format_date(self, date_str: str) -> str:
        """Format date for display"""
        if not date_str:
            return "unknown"
        try:
            # Extract just the date part from ISO timestamp
            return date_str[:10] if len(date_str) > 10 else date_str
        except:
            return "invalid"

    def update_stats(self) -> None:
        """Update schema statistics summary"""
        if not self.schemas_data:
            stats_text = "No schemas in registry"
        else:
            total = len(self.schemas_data)
            active = len([s for s in self.schemas_data if s.get("status") == "active"])
            system = len([s for s in self.schemas_data if s.get("status") == "system"])
            stats_text = f"Registry: {total} schemas | Active: {active} | System: {system}"
        
        try:
            stats_widget = self.query_one("#schema_stats", Static)
            stats_widget.update(stats_text)
        except:
            pass

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle ENTER key or row selection in schema table - opens update wizard"""
        if event.data_table.id == "schema_table":
            row_index = event.cursor_row
            if 0 <= row_index < len(self.schemas_data):
                self.edit_schema_by_index(row_index)

    def action_back_to_overseer(self) -> None:
        """Return to overseer console"""
        self.app.pop_screen()
        
    def action_edit_current(self) -> None:
        """Edit currently highlighted schema (ENTER key)"""
        try:
            table = self.query_one("#schema_table", DataTable)
            current_row = table.cursor_row
            if 0 <= current_row < len(self.schemas_data):
                self.edit_schema_by_index(current_row)
            else:
                self.status_update("No schema selected - use arrow keys or press [1-9]")
        except:
            self.status_update("No schema available to edit")
        
    def select_schema_by_index(self, index: int) -> None:
        """Select schema by index and show details"""
        if 0 <= index < len(self.schemas_data):
            schema_data = self.schemas_data[index]
            schema_name = schema_data["name"]
            
            self.selected_schema = schema_data
            self.status_update(f"Selected: {schema_name} ({schema_data.get('field_count', '0')} fields)")
            
            # Also move table cursor to this row for visual feedback
            try:
                table = self.query_one("#schema_table", DataTable)
                table.cursor_row = index
            except:
                pass
        else:
            self.status_update("Invalid schema selection")

    def edit_schema_by_index(self, index: int) -> None:
        """Edit schema by index - opens update wizard"""
        if 0 <= index < len(self.schemas_data):
            schema_data = self.schemas_data[index]
            schema_name = schema_data["name"]
            
            self.status_update(f"Opening schema wizard: {schema_name}")
            from screens.schema_wizard_screen import SchemaWizardScreen
            self.app.push_screen(SchemaWizardScreen(mode="update", schema_data=schema_data))
        else:
            self.status_update("Invalid schema selection")

    # Individual schema selection methods
    def action_select_schema_1(self) -> None: self.select_schema_by_index(0)
    def action_select_schema_2(self) -> None: self.select_schema_by_index(1)
    def action_select_schema_3(self) -> None: self.select_schema_by_index(2)
    def action_select_schema_4(self) -> None: self.select_schema_by_index(3)
    def action_select_schema_5(self) -> None: self.select_schema_by_index(4)
    def action_select_schema_6(self) -> None: self.select_schema_by_index(5)
    def action_select_schema_7(self) -> None: self.select_schema_by_index(6)
    def action_select_schema_8(self) -> None: self.select_schema_by_index(7)
    def action_select_schema_9(self) -> None: self.select_schema_by_index(8)

    def action_create_schema(self) -> None:
        """Create new schema - opens creation wizard"""
        self.status_update("Opening schema creation wizard...")
        from screens.schema_wizard_screen import SchemaWizardScreen
        self.app.push_screen(SchemaWizardScreen(mode="create"))
        
    def action_find_schema(self) -> None:
        """Find/filter schemas"""
        self.app.bell()
        # TODO: Implement schema search/filter
        self.status_update("Schema search not yet implemented")
        
    def action_update_selected(self) -> None:
        """Update selected schema"""
        if self.selected_schema:
            self.app.bell()
            # TODO: Implement schema update screen
            schema_name = self.selected_schema.get("name", "unknown")
            self.status_update(f"Schema update not yet implemented: {schema_name}")
        else:
            self.status_update("No schema selected - press [1-9] or use arrow keys + ENTER")
            
    def action_delete_selected(self) -> None:
        """Delete selected schema"""
        if self.selected_schema:
            schema_name = self.selected_schema.get("name", "unknown")
            schema_status = self.selected_schema.get("status", "unknown")
            
            if schema_status == "system":
                self.status_update(f"Cannot delete system schema: {schema_name}")
                self.app.bell()
                return
                
            self.app.bell()
            # TODO: Implement schema deletion confirmation
            self.status_update(f"Schema deletion not yet implemented: {schema_name}")
        else:
            self.status_update("No schema selected - press [1-9] or use arrow keys + ENTER")