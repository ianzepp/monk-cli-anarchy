import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { terminalTheme } from '../../styles/terminal-theme';

interface KeyboardFeedbackProps {
  pressedKey: string | null;
  action?: string;
}

const fadeInOut = keyframes`
  0% { opacity: 0; transform: scale(0.8); }
  20% { opacity: 1; transform: scale(1.1); }
  80% { opacity: 1; transform: scale(1); }
  100% { opacity: 0; transform: scale(0.9); }
`;

const FeedbackContainer = styled.div<{ show: boolean }>`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: ${terminalTheme.colors.shadowGray};
  border: 2px solid ${terminalTheme.colors.vaultGreen};
  color: ${terminalTheme.colors.vaultGreen};
  font-family: ${terminalTheme.fonts.terminal};
  font-size: ${terminalTheme.sizes.terminalLg};
  padding: 20px 30px;
  z-index: 9999;
  text-align: center;
  min-width: 200px;
  
  box-shadow: 
    inset 0 0 20px rgba(0, 255, 0, 0.2),
    0 0 40px rgba(0, 255, 0, 0.3);
  
  ${props => props.show && `
    animation: ${fadeInOut} 1.2s ease-out forwards;
  `}
  
  ${props => !props.show && `
    display: none;
  `}
  
  .key {
    display: block;
    font-size: ${terminalTheme.sizes.terminalXl};
    font-weight: bold;
    text-shadow: ${terminalTheme.effects.terminalGlow};
    margin-bottom: 8px;
  }
  
  .action {
    font-size: ${terminalTheme.sizes.terminalSm};
    opacity: 0.8;
    text-transform: uppercase;
  }
`;

export const KeyboardFeedback: React.FC<KeyboardFeedbackProps> = ({ pressedKey, action }) => {
  const [show, setShow] = useState(false);
  const [currentKey, setCurrentKey] = useState<string | null>(null);

  useEffect(() => {
    if (pressedKey && pressedKey !== currentKey) {
      setCurrentKey(pressedKey);
      setShow(true);
      
      // Hide after animation completes
      const timer = setTimeout(() => {
        setShow(false);
        setCurrentKey(null);
      }, 1200);
      
      return () => clearTimeout(timer);
    }
  }, [pressedKey, currentKey]);

  if (!currentKey) return null;

  return (
    <FeedbackContainer show={show}>
      <div className="key">{currentKey}</div>
      {action && <div className="action">{action}</div>}
    </FeedbackContainer>
  );
};