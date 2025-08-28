"""
Module Navigation Widget
"""

from textual.app import ComposeResult
from textual.containers import Grid
from textual.widget import Widget
from textual.widgets import Static

from .vault_container import VaultContainer


class ModuleNavigation(Widget):
    """Vault facility modules navigation"""
    
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
    
    .module-grid {
        grid-size: 1 6;
        margin: 1 0;
        height: 6;
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
            with Grid(classes="module-grid"):
                yield Static("[1] Department Registry    - Multi-tenant vault management", classes="module-item")
                yield Static("[2] Schema Laboratory      - Data structure management", classes="module-item")
                yield Static("[3] Population Management  - Resident record operations", classes="module-item")
                yield Static("[4] Security Protocols     - Observer system monitoring", classes="module-item") 
                yield Static("[5] File Archives         - Document management system", classes="module-item")
                yield Static("[6] Wasteland Testing     - Quality assurance environment", classes="module-item")