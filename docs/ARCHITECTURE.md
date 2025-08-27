# Vault-Tec Enterprise Suite - Technical Architecture

## Technology Stack

### Core Framework
- **Vite 5.2+** - Build tool and development server
- **React 18.2+** - UI framework
- **TypeScript 5.2+** - Type safety and development experience
- **Node.js 18+** - Runtime requirement

### UI & Styling
- **styled-components** - CSS-in-JS with theme support
- **framer-motion** - Animations and terminal effects
- **lucide-react** - Icon system

### State Management
- **zustand** - Lightweight global state management
- **@tanstack/react-query** - Server state and caching
- **react-hook-form** - Form state management

### Data & API
- **axios** - HTTP client for Monk API integration
- **zod** - Runtime type validation

### Development Tools
- **ESLint** - Code linting
- **TypeScript** - Static type checking
- **Vite HMR** - Hot module replacement for rapid development

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── terminal/        # Terminal-specific widgets
│   └── widgets/         # General UI widgets
├── hooks/               # Custom React hooks
├── modules/             # Main application modules (Overseer, Registry, etc.)
├── store/               # Zustand stores
├── styles/              # Theme and global styles
├── types/               # TypeScript type definitions
└── utils/               # Utility functions

docs/
├── DESIGN.md            # UI/UX design specification
└── ARCHITECTURE.md      # Technical architecture (this file)
```

## Component Architecture

### Terminal Components
- **TerminalWidget** - Base container for all terminal interfaces
- **TerminalButton** - Action buttons with variants and hotkeys
- **TerminalTable** - Data display with ASCII styling
- **TerminalForm** - Data entry with terminal aesthetics

### Module Structure
Each major UI module (Overseer Console, Schema Laboratory, etc.) is a self-contained React component with:
- Dedicated state management
- Keyboard event handling
- Terminal-specific styling
- Function key integration

## Styling System

### Theme Configuration
- **terminal-theme.ts** - Centralized color palette and design tokens
- **global-styles.ts** - Global CSS and terminal effects
- CSS custom properties for runtime theming

### Terminal Effects
- Phosphor glow using CSS text-shadow
- CRT scanlines with CSS gradients  
- Typewriter animations with CSS keyframes
- Button hover effects with box-shadow

## Development Workflow

### Quick Start
```bash
npm install
npm run dev        # Start development server
npm run build      # Production build
npm run preview    # Preview production build
```

### Development Features
- **Instant HMR** - See terminal effect changes immediately
- **TypeScript checking** - Full type safety with Monk API
- **ESLint integration** - Code quality enforcement

## Performance Considerations

### Optimization Strategies
- **react-window** for large data tables (2,847+ records)
- **Component lazy loading** for module switching
- **Efficient re-renders** with React.memo and useMemo
- **Bundle optimization** with Vite's tree shaking

### Terminal-Specific Performance
- CSS transforms for smooth animations
- Hardware acceleration for glow effects
- Debounced keyboard event handling
- Optimized ASCII art rendering

## Integration Points

### Monk API Integration
- **Type-safe API client** with TypeScript interfaces
- **React Query** for caching and real-time updates
- **WebSocket support** for observer pipeline monitoring
- **Multi-tenant context** switching

### Keyboard Interface
- **Global hotkey handling** with React hooks
- **Function key mapping** (F1-F12) for terminal authenticity  
- **Sequential command support** (Ctrl+V then 1-9)
- **Context-sensitive shortcuts** per module

## Future Enhancements

### Phase 2 Features
- **WebSocket integration** for real-time observer monitoring
- **Advanced animations** with framer-motion
- **Sound effects** using Web Audio API
- **Accessibility improvements** with ARIA labels

### Performance Upgrades
- **Service Worker** for offline mode
- **Code splitting** by module
- **Advanced caching** strategies
- **Bundle analysis** and optimization

## Development Philosophy

This architecture prioritizes:
1. **Rapid iteration** - Fast HMR for creative terminal UI development
2. **Type safety** - Full TypeScript integration with Monk API
3. **Component reusability** - Terminal widgets across modules
4. **Performance** - Smooth animations and large dataset handling
5. **Maintainability** - Clear separation of concerns and modular structure

The result is a robust foundation for building the Vault-Tec Enterprise Suite with both creative freedom and technical reliability.