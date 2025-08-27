#!/bin/bash

# Reset terminal state
printf '\e[?1000l\e[?1003l\e[?1015l\e[?1006l'
clear

# Activate virtual environment and run the app
source venv/bin/activate
python main.py

# Reset terminal state again on exit
printf '\e[?1000l\e[?1003l\e[?1015l\e[?1006l'