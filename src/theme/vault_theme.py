"""
VAULT-TEC ENTERPRISE SUITE™ 
Terminal Theme Configuration

Color Palette: "Radiation Spectrum"
"""

VAULT_CSS = """
/* ===== COLOR VARIABLES (MUST BE FIRST) ===== */
/* Primary Colors */
$vault-green: #00ff00;
$amber-alert: #ffb000; 
$rad-red: #ff3030;
$steel-blue: #1e3a8a;

/* Background Tones */
$bunker-black: #0a0a0a;
$shadow-gray: #1a1a1a;
$dust-brown: #4a3c2a;

/* Status Colors */
$healthy-green: #22c55e;
$caution-yellow: #f59e0b;
$danger-red: #dc2626;
$offline-gray: #6b7280;

/* ===== GLOBAL VAULT-TEC THEME ===== */

* {
    scrollbar-background: $bunker-black;
    scrollbar-color: $vault-green;
    scrollbar-color-hover: $amber-alert;
}

App {
    background: $bunker-black;
    color: $vault-green;
}

/* ===== HEADER STYLES ===== */
Header {
    background: $shadow-gray;
    color: $vault-green;
    text-style: bold;
    dock: top;
    height: 3;
}

Header .title {
    color: $vault-green;
    text-style: bold;
}

Header .subtitle {
    color: $amber-alert;
    text-style: italic;
}

/* ===== FOOTER STYLES ===== */
Footer {
    background: $shadow-gray;
    color: $vault-green;
    dock: bottom;
    height: 1;
}

Footer .key {
    background: $bunker-black;
    color: $vault-green;
    text-style: bold;
}

Footer .description {
    color: $amber-alert;
}

/* ===== CONTAINER STYLES ===== */
Container {
    background: $bunker-black;
    border: solid $vault-green;
    border-title-color: $amber-alert;
    border-title-style: bold;
}

/* ===== WIDGET STYLES ===== */
Static {
    color: $vault-green;
}

Label {
    color: $vault-green;
}

Button {
    background: $bunker-black;
    color: $vault-green;
    border: solid $vault-green;
    text-style: bold;
}

Button:hover {
    background: $shadow-gray;
    border: solid $amber-alert;
    color: $amber-alert;
}

Button:focus {
    background: $amber-alert;
    color: $bunker-black;
    text-style: bold;
}

Button.-primary {
    background: $vault-green;
    color: $bunker-black;
    border: solid $vault-green;
}

Button.-primary:hover {
    background: $amber-alert;
    color: $bunker-black;
    border: solid $amber-alert;
}

Button.-danger {
    background: $bunker-black;
    color: $rad-red;
    border: solid $rad-red;
}

Button.-danger:hover {
    background: $rad-red;
    color: $bunker-black;
    border: solid $rad-red;
}

/* ===== INPUT STYLES ===== */
Input {
    background: $bunker-black;
    color: $vault-green;
    border: solid $vault-green;
}

Input:focus {
    border: solid $amber-alert;
}

Input.-invalid {
    border: solid $rad-red;
    color: $rad-red;
}

/* ===== STATUS INDICATORS ===== */
.status-ok {
    color: $healthy-green;
}

.status-warning {
    color: $caution-yellow;
}

.status-error {
    color: $danger-red;
}

.status-offline {
    color: $offline-gray;
}

/* ===== SPECIAL ELEMENTS ===== */
.vault-title {
    color: $vault-green;
    text-style: bold;
}

.security-clearance {
    color: $amber-alert;
    text-style: bold;
}

.system-message {
    color: $steel-blue;
    text-style: italic;
}

.terminal-prompt {
    color: $vault-green;
    text-style: bold;
}

.danger-text {
    color: $rad-red;
    text-style: bold;
}

/* ===== ANIMATIONS ===== */
.alert-flash {
    color: $rad-red;
}

.status-pulse {
    color: $amber-alert;
}

/* ===== SCREEN-SPECIFIC ===== */
.auth-screen {
    background: $bunker-black;
}

.overseer-dashboard {
    background: $bunker-black;
}

.schema-lab {
    background: $bunker-black;
}

.wasteland-testing {
    background: $bunker-black;
}
"""