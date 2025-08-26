import React from 'react';
import { Text } from 'ink';
import chalk from 'chalk';

interface StatusIndicatorProps {
  status: 'ok' | 'warning' | 'error' | 'offline';
  children: React.ReactNode;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({ status, children }) => {
  const getStatusIcon = () => {
    switch (status) {
      case 'ok': return chalk.green('●');
      case 'warning': return chalk.yellow('⚠');
      case 'error': return chalk.red('◐');
      case 'offline': return chalk.gray('○');
      default: return chalk.green('●');
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'ok': return 'green';
      case 'warning': return 'yellow';
      case 'error': return 'red';
      case 'offline': return 'gray';
      default: return 'green';
    }
  };

  return (
    <Text>
      {getStatusIcon()} <Text color={getStatusColor()}>{children}</Text>
    </Text>
  );
};