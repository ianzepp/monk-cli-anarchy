import React from 'react';
import styled from 'styled-components';
import { useKeyboardNavigation } from '../../hooks/useKeyboardNavigation';
import { KeyboardFeedback } from '../terminal/KeyboardFeedback';
import { terminalTheme } from '../../styles/terminal-theme';
import { VAULT_MODULES } from '../../types/navigation';

interface VaultShellProps {
  children: React.ReactNode;
}

const ShellContainer = styled.div`
  width: 100vw;
  height: 100vh;
  background: ${terminalTheme.colors.bunkerBlack};
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

const StatusBar = styled.div`
  background: ${terminalTheme.colors.shadowGray};
  border-top: 1px solid ${terminalTheme.colors.vaultGreen};
  color: ${terminalTheme.colors.vaultGreen};
  font-family: ${terminalTheme.fonts.terminal};
  font-size: ${terminalTheme.sizes.terminalXs};
  padding: 4px 12px;
  display: flex;
  gap: 16px;
  align-items: center;
  flex-shrink: 0;
  z-index: 100;
  
  .shortcut {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    
    .key {
      background: ${terminalTheme.colors.bunkerBlack};
      border: 1px solid ${terminalTheme.colors.vaultGreen};
      padding: 2px 6px;
      border-radius: 2px;
      font-weight: bold;
    }
  }
  
  .module-info {
    margin-left: auto;
    display: flex;
    gap: 8px;
    align-items: center;
    
    .current {
      color: ${terminalTheme.colors.amberAlert};
      font-weight: bold;
    }
  }
`;

const ContentArea = styled.div`
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
`;

const ModuleIndicator = styled.div`
  position: fixed;
  top: 20px;
  right: 20px;
  background: ${terminalTheme.colors.shadowGray};
  border: 1px solid ${terminalTheme.colors.vaultGreen};
  color: ${terminalTheme.colors.vaultGreen};
  font-family: ${terminalTheme.fonts.terminal};
  font-size: ${terminalTheme.sizes.terminalXs};
  padding: 8px 12px;
  z-index: 1000;
  opacity: 0.9;
  
  .breadcrumb {
    color: ${terminalTheme.colors.amberAlert};
    font-weight: bold;
  }
`;

export const VaultShell: React.FC<VaultShellProps> = ({ children }) => {
  const { currentModule, currentModuleIndex, pressedKey } = useKeyboardNavigation();

  return (
    <ShellContainer>
      {/* Keyboard feedback overlay */}
      <KeyboardFeedback pressedKey={pressedKey} />

      {/* Module indicator in top-right */}
      <ModuleIndicator>
        <div className="breadcrumb">
          OVERSEER &gt; V111_CAPITAL &gt; {currentModule?.title || 'UNKNOWN'}
        </div>
        <div>Module {currentModuleIndex + 1} of {VAULT_MODULES.length}</div>
      </ModuleIndicator>

      {/* Main content area */}
      <ContentArea>
        {children}
      </ContentArea>

      {/* Status bar with keyboard shortcuts */}
      <StatusBar>
        <div className="shortcut">
          <span className="key">F3</span>
          <span>Next Module</span>
        </div>
        <div className="shortcut">
          <span className="key">Alt+1-6</span>
          <span>Jump to Module</span>
        </div>
        <div className="shortcut">
          <span className="key">F1</span>
          <span>Help</span>
        </div>
        <div className="shortcut">
          <span className="key">F5</span>
          <span>Refresh</span>
        </div>
        <div className="shortcut">
          <span className="key">F11</span>
          <span>Fullscreen</span>
        </div>
        
        <div className="module-info">
          <span>Current:</span>
          <span className="current">{currentModule?.name || 'Unknown'}</span>
          <span>({currentModuleIndex + 1}/{VAULT_MODULES.length})</span>
        </div>
      </StatusBar>
    </ShellContainer>
  );
};