// Navigation and module types for Vault-Tec Enterprise Suite

export interface VaultModule {
  id: string;
  name: string;
  path: string;
  title: string;
  description: string;
  hotkey: number; // Alt + number shortcut
  functionKey?: string; // F-key shortcut
}

export const VAULT_MODULES: VaultModule[] = [
  {
    id: 'overseer',
    name: 'Overseer Console',
    path: '/',
    title: 'OVERSEER CONSOLE',
    description: 'System dashboard and vault overview',
    hotkey: 1,
    functionKey: 'Home'
  },
  {
    id: 'registry',
    name: 'Department Registry', 
    path: '/registry',
    title: 'DEPARTMENT REGISTRY',
    description: 'Multi-tenant vault network management',
    hotkey: 2
  },
  {
    id: 'schema',
    name: 'Schema Laboratory',
    path: '/schema', 
    title: 'SCHEMA LABORATORY',
    description: 'Research & development of data schemas',
    hotkey: 3
  },
  {
    id: 'population',
    name: 'Population Management',
    path: '/population',
    title: 'POPULATION MANAGEMENT', 
    description: 'Resident records and data management',
    hotkey: 4
  },
  {
    id: 'security',
    name: 'Security Protocols',
    path: '/security',
    title: 'SECURITY PROTOCOLS',
    description: 'Observer pipeline monitoring and configuration',
    hotkey: 5
  },
  {
    id: 'files',
    name: 'File Archives',
    path: '/files',
    title: 'FILE ARCHIVES',
    description: 'Data archive and file transfer protocols', 
    hotkey: 6
  }
];

export interface NavigationState {
  currentModule: string;
  breadcrumbs: string[];
  history: string[];
}

export interface KeyboardShortcut {
  key: string;
  ctrlKey?: boolean;
  altKey?: boolean;
  shiftKey?: boolean;
  action: string;
  description: string;
  context?: string; // Which module/context this applies to
}

// Primary shortcuts - these work reliably in ALL browsers
export const GLOBAL_SHORTCUTS: KeyboardShortcut[] = [
  // Tab key for module cycling (like Alt+Tab)
  { key: 'Tab', ctrlKey: true, action: 'module-cycle', description: 'Cycle through modules' },
  
  // Number keys for direct access
  { key: '1', ctrlKey: true, action: 'navigate-overseer', description: 'Overseer Console' },
  { key: '2', ctrlKey: true, action: 'navigate-registry', description: 'Department Registry' },
  { key: '3', ctrlKey: true, action: 'navigate-schema', description: 'Schema Laboratory' },
  { key: '4', ctrlKey: true, action: 'navigate-population', description: 'Population Management' },
  { key: '5', ctrlKey: true, action: 'navigate-security', description: 'Security Protocols' },
  { key: '6', ctrlKey: true, action: 'navigate-files', description: 'File Archives' },
  
  // Other reliable shortcuts
  { key: 'h', ctrlKey: true, action: 'help', description: 'Help system' },
  { key: 'r', ctrlKey: true, action: 'refresh', description: 'Refresh' },
  { key: 't', ctrlKey: true, action: 'terminal', description: 'Command terminal' },
  { key: '`', ctrlKey: true, action: 'terminal-alt', description: 'Command terminal (alt)' },
];

// Fallback function key mappings (best effort)
export const FUNCTION_KEY_SHORTCUTS: KeyboardShortcut[] = [
  { key: 'F1', action: 'help', description: 'Help (may not work in Firefox)' },
  { key: 'F2', action: 'search', description: 'Global search' },
  { key: 'F3', action: 'module-cycle', description: 'Cycle modules' },
  { key: 'F4', action: 'execute', description: 'Execute action' },
  { key: 'F6', action: 'save', description: 'Quick save' },
  { key: 'F7', action: 'filter', description: 'Toggle filters' },
  { key: 'F8', action: 'observer-status', description: 'Observer status' },
  { key: 'F9', action: 'terminal', description: 'Command terminal' },
  { key: 'F10', action: 'emergency', description: 'Emergency' },
  { key: 'F12', action: 'diagnostics', description: 'Diagnostics' }
];

// Alt + Number shortcuts for direct module access
export const MODULE_SHORTCUTS: KeyboardShortcut[] = VAULT_MODULES.map(module => ({
  key: module.hotkey.toString(),
  altKey: true,
  action: `navigate-${module.id}`,
  description: `Jump to ${module.name}`,
  context: 'global'
}));