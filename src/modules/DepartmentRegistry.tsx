import React from 'react';
import styled from 'styled-components';
import { TerminalWidget } from '../components/terminal/TerminalWidget';
import { TerminalButton } from '../components/terminal/TerminalButton';
import { terminalTheme } from '../styles/terminal-theme';

const RegistryContainer = styled.div`
  padding: 0;
  margin: 0;
  width: 100vw;
  min-height: 100vh;
  background: ${terminalTheme.colors.bunkerBlack};
  box-sizing: border-box;
`;

const ModuleHeader = styled.div`
  text-align: center;
  margin: 20px;
  margin-bottom: 20px;
  padding: 20px;
  border: 2px solid ${terminalTheme.colors.vaultGreen};
  background: ${terminalTheme.colors.shadowGray};
  
  h1 {
    font-size: ${terminalTheme.sizes.terminalXl};
    margin: 0 0 10px 0;
    text-shadow: ${terminalTheme.effects.terminalGlow};
    color: ${terminalTheme.colors.vaultGreen};
  }
  
  .subtitle {
    font-size: ${terminalTheme.sizes.terminalSm};
    opacity: 0.8;
  }
`;

export const DepartmentRegistry: React.FC = () => {
  return (
    <RegistryContainer>
      <ModuleHeader>
        <h1>┌─ VAULT NETWORK ADMINISTRATION ─┐</h1>
        <div className="subtitle">Multi-Tenant Management System</div>
      </ModuleHeader>

      <div style={{ margin: '0 20px' }}>
        <TerminalWidget title="CONNECTED VAULTS">
          <div>Status: 12 Active / 3 Offline</div>
          <br />
          <div>Current Vault: V111_CAPITAL_WASTE</div>
          <div>Overseer: admin@vault111</div>
        </TerminalWidget>

        <TerminalWidget title="VAULT REGISTRY">
          <div style={{ fontFamily: 'monospace', fontSize: '12px' }}>
            <div>┌─────────┬─────────────────┬─────────────────┬───────────┐</div>
            <div>│ ID      │ DESIGNATION     │ OVERSEER        │ STATUS    │</div>
            <div>├─────────┼─────────────────┼─────────────────┼───────────┤</div>
            <div>│ V111    │ CAPITAL_WASTE   │ admin           │ ●ONLINE   │</div>
            <div>│ V101    │ LONE_WANDERER   │ admin           │ ●ONLINE   │</div>
            <div>│ V13     │ NECROPOLIS      │ overseer_13     │ ●ONLINE   │</div>
            <div>│ V112    │ GARY_VAULT      │ gary            │ ⚠OFFLINE  │</div>
            <div>└─────────┴─────────────────┴─────────────────┴───────────┘</div>
          </div>
        </TerminalWidget>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', margin: '20px', padding: '20px' }}>
          <TerminalButton variant="primary" hotkey="F4">
            NEW VAULT
          </TerminalButton>
          <TerminalButton variant="secondary" hotkey="F5">
            CONNECT VAULT
          </TerminalButton>
          <TerminalButton variant="danger" hotkey="F10">
            EMERGENCY SHUTDOWN
          </TerminalButton>
        </div>
      </div>
    </RegistryContainer>
  );
};