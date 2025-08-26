import React from 'react';
import styled from 'styled-components';
import { TerminalWidget } from '../components/terminal/TerminalWidget';
import { TerminalButton } from '../components/terminal/TerminalButton';
import { terminalTheme } from '../styles/terminal-theme';

const ConsoleContainer = styled.div`
  padding: 20px;
  min-height: 100vh;
  background: ${terminalTheme.colors.bunkerBlack};
`;

const MainHeader = styled.div`
  text-align: center;
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
  
  .version {
    font-size: ${terminalTheme.sizes.terminalSm};
    opacity: 0.8;
  }
  
  .user {
    margin-top: 10px;
    font-size: ${terminalTheme.sizes.terminalSm};
    color: ${terminalTheme.colors.amberAlert};
  }
`;

const DashboardGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
`;

const StatusIndicator = styled.div<{ status: 'ok' | 'warning' | 'error' }>`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  
  &::before {
    content: '${props => {
      switch (props.status) {
        case 'ok': return '●';
        case 'warning': return '⚠';
        case 'error': return '◐';
        default: return '●';
      }
    }}';
    color: ${props => {
      switch (props.status) {
        case 'ok': return terminalTheme.colors.healthyGreen;
        case 'warning': return terminalTheme.colors.cautionYellow;
        case 'error': return terminalTheme.colors.dangerRed;
        default: return terminalTheme.colors.healthyGreen;
      }
    }};
  }
`;

const OperationsList = styled.div`
  .operation {
    display: flex;
    gap: 8px;
    margin: 4px 0;
    font-size: ${terminalTheme.sizes.terminalSm};
    
    .time {
      color: ${terminalTheme.colors.amberAlert};
      width: 80px;
    }
    
    .type {
      color: ${terminalTheme.colors.steelBlue};
      width: 100px;
      text-transform: uppercase;
    }
    
    .action {
      color: ${terminalTheme.colors.vaultGreen};
      width: 80px;
    }
    
    .details {
      color: ${terminalTheme.colors.vaultGreen};
      opacity: 0.8;
    }
  }
`;

const ActionBar = styled.div`
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 20px;
  padding: 20px;
  border-top: 1px solid ${terminalTheme.colors.vaultGreen};
`;

export const OverseerConsole: React.FC = () => {
  return (
    <ConsoleContainer>
      <MainHeader>
        <h1>┌─ VAULT-TEC ENTERPRISE SUITE v2.0.0 ─┐</h1>
        <div className="user">▼ OVERSEER: admin@vault111 ▼</div>
        <div className="version">Prepared for the Future™</div>
      </MainHeader>

      <DashboardGrid>
        <TerminalWidget title="SYSTEM STATUS">
          <StatusIndicator status="ok">DATABASE: OPERATIONAL</StatusIndicator>
          <br />
          <StatusIndicator status="ok">OBSERVERS: OPERATIONAL</StatusIndicator>
          <br />
          <StatusIndicator status="ok">SECURITY: OPERATIONAL</StatusIndicator>
        </TerminalWidget>

        <TerminalWidget title="ACTIVE RESIDENTS">
          <div>Total: 2,847</div>
          <div>Active: 2,834</div>
          <div>Offline: 13</div>
        </TerminalWidget>

        <TerminalWidget title="ALERTS">
          <StatusIndicator status="warning">3 Schema Violations</StatusIndicator>
          <br />
          <StatusIndicator status="ok">0 Critical Issues</StatusIndicator>
        </TerminalWidget>
      </DashboardGrid>

      <TerminalWidget title="RECENT OPERATIONS">
        <OperationsList>
          <div className="operation">
            <span className="time">14:32:07</span>
            <span className="type">PERSONNEL</span>
            <span className="action">CREATE</span>
            <span className="details">VAULT_DWELLER_2848</span>
          </div>
          <div className="operation">
            <span className="time">14:31:45</span>
            <span className="type">SECURITY</span>
            <span className="action">UPDATE</span>
            <span className="details">ACCESS_CARD_ALPHA_7</span>
          </div>
          <div className="operation">
            <span className="time">14:30:12</span>
            <span className="type">INVENTORY</span>
            <span className="action">DELETE</span>
            <span className="details">STIMPAK_BATCH_A42</span>
          </div>
        </OperationsList>
      </TerminalWidget>

      <ActionBar>
        <TerminalButton variant="primary" hotkey="F9">
          ENTER COMMAND MODE
        </TerminalButton>
        <TerminalButton variant="secondary" hotkey="F3">
          VIEW DEPARTMENTS
        </TerminalButton>
        <TerminalButton variant="danger" hotkey="F10">
          EMERGENCY
        </TerminalButton>
      </ActionBar>
    </ConsoleContainer>
  );
};