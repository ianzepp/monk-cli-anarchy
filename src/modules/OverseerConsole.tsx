import React from 'react';
import { Box, Text } from 'ink';
import chalk from 'chalk';
import { TerminalWidget } from '../components/TerminalWidget';
import { StatusIndicator } from '../components/StatusIndicator';

export const OverseerConsole: React.FC = () => {
  return (
    <Box flexDirection="column" paddingX={2} paddingY={1}>
      {/* Main Header */}
      <Box justifyContent="center" marginBottom={1}>
        <Box 
          borderStyle="round" 
          borderColor="green"
          paddingX={2}
          paddingY={1}
        >
          <Box flexDirection="column" alignItems="center">
            <Text color="green" bold>
              {chalk.green('┌─ VAULT-TEC ENTERPRISE SUITE v2.0.0 ─┐')}
            </Text>
            <Text color="yellow" dimColor>
              ▼ OVERSEER: admin@vault111 ▼
            </Text>
            <Text color="green" dimColor>
              Prepared for the Future™
            </Text>
          </Box>
        </Box>
      </Box>

      {/* Dashboard Grid - Side by side widgets */}
      <Box marginBottom={1}>
        <Box flexDirection="row" width="100%">
          {/* System Status */}
          <Box flex={1} marginRight={2}>
            <TerminalWidget title="SYSTEM STATUS" width={25}>
              <StatusIndicator status="ok">DATABASE: OK</StatusIndicator>
              <StatusIndicator status="ok">OBSERVERS: OK</StatusIndicator>
              <StatusIndicator status="ok">SECURITY: OK</StatusIndicator>
            </TerminalWidget>
          </Box>

          {/* Active Residents */}
          <Box flex={1} marginRight={2}>
            <TerminalWidget title="ACTIVE RESIDENTS" width={25}>
              <Text>Total: {chalk.yellow('2,847')}</Text>
              <Text>Active: {chalk.green('2,834')}</Text>
              <Text>Offline: {chalk.red('13')}</Text>
            </TerminalWidget>
          </Box>

          {/* Alerts */}
          <Box flex={1}>
            <TerminalWidget title="ALERTS" width={25} borderColor="yellow">
              <StatusIndicator status="warning">3 Schema Violations</StatusIndicator>
              <StatusIndicator status="ok">0 Critical Issues</StatusIndicator>
            </TerminalWidget>
          </Box>
        </Box>
      </Box>

      {/* Recent Operations */}
      <Box marginBottom={1}>
        <TerminalWidget title="RECENT OPERATIONS" width={78}>
          <Text>14:32:07 | {chalk.blue('PERSONNEL')} | {chalk.green('CREATE')} | VAULT_DWELLER_2848</Text>
          <Text>14:31:45 | {chalk.blue('SECURITY')}  | {chalk.yellow('UPDATE')} | ACCESS_CARD_ALPHA_7</Text>
          <Text>14:30:12 | {chalk.blue('INVENTORY')} | {chalk.red('DELETE')} | STIMPAK_BATCH_A42</Text>
        </TerminalWidget>
      </Box>

      {/* Action Bar */}
      <Box justifyContent="center" gap={2}>
        <Text backgroundColor="green" color="black" bold> ▶ ENTER COMMAND MODE [F9] </Text>
        <Text backgroundColor="blue" color="white" bold> ◉ VIEW DEPARTMENTS [F3] </Text>
        <Text backgroundColor="red" color="white" bold> ⚠ EMERGENCY [F10] </Text>
      </Box>
    </Box>
  );
};