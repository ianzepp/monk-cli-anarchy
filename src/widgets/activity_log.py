"""
Activity Log Widget
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static
from datetime import datetime

from .vault_container import VaultContainer
from models.vault_data import vault_data


class ActivityLog(Widget):
    """Recent vault operations activity log"""
    
    CSS = """
    ActivityLog {
        width: 100%;
        height: 100%;
    }
    
    .activity-container {
        height: 100%;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        padding: 0 2;
    }
    
    .activity-entry {
        margin: 0 0;
        height: 1;
    }
    
    .activity-create {
        color: #22c55e;
    }
    
    .activity-update {
        color: #ffb000;
    }
    
    .activity-delete {
        color: #ff3030;
    }
    
    .activity-deploy {
        color: #1e3a8a;
    }
    
    .activity-info {
        color: #6b7280;
    }
    """

    def __init__(self):
        super().__init__()
        self.activity_entries = []

    def compose(self) -> ComposeResult:
        """Build the activity log"""
        with VaultContainer(title="RECENT VAULT OPERATIONS", classes="activity-container"):
            with Vertical(id="activity_list"):
                # Load initial dummy data
                initial_activities = vault_data.generate_recent_activity(5)
                for activity in initial_activities:
                    action_class = f"activity-{activity['action'].lower()}"
                    if action_class not in ["activity-create", "activity-update", "activity-delete", 
                                           "activity-deploy", "activity-info"]:
                        action_class = "activity-info"
                        
                    entry_text = f"{activity['timestamp']} | {activity['module']:8} | {activity['action']:6} | {activity['description']}"
                    yield Static(entry_text, classes=f"activity-entry {action_class}")
                    
                # Store activities for management
                self.activity_entries = [
                    {
                        "timestamp": a["timestamp"],
                        "module": a["module"],
                        "action": a["action"],
                        "description": a["description"], 
                        "text": f"{a['timestamp']} | {a['module']:8} | {a['action']:6} | {a['description']}",
                        "class": f"activity-{a['action'].lower()}" if f"activity-{a['action'].lower()}" in 
                                ["activity-create", "activity-update", "activity-delete", "activity-deploy", "activity-info"]
                                else "activity-info"
                    } for a in initial_activities
                ]

    def add_activity_entry(self, module: str, action: str, description: str):
        """Add new activity entry"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry_text = f"{timestamp} | {module:8} | {action:6} | {description}"
        
        # Determine CSS class based on action
        action_class = f"activity-{action.lower()}"
        if action_class not in ["activity-create", "activity-update", "activity-delete", 
                               "activity-deploy", "activity-info"]:
            action_class = "activity-info"
        
        # Add to internal list
        self.activity_entries.insert(0, {
            "timestamp": timestamp,
            "module": module,
            "action": action,
            "description": description,
            "text": entry_text,
            "class": action_class
        })
        
        # Keep only last 10 entries
        if len(self.activity_entries) > 10:
            self.activity_entries = self.activity_entries[:10]
            
        # Refresh display
        self.refresh_activity_display()
    
    def refresh_activity_display(self):
        """Refresh the activity log display"""
        activity_list = self.query_one("#activity_list", Vertical)
        activity_list.remove_children()
        
        for entry in self.activity_entries[:5]:  # Show last 5 entries
            activity_list.mount(Static(
                entry["text"], 
                classes=f"activity-entry {entry['class']}"
            ))