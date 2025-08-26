import React from 'react';
import { Box, Text } from 'ink';
import chalk from 'chalk';

interface FunctionKeyBarProps {
  position: 'top' | 'bottom';
}

export const FunctionKeyBar: React.FC<FunctionKeyBarProps> = ({ position }) => {
  const topKeys = [
    { key: 'F1', label: 'Help' },
    { key: 'F2', label: 'Search' },
    { key: 'F3', label: 'Next Module' },
    { key: 'F4', label: 'Execute' },
    { key: 'F5', label: 'Refresh' },
  ];

  const bottomKeys = [
    { key: 'F6', label: 'Save' },
    { key: 'F7', label: 'Filter' },
    { key: 'F8', label: 'Status' },
    { key: 'F9', label: 'Terminal' },
    { key: 'F10', label: 'Emergency' },
  ];

  const keys = position === 'top' ? topKeys : bottomKeys;
  const terminalWidth = process.stdout.columns || 80;
  const keyWidth = Math.floor((terminalWidth - 10) / keys.length);

  return (
    <Box>
      <Text backgroundColor="gray" color="green" bold>
        {keys.map(({ key, label }, index) => {
          const keyDisplay = chalk.black.bgGreen(` ${key} `);
          const labelDisplay = chalk.green(` ${label}`);
          const padding = ' '.repeat(Math.max(0, keyWidth - key.length - label.length - 3));
          
          return `${keyDisplay}${labelDisplay}${padding}`;
        }).join('')}
      </Text>
    </Box>
  );
};