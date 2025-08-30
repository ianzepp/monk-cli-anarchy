"""
SCHEMA CREATION/UPDATE WIZARD
JSON Schema Management Interface
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Checkbox, Input, Label, RadioButton, RadioSet, Select, Static
from typing import Dict, Any, Optional

from screens.base_screen import BaseVaultScreen
from api.monk_client import monk


class SchemaWizardScreen(BaseVaultScreen):
    """Schema Creation/Update Wizard - unified interface for both create and update operations"""
    
    CSS = """
    .wizard-title {
        text-style: bold;
        text-align: center;
        margin: 1 0;
    }
    
    .wizard-subtitle {
        text-align: center;
        text-style: italic;
        margin: 1 0;
    }
    
    .section-header {
        text-style: bold;
        margin: 2 0 1 0;
    }
    
    .form-row {
        margin: 0 0;
        padding: 0 0;
        height: 3;
    }
    
    .form-label {
        width: 20;
        text-align: right;
        margin: 0 2 0 0;
        height: 3;
        content-align: center middle;
    }
    
    .form-input {
        width: 1fr;
        height: 3;
    }
    
    .form-group {
        margin: 0 0;
    }
    """
    
    BINDINGS = BaseVaultScreen.BINDINGS + [
        Binding("escape", "back_to_lab", "Back", show=True),
        Binding("enter", "save_schema", "Save", show=True),
        Binding("s", "save_draft", "Save Draft", show=True),
        Binding("tab", "focus_next", "Next Field", show=False),
        Binding("shift+tab", "focus_previous", "Previous Field", show=False),
    ]

    def __init__(self, mode: str = "create", schema_data: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.mode = mode  # "create" or "update"
        self.schema_data = schema_data or {}
        self.existing_schemas = []

    def compose_content(self) -> ComposeResult:
        """Define schema wizard content"""
        # Determine title based on mode
        if self.mode == "create":
            title = "NEW EXPERIMENTAL PROTOCOL"
            subtitle = '"New schemas require careful consideration and proper forms."'
        else:
            schema_name = self.schema_data.get("name", "unknown")
            title = f"MODIFY PROTOCOL: {schema_name}"
            subtitle = f'"Existing schema modification requires precision. Handle with care."'
            
        with Vertical():
            yield Label(title, classes="wizard-title amber-alert-text")
            yield Label(subtitle, classes="wizard-subtitle steel-blue-text")
            
            # Basic Information Section
            yield Static("BASIC INFORMATION", classes="section-header amber-alert-text")
            
            with Horizontal(classes="form-row"):
                yield Label("Schema Name:", classes="form-label")
                yield Input(
                    value=self.schema_data.get("name", ""),
                    placeholder="e.g., employee_evaluations",
                    id="schema_name",
                    classes="form-input"
                )
            
            with Horizontal(classes="form-row"):
                yield Label("Description:", classes="form-label") 
                yield Input(
                    value=self.schema_data.get("description", ""),
                    placeholder="Brief description of schema purpose",
                    id="schema_description",
                    classes="form-input"
                )
            
            with Horizontal(classes="form-row"):
                yield Label("Table Name:", classes="form-label")
                yield Input(
                    value=self.schema_data.get("table_name", ""),
                    placeholder="Database table name (auto-generated if empty)",
                    id="table_name",
                    classes="form-input"
                )
            
            with Horizontal(classes="form-row"):
                yield Label("Status:", classes="form-label")
                yield Select(
                    options=[
                        ("pending", "pending"),
                        ("active", "active"),
                        ("disabled", "disabled")
                    ],
                    value=self.schema_data.get("status", "pending"),
                    id="schema_status",
                    classes="form-input"
                )
            
            # Schema Template Section (only for create mode)
            if self.mode == "create":
                yield Static("SCHEMA TEMPLATE", classes="section-header amber-alert-text")
                
                with Horizontal(classes="form-row"):
                    yield Label("Clone from:", classes="form-label")
                    yield Select(
                        options=[("scratch", "Start from scratch")],  # Default option, others populated in load_existing_schemas
                        value="scratch",
                        id="template_source",
                        classes="form-input"
                    )
            
            # Deployment Settings Section
            yield Static("DEPLOYMENT SETTINGS", classes="section-header amber-alert-text")
            
            yield Checkbox("Enable data validation", value=True, id="enable_validation", classes="form-group")
            yield Checkbox("Create audit trail", value=True, id="create_audit", classes="form-group") 
            yield Checkbox("Auto-backup before changes", value=False, id="auto_backup", classes="form-group")
            yield Checkbox("Require approval for deployment", value=False, id="require_approval", classes="form-group")
            
            # Status/Info Section
            yield Static("", id="wizard_status", classes="stats-summary healthy-green-text")
            
    def compose_status(self) -> str:
        """Define default status message"""
        if self.mode == "create":
            return "Ready to create new schema - fill required fields and press ENTER"
        else:
            return f"Ready to update schema: {self.schema_data.get('name', 'unknown')}"

    def on_mount(self) -> None:
        """Initialize wizard on startup"""
        super().on_mount()
        
        if self.mode == "create":
            # Load existing schemas for template dropdown
            self.load_existing_schemas()
        
        # Focus the schema name input
        self.call_later(self.focus_name_input)
        
    def focus_name_input(self) -> None:
        """Focus the schema name input field"""
        try:
            name_input = self.query_one("#schema_name", Input)
            name_input.focus()
        except:
            pass

    def load_existing_schemas(self) -> None:
        """Load existing schemas for template dropdown"""
        result = monk.data_select("schema")
        if result.success and isinstance(result.data, list):
            self.existing_schemas = result.data
            
            # Populate template dropdown with "Start from scratch" + existing schemas
            try:
                template_select = self.query_one("#template_source", Select)
                
                # Start with "Start from scratch" option
                options = [("scratch", "Start from scratch")]
                
                # Add existing schemas that can be cloned
                for schema in self.existing_schemas:
                    if schema.get("status") in ["active", "system"]:
                        name = schema.get("name", "unknown")
                        display_name = f"Clone: {name}"
                        options.append((name, display_name))
                
                template_select.set_options(options)
            except:
                pass


    def action_back_to_lab(self) -> None:
        """Return to schema laboratory"""
        self.app.pop_screen()

    def action_save_schema(self) -> None:
        """Save schema (create or update)"""
        # Collect form data
        try:
            schema_name = self.query_one("#schema_name", Input).value.strip()
            description = self.query_one("#schema_description", Input).value.strip()
            table_name = self.query_one("#table_name", Input).value.strip()
            status = self.query_one("#schema_status", Select).value
            
            # Validation
            if not schema_name:
                self.status_update("⚠ Schema name is required")
                return
                
            if not description:
                self.status_update("⚠ Description is required")
                return
            
            # Auto-generate table name if empty
            if not table_name:
                table_name = schema_name.lower().replace(" ", "_").replace("-", "_")
            
            # Build schema definition
            schema_definition = {
                "type": "object",
                "title": schema_name.title(),
                "description": description,
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
            
            # Prepare schema data for monk CLI
            schema_payload = {
                "name": schema_name,
                "table_name": table_name,
                "status": status,
                "definition": schema_definition
            }
            
            self.status_update(f"{'Creating' if self.mode == 'create' else 'Updating'} schema...")
            
            # Call monk CLI
            if self.mode == "create":
                result = monk.meta_create(schema_name, schema_definition)
            else:
                result = monk.meta_update(schema_name, schema_definition)
            
            if result.success:
                self.status_update(f"✅ Schema {'created' if self.mode == 'create' else 'updated'} successfully")
                # Return to lab after brief display
                self.set_timer(2.0, lambda: self.app.pop_screen())
            else:
                error_msg = result.error or f"Schema {'creation' if self.mode == 'create' else 'update'} failed"
                self.status_update(f"❌ {error_msg}")
                
        except Exception as e:
            self.status_update(f"❌ Form error: {str(e)}")

    def action_save_draft(self) -> None:
        """Save schema as draft"""
        # Set status to pending and save
        try:
            status_select = self.query_one("#schema_status", Select)
            status_select.value = "pending"
            self.action_save_schema()
        except:
            self.status_update("❌ Could not save as draft")
    
    def action_focus_next(self) -> None:
        """Move to next form field"""
        self.screen.focus_next()
    
    def action_focus_previous(self) -> None:
        """Move to previous form field"""
        self.screen.focus_previous()