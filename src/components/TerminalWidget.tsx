import React from 'react';
import { Box, Text } from 'ink';
import chalk from 'chalk';

interface TerminalWidgetProps {
  title?: string;
  children: React.ReactNode;
  width?: number;
  height?: number;
  borderColor?: 'green' | 'yellow' | 'red' | 'blue';
}

export const TerminalWidget: React.FC<TerminalWidgetProps> = ({
  title,
  children,
  width = 60,
  height,
  borderColor = 'green'
}) => {
  const colors = {
    green: chalk.green,
    yellow: chalk.yellow,
    red: chalk.red,
    blue: chalk.blue,
  };
  
  const borderStyle = colors[borderColor];
  
  // Create top border
  const topBorder = title 
    ? `┌─ ${title.toUpperCase()} ${'─'.repeat(Math.max(0, width - title.length - 5))}┐`
    : `┌${'─'.repeat(width - 2)}┐`;
    
  const bottomBorder = `└${'─'.repeat(width - 2)}┘`;

  return (
    <Box flexDirection="column" marginY={1}>
      <Text color={borderColor}>{topBorder}</Text>
      <Box 
        flexDirection="column" 
        paddingX={1}
        height={height}
      >
        {children}
      </Box>
      <Text color={borderColor}>{bottomBorder}</Text>
    </Box>
  );
};