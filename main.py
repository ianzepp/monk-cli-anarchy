#!/usr/bin/env python3
"""
VAULT-TEC ENTERPRISE SUITE™
Main Application Entry Point

"Building Tomorrow's Business Solutions... Yesterday's Way"
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from vault_app import VaultApp

if __name__ == "__main__":
    app = VaultApp()
    app.run()