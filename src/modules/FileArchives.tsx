import React from 'react';
import styled from 'styled-components';
import { TerminalWidget } from '../components/terminal/TerminalWidget';
import { TerminalButton } from '../components/terminal/TerminalButton';
import { VaultLayout, VaultSection } from '../components/terminal/VaultLayout';
import { terminalTheme } from '../styles/terminal-theme';

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

const DirectoryContents = styled.div`
  font-family: monospace;
  font-size: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
`;

const FileList = styled.div`
  flex: 1;
  overflow-y: auto;
  min-height: 200px;
`;

const FileSelection = styled.div`
  margin-top: 12px;
  border-top: 1px solid ${terminalTheme.colors.dustBrown};
  padding-top: 8px;
  flex-shrink: 0;
`;

export const FileArchives: React.FC = () => {
  return (
    <VaultLayout>
      {/* Header Section - Fixed size */}
      <VaultSection>
        <ModuleHeader>
          <h1>┌─ VAULT DATA ARCHIVE SYSTEM ─┐</h1>
          <div className="subtitle">File Transfer & Management Protocol</div>
        </ModuleHeader>
      </VaultSection>

      {/* Status Section - Fixed size */}
      <VaultSection>
        <TerminalWidget title="CURRENT DIRECTORY">
          <div>Path: /data/personnel_records/</div>
          <div>Files: 2,847 | Directories: 3 | Space Used: 142.8 MB</div>
        </TerminalWidget>
      </VaultSection>

      {/* Directory Contents - Expandable primary content */}
      <VaultSection flex minHeight="300px">
        <TerminalWidget title="DIRECTORY CONTENTS" flex scrollable>
          <DirectoryContents>
            <FileList>
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
              {/* Add more entries to test scrolling */}
              {Array.from({ length: 50 }, (_, i) => (
                <FileEntry key={i}>
                  <span className="icon">[📄]</span>
                  <span className="name">V111{String(i + 100).padStart(3, '0')}_RESIDENT_{i + 100}.json</span>
                  <span className="size">{(Math.random() * 5 + 1).toFixed(1)}KB</span>
                  <span className="date">2287.10.{String(Math.floor(Math.random() * 30) + 1).padStart(2, '0')}</span>
                </FileEntry>
              ))}
            </FileList>
            <FileSelection>
              Selected: V111001_LONE_WANDERER.json
            </FileSelection>
          </DirectoryContents>
        </TerminalWidget>
      </VaultSection>

      {/* Action Bar - Fixed size */}
      <VaultSection>
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
      </VaultSection>
    </VaultLayout>
  );
};