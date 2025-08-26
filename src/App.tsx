import React from 'react';
import { GlobalTerminalStyles } from './styles/global-styles';
import { AppRouter } from './router/AppRouter';

function App() {
  return (
    <>
      <GlobalTerminalStyles />
      <AppRouter />
    </>
  );
}

export default App;
