import React from 'react';
import styled from 'styled-components';
import { TerminalWidget } from '../components/terminal/TerminalWidget';
import { TerminalButton } from '../components/terminal/TerminalButton';
import { VaultLayout, VaultSection } from '../components/terminal/VaultLayout';
import { terminalTheme } from '../styles/terminal-theme';

const SecurityContainer = styled.div`
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

const RingStatus = styled.div<{ status: 'active' | 'warning' | 'error' }>`
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 4px 0;
  
  .ring-indicator {
    color: ${props => {
      switch (props.status) {
        case 'active': return terminalTheme.colors.healthyGreen;
        case 'warning': return terminalTheme.colors.cautionYellow;
        case 'error': return terminalTheme.colors.dangerRed;
        default: return terminalTheme.colors.healthyGreen;
      }
    }};
  }
`;

const RingConfigurationList = styled.div`
  font-family: monospace;
  font-size: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow-y: auto;
`;

export const SecurityProtocols: React.FC = () => {
  return (
    <VaultLayout>
      {/* Header Section */}
      <VaultSection>
        <ModuleHeader>
          <h1>┌─ AUTOMATED SECURITY MONITORING ─┐</h1>
          <div className="subtitle">Observer Pipeline Management</div>
        </ModuleHeader>
      </VaultSection>

      {/* Status Overview */}
      <VaultSection>
        <TerminalWidget title="OBSERVER PIPELINE STATUS">
          <div>Status: ●OPERATIONAL | Total Rings: 10 | Active: 10</div>
        </TerminalWidget>
      </VaultSection>

      {/* Ring Configuration - Primary expanding content */}
      <VaultSection flex minHeight="250px">
        <TerminalWidget title="SECURITY RING CONFIGURATION" flex scrollable>
          <RingConfigurationList>
            <RingStatus status="active">
              <span className="ring-indicator">●</span> RING 0: Data Preparation | ●ACTIVE | 12ms avg
            </RingStatus>
            <RingStatus status="active">
              <span className="ring-indicator">●</span> RING 1: Input Validation | ●ACTIVE | 8ms avg
            </RingStatus>
            <RingStatus status="active">
              <span className="ring-indicator">●</span> RING 2: Security Checks | ●ACTIVE | 15ms avg
            </RingStatus>
            <RingStatus status="active">
              <span className="ring-indicator">●</span> RING 3: Business Logic | ●ACTIVE | 23ms avg
            </RingStatus>
            <RingStatus status="active">
              <span className="ring-indicator">●</span> RING 4: Data Enrichment | ●ACTIVE | 11ms avg
            </RingStatus>
            <RingStatus status="warning">
              <span className="ring-indicator">⚠</span> RING 5: Database Operations | ●ACTIVE | 156ms avg
            </RingStatus>
            <RingStatus status="active">
              <span className="ring-indicator">●</span> RING 6: Post-Processing | ●ACTIVE | 7ms avg
            </RingStatus>
            <RingStatus status="active">
              <span className="ring-indicator">●</span> RING 7: Audit Logging | ●ACTIVE | 9ms avg
            </RingStatus>
            <RingStatus status="active">
              <span className="ring-indicator">●</span> RING 8: External Systems | ●ACTIVE | 89ms avg
            </RingStatus>
            <RingStatus status="active">
              <span className="ring-indicator">●</span> RING 9: Notifications | ●ACTIVE | 67ms avg
            </RingStatus>
            {/* Add more ring details for scrolling */}
            {Array.from({ length: 20 }, (_, i) => (
              <RingStatus key={i} status={Math.random() > 0.8 ? 'warning' : 'active'}>
                <span className="ring-indicator">{Math.random() > 0.8 ? '⚠' : '●'}</span> 
                OBSERVER_{i + 10}: {['Validation', 'Security', 'Audit', 'Monitor'][Math.floor(Math.random() * 4)]} | 
                ●ACTIVE | {Math.floor(Math.random() * 100) + 5}ms avg
              </RingStatus>
            ))}
          </RingConfigurationList>
        </TerminalWidget>
      </VaultSection>

      {/* Security Events */}
      <VaultSection>
        <TerminalWidget title="RECENT SECURITY EVENTS">
          <div style={{ fontFamily: 'monospace', fontSize: '12px' }}>
            <div>14:32:15 │ VIOLATION │ Invalid schema access attempt      │</div>
            <div>14:31:22 │ WARNING   │ Bulk operation threshold exceeded  │</div>
            <div>14:30:45 │ SUCCESS   │ Security validation passed         │</div>
            <div>14:29:33 │ INFO      │ Observer ring reconfigured         │</div>
          </div>
        </TerminalWidget>
      </VaultSection>

      {/* Action Bar */}
      <VaultSection>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', margin: '20px', padding: '20px' }}>
          <TerminalButton variant="primary" hotkey="F4">
            CONFIGURE RINGS
          </TerminalButton>
          <TerminalButton variant="secondary" hotkey="F8">
            VIEW LOGS
          </TerminalButton>
          <TerminalButton variant="danger" hotkey="F10">
            EMERGENCY STOP
          </TerminalButton>
        </div>
      </VaultSection>
    </VaultLayout>
  );
};