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

## Features

- **Authentication System**: Vault-Tec Network Access Terminal
- **Overseer Console**: Main dashboard with real-time monitoring
- **Keyboard Navigation**: Full keyboard control with Fallout-themed shortcuts
- **Vault-Tec Theming**: Authentic terminal aesthetics with radiation spectrum colors
- **Modular Architecture**: Easy to extend with new vault facility modules

## Current Status

✅ **Implemented:**
- Basic application structure
- Authentication screen with Vault-Tec styling
- Main Overseer Console dashboard
- System status panels and activity log
- Theme system with Fallout color palette

🚧 **In Progress:**
- Module navigation (Schema Lab, Population Management, etc.)
- Real Monk API integration
- WebSocket real-time updates

📋 **Planned:**
- Schema Laboratory (visual + YAML editing)
- Population Management (CRUD operations)
- Security Protocols (Observer monitoring)
- Wasteland Testing (Mad Max-themed QA environment)

## Development

The application is structured as a collection of Textual screens and widgets, with a comprehensive theming system that brings the Fallout universe to your terminal.

Each major feature corresponds to a "vault facility module" as described in the design documents in `docs/`.

## Authentication

Default test credentials:
- **Tenant:** `test-1756112139`
- **Username:** `root`
- **Password:** (any value for demo)