# MONK CLI ANARCHY

*"Rebelling against boring command-line interfaces since 2287"*

**VAULT-TEC ENTERPRISE SUITE™** - A Fallout-themed terminal user interface for monk-cli, built with Python Textual.

*"Building Tomorrow's Business Solutions... Yesterday's Way"*

## Quick Start

1. **Install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   python3 -m pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   ./run.sh
   ```

## Configuration

Set environment variables to customize behavior:

```bash
# For development (point to local monk-cli build)
export MONK_EXECUTABLE="/Users/ianzepp/Workspaces/monk-cli/monk"

# For production (use global monk binary)
export MONK_EXECUTABLE="monk"

# Other configuration options
export OVERSEER_ALWAYS=true          # Auto-authenticate in dev mode
export DEFAULT_TENANT="test-1756112139"  # Default vault identifier
export DEFAULT_USERNAME="root"       # Default username
```

## Project Structure

```
monk-uix-anarchy/
├── docs/              # Design documentation
├── src/
│   ├── screens/       # Application screens (Auth, Overseer, etc.)
│   ├── widgets/       # Reusable UI components
│   ├── theme/         # Vault-Tec color scheme and styling
│   ├── api/           # Monk API client (TODO)
│   └── models/        # Data models (TODO)
├── main.py           # Application entry point
└── requirements.txt  # Python dependencies
```

## Design Language

monk-cli-anarchy implements a comprehensive UI framework designed for enterprise terminal applications with consistent navigation patterns and efficient workflows.

### **Global Layout Structure**

**4-Row Application Layout:**
1. **Header Row**: Server/tenant context (left) + time (center) + global killboxes (right)
2. **Content Window**: Massive main workspace for all operations and data display
3. **Status Row**: Success/error messages and operational feedback
4. **Killbox Row**: Context-specific command shortcuts for current screen

### **Navigation Conventions**

**Killbox Notation `[key]`:**
- **Universal principle**: Anything in brackets is a hot key that interrupts current flow
- **Global killboxes**: `[?]` AI Assistant, `[s]` Global Search, `[q]` Logout
- **Local killboxes**: `[f]` Find, `[c]` Create, `[d]` Delete, `[u]` Update
- **Module killboxes**: `[1-6]` Vault Facility Modules, `[1-9]` Item Selection

**Keyboard Interaction Rules:**
- **Buttons**: Always horizontal, left/right arrows navigate, no looping at boundaries
- **Forms**: Always vertical, up/down between inputs, Enter submits
- **Tables**: Up/down scrolling, `[u][d]` actions on selected row only
- **Complex forms**: Split content window, Tab switches focus between sides

**Form Layout Patterns:**
- **Simple forms**: Single column, vertical navigation
- **Complex forms**: Two side-by-side forms in content window with Tab switching
- **Each form**: Independent up/down navigation and left/right button control

**Table Interaction Model:**
```
┌─ DATA RESULTS ────────────────────────────────────┐
│ [u][d] │ 12345 │ John Doe     │ Engineering     │ ← Actions only on selected
│        │ 12346 │ Jane Smith   │ Sales           │   
│        │ 12347 │ Mike Johnson │ Operations      │
└────────────────────────────────────────────────────┘
```
- **Enter**: Open record in view mode (assumed, not displayed)
- **[u]**: Update/edit selected record
- **[d]**: Delete selected record with confirmation

**Modal Dialog Strategy:**
- **Simple confirmations**: Dialog within content window
- **Complex operations**: Full 4-row screen (e.g., tenant deletion with re-authentication)

**Responsive Design Priority:**
1. **Server/tenant context**: Always preserved (most critical)
2. **Time display**: Removed first on narrow terminals
3. **Global killboxes**: Shortened (`[?] AI Assistant` → `[?]`)
4. **Local killboxes**: Progressive shortening (`[c] Create Tenant` → `[c] Create` → `[c]`)

### **Implementation Benefits**

**Consistency**: Same patterns work across all vault facility modules
**Efficiency**: Muscle memory applies universally (F/C/D/U everywhere)
**Scalability**: Framework handles simple lists to complex multi-form operations
**Professional**: Enterprise-grade terminal interface design
**Intuitive**: Natural keyboard flow without mode confusion

This design language ensures every vault facility module feels familiar while maintaining the distinctive Vault-Tec aesthetic and enterprise functionality.

## Features

### **Three-Step Authentication**
- **Server Selection**: Killbox [1-9] selection from real monk CLI server registry
- **Tenant Selection**: Server-scoped tenant databases with authentication status
- **Session Selection**: Existing session detection + familiar authentication interface

### **Vault Facility Modules**
- **Department Registry**: Multi-server and tenant management with real monk CLI integration
- **Schema Laboratory**: Data structure design with JSON/YAML support
- **Population Management**: Record operations with AI-powered filtering
- **Security Protocols**: Observer system monitoring (planned)
- **File Archives**: Document management system (planned)  
- **Wasteland Testing**: QA environment with Mad Max theming (planned)

### **AI-Powered Features**
- **Global AI Assistant**: `?` key accessible from anywhere for vault operations help
- **Natural Language Queries**: "What are my servers?" → Navigation guidance
- **Filter Builder**: English to Filter DSL conversion for complex database searches
- **Intent Recognition**: Converts questions to appropriate module navigation and filtering

### **Enterprise Features**
- **Real monk-cli Integration**: Subprocess calls to monk commands with JSON parsing
- **Universal Killbox Notation**: [f/c/d/u] muscle memory across all modules
- **Session Management**: Live JWT countdown with expiration handling
- **Record Management**: Complete List → View → Edit workflow with database field editing
- **Server-Scoped Architecture**: Logical separation of infrastructure → tenants → sessions

### **Professional UI**
- **4-Row Layout**: Consistent structure across all screens
- **Vault-Tec Theming**: Authentic Fallout terminal aesthetics
- **Focus Management**: Proper button highlighting and navigation
- **Error Handling**: Graceful fallbacks when monk CLI unavailable
- **Responsive Design**: Adaptive to different terminal sizes

## Current Status

✅ **Production Ready:**
- Three-step authentication with real monk CLI integration
- Universal killbox notation and navigation patterns
- AI assistant with natural language processing
- Record management with realistic database operations
- Comprehensive design language framework

🚧 **In Development:**
- Enhanced table interactions with per-row action display
- Global search interface connecting to /api/find endpoint
- Advanced filter builder with visual condition groups

📋 **Planned Enhancements:**
- Wasteland Testing environment (Mad Max-themed QA)
- Real-time WebSocket updates for live vault monitoring
- Command trace bars for development debugging