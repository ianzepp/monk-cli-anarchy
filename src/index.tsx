#!/usr/bin/env node
import React, { useState, useEffect } from 'react';
import { render, Box, Text, useInput } from 'ink';
import chalk from 'chalk';
import { FunctionKeyBar } from './components/FunctionKeyBar';
import { OverseerConsole } from './modules/OverseerConsole';

// Module definitions
const MODULES = [
  { id: 'overseer', name: 'Overseer Console', component: OverseerConsole },
  { id: 'registry', name: 'Department Registry', component: () => <Text>Registry Module - Coming Soon</Text> },
  { id: 'schema', name: 'Schema Laboratory', component: () => <Text>Schema Module - Coming Soon</Text> },
  { id: 'population', name: 'Population Management', component: () => <Text>Population Module - Coming Soon</Text> },
  { id: 'security', name: 'Security Protocols', component: () => <Text>Security Module - Coming Soon</Text> },
  { id: 'files', name: 'File Archives', component: () => <Text>Files Module - Coming Soon</Text> },
];

const VaultTecApp: React.FC = () => {
  const [currentModuleIndex, setCurrentModuleIndex] = useState(0);
  const [showHelp, setShowHelp] = useState(false);
  
  const currentModule = MODULES[currentModuleIndex];
  const CurrentComponent = currentModule.component;

  // Handle keyboard input
  useInput((input, key) => {
    // F1 - Help toggle
    if (key.f1) {
      setShowHelp(!showHelp);
      return;
    }
    
    // F3 - Next module
    if (key.f3) {
      setCurrentModuleIndex((prev) => (prev + 1) % MODULES.length);
      return;
    }
    
    // F10 - Emergency (exit)
    if (key.f10) {
      process.exit(0);
    }
    
    // ESC - Close help or go to overseer
    if (key.escape) {
      if (showHelp) {
        setShowHelp(false);
      } else {
        setCurrentModuleIndex(0);
      }
      return;
    }

    // Alt+Number - Direct module access
    const numbers = ['1', '2', '3', '4', '5', '6'];
    if (key.alt && numbers.includes(input)) {
      const moduleIndex = parseInt(input) - 1;
      if (moduleIndex >= 0 && moduleIndex < MODULES.length) {
        setCurrentModuleIndex(moduleIndex);
      }
      return;
    }

    // Backtick - Next module (like web version)
    if (input === '`') {
      setCurrentModuleIndex((prev) => (prev + 1) % MODULES.length);
      return;
    }
    
    // Tilde - Previous module
    if (input === '~') {
      setCurrentModuleIndex((prev) => prev === 0 ? MODULES.length - 1 : prev - 1);
      return;
    }
  });

  if (showHelp) {
    return (
      <Box flexDirection="column" padding={1}>
        <FunctionKeyBar position="top" />
        
        <Box justifyContent="center" marginY={1}>
          <Text color="green" bold>
            {chalk.green('┌─ VAULT-TEC HELP SYSTEM ─┐')}
          </Text>
        </Box>

        <Box flexDirection="column" paddingX={4}>
          <Text color="yellow" bold>NAVIGATION SHORTCUTS:</Text>
          <Text>  <Text color="green">F3</Text> or <Text color="green">`</Text>     - Next Module</Text>
          <Text>  <Text color="green">~</Text>           - Previous Module</Text>
          <Text>  <Text color="green">Alt+1-6</Text>     - Jump to Module</Text>
          <Text>  <Text color="green">ESC</Text>         - Return to Overseer</Text>
          <Text></Text>
          
          <Text color="yellow" bold>FUNCTION KEYS:</Text>
          <Text>  <Text color="green">F1</Text>          - Toggle Help</Text>
          <Text>  <Text color="green">F10</Text>         - Emergency Exit</Text>
          <Text></Text>
          
          <Text color="yellow" bold>MODULES:</Text>
          {MODULES.map((module, index) => (
            <Text key={module.id}>
              {`  ${index + 1}. ${module.name}`}
              {index === currentModuleIndex ? chalk.yellow(' (CURRENT)') : ''}
            </Text>
          ))}
        </Box>
        
        <Box justifyContent="center" marginY={1}>
          <Text color="gray">Press ESC to close help, F1 to toggle</Text>
        </Box>
        
        <FunctionKeyBar position="bottom" />
      </Box>
    );
  }

  return (
    <Box flexDirection="column" width="100%" height="100%">
      <FunctionKeyBar position="top" />
      
      {/* Module indicator */}
      <Box justifyContent="space-between" paddingX={2} marginY={1}>
        <Text color="green">
          OVERSEER &gt; V111_CAPITAL &gt; {currentModule.name.toUpperCase()}
        </Text>
        <Text color="yellow">
          Module {currentModuleIndex + 1} of {MODULES.length}
        </Text>
      </Box>

      {/* Current module content */}
      <Box flex={1} flexDirection="column">
        <CurrentComponent />
      </Box>

      <FunctionKeyBar position="bottom" />
    </Box>
  );
};

// Render the app
render(<VaultTecApp />);