import React from 'react';
import styled from 'styled-components';
import { TerminalWidget } from '../components/terminal/TerminalWidget';
import { TerminalButton } from '../components/terminal/TerminalButton';
import { terminalTheme } from '../styles/terminal-theme';

const LaboratoryContainer = styled.div`
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

const SchemaEditor = styled.div`
  background: ${terminalTheme.colors.bunkerBlack};
  border: 1px solid ${terminalTheme.colors.dustBrown};
  padding: 12px;
  font-family: ${terminalTheme.fonts.terminal};
  font-size: ${terminalTheme.sizes.terminalSm};
  color: ${terminalTheme.colors.vaultGreen};
  min-height: 200px;
  
  .line-numbers {
    color: ${terminalTheme.colors.dustBrown};
    margin-right: 12px;
  }
`;

export const SchemaLaboratory: React.FC = () => {
  return (
    <LaboratoryContainer>
      <ModuleHeader>
        <h1>┌─ RESEARCH & DEVELOPMENT LAB ─┐</h1>
        <div className="subtitle">Schema Development & Deployment</div>
      </ModuleHeader>

      <div style={{ margin: '0 20px' }}>
        <TerminalWidget title="ACTIVE EXPERIMENTS (SCHEMAS)">
          <div style={{ fontFamily: 'monospace', fontSize: '12px' }}>
            <div>┌───────────────────────┬─────────┬──────────┬─────────────┐</div>
            <div>│ DESIGNATION           │ VERSION │ SUBJECTS │ LAST_UPDATE │</div>
            <div>├───────────────────────┼─────────┼──────────┼─────────────┤</div>
            <div>│ personnel_records     │ v2.1.4  │ 2,847    │ 2287.10.23  │</div>
            <div>│ security_clearance    │ v1.0.8  │ 156      │ 2287.10.22  │</div>
            <div>│ inventory_management  │ v3.2.1  │ 45,231   │ 2287.10.23  │</div>
            <div>│ medical_records       │ v1.4.2  │ 2,834    │ 2287.10.20  │</div>
            <div>└───────────────────────┴─────────┴──────────┴─────────────┘</div>
          </div>
        </TerminalWidget>

        <TerminalWidget title="SCHEMA EDITOR: personnel_records">
          <SchemaEditor>
            <div><span className="line-numbers">001│</span>{`{`}</div>
            <div><span className="line-numbers">002│</span>{`  "type": "object",`}</div>
            <div><span className="line-numbers">003│</span>{`  "properties": {`}</div>
            <div><span className="line-numbers">004│</span>{`    "id": {"type": "string", "format": "vault-id"},`}</div>
            <div><span className="line-numbers">005│</span>{`    "name": {"type": "string", "maxLength": 50},`}</div>
            <div><span className="line-numbers">006│</span>{`    "security_level": {"enum": ["CIVILIAN", "OFFICER"]}`}</div>
            <div><span className="line-numbers">007│</span>{`  }`}</div>
            <div><span className="line-numbers">008│</span>{`}`}</div>
          </SchemaEditor>
        </TerminalWidget>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', margin: '20px', padding: '20px' }}>
          <TerminalButton variant="primary" hotkey="F3">
            DEPLOY SCHEMA
          </TerminalButton>
          <TerminalButton variant="secondary" hotkey="F2">
            VALIDATE
          </TerminalButton>
          <TerminalButton variant="danger" hotkey="F10">
            ROLLBACK
          </TerminalButton>
          <TerminalButton variant="secondary" hotkey="F6">
            BACKUP
          </TerminalButton>
        </div>
      </div>
    </LaboratoryContainer>
  );
};