"""
VAULT POPULATION RECORDS
Population Management Interface Implementation
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, Select, Static, TextArea

from widgets.vault_container import VaultContainer
from models.vault_data import vault_data


class PopulationManagementScreen(Screen):
    """Vault Population Records - Resident Record Operations"""
    
    CSS = """
    .population-header {
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
    
    .population-motto {
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
    
    .search-section {
        height: 8;
        margin: 1 2;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        padding: 0 2;
    }
    
    .results-section {
        height: 12;
        margin: 1 2;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        padding: 0 2;
    }
    
    .results-section:focus-within {
        border: solid #ffb000;
        border-title-color: #ff3030;
    }
    
    .action-bar {
        dock: bottom;
        height: 4;
        background: #1a1a1a;
        margin: 0 2;
    }
    
    .action-buttons {
        height: 1;
        margin: 1 0;
        align: center middle;
    }
    
    .selection-info {
        height: 1;
        margin: 0 0;
        text-align: center;
        color: #ffb000;
    }
    
    .filter-input {
        margin: 0 1;
        width: 1fr;
    }
    
    .schema-select {
        margin: 0 1;
        width: 20;
    }
    """
    
    BINDINGS = [
        Binding("escape", "back_to_overseer", "Back", show=True),
        Binding("f", "find_records", "Find", show=True),        # Standard: Find/Filter
        Binding("c", "create_record", "Create", show=True),     # Standard: Create new
        Binding("d", "delete_record", "Delete", show=True),     # Standard: Delete selected  
        Binding("u", "update_record", "Update", show=True),     # Standard: Update/Edit selected
        Binding("s", "execute_search", "Search", show=True),    # Execute current filter
        Binding("r", "refresh", "Refresh", show=True),
        Binding("x", "clear_filter", "Clear", show=True),       # Clear filters
        Binding("b", "bulk_operations", "Bulk Ops", show=True),
        Binding("enter", "update_record", "Edit Record", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.current_schema = "personnel_records"
        self.selected_records = []
        self.population_data = []
        self.filter_query = ""

    def compose(self) -> ComposeResult:
        """Build the population management interface"""
        # Header with vault info
        with Container(classes="population-header"):
            yield Label(f"Current Vault: {self.app.current_vault}", classes="vault-info")
            yield Label('"Managing vault resident data with precision and care"', classes="population-motto")
        
        # Statistics bar with dynamic data
        with Container(classes="stats-bar"):
            yield Label("Population: Loading... | Schema: personnel_records | Selected: 0 records", id="population_stats")
            
        # Record list (main interface - not search)
        with Container(classes="results-section") as container:
            container.border_title = "PERSONNEL RECORDS"
            
            # Population records table
            table = DataTable(id="population_table")
            table.add_columns("☐", "ID", "NAME", "DEPARTMENT", "STATUS", "MODIFIED")
            yield table

        # Selection info and action buttons
        with Container(classes="action-bar"):
            yield Label("Selected: 0 records", id="selection_info", classes="selection-info")
            with Horizontal(classes="action-buttons"):
                yield Button("[f] FIND/FILTER", variant="primary", id="find_btn")
                yield Button("[c] CREATE", variant="default", id="create_btn")
                yield Button("[d] DELETE", variant="default", id="delete_btn")
                yield Button("[u] UPDATE", variant="default", id="update_btn")
                yield Button("[r] REFRESH", variant="default", id="refresh_btn")
                yield Button("[x] EXPORT", variant="default", id="export_btn")
                
        yield Footer()

    def on_mount(self) -> None:
        """Load initial population data"""
        self.load_population_data()

    def load_population_data(self) -> None:
        """Load population data (mock data with realistic fields)"""
        # Generate mock data that represents real database records
        population_data = [
            {
                "id": "12345", "first_name": "John", "last_name": "Doe", "email": "john.doe@company.com",
                "department": "engineering", "status": "active", "hire_date": "2024-03-15", "selected": False,
                "phone": "+1-555-123-4567", "security_clearance": "standard", "employee_id": "EMP-2024-001",
                "created_at": "2024-03-15 09:00:00", "modified_at": "2025-08-28 16:15:22", "created_by": "admin",
                "_metadata": {"size": "1.2KB", "valid": True, "backed_up": True, "last_access": "2025-08-28"}
            },
            {
                "id": "12346", "first_name": "Jane", "last_name": "Smith", "email": "jane.smith@company.com", 
                "department": "sales", "status": "active", "hire_date": "2024-01-10", "selected": False,
                "phone": "+1-555-987-6543", "security_clearance": "elevated", "employee_id": "EMP-2024-002",
                "created_at": "2024-01-10 10:30:00", "modified_at": "2025-08-27 14:22:11", "created_by": "hr_admin",
                "_metadata": {"size": "1.1KB", "valid": True, "backed_up": True, "last_access": "2025-08-27"}
            },
            {
                "id": "12347", "first_name": "Mike", "last_name": "Johnson", "email": "mike.johnson@company.com",
                "department": "operations", "status": "suspended", "hire_date": "2023-11-20", "selected": False,
                "phone": "+1-555-456-7890", "security_clearance": "standard", "employee_id": "EMP-2023-047",
                "created_at": "2023-11-20 14:15:00", "modified_at": "2025-08-26 09:45:33", "created_by": "admin",
                "_metadata": {"size": "1.3KB", "valid": False, "backed_up": True, "last_access": "2025-08-25"}
            },
            {
                "id": "12348", "first_name": "Sarah", "last_name": "Wilson", "email": "sarah.wilson@company.com",
                "department": "marketing", "status": "active", "hire_date": "2024-06-01", "selected": False,
                "phone": "+1-555-321-0987", "security_clearance": "restricted", "employee_id": "EMP-2024-023",
                "created_at": "2024-06-01 11:00:00", "modified_at": "2025-08-28 12:30:15", "created_by": "manager",
                "_metadata": {"size": "0.9KB", "valid": True, "backed_up": False, "last_access": "2025-08-28"}
            },
        ]
        
        self.population_data = population_data
        self.populate_results_table()
        self.update_population_stats()

    def populate_results_table(self) -> None:
        """Populate results table with current data"""
        table = self.query_one("#population_table", DataTable)
        table.clear()
        
        for record in self.population_data:
            checkbox = "☑" if record.get("selected", False) else "☐"
            # Display real field data in table
            full_name = f"{record.get('first_name', '')} {record.get('last_name', '')}"
            table.add_row(
                checkbox,
                record["id"],
                full_name,
                record.get("department", "unknown"),
                record["status"],
                record.get("modified_at", "unknown")[:10]  # Just date part
            )

    def update_population_stats(self) -> None:
        """Update population statistics"""
        total_records = len(self.population_data)
        selected_count = len([r for r in self.population_data if r.get("selected", False)])
        active_filters = "security_level=HIGH" if self.filter_query else "None"
        
        stats_text = f"Population: {total_records:,} | Active Filters: {active_filters} | Selected: {selected_count} records"
        self.query_one("#population_stats", Label).update(stats_text)
        
        selection_text = f"Selected: {selected_count} records"
        self.query_one("#selection_info", Label).update(selection_text)

    def action_back_to_overseer(self) -> None:
        """Return to the overseer console"""
        self.app.pop_screen()
        
    def action_find_records(self) -> None:
        """Open advanced filter/search interface"""
        from screens.filter_builder_screen import FilterBuilderScreen
        self.app.push_screen(FilterBuilderScreen(self.current_schema))
        
    def action_create_record(self) -> None:
        """Create new population record"""
        self.app.bell()
        # TODO: Implement new record creation dialog
        
    def action_update_record(self) -> None:
        """Update/Edit selected record"""
        table = self.query_one("#population_table", DataTable)
        if table.cursor_row >= 0:
            record = self.population_data[table.cursor_row]
            from screens.record_view_screen import RecordViewScreen
            self.app.push_screen(RecordViewScreen(self.current_schema, record["id"], record))
            
    def action_execute_search(self) -> None:
        """Execute search with current filters"""
        schema = self.query_one("#schema_select", Select).value
        filter_text = self.query_one("#filter_input", Input).value.strip()
        
        if not schema:
            schema = self.current_schema
            
        # For now, simulate search with filter
        if filter_text:
            self.filter_query = filter_text
            # Apply mock filtering based on text content
            if "OFFICER" in filter_text.upper():
                filtered_data = [r for r in self.population_data if "COMMAND" in r["section"] or "SECURITY" in r["section"]]
            elif "ACTIVE" in filter_text.upper():
                filtered_data = [r for r in self.population_data if "●ACTIVE" in r["status"]]
            else:
                filtered_data = self.population_data
        else:
            filtered_data = self.population_data
            self.filter_query = ""
        
        # Update display
        self.population_data = filtered_data
        self.populate_results_table()
        self.update_population_stats()
        
        # Show status
        total_results = len(filtered_data)
        if filter_text:
            self.app.bell()  # Success sound
        
    def action_clear_filter(self) -> None:
        """Clear all filters and reload"""
        self.query_one("#filter_input", Input).value = ""
        self.filter_query = ""
        self.load_population_data()  # Reload full data
        
    def action_new_record(self) -> None:
        """Legacy method - redirect to create"""
        self.action_create_record()
        
    def action_edit_record(self) -> None:
        """Legacy method - redirect to update"""
        self.action_update_record()
            
    def action_delete_record(self) -> None:
        """Delete selected records"""
        selected_count = len([r for r in self.population_data if r.get("selected", False)])
        if selected_count > 0:
            self.app.bell()
            # TODO: Implement deletion confirmation
        else:
            self.app.bell()
            
    def action_bulk_operations(self) -> None:
        """Open bulk operations menu"""
        self.app.bell()
        # TODO: Implement bulk operations interface
        
    def action_refresh(self) -> None:
        """Refresh population data"""
        self.load_population_data()
        self.app.bell()
        

    def on_data_table_row_selected(self, event) -> None:
        """Handle record selection in table"""
        table = self.query_one("#population_table", DataTable)
        if table.cursor_row >= 0 and table.cursor_row < len(self.population_data):
            # Toggle selection
            record = self.population_data[table.cursor_row]
            record["selected"] = not record.get("selected", False)
            self.populate_results_table()
            self.update_population_stats()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "find_btn":
            self.action_find_records()
        elif event.button.id == "create_btn":
            self.action_create_record()
        elif event.button.id == "delete_btn":
            self.action_delete_record()
        elif event.button.id == "update_btn":
            self.action_update_record()
        elif event.button.id == "search_btn":
            self.action_execute_search()
        elif event.button.id == "clear_btn":
            self.action_clear_filter()
        # Quick filter buttons
        elif event.button.id == "filter_active":
            self.apply_quick_filter("status", "●ACTIVE")
        elif event.button.id == "filter_injured":
            self.apply_quick_filter("status", "⚠INJURED")
        elif event.button.id == "filter_offline":
            self.apply_quick_filter("status", "◐OFFLINE")
        elif event.button.id == "filter_officers":
            self.apply_quick_filter("section", ["OVERSEER", "COMMAND", "SECURITY"])
        elif event.button.id == "filter_security":
            self.apply_quick_filter("section", "SECURITY")
        elif event.button.id == "filter_radio":
            self.apply_quick_filter("section", "RADIO")
        elif event.button.id == "filter_all":
            self.action_clear_filter()
            
    def apply_quick_filter(self, field: str, value) -> None:
        """Apply a quick filter to the population data"""
        # Reset to full dataset
        self.load_population_data()
        
        # Apply filter
        if isinstance(value, list):
            # Multiple values (e.g., officers)
            filtered_data = [r for r in self.population_data if r[field] in value]
            filter_desc = f"{field} in {value}"
        else:
            # Single value
            filtered_data = [r for r in self.population_data if r[field] == value]
            filter_desc = f"{field}={value}"
        
        # Update display
        self.population_data = filtered_data
        self.populate_results_table() 
        self.filter_query = filter_desc
        self.update_population_stats()
        self.app.bell()