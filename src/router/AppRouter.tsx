import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { VaultShell } from '../components/layout/VaultShell';
import { OverseerConsole } from '../modules/OverseerConsole';
import { DepartmentRegistry } from '../modules/DepartmentRegistry';
import { SchemaLaboratory } from '../modules/SchemaLaboratory';
import { PopulationManagement } from '../modules/PopulationManagement';
import { SecurityProtocols } from '../modules/SecurityProtocols';
import { FileArchives } from '../modules/FileArchives';
import { VaultError } from '../modules/VaultError';

export const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <VaultShell>
        <Routes>
          {/* Default route - Overseer Console */}
          <Route path="/" element={<OverseerConsole />} />
          
          {/* Main vault modules */}
          <Route path="/registry" element={<DepartmentRegistry />} />
          <Route path="/schema" element={<SchemaLaboratory />} />
          <Route path="/population" element={<PopulationManagement />} />
          <Route path="/security" element={<SecurityProtocols />} />
          <Route path="/files" element={<FileArchives />} />
          
          {/* Overseer Console (explicit route) */}
          <Route path="/overseer" element={<OverseerConsole />} />
          
          {/* 404 and error routes */}
          <Route path="/error" element={<VaultError errorType="system-failure" />} />
          <Route path="/access-denied" element={<VaultError errorType="access-denied" />} />
          
          {/* Catch-all 404 route */}
          <Route 
            path="*" 
            element={
              <VaultError 
                errorCode="404"
                errorMessage="Vault section not found in database"
                errorType="not-found"
              />
            } 
          />
        </Routes>
      </VaultShell>
    </BrowserRouter>
  );
};