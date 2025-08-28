"""
KILLBOX TABLE WIDGET
Reusable table component for data display with killbox navigation
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import DataTable
from typing import List, Dict, Any, Callable, Optional


class KillboxTable(DataTable):
    """DataTable with automatic killbox notation and ENTER selection"""
    
    def __init__(
        self,
        columns: List[str],
        data: List[Dict[str, Any]] = None,
        id_field: str = "id",
        on_select: Callable[[int, Dict], None] = None,
        max_items: int = 9,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Configuration
        self.columns = columns
        self.data_items = data or []
        self.id_field = id_field
        self.on_select_callback = on_select
        self.max_items = max_items
        
        # DataTable setup
        self.show_header = False
        self.cursor_type = "row"
        self.can_focus = True

    def setup_columns(self) -> None:
        """Setup table columns"""
        # Clear existing columns and add new ones
        self.clear(columns=True)
        # Add columns with killbox prefix
        self.add_columns("", *self.columns)
        
    def populate_data(self, data: List[Dict[str, Any]] = None) -> None:
        """Populate table with data and killbox notation"""
        if data is not None:
            self.data_items = data
        
        # Setup columns first
        self.setup_columns()
        
        if not self.data_items:
            # Show empty state
            empty_row = ["", "No data available"] + [""] * (len(self.columns) - 1)
            self.add_row(*empty_row)
            return
        
        # Add data rows with killbox notation
        for i, item in enumerate(self.data_items[:self.max_items]):
            killbox = f"[{i+1}]"
            
            # Build row data from item fields
            row_data = [killbox]
            for column in self.columns:
                # Handle nested field access (e.g., "metadata.size")
                value = self.get_field_value(item, column)
                row_data.append(str(value))
            
            self.add_row(*row_data)

    def get_field_value(self, item: Dict[str, Any], field_path: str) -> Any:
        """Get field value from item, supporting dot notation"""
        try:
            # Simple field access first
            if field_path in item:
                return item[field_path]
            
            # Try common field mappings
            field_mappings = {
                "NAME": "name",
                "DISPLAY_NAME": "display_name", 
                "ENDPOINT": "endpoint",
                "STATUS": "status",
                "SESSIONS": "auth_sessions",
                "AUTH_STATUS": "authenticated",
                "DESCRIPTION": "description"
            }
            
            mapped_field = field_mappings.get(field_path, field_path.lower())
            if mapped_field in item:
                value = item[mapped_field]
                
                # Format specific fields
                if field_path == "STATUS":
                    return "●ONLINE" if value == "up" else "◐OFFLINE"
                elif field_path == "AUTH_STATUS":
                    auth = "✅ AUTH" if value else "❌ NO_AUTH"
                    current = " *" if item.get("is_current", False) else ""
                    return f"{auth}{current}"
                elif field_path == "SESSIONS":
                    current = " *" if item.get("is_current", False) else ""
                    return f"{value} sessions{current}"
                
                return value
            
            return "unknown"
            
        except Exception:
            return "error"

    def on_row_selected(self, event) -> None:
        """Handle ENTER key or row selection"""
        if self.on_select_callback and event.cursor_row >= 0:
            if event.cursor_row < len(self.data_items):
                selected_item = self.data_items[event.cursor_row]
                self.on_select_callback(event.cursor_row, selected_item)

    def get_selected_item(self) -> Optional[Dict[str, Any]]:
        """Get currently selected item"""
        if 0 <= self.cursor_row < len(self.data_items):
            return self.data_items[self.cursor_row]
        return None
        
    def get_binding_methods(self, action_prefix: str) -> List[Binding]:
        """Generate killbox bindings for this table"""
        bindings = []
        for i in range(min(len(self.data_items), self.max_items)):
            num = str(i + 1)
            bindings.append(
                Binding(num, f"{action_prefix}_{num}", "\u200b", show=False)
            )
        return bindings