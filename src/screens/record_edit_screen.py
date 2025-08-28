"""
RECORD EDIT SCREEN
Form-based record editing with validation
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, Label, Select, Static
from datetime import datetime

from widgets.vault_container import VaultContainer


class RecordEditScreen(Screen):
    """Record Edit - Form-based record editing"""
    
    CSS = """
    .centering-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .edit-container {
        width: 85;
        height: auto;
        max-height: 90%;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        overflow-y: auto;
        padding: 0 2;
    }
    
    .section-label {
        color: #ffb000;
        text-style: bold;
        margin: 1 0 0 0;
    }
    
    .field-label {
        color: #00ff00;
        width: 20;
        margin: 0 1 0 0;
    }
    
    .field-input {
        width: 50;
        margin: 0 0 1 0;
    }
    
    .readonly-field {
        color: #6b7280;
        width: 50;
        margin: 0 0 1 0;
    }
    
    .validation-section {
        background: #1a1a1a;
        margin: 1 0;
        padding: 1;
    }
    
    .validation-item {
        height: 1;
        margin: 0 0;
    }
    
    .validation-ok {
        color: #22c55e;
    }
    
    .validation-warning {
        color: #f59e0b;
    }
    
    .validation-error {
        color: #dc2626;
    }
    
    .action-buttons {
        height: 1;
        margin: 2 0;
        align: center middle;
    }
    
    .metadata-footer {
        color: #6b7280;
        text-style: italic;
        text-align: center;
        margin: 1 0;
    }
    """
    
    BINDINGS = [
        Binding("escape", "cancel_edit", "Cancel", show=True),
        Binding("s", "save_record", "Save", show=True),
        Binding("x", "cancel_edit", "Cancel", show=True), 
        Binding("d", "delete_record", "Delete", show=True),
        Binding("t", "test_validation", "Test", show=True),
    ]

    def __init__(self, schema: str, record_id: str, record_data: dict):
        super().__init__()
        self.schema = schema
        self.record_id = record_id
        self.record_data = record_data.copy()
        self.validation_results = []
        self.has_changes = False

    def compose(self) -> ComposeResult:
        """Build the record edit interface"""
        with Container(classes="centering-container"):
            with Container(classes="edit-container") as container:
                container.border_title = f"EDIT RECORD: {self.schema}/{self.record_id}"
                
                with Vertical():
                    # Schema and ID info
                    yield Label(f"SCHEMA: {self.schema} (v2.1.4)", classes="section-label")
                    with Horizontal():
                        yield Label("ID:", classes="field-label")
                        yield Label(f"{self.record_id} (read-only)", classes="readonly-field")
                    
                    # Field editing section
                    yield Label("FIELD EDITING:", classes="section-label")
                    
                    # Generate form fields based on record data
                    for field_name, field_value in self.record_data.items():
                        if field_name not in ["id", "_metadata", "created_at", "modified_at", "created_by"]:
                            with Horizontal():
                                yield Label(f"{field_name}:", classes="field-label")
                                
                                # Different input types based on field name/value
                                if field_name.endswith("_date"):
                                    yield Input(
                                        value=str(field_value),
                                        placeholder="YYYY-MM-DD",
                                        id=f"field_{field_name}",
                                        classes="field-input"
                                    )
                                elif field_name in ["department", "security_clearance", "status"]:
                                    # Dropdown fields
                                    options = self.get_field_options(field_name)
                                    yield Select(
                                        options,
                                        value=str(field_value),
                                        id=f"field_{field_name}",
                                        classes="field-input"
                                    )
                                else:
                                    # Regular text fields
                                    yield Input(
                                        value=str(field_value),
                                        id=f"field_{field_name}",
                                        classes="field-input"
                                    )
                    
                    # Validation status section
                    with Container(classes="validation-section"):
                        yield Label("VALIDATION STATUS:", classes="section-label")
                        yield Label("✅ All fields validated", id="validation_summary", classes="validation-item validation-ok")
                        yield Static("", id="validation_details")
                    
                    # Action buttons with killbox notation
                    with Horizontal(classes="action-buttons"):
                        yield Button("[s] SAVE", variant="primary", id="save_btn")
                        yield Button("[x] CANCEL", variant="default", id="cancel_btn")
                        yield Button("[d] DELETE", variant="default", id="delete_btn")
                        yield Button("[t] TEST", variant="default", id="test_btn")
                    
                    # Metadata footer
                    yield Label(
                        f"Last Modified: {self.record_data.get('modified_at', 'Unknown')} by {self.record_data.get('created_by', 'system')}",
                        classes="metadata-footer"
                    )

    def get_field_options(self, field_name: str):
        """Get dropdown options for specific fields"""
        field_options = {
            "department": [
                ("Engineering", "engineering"),
                ("Sales", "sales"), 
                ("Marketing", "marketing"),
                ("Operations", "operations"),
                ("Finance", "finance")
            ],
            "security_clearance": [
                ("Standard", "standard"),
                ("Elevated", "elevated"),
                ("Restricted", "restricted"),
                ("Classified", "classified")
            ],
            "status": [
                ("Active", "active"),
                ("Suspended", "suspended"),
                ("Terminated", "terminated"),
                ("Medical Leave", "medical_leave")
            ]
        }
        return field_options.get(field_name, [("Unknown", "unknown")])

    def validate_record(self) -> list:
        """Validate all form fields"""
        validation_results = []
        
        # Get all field values
        for field_name in self.record_data.keys():
            if field_name.startswith("_") or field_name in ["id", "created_at", "modified_at", "created_by"]:
                continue
                
            try:
                widget = self.query_one(f"#field_{field_name}")
                if hasattr(widget, 'value'):
                    field_value = widget.value
                    
                    # Basic validation examples
                    if field_name == "email" and "@" not in field_value:
                        validation_results.append(("error", f"{field_name}: Invalid email format"))
                    elif field_name.endswith("_date") and len(field_value) != 10:
                        validation_results.append(("warning", f"{field_name}: Date format should be YYYY-MM-DD"))
                    elif field_name == "phone" and len(field_value.replace("-", "").replace(" ", "")) < 10:
                        validation_results.append(("warning", f"{field_name}: Phone number seems incomplete"))
                    else:
                        validation_results.append(("ok", f"{field_name}: Valid"))
            except:
                pass
                
        return validation_results

    def action_back_to_list(self) -> None:
        """Return to record list"""
        if self.has_changes:
            # TODO: Show unsaved changes warning
            pass
        self.app.pop_screen()
        
    def action_save_record(self) -> None:
        """Save record changes"""
        validation_results = self.validate_record()
        errors = [r for r in validation_results if r[0] == "error"]
        
        if errors:
            self.app.bell()
            # Show validation errors
            return
            
        # TODO: Execute monk data update command
        self.app.bell()
        # For now, just return to list
        self.app.pop_screen()
        
    def action_cancel_edit(self) -> None:
        """Cancel editing and return"""
        self.action_back_to_list()
        
    def action_delete_record(self) -> None:
        """Delete this record"""
        self.app.bell()
        # TODO: Implement deletion confirmation
        
    def action_test_validation(self) -> None:
        """Test field validation"""
        validation_results = self.validate_record()
        
        # Update validation display
        errors = len([r for r in validation_results if r[0] == "error"])
        warnings = len([r for r in validation_results if r[0] == "warning"])
        
        if errors > 0:
            summary_text = f"❌ {errors} errors, {warnings} warnings"
            summary_class = "validation-error"
        elif warnings > 0:
            summary_text = f"⚠ {warnings} warnings"
            summary_class = "validation-warning"  
        else:
            summary_text = "✅ All fields validated"
            summary_class = "validation-ok"
            
        summary_widget = self.query_one("#validation_summary", Label)
        summary_widget.update(summary_text)
        summary_widget.remove_class("validation-ok", "validation-warning", "validation-error")
        summary_widget.add_class(summary_class)
        
        self.app.bell()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "save_btn":
            self.action_save_record()
        elif event.button.id == "cancel_btn":
            self.action_cancel_edit()
        elif event.button.id == "delete_btn":
            self.action_delete_record()
        elif event.button.id == "test_btn":
            self.action_test_validation()
        elif event.button.id == "back_btn":
            self.action_back_to_list()