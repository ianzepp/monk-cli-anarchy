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

export const GLOBAL_SHORTCUTS: KeyboardShortcut[] = [
  { key: 'F1', action: 'help', description: 'Context-sensitive help' },
  { key: 'F2', action: 'search', description: 'Global search' },
  { key: 'F3', action: 'module-cycle', description: 'Cycle through modules' },
  { key: 'F4', action: 'execute', description: 'Execute selected action' },
  { key: 'F5', action: 'refresh', description: 'Refresh current view' },
  { key: 'F6', action: 'save', description: 'Quick save' },
  { key: 'F7', action: 'filter', description: 'Toggle filters' },
  { key: 'F8', action: 'observer-status', description: 'Observer status overlay' },
  { key: 'F9', action: 'terminal', description: 'Command terminal mode' },
  { key: 'F10', action: 'emergency', description: 'Emergency protocols' },
  { key: 'F11', action: 'fullscreen', description: 'Toggle fullscreen' },
  { key: 'F12', action: 'diagnostics', description: 'System diagnostics' }
];

// Alt + Number shortcuts for direct module access
export const MODULE_SHORTCUTS: KeyboardShortcut[] = VAULT_MODULES.map(module => ({
  key: module.hotkey.toString(),
  altKey: true,
  action: `navigate-${module.id}`,
  description: `Jump to ${module.name}`,
  context: 'global'
}));