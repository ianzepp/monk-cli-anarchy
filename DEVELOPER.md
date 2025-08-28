# MONK CLI ANARCHY - Developer Guide

*"Rebelling against boring command-line interfaces since 2287"*

## Technical Overview

monk-cli-anarchy is a comprehensive terminal user interface for monk-cli operations built with Python Textual, implementing enterprise-grade navigation patterns and a Fallout-themed aesthetic. The project provides a visual frontend for all monk-cli commands while maintaining professional database operation capabilities.

## Architecture

### **Core Framework: BaseVaultScreen**

All vault facility modules inherit from `BaseVaultScreen` which provides:

**3-Row Layout Structure:**
1. **Header Row (2 lines)**: Dynamic authentication context + live status messages
2. **Content Window**: Main workspace for module-specific functionality  
3. **Footer Row**: Standard Textual footer with automatic keybinding display

**Child Class Implementation:**
```python
class MyScreen(BaseVaultScreen):
    def compose_content(self) -> ComposeResult:
        # Define only the main content area
        yield MyWidgets()
    
    def compose_status(self) -> str:
        # Define default status message
        return "Ready for operations"
        
    # Use self.status_update("message") for runtime feedback
```

### **Universal Killbox Notation**

**Killbox Pattern `[key]`:**
- **Universal principle**: Anything in brackets interrupts current flow
- **Global killboxes**: `[?]` AI Assistant, `[q]` Quit (with confirmation)
- **Standard CRUD**: `[f]` Find, `[c]` Create, `[d]` Delete, `[u]` Update
- **Selection**: `[1-9]` Item selection, `[ESC]` Back navigation

**Navigation Rules:**
- **Buttons**: Horizontal left/right arrow navigation, no looping at boundaries
- **Forms**: Vertical up/down between inputs, Enter submits
- **Tables**: Up/down scrolling, Enter selects, `[u][d]` actions on selected row
- **Complex layouts**: Tab switches between sections, each maintains independent navigation

### **Data Integration Architecture**

**monk-cli Subprocess Integration:**
```python
# Centralized monk command execution
from api.monk_client import monk

# Server operations
result = monk.server_list()  # Calls "monk server list --json"
result = monk.server_use("local")  # Calls "monk server use local"

# Tenant operations  
result = monk.tenant_list()  # Calls "monk tenant list --json" (server-scoped)
result = monk.tenant_use("test-vault")  # Calls "monk tenant use test-vault"

# Authentication operations
result = monk.auth_login("tenant", "user", "pass")  # Calls "monk auth login"
result = monk.auth_status()  # Calls "monk auth status --json"
result = monk.auth_expires()  # Calls "monk auth expires" (raw timestamp)
```

**Configuration Management:**
```python
# Environment variable configuration
MONK_EXECUTABLE="/path/to/monk"  # Development vs production monk binary
OVERSEER_ALWAYS=true             # Auto-authentication for development
```

## Screen Development Patterns

### **Authentication Flow**

**Three-Step Process:**
1. **Server Selection**: Choose vault facility connection
2. **Tenant Selection**: Choose database (server-scoped)
3. **Session Selection**: Authentication with existing session detection

**Implementation Pattern:**
- Each step uses BaseVaultScreen inheritance
- DataTable with killbox notation for selection lists
- Automatic progression through authentication workflow
- Real monk-cli integration with proper error handling

### **DataTable Pattern**

**Standard Table Setup:**
```python
# In compose_content()
table = DataTable(id="my_table", classes="data-list")
table.add_columns("", "NAME", "STATUS", "OTHER_FIELDS")
table.show_header = False
table.cursor_type = "row"
table.can_focus = True
yield table

# Event handling for ENTER key
def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
    if event.data_table.id == "my_table":
        row_index = event.cursor_row
        if 0 <= row_index < len(self.data_items):
            self.handle_selection(row_index)

# Population with killbox notation
def populate_table(self) -> None:
    table = self.query_one("#my_table", DataTable)
    table.clear()
    
    for i, item in enumerate(self.data_items[:9]):
        killbox = f"[{i+1}]"
        table.add_row(killbox, item["name"], item["status"], ...)
```

### **Status Management**

**BaseVaultScreen provides:**
```python
# Runtime status updates (appears in header)
self.status_update("Processing request...")
self.status_clear()  # Reset to default message

# Override default status in child class
def compose_status(self) -> str:
    return "Default status for this screen"
```

### **AI Assistant Integration**

**Global AI Assistant (`?` key):**
- **Natural language processing**: "What are my servers?" → Navigation guidance
- **Intent recognition**: Converts questions to module navigation and filtering
- **Filter building**: English to Filter DSL conversion for database queries
- **Context awareness**: Provides relevant suggestions based on current screen

## User Interface Patterns

### **Form Interaction Rules**

**Simple Forms:**
- Vertical up/down navigation between inputs
- Enter submits form
- ESC cancels and returns to previous screen

**Complex Forms:**
- Side-by-side layout in content window
- Tab switches focus between form sections
- Each section maintains independent up/down navigation

### **Modal Dialog Strategy**

**Simple Confirmations:**
- Dialog within content window for basic yes/no operations
- Example: Delete record confirmation

**Complex Operations:**
- Full 3-row screen for multi-step processes
- Example: Tenant deletion requiring re-authentication

### **Responsive Design**

