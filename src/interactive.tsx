#!/usr/bin/env node
import React, { useState } from 'react';
import { render, Box, Text, useInput } from 'ink';
import chalk from 'chalk';

const MODULES = [
  'Overseer Console',
  'Department Registry', 
  'Schema Laboratory',
  'Population Management',
  'Security Protocols',
  'File Archives'
];

const VaultTecInteractive: React.FC = () => {
  const [currentModule, setCurrentModule] = useState(0);
  const [showHelp, setShowHelp] = useState(false);
  const [lastKey, setLastKey] = useState<string>('');
  
  // Get terminal dimensions
  const terminalWidth = process.stdout.columns || 80;
  const terminalHeight = process.stdout.rows || 24;

  useInput((input, key) => {
    // F1 - Toggle help
    if (key.f1) {
      setShowHelp(!showHelp);
      setLastKey('F1 - Help');
      return;
    }

    // F3 - Next module
    if (key.f3) {
      setCurrentModule((prev) => (prev + 1) % MODULES.length);
      setLastKey('F3 - Next Module');
      return;
    }

    // F10 - Exit
    if (key.f10) {
      setLastKey('F10 - Emergency Exit');
      process.exit(0);
    }

    // ESC - Close help or go home
    if (key.escape) {
      if (showHelp) {
        setShowHelp(false);
        setLastKey('ESC - Close Help');
      } else {
        setCurrentModule(0);
        setLastKey('ESC - Return to Overseer');
      }
      return;
    }

    // Numbers 1-6 - Direct module access
    if (['1', '2', '3', '4', '5', '6'].includes(input)) {
      const moduleIndex = parseInt(input) - 1;
      setCurrentModule(moduleIndex);
      setLastKey(`${input} - ${MODULES[moduleIndex]}`);
      return;
    }

    // Other keys
    if (input) {
      setLastKey(`'${input}' pressed`);
    }
  });

  if (showHelp) {
    return (
      <Box flexDirection="column" width={terminalWidth} height={terminalHeight}>
        {/* Top function bar */}
        <Text color="green" bold>{' '.repeat(terminalWidth)}</Text>
        <Text color="green" bold> F1  Help      F2  Search    F3  Next Module F4  Execute   F5  Refresh{' '.repeat(Math.max(0, terminalWidth - 65))}</Text>
        
        {/* Help content - fill remaining space */}
        <Box flex={1} flexDirection="column" justifyContent="center" alignItems="center">
          <Box flexDirection="column" width={60}>
            <Box justifyContent="center" marginBottom={1}>
              <Text color="green" bold>
                ┌─ VAULT-TEC HELP SYSTEM {('─').repeat(terminalWidth > 80 ? 20 : 10)} ─┐
              </Text>
            </Box>

            <Box flexDirection="column" paddingX={4}>
              <Text color="yellow" bold>NAVIGATION SHORTCUTS:</Text>
              <Text>  <Text color="green">F3</Text>     - Next Module</Text>
              <Text>  <Text color="green">1-6</Text>    - Jump to Module</Text>
              <Text>  <Text color="green">ESC</Text>    - Return to Overseer</Text>
              <Text>  <Text color="green">F10</Text>    - Emergency Exit</Text>
              <Text></Text>
              
              <Text color="yellow" bold>AVAILABLE MODULES:</Text>
              {MODULES.map((module, index) => (
                <Text key={index}>
                  {`  ${index + 1}. ${module}`}
                  {index === currentModule ? chalk.yellow(' (CURRENT)') : ''}
                </Text>
              ))}
              <Text></Text>
              <Text color="gray">Terminal Size: {terminalWidth}x{terminalHeight} | Press F1 to close help</Text>
            </Box>
            
            <Box justifyContent="center" marginTop={1}>
              <Text color="green" bold>
                └{('─').repeat(Math.max(0, terminalWidth > 80 ? 40 : 25))}┘
              </Text>
            </Box>
          </Box>
        </Box>
        
        {/* Bottom function bar */}
        <Text color="green" bold> F6  Save      F7  Filter    F8  Status    F9  Terminal  F10  Emergency{' '.repeat(Math.max(0, terminalWidth - 65))}</Text>
        <Text color="green" bold>{' '.repeat(terminalWidth)}</Text>
      </Box>
    );
  }

  return (
    <Box flexDirection="column" width={terminalWidth} height={terminalHeight}>
      {/* Top function bar - Full width */}
      <Text color="green" bold backgroundColor="gray">
        {' F1  Help      F2  Search    F3  Next Module F4  Execute   F5  Refresh'.padEnd(terminalWidth)}
      </Text>

      {/* Module indicator - Full width */}
      <Box width={terminalWidth} justifyContent="space-between" paddingX={1}>
        <Text color="green">
          OVERSEER &gt; V111_CAPITAL &gt; {MODULES[currentModule].toUpperCase()}
        </Text>
        <Text color="yellow">
          Module {currentModule + 1} of {MODULES.length} | {terminalWidth}x{terminalHeight}
        </Text>
      </Box>

      {/* Main content area - Fill remaining vertical space */}
      <Box flex={1} width={terminalWidth} flexDirection="column">
        
        {currentModule === 0 && (
          <Box flexDirection="column" paddingX={2} flex={1}>
            {/* Vault-Tec Header */}
            <Box justifyContent="center" marginY={1}>
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

            {/* Dashboard - Single full-width display instead of broken columns */}
            <Box flex={1} flexDirection="column" marginY={1}>
              <Box flexDirection="column">
                <Text color="green">┌─ VAULT-TEC ENTERPRISE DASHBOARD {('─').repeat(terminalWidth - 37)}┐</Text>
                <Text color="green">│                                                                       │</Text>
                <Text color="green">│  {chalk.green('●')} DATABASE: OK     {chalk.yellow('Total Residents: 2,847')}     {chalk.yellow('⚠')} 3 Schema Violations  │</Text>
                <Text color="green">│  {chalk.green('●')} OBSERVERS: OK    {chalk.green('Active: 2,834')}            {chalk.green('●')} 0 Critical Issues    │</Text>
                <Text color="green">│  {chalk.green('●')} SECURITY: OK     {chalk.red('Offline: 13')}               Security Level: HIGH      │</Text>
                <Text color="green">│                                                                       │</Text>
                <Text color="green">├─ RECENT OPERATIONS {('─').repeat(terminalWidth - 24)}┤</Text>
                <Text color="green">│ 14:32:07 | {chalk.blue('PERSONNEL')} | {chalk.green('CREATE')} | VAULT_DWELLER_2848{' '.repeat(Math.max(0, terminalWidth - 55))}│</Text>
                <Text color="green">│ 14:31:45 | {chalk.blue('SECURITY')}  | {chalk.yellow('UPDATE')} | ACCESS_CARD_ALPHA_7{' '.repeat(Math.max(0, terminalWidth - 54))}│</Text>
                <Text color="green">│ 14:30:12 | {chalk.blue('INVENTORY')} | {chalk.red('DELETE')} | STIMPAK_BATCH_A42{' '.repeat(Math.max(0, terminalWidth - 52))}│</Text>
                <Text color="green">│{' '.repeat(terminalWidth - 2)}│</Text>
                <Text color="green">└{('─').repeat(terminalWidth - 2)}┘</Text>
              </Box>
            </Box>


            {/* Action Bar */}
            <Box justifyContent="center" gap={2} marginY={1}>
              <Text backgroundColor="green" color="black" bold> ▶ ENTER COMMAND MODE [F9] </Text>
              <Text backgroundColor="blue" color="white" bold> ◉ VIEW DEPARTMENTS [F3] </Text>
              <Text backgroundColor="red" color="white" bold> ⚠ EMERGENCY [F10] </Text>
            </Box>
          </Box>
        )}
        
        {currentModule !== 0 && (
          <Box flex={1} justifyContent="center" alignItems="center">
            <Box flexDirection="column" alignItems="center">
              <Text color="green" bold>
                ┌─ {MODULES[currentModule].toUpperCase()} {('─').repeat(Math.max(0, 40 - MODULES[currentModule].length))} ─┐
              </Text>
              <Text color="yellow">
                ▼ VAULT MODULE {currentModule + 1} OF {MODULES.length} ▼
              </Text>
              <Text> </Text>
              
              <Box flexDirection="column" alignItems="center">
                <Text color="yellow">🚧 MODULE UNDER CONSTRUCTION 🚧</Text>
                <Text> </Text>
                <Text color="gray">This module will feature:</Text>
                <Text color="green">• Terminal-native interface using full {terminalWidth}x{terminalHeight}</Text>
                <Text color="green">• Complete keyboard navigation (F1-F12)</Text>
                <Text color="green">• Real-time Monk API integration</Text>
                <Text color="green">• Authentic Fallout terminal styling</Text>
                <Text color="green">• Scrollable content areas</Text>
                <Text color="green">• Interactive forms and tables</Text>
              </Box>
              
              <Text> </Text>
              <Text color="green" bold>
                └{('─').repeat(Math.max(0, 40 - MODULES[currentModule].length + 10))}┘
              </Text>
            </Box>
          </Box>
        )}
      </Box>

      {/* Status bar - Full width */}
      <Box width={terminalWidth} justifyContent="space-between" paddingX={1}>
        <Text color="green">Last Key: {chalk.yellow(lastKey || 'None')}</Text>
        <Text color="gray">Press F1 for help, F10 to exit</Text>
      </Box>
      
      {/* Bottom function bar - Full width */}
      <Text color="green" bold backgroundColor="gray">
        {' F6  Save      F7  Filter    F8  Status    F9  Terminal  F10  Emergency'.padEnd(terminalWidth)}
      </Text>
    </Box>
  );
};

render(<VaultTecInteractive />);