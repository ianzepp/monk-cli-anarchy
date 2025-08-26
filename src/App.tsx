import React from 'react';
import { GlobalTerminalStyles } from './styles/global-styles';
import { OverseerConsole } from './modules/OverseerConsole';

function App() {
  return (
    <>
      <GlobalTerminalStyles />
      <OverseerConsole />
    </>
  );
}

export default App;
