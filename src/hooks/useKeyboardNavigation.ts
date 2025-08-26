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

  // Navigate to next module (F3 cycling)
  const navigateToNextModule = () => {
    const currentIndex = getCurrentModuleIndex();
    const nextIndex = (currentIndex + 1) % VAULT_MODULES.length;
    const nextModule = VAULT_MODULES[nextIndex];
    showKeyFeedback('F3');
    navigate(nextModule.path);
  };

  // Navigate to specific module by index (Alt+1-6)
  const navigateToModule = (moduleIndex: number) => {
    if (moduleIndex >= 0 && moduleIndex < VAULT_MODULES.length) {
      const module = VAULT_MODULES[moduleIndex];
      showKeyFeedback(`Alt+${moduleIndex + 1}`);
      navigate(module.path);
    }
  };

  // Global keyboard event handler
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Debug logging
      console.log('Key pressed:', event.key, 'Ctrl:', event.ctrlKey, 'Alt:', event.altKey);
      
      // SAFE NAVIGATION SHORTCUTS (avoid browser conflicts)
      
      // Shift+Tab - Module cycling (safe alternative)
      if (event.key === 'Tab' && event.shiftKey && !event.ctrlKey && !event.altKey) {
        event.preventDefault();
        event.stopPropagation();
        console.log('Shift+Tab pressed - cycling modules');
        navigateToNextModule();
        return;
      }

      // Ctrl+Shift+Numbers - Direct module jumping (very safe)
      if (event.ctrlKey && event.shiftKey && !event.altKey && /^[1-6]$/.test(event.key)) {
        const number = parseInt(event.key);
        event.preventDefault();
        event.stopPropagation();
        console.log(`Ctrl+Shift+${number} pressed - jumping to module ${number}`);
        navigateToModule(number - 1);
        return;
      }

      // Simple navigation shortcuts (try to avoid conflicts)
      
      // Backtick (`) for module cycling
      if (event.key === '`' && !event.ctrlKey && !event.altKey && !event.shiftKey) {
        event.preventDefault();
        event.stopPropagation();
        console.log('Backtick pressed - cycling modules');
        navigateToNextModule();
        return;
      }

      // Number keys with Alt (safer than Ctrl+numbers)
      if (event.altKey && !event.ctrlKey && !event.shiftKey && /^[1-6]$/.test(event.key)) {
        const number = parseInt(event.key);
        event.preventDefault();
        event.stopPropagation();
        console.log(`Alt+${number} pressed - jumping to module ${number}`);
        navigateToModule(number - 1);
        return;
      }

      // Try simple F3 (best effort)
      if (event.key === 'F3' && !event.ctrlKey && !event.altKey && !event.shiftKey) {
        try {
          event.preventDefault();
          event.stopPropagation();
          console.log('F3 pressed - cycling modules');
          navigateToNextModule();
        } catch (error) {
          console.error('F3 navigation error:', error);
        }
        return;
      }
    };

    // Add event listener to document
    document.addEventListener('keydown', handleKeyDown);

    // Cleanup on unmount
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [navigate, location.pathname]);

  // Return current module info for use in components
  return {
    currentModule: VAULT_MODULES[getCurrentModuleIndex()],
    currentModuleIndex: getCurrentModuleIndex(),
    navigateToModule,
    navigateToNextModule,
    pressedKey,
  };
};