import React from 'react';
import styled from 'styled-components';
import { TerminalWidget } from '../components/terminal/TerminalWidget';
import { TerminalButton } from '../components/terminal/TerminalButton';
import { terminalTheme } from '../styles/terminal-theme';

const ArchiveContainer = styled.div`
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

const FileEntry = styled.div<{ selected?: boolean }>`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 2px 0;
  background: ${props => props.selected ? terminalTheme.colors.shadowGray : 'transparent'};
  
  .icon {
    width: 20px;
    color: ${terminalTheme.colors.amberAlert};
  }
  
  .name {
    flex: 1;
    color: ${terminalTheme.colors.vaultGreen};
  }
  
  .size {
    width: 80px;
    color: ${terminalTheme.colors.dustBrown};
  }
  
  .date {
    width: 100px;
    color: ${terminalTheme.colors.dustBrown};
  }
`;

export const FileArchives: React.FC = () => {
  return (
    <ArchiveContainer>
      <ModuleHeader>
        <h1>┌─ VAULT DATA ARCHIVE SYSTEM ─┐</h1>
        <div className="subtitle">File Transfer & Management Protocol</div>
      </ModuleHeader>

      <div style={{ margin: '0 20px' }}>
        <TerminalWidget title="CURRENT DIRECTORY">
          <div>Path: /data/personnel_records/</div>
          <div>Files: 2,847 | Directories: 3 | Space Used: 142.8 MB</div>
        </TerminalWidget>

        <TerminalWidget title="DIRECTORY CONTENTS">
          <div style={{ fontFamily: 'monospace', fontSize: '12px' }}>
            <FileEntry>
              <span className="icon">[📁]</span>
              <span className="name">../</span>
              <span className="size">&lt;DIR&gt;</span>
              <span className="date">-------</span>
            </FileEntry>
            <FileEntry selected>
              <span className="icon">[📄]</span>
              <span className="name">V111001_LONE_WANDERER.json</span>
              <span className="size">2.4KB</span>
              <span className="date">2287.10.23</span>
            </FileEntry>
            <FileEntry>
              <span className="icon">[📄]</span>
              <span className="name">V111002_THREE_DOG.json</span>
              <span className="size">1.8KB</span>
              <span className="date">2287.10.22</span>
            </FileEntry>
            <FileEntry>
              <span className="icon">[📄]</span>
              <span className="name">V111003_SARAH_LYONS.json</span>
              <span className="size">2.1KB</span>
              <span className="date">2287.10.20</span>
            </FileEntry>
            <FileEntry>
              <span className="icon">[📁]</span>
              <span className="name">archived/</span>
              <span className="size">&lt;DIR&gt;</span>
              <span className="date">2287.09.15</span>
            </FileEntry>
          </div>
          <div style={{ marginTop: '12px', borderTop: '1px solid ' + terminalTheme.colors.dustBrown, paddingTop: '8px' }}>
            Selected: V111001_LONE_WANDERER.json
          </div>
        </TerminalWidget>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', margin: '20px', padding: '20px' }}>
          <TerminalButton variant="primary" hotkey="F4">
            DOWNLOAD
          </TerminalButton>
          <TerminalButton variant="secondary" hotkey="F9">
            EDIT
          </TerminalButton>
          <TerminalButton variant="danger" hotkey="F10">
            DELETE
          </TerminalButton>
          <TerminalButton variant="secondary" hotkey="F11">
            UPLOAD NEW
          </TerminalButton>
        </div>
      </div>
    </ArchiveContainer>
  );
};