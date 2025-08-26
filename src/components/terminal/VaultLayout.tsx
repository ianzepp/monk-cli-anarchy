import React from 'react';
import styled from 'styled-components';
import { terminalTheme } from '../../styles/terminal-theme';

interface VaultLayoutProps {
  children: React.ReactNode;
}

interface VaultSectionProps {
  children: React.ReactNode;
  flex?: boolean; // Whether this section should expand to fill space
  minHeight?: string;
  maxHeight?: string;
}

const LayoutContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  background: ${terminalTheme.colors.bunkerBlack};
  box-sizing: border-box;
  overflow: hidden;
`;

const VaultSectionContainer = styled.div<{ 
  $flex?: boolean; 
  $minHeight?: string;
  $maxHeight?: string;
}>`
  margin: 0 20px;
  
  ${props => props.$flex && `
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: ${props.$minHeight || '200px'};
    max-height: ${props.$maxHeight || 'none'};
  `}
  
  ${props => !props.$flex && `
    flex-shrink: 0;
  `}
`;

// Layout container for the entire vault interface
export const VaultLayout: React.FC<VaultLayoutProps> = ({ children }) => {
  return <LayoutContainer>{children}</LayoutContainer>;
};

// Section wrapper that can expand to fill available space
export const VaultSection: React.FC<VaultSectionProps> = ({ 
  children, 
  flex = false,
  minHeight,
  maxHeight 
}) => {
  return (
    <VaultSectionContainer 
      $flex={flex}
      $minHeight={minHeight}
      $maxHeight={maxHeight}
    >
      {children}
    </VaultSectionContainer>
  );
};