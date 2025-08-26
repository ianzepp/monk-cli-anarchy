#!/usr/bin/env node
import React from 'react';
import { render, Box, Text } from 'ink';
import chalk from 'chalk';
import { TerminalWidget } from './components/TerminalWidget';
import { StatusIndicator } from './components/StatusIndicator';

const VaultTecDemo: React.FC = () => {
  return (
    <Box flexDirection="column" paddingX={2} paddingY={1}>
      {/* Header */}
      <Text color="green" bold>
        {chalk.green(' F1  Help      F2  Search    F3  Next Module F4  Execute   F5  Refresh')}
      </Text>
      <Text> </Text>

      {/* Main Header */}
      <Box justifyContent="center" marginBottom={1}>
        <Box flexDirection="column" alignItems="center">
          <Text color="green" bold>
            ┌─ VAULT-TEC ENTERPRISE SUITE v2.0.0 ─┐
          </Text>
          <Text color="yellow">
            ▼ OVERSEER: admin@vault111 ▼
          </Text>
          <Text color="green" dimColor>
            Prepared for the Future™
          </Text>
        </Box>
      </Box>

      {/* Dashboard Grid */}
      <Box flexDirection="row" marginBottom={1}>
        {/* System Status */}
        <Box flex={1} marginRight={2}>
          <Box flexDirection="column">
            <Text color="green">┌─ SYSTEM STATUS ─────────┐</Text>
            <Text>│ ● DATABASE: OK          │</Text>
            <Text>│ ● OBSERVERS: OK         │</Text>
            <Text>│ ● SECURITY: OK          │</Text>
            <Text color="green">└─────────────────────────┘</Text>
          </Box>
        </Box>

        {/* Active Residents */}
        <Box flex={1} marginRight={2}>
          <Box flexDirection="column">
            <Text color="green">┌─ ACTIVE RESIDENTS ──────┐</Text>
            <Text>│ Total: {chalk.yellow('2,847')}           │</Text>
            <Text>│ Active: {chalk.green('2,834')}          │</Text>
            <Text>│ Offline: {chalk.red('13')}             │</Text>
            <Text color="green">└─────────────────────────┘</Text>
          </Box>
        </Box>

        {/* Alerts */}
        <Box flex={1}>
          <Box flexDirection="column">
            <Text color="yellow">┌─ ALERTS ────────────────┐</Text>
            <Text>│ {chalk.yellow('⚠')} 3 Schema Violations  │</Text>
            <Text>│ {chalk.green('●')} 0 Critical Issues    │</Text>
            <Text color="yellow">└─────────────────────────┘</Text>
          </Box>
        </Box>
      </Box>

      {/* Recent Operations */}
      <Box marginBottom={1}>
        <Box flexDirection="column">
          <Text color="green">┌─ RECENT OPERATIONS ──────────────────────────────────────────────────┐</Text>
          <Text>│ 14:32:07 | {chalk.blue('PERSONNEL')} | {chalk.green('CREATE')} | VAULT_DWELLER_2848         │</Text>
          <Text>│ 14:31:45 | {chalk.blue('SECURITY')}  | {chalk.yellow('UPDATE')} | ACCESS_CARD_ALPHA_7       │</Text>
          <Text>│ 14:30:12 | {chalk.blue('INVENTORY')} | {chalk.red('DELETE')} | STIMPAK_BATCH_A42         │</Text>
          <Text color="green">└──────────────────────────────────────────────────────────────────────┘</Text>
        </Box>
      </Box>

      {/* Action Bar */}
      <Box justifyContent="center" gap={2} marginBottom={1}>
        <Text backgroundColor="green" color="black" bold> ▶ ENTER COMMAND MODE [F9] </Text>
        <Text backgroundColor="blue" color="white" bold> ◉ VIEW DEPARTMENTS [F3] </Text>
        <Text backgroundColor="red" color="white" bold> ⚠ EMERGENCY [F10] </Text>
      </Box>

      {/* Bottom bar */}
      <Text color="green" bold>
        {chalk.green(' F6  Save      F7  Filter    F8  Status    F9  Terminal  F10  Emergency')}
      </Text>
    </Box>
  );
};

// Render the demo
render(<VaultTecDemo />);