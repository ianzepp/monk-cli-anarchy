import React from 'react';
import styled from 'styled-components';
import { terminalTheme } from '../../styles/terminal-theme';

interface FunctionKeyBarProps {
  position: 'top' | 'bottom';
}

const KeyBarContainer = styled.div<{ $position: 'top' | 'bottom' }>`
  display: flex;
  align-items: center;
  background: ${terminalTheme.colors.shadowGray};
  border-${props => props.$position}: 1px solid ${terminalTheme.colors.vaultGreen};
  color: ${terminalTheme.colors.vaultGreen};
  font-family: ${terminalTheme.fonts.terminal};
  font-size: ${terminalTheme.sizes.terminalXs};
  padding: 6px 12px;
  gap: 8px;
  flex-shrink: 0;
  overflow: hidden;
  
  /* Terminal glow effect */
  box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.1);
`;

const CtrlPrefix = styled.div`
  color: ${terminalTheme.colors.amberAlert};
  font-weight: bold;
  margin-right: 8px;
  flex-shrink: 0;
`;

const KeyGroup = styled.div`
  display: flex;
  flex: 1;
  justify-content: space-evenly;
  align-items: center;
  gap: 4px;
  min-width: 0;
`;

const FunctionKey = styled.div`
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 0;
  flex: 1;
  justify-content: center;
  
  .key {
    background: ${terminalTheme.colors.bunkerBlack};
    border: 1px solid ${terminalTheme.colors.vaultGreen};
    padding: 2px 6px;
    border-radius: 2px;
    font-weight: bold;
    color: ${terminalTheme.colors.vaultGreen};
    text-shadow: ${terminalTheme.effects.terminalGlow};
    min-width: 20px;
    text-align: center;
    flex-shrink: 0;
  }
  
  .label {
    color: ${terminalTheme.colors.vaultGreen};
    text-transform: uppercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: ${terminalTheme.sizes.terminalXs};
  }
  
  &:hover .key {
    box-shadow: 0 0 8px ${terminalTheme.colors.vaultGreen};
  }
`;

export const FunctionKeyBar: React.FC<FunctionKeyBarProps> = ({ position }) => {
  const topKeys = [
    { key: '`', label: 'Next Module' },
    { key: '~', label: 'Prev Module' },  
    { key: 'Alt+1', label: 'Overseer' },
    { key: 'ESC', label: 'Home' },
    { key: 'Ctrl+G', label: 'Go To' },
  ];

  const bottomKeys = [
    { key: 'Ctrl+F3', label: 'Next Module ✓' },
    { key: 'Browser Limits', label: 'Most Ctrl+F* Broken' },
    { key: 'Use Primary', label: 'Backtick & Tilde' },
    { key: 'Alt+1 Works', label: 'Home Only' },
    { key: 'ESC Always', label: 'Safe Return' },
  ];

  const keys = position === 'top' ? topKeys : bottomKeys;

  return (
    <KeyBarContainer $position={position}>
      <CtrlPrefix>KEYS:</CtrlPrefix>
      
      <KeyGroup>
        {keys.map(({ key, label }) => (
          <FunctionKey key={key}>
            <div className="key">{key}</div>
            <div className="label">{label}</div>
          </FunctionKey>
        ))}
      </KeyGroup>
    </KeyBarContainer>
  );
};