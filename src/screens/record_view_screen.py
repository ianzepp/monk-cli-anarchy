"""
RECORD VIEW SCREEN
Read-only record display with full field information
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Static
from datetime import datetime

from widgets.vault_container import VaultContainer


class RecordViewScreen(Screen):
    """Record View - Read-only record display"""
    
    CSS = """
    .centering-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .record-container {
        width: 80;
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
    
    .field-row {
        height: 1;
        margin: 0 0;
    }
    
    .field-name {
        color: #00ff00;
        width: 20;
    }
    
    .field-value {
        color: #ffffff;
        width: 1fr;
    }
    
    .metadata-section {
        background: #1a1a1a;
        margin: 1 0;
        padding: 1;
    }
    
    .activity-section {
        background: #0a0a0a;
        margin: 1 0;
        padding: 1;
        max-height: 6;
        overflow-y: auto;
    }
    
    .action-buttons {
        height: 1;
        margin: 2 0;
        align: center middle;
    }
    """
    
    BINDINGS = [
        Binding("escape", "back_to_list", "Back", show=True),
        Binding("u", "edit_record", "Edit", show=True),
        Binding("d", "delete_record", "Delete", show=True),
    ]

    def __init__(self, schema: str, record_id: str, record_data: dict):
        super().__init__()
        self.schema = schema
        self.record_id = record_id
        self.record_data = record_data

    def compose(self) -> ComposeResult:
        """Build the record view interface"""
        with Container(classes="centering-container"):
            with Container(classes="record-container") as container:
                container.border_title = f"RECORD VIEW: {self.schema}/{self.record_id}"
                
                with Vertical():
                    # Record information section
                    yield Label("RECORD INFORMATION:", classes="section-label")
                    with Horizontal(classes="field-row"):
                        yield Label("ID:", classes="field-name")
                        yield Label(str(self.record_id), classes="field-value")
                        yield Label("Schema:", classes="field-name")
                        yield Label(self.schema, classes="field-value")
                    
                    with Horizontal(classes="field-row"):
                        yield Label("Created:", classes="field-name")
                        yield Label(self.record_data.get("created_at", "Unknown"), classes="field-value")
                        yield Label("Modified:", classes="field-name")
                        yield Label(self.record_data.get("modified_at", "Unknown"), classes="field-value")
                    
                    with Horizontal(classes="field-row"):
                        yield Label("Status:", classes="field-name")
                        yield Label(self.record_data.get("status", "unknown"), classes="field-value")
                        yield Label("Created By:", classes="field-name")
                        yield Label(self.record_data.get("created_by", "system"), classes="field-value")
                    
                    # Field data section
                    yield Label("FIELD DATA:", classes="section-label")
                    
                    # Dynamic field display based on record data
                    for field_name, field_value in self.record_data.items():
                        if field_name not in ["id", "created_at", "modified_at", "status", "created_by", "_metadata"]:
                            with Horizontal(classes="field-row"):
                                yield Label(f"{field_name}:", classes="field-name")
                                yield Label(str(field_value), classes="field-value")
                    
                    # System metadata section
                    with Container(classes="metadata-section"):
                        yield Label("SYSTEM METADATA:", classes="section-label")
                        metadata = self.record_data.get("_metadata", {})
                        
                        with Horizontal(classes="field-row"):
                            yield Label("Record Size:", classes="field-name")
                            yield Label(f"{metadata.get('size', 'Unknown')}", classes="field-value")
                            yield Label("Validation:", classes="field-name")
                            yield Label("✅ PASSED" if metadata.get("valid", True) else "❌ FAILED", classes="field-value")
                        
                        with Horizontal(classes="field-row"):
                            yield Label("Last Access:", classes="field-name")
                            yield Label(metadata.get("last_access", "Unknown"), classes="field-value")
                            yield Label("Backup Status:", classes="field-name")
                            yield Label("✅ BACKED_UP" if metadata.get("backed_up", True) else "⚠ PENDING", classes="field-value")
                    
                    # Recent activity section
                    with Container(classes="activity-section"):
                        yield Label("RECENT ACTIVITY:", classes="section-label")
                        activity_log = metadata.get("recent_activity", [])
                        
                        if activity_log:
                            for entry in activity_log[:5]:  # Show last 5 activities
                                yield Label(f"{entry.get('timestamp', 'Unknown')} | {entry.get('action', 'Unknown')}", classes="field-row")
                        else:
                            yield Label("No recent activity recorded", classes="field-row")
                    
                    # Action buttons with killbox notation
                    with Horizontal(classes="action-buttons"):
                        yield Button("[u] EDIT RECORD", variant="primary", id="edit_btn")
                        yield Button("[d] DELETE", variant="default", id="delete_btn")
                        yield Button("[ESC] BACK", variant="default", id="back_btn")

    def action_back_to_list(self) -> None:
        """Return to record list"""
        self.app.pop_screen()
        
    def action_edit_record(self) -> None:
        """Open record for editing"""
        from screens.record_edit_screen import RecordEditScreen
        self.app.push_screen(RecordEditScreen(self.schema, self.record_id, self.record_data))
        
    def action_delete_record(self) -> None:
        """Delete this record"""
        self.app.bell()
        # TODO: Implement deletion confirmation modal
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "edit_btn":
            self.action_edit_record()
        elif event.button.id == "delete_btn":
            self.action_delete_record()
        elif event.button.id == "back_btn":
            self.action_back_to_list()