"""
Vault-Tec styled container widgets
"""

from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Static


class VaultContainer(Container):
    """Container with Vault-Tec styling and optional title"""
    
    def __init__(self, title: str = None, **kwargs):
        super().__init__(**kwargs)
        if title:
            self.border_title = title
        self.add_class("vault-container")


class StatusIndicator(Static):
    """Status indicator with color coding"""
    
    def __init__(self, status: str, text: str, **kwargs):
        self.status = status
        super().__init__(text, **kwargs)
        self.update_status(status)
    
    def update_status(self, status: str):
        """Update status and apply appropriate styling"""
        self.status = status
        self.remove_class("status-ok", "status-warning", "status-error", "status-offline")
        
        if status == "ok":
            self.add_class("status-ok")
        elif status == "warning":
            self.add_class("status-warning")
        elif status == "error":
            self.add_class("status-error")
        else:
            self.add_class("status-offline")