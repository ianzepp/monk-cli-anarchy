import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { VAULT_MODULES } from '../types/navigation';

export const useKeyboardNavigation = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [pressedKey, setPressedKey] = useState<string | null>(null);

  // Get current module index for F3 cycling
  const getCurrentModuleIndex = (): number => {
    const currentPath = location.pathname;
    const moduleIndex = VAULT_MODULES.findIndex(module => module.path === currentPath);
    return moduleIndex >= 0 ? moduleIndex : 0; // Default to Overseer Console
  };

  // Show key feedback
  const showKeyFeedback = (key: string, duration: number = 800) => {
    setPressedKey(key);
    setTimeout(() => setPressedKey(null), duration);
  };

  // Navigate to next module (F3 cycling) - using safe window.location method
  const navigateToNextModule = () => {
    const currentIndex = getCurrentModuleIndex();
    const nextIndex = (currentIndex + 1) % VAULT_MODULES.length;
    const nextModule = VAULT_MODULES[nextIndex];
    showKeyFeedback('Next');
    console.log(`Navigating to: ${nextModule.path} (${nextModule.name})`);
    window.location.href = nextModule.path;
  };

  // Navigate to specific module by index (Alt+1-6) - using safe window.location method
  const navigateToModule = (moduleIndex: number) => {
    if (moduleIndex >= 0 && moduleIndex < VAULT_MODULES.length) {
      const module = VAULT_MODULES[moduleIndex];
      showKeyFeedback(`Module ${moduleIndex + 1}`);
      console.log(`Navigating to: ${module.path} (${module.name})`);
      window.location.href = module.path;
    }
  };

  // Simple keyboard handler for testing
  useEffect(() => {
    console.log('Keyboard navigation hook loaded');
    console.log('Current location:', location.pathname);
    
    const handleKeyDown = (event: KeyboardEvent) => {
      console.log('Key pressed:', event.key);
      
      // Simple backtick test
      if (event.key === '`') {
        console.log('Backtick pressed - attempting navigation');
        event.preventDefault();
        navigateToNextModule();
      }
      
      // Simple Alt+1 test
      if (event.key === '1' && event.altKey) {
        console.log('Alt+1 pressed - attempting navigation to overseer');
        event.preventDefault();
        navigateToModule(0);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [location.pathname]);

  // Return current module info for use in components
  return {
    currentModule: VAULT_MODULES[getCurrentModuleIndex()],
    currentModuleIndex: getCurrentModuleIndex(),
    navigateToModule,
    navigateToNextModule,
    pressedKey,
  };
};