import React from 'react';
import styled from 'styled-components';
import { TerminalWidget } from '../components/terminal/TerminalWidget';
import { TerminalButton } from '../components/terminal/TerminalButton';
import { terminalTheme } from '../styles/terminal-theme';

const ErrorContainer = styled.div`
  padding: 0;
  margin: 0;
  width: 100vw;
  min-height: 100vh;
  background: ${terminalTheme.colors.bunkerBlack};
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const ErrorHeader = styled.div`
  text-align: center;
  margin: 20px;
  padding: 20px;
  border: 2px solid ${terminalTheme.colors.radRed};
  background: ${terminalTheme.colors.shadowGray};
  max-width: 600px;
  
  h1 {
    font-size: ${terminalTheme.sizes.terminalXl};
    margin: 0 0 10px 0;
    text-shadow: ${terminalTheme.effects.terminalGlow};
    color: ${terminalTheme.colors.radRed};
  }
  
  .error-code {
    font-size: ${terminalTheme.sizes.terminalLg};
    color: ${terminalTheme.colors.cautionYellow};
    margin-bottom: 10px;
  }
  
  .message {
    font-size: ${terminalTheme.sizes.terminalSm};
    opacity: 0.8;
  }
`;

const ErrorDetails = styled.div`
  max-width: 600px;
  margin: 0 20px;
`;

interface VaultErrorProps {
  errorCode?: string;
  errorMessage?: string;
  errorType?: 'not-found' | 'access-denied' | 'system-failure';
}

export const VaultError: React.FC<VaultErrorProps> = ({ 
  errorCode = "404", 
  errorMessage = "Vault section not found",
  errorType = "not-found"
}) => {
  const getErrorIcon = () => {
    switch (errorType) {
      case 'not-found': return '🚨';
      case 'access-denied': return '🔒';
      case 'system-failure': return '💀';
      default: return '⚠';
    }
  };

  const getErrorTitle = () => {
    switch (errorType) {
      case 'not-found': return 'VAULT SECTION NOT FOUND';
      case 'access-denied': return 'ACCESS DENIED';
      case 'system-failure': return 'CRITICAL SYSTEM FAILURE';
      default: return 'VAULT MALFUNCTION';
    }
  };

  const getErrorDescription = () => {
    switch (errorType) {
      case 'not-found': return 'The requested vault section does not exist in our database. Please verify the location and try again.';
      case 'access-denied': return 'Your security clearance is insufficient for this operation. Contact your local Overseer.';
      case 'system-failure': return 'A critical system failure has occurred. Emergency protocols have been activated.';
      default: return 'An unknown error has occurred. Please consult your Vault-Tec manual.';
    }
  };

  return (
    <ErrorContainer>
      <ErrorHeader>
        <div className="error-code">ERROR CODE: {errorCode}</div>
        <h1>{getErrorIcon()} {getErrorTitle()} {getErrorIcon()}</h1>
        <div className="message">{errorMessage}</div>
      </ErrorHeader>

      <ErrorDetails>
        <TerminalWidget title="ERROR DETAILS">
          <div>{getErrorDescription()}</div>
          <br />
          <div>TIMESTAMP: {new Date().toISOString()}</div>
          <div>VAULT ID: V111_CAPITAL_WASTE</div>
          <div>USER: admin@vault111</div>
        </TerminalWidget>

        <TerminalWidget title="RECOVERY OPTIONS">
          <div>• Return to Overseer Console</div>
          <div>• Contact Technical Support</div>
          <div>• Review Security Protocols</div>
          <div>• Restart Vault Systems</div>
        </TerminalWidget>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', margin: '20px 0' }}>
          <TerminalButton 
            variant="primary" 
            hotkey="F1"
            onClick={() => window.location.href = '/'}
          >
            RETURN TO OVERSEER
          </TerminalButton>
          <TerminalButton variant="secondary" hotkey="F5">
            RETRY
          </TerminalButton>
          <TerminalButton variant="danger" hotkey="F10">
            EMERGENCY PROTOCOLS
          </TerminalButton>
        </div>
      </ErrorDetails>
    </ErrorContainer>
  );
};