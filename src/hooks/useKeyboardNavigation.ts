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

  // Safe keyboard shortcuts that avoid browser conflicts
  useEffect(() => {
    console.log('Keyboard navigation hook loaded');
    console.log('Current location:', location.pathname);
    
    const handleKeyDown = (event: KeyboardEvent) => {
      // Backtick (`) - Module cycling (SAFE - works perfectly)
      if (event.key === '`') {
        event.preventDefault();
        console.log('Backtick - cycling to next module');
        navigateToNextModule();
        return;
      }
      
      // Tilde (~) - Reverse module cycling  
      if (event.key === '~') {
        event.preventDefault();
        console.log('Tilde - cycling to previous module');
        const currentIndex = getCurrentModuleIndex();
        const prevIndex = currentIndex === 0 ? VAULT_MODULES.length - 1 : currentIndex - 1;
        navigateToModule(prevIndex);
        return;
      }

      // Alt+1 only (SAFE - works perfectly)
      if (event.key === '1' && event.altKey && !event.ctrlKey && !event.shiftKey) {
        event.preventDefault();
        console.log('Alt+1 - jumping to Overseer Console');
        navigateToModule(0);
        return;
      }

      // Alt+letter combinations (MUCH SAFER than Ctrl+F*)
      if (event.altKey && !event.ctrlKey && !event.shiftKey) {
        switch (event.key.toLowerCase()) {
          case 'n': // Alt+N - Next module
            event.preventDefault();
            console.log('Alt+N - Next module');
            showKeyFeedback('Alt+N');
            navigateToNextModule();
            return;
            
          case 'p': // Alt+P - Previous module  
            event.preventDefault();
            console.log('Alt+P - Previous module');
            showKeyFeedback('Alt+P');
            const currentIndex = getCurrentModuleIndex();
            const prevIndex = currentIndex === 0 ? VAULT_MODULES.length - 1 : currentIndex - 1;
            navigateToModule(prevIndex);
            return;
            
          case 'h': // Alt+H - Home (Overseer)
            event.preventDefault();
            console.log('Alt+H - Home/Overseer');
            showKeyFeedback('Alt+H');
            navigateToModule(0);
            return;
            
          case 'r': // Alt+R - Registry
            event.preventDefault();
            console.log('Alt+R - Department Registry');
            showKeyFeedback('Alt+R');
            navigateToModule(1);
            return;
            
          case 's': // Alt+S - Schema Laboratory
            event.preventDefault();
            console.log('Alt+S - Schema Laboratory');
            showKeyFeedback('Alt+S');
            navigateToModule(2);
            return;
        }
      }

      // Escape - Always go back to Overseer (SAFE)
      if (event.key === 'Escape' && !event.ctrlKey && !event.altKey && !event.shiftKey) {
        event.preventDefault();
        console.log('Escape - returning to Overseer Console');
        showKeyFeedback('ESC');
        navigateToModule(0);
        return;
      }

      // ONLY SAFE Ctrl+F key that we've confirmed works
      if (event.key === 'F3' && event.ctrlKey && !event.altKey && !event.shiftKey) {
        event.preventDefault();
        event.stopPropagation();
        console.log('Ctrl+F3 - Module cycling (CONFIRMED SAFE!)');
        showKeyFeedback('Ctrl+F3');
        navigateToNextModule();
        return;
      }
      
      // DO NOT ADD OTHER Ctrl+F* KEYS - they have dangerous browser behaviors:
      // Ctrl+F4 = Close tab (DANGEROUS!)
      // Ctrl+F5 = Hard refresh  
      // Ctrl+F6 = Switch between frames
      // etc.
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