import React from 'react';
import styled from 'styled-components';
import { useKeyboardNavigation } from '../../hooks/useKeyboardNavigation';
import { KeyboardFeedback } from '../terminal/KeyboardFeedback';
import { FunctionKeyBar } from '../terminal/FunctionKeyBar';
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

const StatusInfo = styled.div`
  background: ${terminalTheme.colors.bunkerBlack};
  border: 1px solid ${terminalTheme.colors.vaultGreen};
  color: ${terminalTheme.colors.vaultGreen};
  font-family: ${terminalTheme.fonts.terminal};
  font-size: ${terminalTheme.sizes.terminalXs};
  padding: 6px 12px;
  margin: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
  
  .module-info {
    display: flex;
    gap: 8px;
    align-items: center;
    
    .current {
      color: ${terminalTheme.colors.amberAlert};
      font-weight: bold;
    }
  }
  
  .shortcuts-help {
    color: ${terminalTheme.colors.dustBrown};
    font-size: ${terminalTheme.sizes.terminalXs};
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

      {/* Top function key bar (F1-F5) */}
      <FunctionKeyBar position="top" />

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

      {/* Status info bar */}
      <StatusInfo>
        <div className="module-info">
          <span>Current Module:</span>
          <span className="current">{currentModule?.name || 'Unknown'}</span>
          <span>({currentModuleIndex + 1}/{VAULT_MODULES.length})</span>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button onClick={() => window.location.href = '/registry'} style={{ padding: '4px 8px' }}>
            Test Registry
          </button>
          <button onClick={() => window.location.href = '/schema'} style={{ padding: '4px 8px' }}>
            Test Schema
          </button>
          <button onClick={() => window.location.href = '/'} style={{ padding: '4px 8px' }}>
            Test Home
          </button>
        </div>
      </StatusInfo>

      {/* Bottom function key bar (F6-F10) */}
      <FunctionKeyBar position="bottom" />
    </ShellContainer>
  );
};