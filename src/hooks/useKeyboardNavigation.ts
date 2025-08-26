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
      // Prevent default browser behavior for our function keys
      const functionKeys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12'];
      if (functionKeys.includes(event.key)) {
        event.preventDefault();
      }

      // F3 - Module cycling
      if (event.key === 'F3' && !event.ctrlKey && !event.altKey && !event.shiftKey) {
        event.preventDefault();
        navigateToNextModule();
        return;
      }

      // Alt + Number - Direct module jumping
      if (event.altKey && !event.ctrlKey && !event.shiftKey) {
        const number = parseInt(event.key);
        if (number >= 1 && number <= 6) {
          event.preventDefault();
          navigateToModule(number - 1); // Convert to 0-based index
          return;
        }
      }

      // F1 - Help (placeholder for now)
      if (event.key === 'F1' && !event.ctrlKey && !event.altKey && !event.shiftKey) {
        event.preventDefault();
        showKeyFeedback('F1');
        console.log('F1 Help - Current module:', VAULT_MODULES[getCurrentModuleIndex()]?.name);
        return;
      }

      // F5 - Refresh
      if (event.key === 'F5' && !event.ctrlKey && !event.altKey && !event.shiftKey) {
        event.preventDefault();
        showKeyFeedback('F5');
        window.location.reload();
        return;
      }

      // F9 - Command Terminal (placeholder for now)
      if (event.key === 'F9' && !event.ctrlKey && !event.altKey && !event.shiftKey) {
        event.preventDefault();
        showKeyFeedback('F9');
        console.log('F9 Command Terminal - Not yet implemented');
        return;
      }

      // F11 - Fullscreen toggle
      if (event.key === 'F11' && !event.ctrlKey && !event.altKey && !event.shiftKey) {
        event.preventDefault();
        showKeyFeedback('F11');
        if (document.fullscreenElement) {
          document.exitFullscreen();
        } else {
          document.documentElement.requestFullscreen();
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