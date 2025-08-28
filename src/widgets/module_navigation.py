"""
Module Navigation Widget
"""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static

from .vault_container import VaultContainer


class ModuleNavigation(Widget):
    """Vault facility modules navigation with killbox notation"""
    
    CSS = """
    ModuleNavigation {
        width: 100%;
        height: 100%;
    }
    
    .modules-container {
        height: 100%;
        border: solid #00ff00;
        border-title-color: #ffb000;
        border-title-style: bold;
        padding: 0 2;
    }
    
    .module-list {
        margin: 1 0;
        height: auto;
    }
    
    .module-item {
        height: 1;
        color: #00ff00;
        text-style: bold;
    }
    
    .module-number {
        color: #ffb000;
        text-style: bold;
    }
    
    .module-item:hover {
        background: rgba(0, 255, 0, 0.1);
    }
    """

    def compose(self) -> ComposeResult:
        """Build the module navigation"""
        with VaultContainer(title="VAULT FACILITY MODULES", classes="modules-container"):
            with Vertical(classes="module-list"):
                yield Static("[1] Department Registry    - Server & tenant management", classes="module-item", id="module_1")
                yield Static("[2] Schema Laboratory      - Data structure design", classes="module-item", id="module_2")
                yield Static("[3] Population Management  - Resident records", classes="module-item", id="module_3")
                yield Static("[4] Security Protocols     - System monitoring", classes="module-item", id="module_4") 
                yield Static("[5] File Archives         - Document storage", classes="module-item", id="module_5")
                yield Static("[6] Wasteland Testing     - QA environment", classes="module-item", id="module_6")