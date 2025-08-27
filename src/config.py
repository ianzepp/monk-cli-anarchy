"""
VAULT-TEC ENTERPRISE SUITE™
Configuration Management
"""

import os
from typing import Optional


class VaultConfig:
    """Global configuration for Vault-Tec Enterprise Suite"""
    
    def __init__(self):
        self.overseer_always = self._get_bool_env("OVERSEER_ALWAYS", True)  # Default to True for development
        self.debug_mode = self._get_bool_env("DEBUG", False)
        self.api_base_url = os.getenv("MONK_API_URL", "http://localhost:9001")
        self.default_tenant = os.getenv("DEFAULT_TENANT", "test-1756112139")
        self.default_username = os.getenv("DEFAULT_USERNAME", "root")
    
    def _get_bool_env(self, key: str, default: bool = False) -> bool:
        """Get boolean environment variable"""
        value = os.getenv(key, "").lower()
        if value in ("true", "1", "yes", "on"):
            return True
        elif value in ("false", "0", "no", "off"):
            return False
        return default
    
    @property
    def is_overseer_mode(self) -> bool:
        """Check if running in overseer mode (bypass authentication)"""
        return self.overseer_always


# Global configuration instance
config = VaultConfig()