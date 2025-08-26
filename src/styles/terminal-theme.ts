// Vault-Tec Terminal Theme Configuration
export const terminalTheme = {
  colors: {
    // Primary Colors
    vaultGreen: '#00ff00',
    amberAlert: '#ffb000', 
    radRed: '#ff3030',
    steelBlue: '#1e3a8a',
    
    // Background Tones
    bunkerBlack: '#0a0a0a',
    shadowGray: '#1a1a1a',
    dustBrown: '#4a3c2a',
    
    // Status Colors
    healthyGreen: '#22c55e',
    cautionYellow: '#f59e0b',
    dangerRed: '#dc2626',
    offlineGray: '#6b7280',
  },
  
  fonts: {
    terminal: "'Courier New', 'Consolas', 'Monaco', monospace",
  },
  
  sizes: {
    terminalXl: '24px',
    terminalLg: '18px', 
    terminalMd: '14px',
    terminalSm: '12px',
    terminalXs: '10px',
  },
  
  effects: {
    terminalGlow: '0 0 10px currentColor',
    screenFlicker: 'flicker 0.15s infinite linear',
    scanlines: `repeating-linear-gradient(
      0deg, 
      transparent, 
      transparent 2px, 
      rgba(0, 255, 0, 0.03) 2px, 
      rgba(0, 255, 0, 0.03) 4px
    )`,
  },
  
  ascii: {
    borders: '┌─┐│└─┘├┤┬┴┼',
    bullets: '●○◉◐◑◒◓◔◕',
    arrows: '▶◀▲▼',
  },
} as const;

// CSS Custom Properties for runtime theming
export const terminalCSSVars = {
  '--vault-green': terminalTheme.colors.vaultGreen,
  '--amber-alert': terminalTheme.colors.amberAlert,
  '--rad-red': terminalTheme.colors.radRed,
  '--steel-blue': terminalTheme.colors.steelBlue,
  '--bunker-black': terminalTheme.colors.bunkerBlack,
  '--shadow-gray': terminalTheme.colors.shadowGray,
  '--dust-brown': terminalTheme.colors.dustBrown,
  '--healthy-green': terminalTheme.colors.healthyGreen,
  '--caution-yellow': terminalTheme.colors.cautionYellow,
  '--danger-red': terminalTheme.colors.dangerRed,
  '--offline-gray': terminalTheme.colors.offlineGray,
  '--terminal-font': terminalTheme.fonts.terminal,
  '--terminal-glow': terminalTheme.effects.terminalGlow,
} as const;