"""
OVERSEER CONSOLE MODULE
Main Dashboard Interface Implementation
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static, Select
from textual.timer import Timer

from widgets.alert_panel import AlertPanel
from widgets.activity_log import ActivityLog
from widgets.module_navigation import ModuleNavigation
from models.vault_data import vault_data
from api.monk_client import monk
from utils.session_timer import SessionTimer
import random


class OverseerScreen(Screen):
    """Overseer Console - Main Dashboard"""
    
    CSS = """
    .overseer-header {
        dock: top;
        height: 3;
        background: #1a1a1a;
        color: #00ff00;
    }
    
    .status-icons {
        text-align: center;
        color: #22c55e;
        margin: 1 1 0 1;
    }
    
    .session-info {
        text-align: right;
        color: #ffb000;
        margin: 1 2 0 0;
    }
    
    .user-info {
        text-align: left;
        color: #00ff00;
        text-style: bold;
        margin: 1 0 0 2;
        width: auto;
    }
    
    .session-dropdown {
        width: 30;
        margin: 1 1;
    }
    
    .dashboard-panels {
        height: 8;
        margin: 1 2;
    }
    
    ActivityLog {
        height: 12;
        margin: 1 2;
    }
    
    ModuleNavigation {
        height: 8;
        margin: 1 2;
    }
    
    .command-bar {
        dock: bottom;
        height: 3;
        background: #1a1a1a;
    }
    
    .command-hint {
        text-align: center;
        color: #ffb000;
        margin: 1;
    }
    """
    
    BINDINGS = [
        Binding("1", "module_1", "[1]", show=True),
        Binding("2", "module_2", "[2]", show=True), 
        Binding("3", "module_3", "[3]", show=True),
        Binding("4", "module_4", "[4]", show=True),
        Binding("5", "module_5", "[5]", show=True),
        Binding("6", "module_6", "[6]", show=True),
        Binding("v", "switch_vault", "[v] Switch", show=True),
        Binding("r", "refresh", "Refresh", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.refresh_timer = None
        self.session_timer = None

    def compose(self) -> ComposeResult:
        """Build the overseer console interface"""
        # Header with user info, population stats, and session
        with Container(classes="overseer-header"):
            yield Label("👑 Loading... | # 0/0/0 | ● API ● DB ● SEC | Session: Initializing... | V=Switch", id="user_info_label")
        
        # Module navigation (moved to top)
        yield ModuleNavigation()
            
        # Main dashboard panels (removed system status and population)
        with Horizontal(classes="dashboard-panels"):
            yield AlertPanel()
            
        # Activity log
        yield ActivityLog()
            
        # Command hints
        with Container(classes="command-bar"):
            yield Static(
                "Keys: 1-6=Modules | Enter=Execute | H=Help | S=Search | R=Refresh | Q=Quit",
                classes="command-hint"
            )
            
        yield Footer()

    def on_mount(self) -> None:
        """Start refresh timer and initial data load"""
        self.start_refresh_timer()
        self.refresh_dashboard()
        self.update_auth_context()
        
    def on_unmount(self) -> None:
        """Clean up timers when screen is removed"""
        if self.refresh_timer:
            self.refresh_timer.stop()
        if self.session_timer:
            self.session_timer.stop()

    def start_refresh_timer(self) -> None:
        """Start automatic dashboard refresh and session countdown"""
        self.refresh_timer = self.set_interval(30, self.refresh_dashboard)
        # Update session countdown every 10 seconds
        self.session_timer = self.set_interval(10, self.update_session_countdown)

    def refresh_dashboard(self) -> None:
        """Refresh dashboard data"""
        # Generate fresh mock data
        data = vault_data.generate_dashboard_data()
        
        # Update status icons in header
        try:
            status_icons = self.query_one("#status_icons", Label)
            # Simple status display - green dots when all good
            status_icons.update("● API ● DB ● SEC")
        except:
            pass
            
        # Update population panel  
        try:
            pop_panel = self.query_one(PopulationPanel)
            pop_panel.update_population_stats(data["population_stats"])
        except:
            pass
            
        # Update alert panel
        try:
            alert_panel = self.query_one(AlertPanel)
            alert_panel.update_alerts(data["alerts"])
        except:
            pass
            
        # Update activity log with new entries
        try:
            activity_log = self.query_one(ActivityLog)
            # Add a random new activity entry occasionally
            if random.randint(1, 10) <= 3:  # 30% chance
                recent = vault_data.generate_recent_activity(1)[0]
                activity_log.add_activity_entry(
                    recent["module"],
                    recent["action"], 
                    recent["description"]
                )
        except:
            pass

    def update_auth_context(self) -> None:
        """Update user and session info from real monk auth data"""
        try:
            # Get current auth info
            info_result = monk.auth_info()
            if info_result.success and isinstance(info_result.data, dict):
                auth_info = info_result.data
                
                tenant = auth_info.get("tenant", self.app.current_vault)
                username = auth_info.get("name", self.app.current_user)
                
                # Get live session countdown
                expires_result = monk.auth_expires()
                session_display = "Session: Loading..."
                if expires_result.success:
                    session_display = SessionTimer.get_session_display(expires_result.data)
                
                # Get population stats for header
                pop_data = vault_data.generate_population_stats()
                total = pop_data.get("total", 0)
                active = pop_data.get("active", 0) 
                offline = pop_data.get("offline", 0)
                
                # Get access level icon from JWT
                access_level = auth_info.get("access", "read")
                access_icons = {
                    "root": "👑",    # Crown for root access
                    "full": "🔓",    # Unlocked for full access  
                    "edit": "✏️",     # Pencil for edit access
                    "read": "👁️",     # Eye for read-only access
                }
                access_icon = access_icons.get(access_level, "❓")
                
                # Build header with access icon and population stats
                header_text = f"{access_icon} {username}@{tenant} | # {total}/{active}/{offline} | ● API ● DB ● SEC | {session_display} | V=Switch"
                user_label = self.query_one("#user_info_label", Label)
                user_label.update(header_text)
                
                # Update app context with real data
                self.app.current_user = username
                self.app.current_vault = tenant
                
        except Exception as e:
            # Fallback to existing app data
            pass
            
    def update_session_countdown(self) -> None:
        """Update the live session countdown"""
        try:
            expires_result = monk.auth_expires()
            session_display = "Session: Loading..."
            if expires_result.success:
                session_display = SessionTimer.get_session_display(expires_result.data)
            
            # Get fresh population stats for countdown update
            pop_data = vault_data.generate_population_stats()
            total = pop_data.get("total", 0)
            active = pop_data.get("active", 0)
            offline = pop_data.get("offline", 0)
            
            # Get access level for icon (fallback if no auth context)
            access_icon = "👑"  # Default to root for session countdown updates
            
            # Update the combined header with population
            header_text = f"{access_icon} {self.app.current_user}@{self.app.current_vault} | # {total}/{active}/{offline} | ● API ● DB ● SEC | {session_display} | V=Switch"
            user_label = self.query_one("#user_info_label", Label)
            user_label.update(header_text)
        except Exception:
            pass

    def action_module_1(self) -> None:
        """Navigate to Department Registry"""
        from screens.department_registry_screen import DepartmentRegistryScreen
        self.app.push_screen(DepartmentRegistryScreen())
        
    def action_module_2(self) -> None:
        """Navigate to Schema Laboratory"""
        from screens.schema_lab_screen import SchemaLabScreen
        self.app.push_screen(SchemaLabScreen())
        
    def action_module_3(self) -> None:
        """Navigate to Population Management"""
        from screens.population_management_screen import PopulationManagementScreen
        self.app.push_screen(PopulationManagementScreen())
        
    def action_module_4(self) -> None:
        """Navigate to Security Protocols"""
        self.app.bell()
        # TODO: Implement navigation to security screen
        
    def action_module_5(self) -> None:
        """Navigate to File Archives"""
        self.app.bell()
        # TODO: Implement navigation to file archives screen
        
    def action_module_6(self) -> None:
        """Navigate to Wasteland Testing"""
        self.app.bell()
        # TODO: Implement navigation to wasteland testing screen

    def action_search(self) -> None:
        """Global search functionality"""
        self.app.bell()
        # TODO: Implement global search modal

    def action_switch_vault(self) -> None:
        """Switch vault/tenant"""
        self.app.bell()
        # TODO: Implement vault switching

    def action_refresh(self) -> None:
        """Manual refresh"""
        self.refresh_dashboard()
        self.app.bell()

    def action_command(self) -> None:
        """Enter command terminal mode"""
        self.app.bell()
        # TODO: Implement command terminal modal
        
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle session dropdown selection"""
        if event.select.id == "session_select" and event.value != "loading":
            # User selected a different server session
            selected_server = event.value
            
            # Switch to the selected server
            switch_result = monk.server_use(selected_server)
            if switch_result.success:
                # Refresh auth context after switch
                self.call_later(self.update_auth_context)
            else:
                self.app.bell()  # Error sound