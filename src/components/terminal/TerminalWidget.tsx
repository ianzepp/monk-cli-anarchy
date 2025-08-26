import React from 'react';
import styled from 'styled-components';
import { terminalTheme } from '../../styles/terminal-theme';

interface TerminalWidgetProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
  width?: string;
  height?: string;
  flex?: boolean; // Whether content should expand to fill available space
  scrollable?: boolean; // Whether content should scroll if it overflows
}

const WidgetContainer = styled.div<{ 
  width?: string; 
  height?: string;
  $flex?: boolean;
  $scrollable?: boolean;
}>`
  background: ${terminalTheme.colors.bunkerBlack};
  border: 1px solid ${terminalTheme.colors.vaultGreen};
  color: ${terminalTheme.colors.vaultGreen};
  font-family: ${terminalTheme.fonts.terminal};
  text-shadow: ${terminalTheme.effects.terminalGlow};
  position: relative;
  width: ${props => props.width || 'auto'};
  height: ${props => props.height || 'auto'};
  margin: 4px;
  
  /* Flex layout for expandable widgets */
  ${props => props.$flex && `
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0; /* Allow shrinking below content size */
  `}
  
  /* CRT glow effect */
  box-shadow: 
    inset 0 0 20px rgba(0, 255, 0, 0.1),
    0 0 20px rgba(0, 255, 0, 0.2);
`;

const WidgetHeader = styled.div`
  background: ${terminalTheme.colors.shadowGray};
  border-bottom: 1px solid ${terminalTheme.colors.vaultGreen};
  padding: 8px 12px;
  font-size: ${terminalTheme.sizes.terminalSm};
  font-weight: bold;
  text-transform: uppercase;
  display: flex;
  align-items: center;
  
  &::before {
    content: '┌─ ';
  }
  
  &::after {
    content: ' ─┐';
    margin-left: auto;
  }
`;

const WidgetContent = styled.div<{ $flex?: boolean; $scrollable?: boolean }>`
  padding: 12px;
  min-height: 40px;
  
  /* Flex content for expandable widgets */
  ${props => props.$flex && `
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
  `}
  
  /* Scrollable content */
  ${props => props.$scrollable && `
    overflow-y: auto;
    overflow-x: hidden;
  `}
`;

export const TerminalWidget: React.FC<TerminalWidgetProps> = ({
  title,
  children,
  className,
  width,
  height,
  flex = false,
  scrollable = false,
}) => {
  return (
    <WidgetContainer 
      className={className} 
      width={width} 
      height={height}
      $flex={flex}
      $scrollable={scrollable}
    >
      {title && <WidgetHeader>{title}</WidgetHeader>}
      <WidgetContent $flex={flex} $scrollable={scrollable}>
        {children}
      </WidgetContent>
    </WidgetContainer>
  );
};