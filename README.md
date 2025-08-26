# Vault-Tec Enterprise Suite™

*"Building Tomorrow's Business Solutions... Yesterday's Way"*

A post-apocalyptic frontend for the Monk API, combining enterprise functionality with authentic Fallout terminal aesthetics.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 📱 Navigation

### Available Routes

- `/` - Overseer Console (Dashboard)
- `/registry` - Department Registry (Vault Management)
- `/schema` - Schema Laboratory (Meta API)
- `/population` - Population Management (Data API)
- `/security` - Security Protocols (Observer System)
- `/files` - File Archives (FTP Middleware)

### Keyboard Navigation (Coming Soon)

- **F3** - Cycle through modules
- **Alt+1-6** - Jump directly to specific modules
- **F1** - Help system
- **F9** - Command terminal mode

## 🎨 Features

### Current (Phase 1-2)
- ✅ React + TypeScript + Vite setup
- ✅ Terminal UI component system
- ✅ Fallout-inspired color scheme and typography
- ✅ Full-width responsive layout
- ✅ React Router navigation between 6 main modules
- ✅ Vault-themed 404 error pages

### Coming Soon (Phase 3-4)
- 🔄 Global keyboard shortcuts (F1-F12)
- 🔄 Real-time status bar with function key display
- 🔄 Monk API integration
- 🔄 Advanced filtering and search
- 🔄 Multi-tenant vault switching

## 🏗️ Architecture

- **Framework**: Vite + React 18 + TypeScript
- **Styling**: Styled Components with terminal theme
- **Routing**: React Router 6 with module-based organization
- **State**: Zustand (planned) + React Query (planned)
- **UI**: Custom terminal widget system

## 📁 Project Structure

```
src/
├── components/terminal/     # Terminal UI widgets
├── modules/                # Main application screens
├── router/                 # Route configuration
├── styles/                 # Theme and global styles
├── types/                  # TypeScript definitions
└── utils/                  # Utility functions
```

## 🎯 Development Status

**Current Phase**: Navigation System (Phase 2)
- ✅ React Router setup complete
- 🔄 Working on keyboard shortcuts
- 🔄 Status bar implementation
- 🔄 Breadcrumb navigation

**Next Phase**: Core Module Implementation (Phase 3)

## 🎮 Terminal Experience

The interface simulates a pre-war corporate terminal system with:
- Phosphor green CRT styling with glow effects
- ASCII art borders and layout elements
- Monospace typography throughout
- Authentic Fallout-inspired terminology
- Keyboard-heavy interaction model

## 📋 Documentation

- [Design Specification](docs/DESIGN.md) - Complete UI/UX design system
- [Architecture Guide](docs/ARCHITECTURE.md) - Technical implementation details

---

**VAULT-TEC ENTERPRISES: PREPARED FOR THE FUTURE™**