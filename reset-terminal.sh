#!/bin/bash

# Emergency terminal reset script
# Use this if mouse reporting gets stuck

echo "Emergency terminal reset..."
echo "Option 1: Preserve text selection (recommended)"
printf '\e[?1003l\e[?1015l\e[?1006l\e[?25h'

echo "Option 2: Full reset (if still having issues)"
echo "Run: printf '\\e[?1000l\\e[?1003l\\e[?1015l\\e[?1006l\\e[?25h' && stty sane && reset"

tput rmcup 2>/dev/null || true
clear
echo "Terminal reset complete. Text selection should now work."