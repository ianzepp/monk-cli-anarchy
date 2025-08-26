import React from 'react';
import styled, { keyframes } from 'styled-components';
import { terminalTheme } from '../../styles/terminal-theme';

interface TerminalButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'danger' | 'disabled';
  disabled?: boolean;
  hotkey?: string;
  className?: string;
}

const buttonGlow = keyframes`
  0% { box-shadow: 0 0 10px currentColor; }
  50% { box-shadow: 0 0 20px currentColor; }
  100% { box-shadow: 0 0 10px currentColor; }
`;

const StyledButton = styled.button<{ $variant: string }>`
  background: ${terminalTheme.colors.shadowGray};
  border: 1px solid ${props => {
    switch (props.$variant) {
      case 'primary': return terminalTheme.colors.vaultGreen;
      case 'secondary': return terminalTheme.colors.steelBlue;
      case 'danger': return terminalTheme.colors.radRed;
      case 'disabled': return terminalTheme.colors.dustBrown;
      default: return terminalTheme.colors.vaultGreen;
    }
  }};
  color: ${props => {
    switch (props.$variant) {
      case 'primary': return terminalTheme.colors.vaultGreen;
      case 'secondary': return terminalTheme.colors.steelBlue;
      case 'danger': return terminalTheme.colors.radRed;
      case 'disabled': return terminalTheme.colors.dustBrown;
      default: return terminalTheme.colors.vaultGreen;
    }
  }};
  font-family: ${terminalTheme.fonts.terminal};
  font-size: ${terminalTheme.sizes.terminalSm};
  padding: 6px 12px;
  margin: 2px;
  cursor: ${props => props.$variant === 'disabled' ? 'not-allowed' : 'pointer'};
  text-transform: uppercase;
  font-weight: bold;
  
  text-shadow: 0 0 5px currentColor;
  box-shadow: 0 0 10px currentColor;
  
  transition: all 0.2s ease;
  
  &:hover:not(:disabled) {
    animation: ${buttonGlow} 1s ease-in-out infinite;
    transform: translateY(-1px);
  }
  
  &:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: 0 0 15px currentColor;
  }
  
  &:focus {
    outline: 2px solid currentColor;
    outline-offset: 2px;
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const ButtonContent = styled.span`
  display: flex;
  align-items: center;
  gap: 4px;
`;

const Hotkey = styled.span`
  font-size: ${terminalTheme.sizes.terminalXs};
  opacity: 0.7;
`;

export const TerminalButton: React.FC<TerminalButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  disabled = false,
  hotkey,
  className,
}) => {
  const getButtonIcon = () => {
    switch (variant) {
      case 'primary': return '▶ ';
      case 'secondary': return '◉ ';
      case 'danger': return '⚠ ';
      case 'disabled': return '□ ';
      default: return '▶ ';
    }
  };

  return (
    <StyledButton
      $variant={variant}
      onClick={onClick}
      disabled={disabled}
      className={className}
      type="button"
    >
      <ButtonContent>
        {getButtonIcon()}{children}
        {hotkey && <Hotkey>[{hotkey}]</Hotkey>}
      </ButtonContent>
    </StyledButton>
  );
};