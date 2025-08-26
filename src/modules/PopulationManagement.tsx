import React from 'react';
import styled from 'styled-components';
import { TerminalWidget } from '../components/terminal/TerminalWidget';
import { TerminalButton } from '../components/terminal/TerminalButton';
import { terminalTheme } from '../styles/terminal-theme';

const PopulationContainer = styled.div`
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

const SearchConsole = styled.div`
  background: ${terminalTheme.colors.bunkerBlack};
  border: 1px solid ${terminalTheme.colors.dustBrown};
  padding: 12px;
  font-family: ${terminalTheme.fonts.terminal};
  font-size: ${terminalTheme.sizes.terminalSm};
  color: ${terminalTheme.colors.vaultGreen};
  min-height: 120px;
`;

export const PopulationManagement: React.FC = () => {
  return (
    <PopulationContainer>
      <ModuleHeader>
        <h1>┌─ VAULT POPULATION RECORDS ─┐</h1>
        <div className="subtitle">Resident Management System</div>
      </ModuleHeader>

      <div style={{ margin: '0 20px' }}>
        <TerminalWidget title="POPULATION STATISTICS">
          <div>Active Schema: personnel_records</div>
          <div>Population Count: 2,847 | Active Filters: security_level=HIGH</div>
        </TerminalWidget>

        <TerminalWidget title="ADVANCED SEARCH CONSOLE">
          <SearchConsole>
            <div>FILTER_EXPR: {`{`}</div>
            <div>{`  "$and": [`}</div>
            <div>{`    {"security_level": {"$in": ["OFFICER", "OVERSEER"]}},`}</div>
            <div>{`    {"status": {"$ne": "TERMINATED"}},`}</div>
            <div>{`    {"last_seen": {"$gte": "2287.10.20"}}`}</div>
            <div>{`  ]`}</div>
            <div>{`}`}</div>
          </SearchConsole>
        </TerminalWidget>

        <TerminalWidget title="SEARCH RESULTS">
          <div style={{ fontFamily: 'monospace', fontSize: '12px' }}>
            <div>┌─ □ ─┬─────────────────┬───────────┬─────────┬────────────┐</div>
            <div>│ □   │ ID              │ NAME      │ LEVEL   │ STATUS     │</div>
            <div>├─────┼─────────────────┼───────────┼─────────┼────────────┤</div>
            <div>│ ► □ │ V111001         │ LONE_WAND │ OVERSEE │ ●ACTIVE    │</div>
            <div>│   □ │ V111023         │ ELDER_LYO │ OFFICER │ ●ACTIVE    │</div>
            <div>│   □ │ V111045         │ KNIGHT_CA │ OFFICER │ ●ACTIVE    │</div>
            <div>└─────┴─────────────────┴───────────┴─────────┴────────────┘</div>
          </div>
          <div style={{ marginTop: '12px' }}>
            Selected: 3 records
          </div>
        </TerminalWidget>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', margin: '20px', padding: '20px' }}>
          <TerminalButton variant="primary" hotkey="F4">
            BULK UPDATE
          </TerminalButton>
          <TerminalButton variant="secondary" hotkey="F6">
            EXPORT
          </TerminalButton>
          <TerminalButton variant="danger" hotkey="F10">
            TERMINATE
          </TerminalButton>
          <TerminalButton variant="secondary" hotkey="F11">
            NEW RECORD
          </TerminalButton>
        </div>
      </div>
    </PopulationContainer>
  );
};