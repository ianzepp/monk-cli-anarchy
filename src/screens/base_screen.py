"""
BASE SCREEN CLASS
Foundation for all vault facility screens with 4-row layout
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Static
from datetime import datetime


class BaseVaultScreen(Screen):
    """Base class for all vault screens with automatic header management"""
    
    # Global killbox bindings available on all screens
    BINDINGS = [
        Binding("?", "ai_assistant", "AI Assistant", priority=True, show=True),
        Binding("q", "quit_vault", "Quit", priority=True, show=True),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vault_header = ""
        self.vault_status = "Ready"
        self.header_timer = None
        # Build initial header immediately
        self.build_vault_header()

    def compose(self) -> ComposeResult:
        """Build the standard 3-row layout"""
        # Row 1: Header (2 lines: title + status)
        with Container(classes="header-row"):
            yield Static(self.vault_header, id="vault_header_display")
            yield Static(self.vault_status, id="vault_status_display", classes="status-line")
        
        # Row 2: Content Window (to be overridden by child classes)
        with Container(classes="content-window"):
            yield from self.compose_content()
        
        # Row 3: Footer (standard Textual footer with killboxes)
        from textual.widgets import Footer
        yield Footer()

    def compose_content(self) -> ComposeResult:
        """Override this method in child classes to define content area"""
        yield Static("Override compose_content() in child class")
        
    def compose_commands(self) -> list[str]:
        """Override this method in child classes to define local killboxes"""
        return []
        
    def compose_status(self) -> str:
        """Override this method in child classes for custom status display"""
        return "Ready"

    def on_mount(self) -> None:
        """Start header updates"""
        self.build_vault_header()
        self.build_vault_status()
        self.header_timer = self.set_interval(1.0, self.update_vault_header)
        
    def on_unmount(self) -> None:
        """Clean up timer"""
        if self.header_timer:
            self.header_timer.stop()

    def build_vault_header(self) -> None:
        """Build vault header based on authentication state"""
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Check if authenticated
        if hasattr(self.app, 'authenticated') and self.app.authenticated:
            # Authenticated: server • tenant • user • time • killboxes
            server = getattr(self.app, 'current_server', 'unknown')
            tenant = getattr(self.app, 'current_vault', 'unknown') 
            user = getattr(self.app, 'current_user', 'unknown')
            self.vault_header = f"{server} • {tenant} • {user} • {current_time} • [?] [s] [q]"
        else:
            # Not authenticated: brand • time • killboxes
            self.vault_header = f"VAULT-TEC ENTERPRISE SUITE™ • {current_time} • [?] [s] [q]"

    def update_vault_header(self) -> None:
        """Update header display"""
        self.build_vault_header()
        try:
            header_display = self.query_one("#vault_header_display", Static)
            header_display.update(self.vault_header)
        except:
            pass

    def update_vault_status(self, message: str) -> None:
        """Update status row message"""
        self.vault_status = message
        try:
            status_display = self.query_one("#vault_status_display", Static)
            status_display.update(self.vault_status)
        except:
            pass

    def build_vault_commands(self) -> None:
        """Build killbox commands from child class definition"""
        commands = self.compose_commands()
        self.vault_killboxes = " ".join(commands) if commands else ""
        try:
            killbox_display = self.query_one("#vault_killbox_display", Static)
            killbox_display.update(self.vault_killboxes)
        except:
            pass
            
    def build_vault_status(self) -> None:
        """Build status from child class definition"""
        self.vault_status = self.compose_status()
        try:
            status_display = self.query_one("#vault_status_display", Static)
            status_display.update(self.vault_status)
        except:
            pass
            
    def status_update(self, text: str) -> None:
        """Update status message (for child classes)"""
        self.vault_status = text
        try:
            status_display = self.query_one("#vault_status_display", Static)
            status_display.update(self.vault_status)
        except:
            pass
            
    def status_clear(self) -> None:
        """Clear status message (for child classes)"""
        self.vault_status = self.compose_status()  # Reset to default
        try:
            status_display = self.query_one("#vault_status_display", Static)
            status_display.update(self.vault_status)
        except:
            pass

    def action_ai_assistant(self) -> None:
        """Open global AI assistant"""
        from screens.ai_assistant_screen import AIAssistantScreen
        self.app.push_screen(AIAssistantScreen())

    def action_quit_vault(self) -> None:
        """Show quit confirmation screen"""
        from screens.quit_confirmation_screen import QuitConfirmationScreen
        self.app.push_screen(QuitConfirmationScreen())