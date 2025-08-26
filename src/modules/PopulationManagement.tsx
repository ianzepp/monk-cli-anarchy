import React from 'react';
import styled from 'styled-components';
import { TerminalWidget } from '../components/terminal/TerminalWidget';
import { TerminalButton } from '../components/terminal/TerminalButton';
import { VaultLayout, VaultSection } from '../components/terminal/VaultLayout';
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

const ResultsTable = styled.div`
  font-family: monospace;
  font-size: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
`;

const TableHeader = styled.div`
  flex-shrink: 0;
  margin-bottom: 8px;
`;

const TableBody = styled.div`
  flex: 1;
  overflow-y: auto;
  min-height: 150px;
`;

const TableFooter = styled.div`
  margin-top: 12px;
  border-top: 1px solid ${terminalTheme.colors.dustBrown};
  padding-top: 8px;
  flex-shrink: 0;
`;

export const PopulationManagement: React.FC = () => {
  return (
    <VaultLayout>
      {/* Header Section */}
      <VaultSection>
        <ModuleHeader>
          <h1>┌─ VAULT POPULATION RECORDS ─┐</h1>
          <div className="subtitle">Resident Management System</div>
        </ModuleHeader>
      </VaultSection>

      {/* Statistics Section */}
      <VaultSection>
        <TerminalWidget title="POPULATION STATISTICS">
          <div>Active Schema: personnel_records</div>
          <div>Population Count: 2,847 | Active Filters: security_level=HIGH</div>
        </TerminalWidget>
      </VaultSection>

      {/* Search Console Section */}
      <VaultSection>
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
      </VaultSection>

      {/* Search Results - Primary expanding content */}
      <VaultSection flex minHeight="250px">
        <TerminalWidget title="SEARCH RESULTS" flex scrollable>
          <ResultsTable>
            <TableHeader>
              <div>┌─ □ ─┬─────────────────┬───────────┬─────────┬────────────┐</div>
              <div>│ □   │ ID              │ NAME      │ LEVEL   │ STATUS     │</div>
              <div>├─────┼─────────────────┼───────────┼─────────┼────────────┤</div>
            </TableHeader>
            <TableBody>
              <div>│ ► □ │ V111001         │ LONE_WAND │ OVERSEE │ ●ACTIVE    │</div>
              <div>│   □ │ V111023         │ ELDER_LYO │ OFFICER │ ●ACTIVE    │</div>
              <div>│   □ │ V111045         │ KNIGHT_CA │ OFFICER │ ●ACTIVE    │</div>
              {/* Add more entries to test scrolling */}
              {Array.from({ length: 50 }, (_, i) => (
                <div key={i}>
                  │   □ │ V111{String(i + 100).padStart(3, '0')} │ RESIDENT_{i + 100} │ {Math.random() > 0.5 ? 'OFFICER' : 'CIVILIAN'} │ ●ACTIVE    │
                </div>
              ))}
              <div>└─────┴─────────────────┴───────────┴─────────┴────────────┘</div>
            </TableBody>
            <TableFooter>
              Selected: 3 records
            </TableFooter>
          </ResultsTable>
        </TerminalWidget>
      </VaultSection>

      {/* Action Bar */}
      <VaultSection>
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
      </VaultSection>
    </VaultLayout>
  );
};