import React from 'react';
import styled from 'styled-components';
import { terminalTheme } from '../../styles/terminal-theme';

interface TerminalWidgetProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
  width?: string;
  height?: string;
}

const WidgetContainer = styled.div<{ width?: string; height?: string }>`
  background: ${terminalTheme.colors.bunkerBlack};
  border: 1px solid ${terminalTheme.colors.vaultGreen};
  color: ${terminalTheme.colors.vaultGreen};
  font-family: ${terminalTheme.fonts.terminal};
  text-shadow: ${terminalTheme.effects.terminalGlow};
  position: relative;
  width: ${props => props.width || 'auto'};
  height: ${props => props.height || 'auto'};
  margin: 4px;
  
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

const WidgetContent = styled.div`
  padding: 12px;
  min-height: 40px;
`;

export const TerminalWidget: React.FC<TerminalWidgetProps> = ({
  title,
  children,
  className,
  width,
  height,
}) => {
  return (
    <WidgetContainer className={className} width={width} height={height}>
      {title && <WidgetHeader>{title}</WidgetHeader>}
      <WidgetContent>{children}</WidgetContent>
    </WidgetContainer>
  );
};