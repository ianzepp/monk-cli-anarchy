"""
QUERY CONSTRUCTION TERMINAL
Advanced Filter Builder Interface Implementation
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Select, Static, TextArea

from widgets.vault_container import VaultContainer


class FilterBuilderScreen(Screen):
    """Query Construction Terminal - Advanced Filter Builder"""
    
    CSS = """
    .centering-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .filter-container {
        width: 90;
        height: auto;
        max-height: 90%;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        overflow-y: auto;
        padding: 0 2;
    }
    
    .ai-section {
        border: solid #22c55e;
        border-title-color: #22c55e;
        border-title-style: bold;
        background: #0a0a0a;
        margin: 1 0;
        padding: 1;
        height: 6;
    }
    
    .ai-textarea {
        height: 3;
        margin: 0 0 1 0;
        background: #1a1a1a;
        color: #ffffff;
        border: solid #22c55e;
    }
    
    .ai-hint {
        color: #6b7280;
        text-style: italic;
        margin: 0 1;
    }
    
    .section-label {
        color: #ffb000;
        text-style: bold;
        margin: 1 0;
    }
    
    .condition-group {
        border: solid #1a1a1a;
        background: #0a0a0a;
        margin: 1 0;
        padding: 1;
        height: 4;
    }
    
    .logic-group {
        border: solid #1a1a1a;
        background: #0a0a0a;
        margin: 1 2;
        padding: 1;
        width: 15;
        height: 4;
    }
    
    .field-row {
        height: 1;
        margin: 0 0 1 0;
    }
    
    .field-label {
        color: #00ff00;
        width: 8;
    }
    
    .field-select {
        width: 20;
        margin: 0 1;
    }
    
    .field-input {
        width: 30;
        margin: 0 1;
    }
    
    .preview-section {
        background: #1a1a1a;
        margin: 1 0;
        padding: 1;
        height: 6;
    }
    
    .generated-query {
        color: #22c55e;
        text-style: bold;
        margin: 1 0;
    }
    
    .action-buttons {
        height: 1;
        margin: 2 0;
        align: center middle;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel_filter", "Cancel", show=True),
        Binding("a", "ai_convert", "AI Convert", show=True),
        Binding("s", "save_query", "Save Query", show=True),
        Binding("x", "execute_filter", "Execute", show=True),
        Binding("c", "clear_all", "Clear All", show=True),
    ]

    def __init__(self, schema: str):
        super().__init__()
        self.schema = schema
        self.conditions = []
        
    def on_mount(self) -> None:
        """Focus the AI input on startup"""
        self.call_later(self.focus_ai_input)
        
    def focus_ai_input(self) -> None:
        """Focus the AI textarea"""
        try:
            ai_input = self.query_one("#ai_query_input", TextArea)
            ai_input.focus()
        except:
            pass

    def compose(self) -> ComposeResult:
        """Build the filter builder interface"""
        with Container(classes="centering-container"):
            with Container(classes="filter-container") as container:
                container.border_title = f"QUERY CONSTRUCTION TERMINAL - {self.schema}"
                
                with Vertical():
                    # AI Query Input Section
                    with Container(classes="ai-section") as ai_container:
                        ai_container.border_title = "AI QUERY ASSISTANT"
                        
                        with Vertical():
                            yield Label("Describe your search in plain English:", classes="field-label")
                            ai_input = TextArea(
                                text="Find all engineers hired after 2024 with standard security clearance",
                                id="ai_query_input",
                                classes="ai-textarea"
                            )
                            ai_input.show_line_numbers = False
                            ai_input.wrap = True
                            yield ai_input
                            
                            with Horizontal():
                                yield Button("[a] AI CONVERT", variant="primary", id="ai_convert_btn")
                                yield Button("[c] CLEAR", variant="default", id="ai_clear_btn")
                                yield Static("AI converts English to Filter DSL automatically", classes="ai-hint")
                    
                    # Manual Condition Groups (below AI)
                    yield Label("MANUAL FILTER BUILDER:", classes="section-label")
                    
                    # Condition Group 1
                    with Container(classes="condition-group") as group1:
                        group1.border_title = "CONDITION GROUP 1"
                        
                        with Vertical():
                            with Horizontal(classes="field-row"):
                                yield Label("FIELD:", classes="field-label")
                                yield Select(
                                    self.get_schema_fields(),
                                    id="field1_select",
                                    classes="field-select"
                                )
                            
                            with Horizontal(classes="field-row"):
                                yield Label("OP:", classes="field-label") 
                                yield Select(
                                    [("equals", "$eq"), ("not equals", "$ne"), ("greater than", "$gt"), 
                                     ("less than", "$lt"), ("contains", "$like"), ("in list", "$in")],
                                    id="op1_select",
                                    classes="field-select"
                                )
                            
                            with Horizontal(classes="field-row"):
                                yield Label("VALUE:", classes="field-label")
                                yield Input(
                                    placeholder="Enter value...",
                                    id="value1_input",
                                    classes="field-input"
                                )
                    
                    # Logic connector
                    with Horizontal():
                        with Container(classes="logic-group") as logic:
                            logic.border_title = "LOGIC"
                            with Vertical():
                                yield Button("AND", variant="primary", id="logic_and")
                                yield Button("OR", variant="default", id="logic_or")
                                yield Button("NOT", variant="default", id="logic_not")
                    
                    # Condition Group 2
                    with Container(classes="condition-group") as group2:
                        group2.border_title = "CONDITION GROUP 2"
                        
                        with Vertical():
                            with Horizontal(classes="field-row"):
                                yield Label("FIELD:", classes="field-label")
                                yield Select(
                                    self.get_schema_fields(),
                                    id="field2_select", 
                                    classes="field-select"
                                )
                            
                            with Horizontal(classes="field-row"):
                                yield Label("OP:", classes="field-label")
                                yield Select(
                                    [("equals", "$eq"), ("not equals", "$ne"), ("greater than", "$gt"), 
                                     ("less than", "$lt"), ("contains", "$like"), ("in list", "$in")],
                                    id="op2_select",
                                    classes="field-select"
                                )
                            
                            with Horizontal(classes="field-row"):
                                yield Label("VALUE:", classes="field-label")
                                yield Input(
                                    placeholder="Enter value...",
                                    id="value2_input",
                                    classes="field-input"
                                )
                    
                    # Generated query preview
                    with Container(classes="preview-section"):
                        yield Label("Generated Query Preview:", classes="field-label")
                        yield Static(
                            '{"$and":[{"department":"engineering"},{"status":"active"}]}',
                            id="query_preview",
                            classes="generated-query"
                        )
                    
                    # Action buttons with killbox notation
                    with Horizontal(classes="action-buttons"):
                        yield Button("[x] EXECUTE", variant="primary", id="execute_btn")
                        yield Button("[s] SAVE QUERY", variant="default", id="save_btn")
                        yield Button("[l] LOAD PRESET", variant="default", id="load_btn")
                        yield Button("[c] CLEAR", variant="default", id="clear_btn")

    def get_schema_fields(self):
        """Get available fields for the current schema"""
        # Return realistic database fields
        return [
            ("ID", "id"),
            ("First Name", "first_name"), 
            ("Last Name", "last_name"),
            ("Email", "email"),
            ("Department", "department"),
            ("Status", "status"),
            ("Hire Date", "hire_date"),
            ("Security Clearance", "security_clearance"),
            ("Employee ID", "employee_id"),
            ("Phone", "phone")
        ]

    def build_query(self) -> dict:
        """Build query from current form values"""
        try:
            # Get condition 1
            field1 = self.query_one("#field1_select", Select).value
            op1 = self.query_one("#op1_select", Select).value
            value1 = self.query_one("#value1_input", Input).value.strip()
            
            # Get condition 2  
            field2 = self.query_one("#field2_select", Select).value
            op2 = self.query_one("#op2_select", Select).value
            value2 = self.query_one("#value2_input", Input).value.strip()
            
            # Build query structure
            conditions = []
            
            if field1 and value1:
                if op1 == "$in":
                    # Handle list values
                    list_values = [v.strip() for v in value1.split(",")]
                    conditions.append({field1: {op1: list_values}})
                else:
                    conditions.append({field1: {op1: value1}})
            
            if field2 and value2:
                if op2 == "$in":
                    list_values = [v.strip() for v in value2.split(",")]
                    conditions.append({field2: {op2: list_values}})
                else:
                    conditions.append({field2: {op2: value2}})
            
            if len(conditions) > 1:
                return {"$and": conditions}
            elif len(conditions) == 1:
                return conditions[0]
            else:
                return {}
                
        except Exception:
            return {}

    def update_query_preview(self) -> None:
        """Update the generated query preview"""
        query = self.build_query()
        import json
        
        if query:
            query_text = json.dumps(query, indent=2)
        else:
            query_text = "{}"
            
        preview = self.query_one("#query_preview", Static)
        preview.update(query_text)

    def action_cancel_filter(self) -> None:
        """Cancel filter building and return"""
        self.app.pop_screen()
        
    def action_execute_filter(self) -> None:
        """Execute the built filter"""
        query = self.build_query()
        # TODO: Pass filter back to population management screen
        self.app.bell()
        self.app.pop_screen()
        
    def action_save_query(self) -> None:
        """Save query as preset"""
        self.app.bell()
        # TODO: Implement query saving
        
    def action_ai_convert(self) -> None:
        """Convert natural language to filter query using AI"""
        ai_input = self.query_one("#ai_query_input", TextArea)
        natural_query = ai_input.text.strip()
        
        if not natural_query:
            self.app.bell()
            return
            
        # Simple rule-based conversion (placeholder for real AI)
        # TODO: Replace with actual AI API call
        converted_query = self.convert_natural_language(natural_query)
        
        # Update the query preview
        import json
        query_text = json.dumps(converted_query, indent=2)
        preview = self.query_one("#query_preview", Static)
        preview.update(query_text)
        
        self.app.bell()
        
    def convert_natural_language(self, text: str) -> dict:
        """Convert natural language to filter query (simple rule-based for demo)"""
        text = text.lower()
        conditions = []
        
        # Simple pattern matching
        if "engineer" in text:
            conditions.append({"department": {"$eq": "engineering"}})
        if "after 2024" in text or "hired after 2024" in text:
            conditions.append({"hire_date": {"$gt": "2024-01-01"}})
        if "standard security" in text:
            conditions.append({"security_clearance": {"$eq": "standard"}})
        if "active" in text:
            conditions.append({"status": {"$eq": "active"}})
        if "suspended" in text:
            conditions.append({"status": {"$eq": "suspended"}})
        if "sales" in text:
            conditions.append({"department": {"$eq": "sales"}})
        if "marketing" in text:
            conditions.append({"department": {"$eq": "marketing"}})
            
        # Build final query
        if len(conditions) > 1:
            return {"$and": conditions}
        elif len(conditions) == 1:
            return conditions[0]
        else:
            return {"message": "Could not parse query - try being more specific"}

    def action_clear_all(self) -> None:
        """Clear all conditions"""
        self.query_one("#field1_select", Select).value = self.get_schema_fields()[0][1]
        self.query_one("#value1_input", Input).value = ""
        self.query_one("#field2_select", Select).value = self.get_schema_fields()[0][1]
        self.query_one("#value2_input", Input).value = ""
        self.query_one("#ai_query_input", TextArea).text = ""
        self.update_query_preview()

    def on_select_changed(self, event: Select.Changed) -> None:
        """Update preview when selections change"""
        self.update_query_preview()
        
    def on_input_changed(self, event: Input.Changed) -> None:
        """Update preview when inputs change"""
        self.update_query_preview()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "execute_btn":
            self.action_execute_filter()
        elif event.button.id == "save_btn":
            self.action_save_query()
        elif event.button.id == "clear_btn":
            self.action_clear_all()
        elif event.button.id == "load_btn":
            self.app.bell()  # TODO: Implement preset loading
        elif event.button.id == "ai_convert_btn":
            self.action_ai_convert()
        elif event.button.id == "ai_clear_btn":
            self.query_one("#ai_query_input", TextArea).text = ""