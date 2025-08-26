import React from 'react';
import styled from 'styled-components';
import { TerminalWidget } from '../components/terminal/TerminalWidget';
import { TerminalButton } from '../components/terminal/TerminalButton';
import { VaultLayout, VaultSection } from '../components/terminal/VaultLayout';
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
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow-y: auto;
  
  .line-numbers {
    color: ${terminalTheme.colors.dustBrown};
    margin-right: 12px;
  }
`;

export const SchemaLaboratory: React.FC = () => {
  return (
    <VaultLayout>
      {/* Header Section */}
      <VaultSection>
        <ModuleHeader>
          <h1>┌─ RESEARCH & DEVELOPMENT LAB ─┐</h1>
          <div className="subtitle">Schema Development & Deployment</div>
        </ModuleHeader>
      </VaultSection>

      {/* Schema List Section */}
      <VaultSection>
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
      </VaultSection>

      {/* Schema Editor - Primary expanding content */}
      <VaultSection flex minHeight="300px">
        <TerminalWidget title="SCHEMA EDITOR: personnel_records" flex scrollable>
          <SchemaEditor>
            <div><span className="line-numbers">001│</span>{`{`}</div>
            <div><span className="line-numbers">002│</span>{`  "type": "object",`}</div>
            <div><span className="line-numbers">003│</span>{`  "properties": {`}</div>
            <div><span className="line-numbers">004│</span>{`    "id": {"type": "string", "format": "vault-id"},`}</div>
            <div><span className="line-numbers">005│</span>{`    "name": {"type": "string", "maxLength": 50},`}</div>
            <div><span className="line-numbers">006│</span>{`    "security_level": {"enum": ["CIVILIAN", "OFFICER"]},`}</div>
            <div><span className="line-numbers">007│</span>{`    "section": {"type": "string"},`}</div>
            <div><span className="line-numbers">008│</span>{`    "status": {"enum": ["ACTIVE", "INACTIVE", "TERMINATED"]},`}</div>
            <div><span className="line-numbers">009│</span>{`    "last_seen": {"type": "string", "format": "date"},`}</div>
            <div><span className="line-numbers">010│</span>{`    "access_permissions": {`}</div>
            <div><span className="line-numbers">011│</span>{`      "type": "array",`}</div>
            <div><span className="line-numbers">012│</span>{`      "items": {"type": "string"}`}</div>
            <div><span className="line-numbers">013│</span>{`    },`}</div>
            <div><span className="line-numbers">014│</span>{`    "medical_status": {"type": "string"},`}</div>
            <div><span className="line-numbers">015│</span>{`    "vault_entry_date": {"type": "string", "format": "date"},`}</div>
            <div><span className="line-numbers">016│</span>{`    "emergency_contact": {"type": "string"},`}</div>
            <div><span className="line-numbers">017│</span>{`    "special_notes": {"type": "string"},`}</div>
            {/* Add more lines for scrolling */}
            {Array.from({ length: 30 }, (_, i) => (
              <div key={i}>
                <span className="line-numbers">{String(i + 18).padStart(3, '0')}│</span>
                {`    "field_${i + 18}": {"type": "${Math.random() > 0.5 ? 'string' : 'number'}"},`}
              </div>
            ))}
            <div><span className="line-numbers">049│</span>{`  },`}</div>
            <div><span className="line-numbers">050│</span>{`  "required": ["id", "name", "security_level", "status"]`}</div>
            <div><span className="line-numbers">051│</span>{`}`}</div>
          </SchemaEditor>
        </TerminalWidget>
      </VaultSection>

      {/* Action Bar */}
      <VaultSection>
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
      </VaultSection>
    </VaultLayout>
  );
};