**Priority Order for Narrow Terminals:**
1. **Server/tenant context**: Always preserved (most critical)
2. **Time display**: Removed first on space constraints
3. **Global killboxes**: Progressive shortening (`[?] AI Assistant` → `[?]`)
4. **Local killboxes**: Text reduction (`[c] Create Tenant` → `[c] Create` → `[c]`)

## Development Workflow

### **Project Structure**

```
monk-cli-anarchy/
├── docs/                    # Original design documentation
├── src/
│   ├── screens/            
│   │   ├── base_screen.py   # Foundation class for all screens
│   │   ├── welcome_screen.py # Entry point with 3-row layout demo
│   │   ├── *_selection_screen.py # Authentication flow screens
│   │   └── *_management_screen.py # Vault facility modules
│   ├── widgets/
│   │   ├── vault_container.py # Styled container components
│   │   └── killbox_table.py  # Reusable table component (experimental)
│   ├── theme/
│   │   └── vault_theme.py    # Global CSS with 3-row layout framework
│   ├── api/
│   │   └── monk_client.py    # monk-cli subprocess integration
│   ├── utils/
│   │   ├── session_timer.py  # JWT expiration countdown utilities
│   │   └── key_conventions.py # Standard keybinding definitions
│   └── models/
│       └── vault_data.py     # Mock data generators for development
├── main.py                  # Application entry point
├── run.sh                   # Launch script with environment setup
└── requirements.txt         # Python dependencies
```

### **Adding New Vault Facility Modules**

**Step 1: Inherit BaseVaultScreen**
```python
from screens.base_screen import BaseVaultScreen

class NewModuleScreen(BaseVaultScreen):
    """New vault facility module"""
```

**Step 2: Define Content**
```python
def compose_content(self) -> ComposeResult:
    with Vertical():
        yield Label("Module Title", classes="amber-alert-text")
        # Add your module content
        yield MyDataTable()
        
def compose_status(self) -> str:
    return "Ready for module operations"
```

**Step 3: Add Navigation**
```python
BINDINGS = BaseVaultScreen.BINDINGS + [
    Binding("f", "find_records", "Find", show=True),
    Binding("c", "create_record", "Create", show=True),
    # Add module-specific bindings
]
```

### **Testing & Validation**

**Syntax Checking:**
```bash
# Check files being modified
python3 -m py_compile src/screens/modified_file.py

# Full project check (when ready)
python3 -m compileall src/
```

**Mock Data Testing:**
- Use `vault_data.py` generators for realistic test data
- Configure monk-cli with test servers and tenants
- Test authentication flow with existing session detection

## Styling & Theming

### **Global CSS Framework**

**3-Row Layout Classes (theme/vault_theme.py):**
```css
.header-row      /* Header: title + status lines */
.content-window  /* Main workspace with padding */
.killbox-row     /* Footer area for killboxes */
```

**Utility Color Classes:**
```css
.vault-green-text    /* Primary text color */
.amber-alert-text    /* Warning/attention color */
.steel-blue-text     /* Secondary information */
.healthy-green-text  /* Success/operational status */
.offline-gray-text   /* Disabled/inactive elements */
```

**Background Utilities:**
```css
.bg-black        /* Primary background */
.bg-gray         /* Secondary backgrounds */
.bg-transparent  /* No background */
```

### **Color Palette: "Radiation Spectrum"**

**Primary Colors:**
- `$vault-green: #00ff00` - Primary UI elements
- `$amber-alert: #ffb000` - Warnings and attention states  
- `$steel-blue: #1e3a8a` - Secondary actions

**Background Tones:**
- `$bunker-black: #0a0a0a` - Primary background
- `$shadow-gray: #1a1a1a` - Secondary backgrounds

**Status Colors:**
- `$healthy-green: #22c55e` - Success states
- `$caution-yellow: #f59e0b` - Warning states
- `$danger-red: #dc2626` - Error states

## Implementation Guidelines

### **Design Language Compliance**

**Layout Requirements:**
- All screens must inherit BaseVaultScreen
- Content area gets automatic 1-character padding for alignment
- Status messages appear in header (more visible than bottom)
- Footer shows context-appropriate killboxes automatically

**Navigation Standards:**
- F/C/D/U pattern for all CRUD operations
- [1-9] for item selection in lists
- ESC for back navigation, Enter for default action
- Arrow keys for table/button navigation within content areas

### **Error Handling**

**monk-cli Integration:**
- Graceful fallbacks when monk commands fail
- Proper error messages with vault theming ("Overseer resource list not found!")
- Status updates during long-running operations
- Timeout handling for network operations

**User Experience:**
- Clear feedback for all operations
- Confirmation screens for destructive actions
- Existing session detection and smart defaults
- Professional enterprise application behavior

### **Future Development**

**Planned Enhancements:**
- **Wasteland Testing**: Mad Max-themed QA environment module
- **Security Protocols**: Observer system monitoring with real-time metrics
- **Command Traces**: Development debugging with send/recv command display
- **Enhanced Tables**: Utility functions to reduce DataTable setup duplication

**Extension Points:**
- Additional vault facility modules following established patterns
- Enhanced AI assistant with more sophisticated natural language processing
- Real-time WebSocket updates for live vault monitoring
- Advanced filter builder with visual query construction

---

**This guide provides complete technical foundation for extending and maintaining the monk-cli-anarchy terminal interface.**