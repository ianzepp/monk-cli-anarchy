import styled, { createGlobalStyle, keyframes } from 'styled-components';
import { terminalTheme } from './terminal-theme';

// Terminal flicker animation
const flicker = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
`;

// Typewriter animation
const typewriter = keyframes`
  from { width: 0; }
  to { width: 100%; }
`;

// Global styles for Vault-Tec terminal interface
export const GlobalTerminalStyles = createGlobalStyle`
  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    padding: 0;
    background: ${terminalTheme.colors.bunkerBlack};
    color: ${terminalTheme.colors.vaultGreen};
    font-family: ${terminalTheme.fonts.terminal};
    font-size: ${terminalTheme.sizes.terminalMd};
    line-height: 1.4;
    overflow-x: hidden;
    
    /* CRT screen effect */
    background-image: ${terminalTheme.effects.scanlines};
    
    /* Prevent text selection highlighting */
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }

  #root {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  /* Terminal text effects */
  .text-glow {
    text-shadow: ${terminalTheme.effects.terminalGlow};
  }

  .text-flicker {
    animation: ${flicker} 0.15s infinite linear;
  }

  .text-typewriter {
    overflow: hidden;
    border-right: 2px solid ${terminalTheme.colors.vaultGreen};
    white-space: nowrap;
    animation: ${typewriter} 2s steps(40) forwards;
  }

  /* Terminal cursor */
  .cursor {
    display: inline-block;
    background-color: ${terminalTheme.colors.vaultGreen};
    animation: ${flicker} 1s infinite;
    width: 8px;
    height: 16px;
    margin-left: 2px;
  }

  /* Accessibility */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  /* Focus styles for keyboard navigation */
  *:focus {
    outline: 2px solid ${terminalTheme.colors.vaultGreen};
    outline-offset: 2px;
  }

  /* Scrollbars */
  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: ${terminalTheme.colors.shadowGray};
  }

  ::-webkit-scrollbar-thumb {
    background: ${terminalTheme.colors.vaultGreen};
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: ${terminalTheme.colors.healthyGreen};
  }
`;

// Base terminal container
export const TerminalContainer = styled.div`
  background: ${terminalTheme.colors.bunkerBlack};
  border: 1px solid ${terminalTheme.colors.vaultGreen};
  color: ${terminalTheme.colors.vaultGreen};
  font-family: ${terminalTheme.fonts.terminal};
  text-shadow: ${terminalTheme.effects.terminalGlow};
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: ${terminalTheme.effects.scanlines};
    pointer-events: none;
    z-index: 1;
  }
  
  & > * {
    position: relative;
    z-index: 2;
  }
`;