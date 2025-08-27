# AUTHENTICATION MODULE
## Vault-Tec Network Access Terminal Interface Design

*"Security clearance protocols ensure only authorized personnel access vault facilities."*

---

## 🔐 **MODULE OVERVIEW**

The Authentication module provides secure access to Vault-Tec facilities through integration with the existing Monk CLI server management system. The interface leverages the `~/.config/monk/servers.json` file for server configurations and JWT token storage, presenting a corporate-themed authentication experience.

**Core Philosophy:**
- Seamless integration with existing CLI infrastructure
- Smart authentication flow prioritizing convenience and security
- Visual server status and authentication state management
- Professional vault facility access protocols

**Integration Points:**
- **Server Configuration**: Uses `~/.config/monk/servers.json` for server definitions
- **JWT Management**: Stores and validates authentication tokens per server
- **Status Monitoring**: Displays server connectivity and authentication status
- **Multi-tenant Support**: Handles multiple vault connections simultaneously

---

## 📁 **servers.json Structure Reference**

```json
{
  "servers": {
    "server_name": {
      "hostname": "localhost",
      "port": 9001,
      "protocol": "http",
      "description": "Server description",
      "added_at": "2025-08-22T01:25:19Z",
      "last_ping": "2025-08-22T01:29:59Z",
      "status": "up|down",
      "jwt_token": "eyJhbGciOiJIUzI1NiIs..." // When authenticated
    }
  },
  "current": "server_name"
}
```

**Authentication Flow:**
1. **tenant** (vault identifier) + **username** (default: "root") + **password**
2. **JWT token** returned and stored in server configuration
3. **Current server** selection maintained across sessions

---

## 🖥️ **SCREEN DESIGNS**

### **1. Main Authentication Dashboard**
```
┌─ VAULT-TEC NETWORK ACCESS TERMINAL ─────────────────────────────┐
│                 ▼ SELECT VAULT CONNECTION ▼                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ AUTHENTICATED VAULT CONNECTIONS:                                │
│ ┌─ ACTIVE SESSION ─────────────────────────────────────────────┐ │
│ │ ● dev          │ localhost:9001 │ test-1756112139 │ [ENTER]  │ │  
│ │   Description: Development server                            │ │
│ │   Last Access: 2025-08-22 01:29:59 │ Token Valid: ✅        │ │
│ └─────────────────────────────────────────────────────────────── │ │
│                                                                 │
│ AVAILABLE VAULT CONNECTIONS:                                    │
│ ┌─ REQUIRES AUTHENTICATION ───────────────────────────────────┐  │
│ │ ○ local        │ localhost:9001 │ (not authenticated) │[AUTH]│  │
│ │ ○ test         │ localhost:3009 │ (not authenticated) │[AUTH]│  │
│ │ ◐               │ localhost:3001 │ (connection failed) │[FIX] │  │
│ └─────────────────────────────────────────────────────────────── │ │
│                                                                 │
│ [▶ CONNECT TO SELECTED] [◉ ADD NEW VAULT] [○ REMOVE VAULT]     │
│                                                                 │
│ Current Selection: dev (authenticated)                          │
│ Status: Ready for immediate access                              │
└─────────────────────────────────────────────────────────────────┘

Navigation:
- ↑/↓ arrows: Select server
- Enter: Connect to authenticated server OR authenticate if needed  
- Ctrl+N: Add new server
- Ctrl+D: Remove selected server
- F5: Refresh connection status
```

### **2. Quick Server Selection (Multiple Authenticated)**
```
┌─ QUICK VAULT ACCESS ────────────────────────────────────────────┐
│ Multiple authenticated vault connections available              │
│                                                                 │
│ ► dev          │ localhost:9001 │ Development server            │
│   local        │ localhost:9001 │ Local testing environment    │  
│   prod-east    │ prod-east:443  │ Production East Coast        │
│   staging      │ staging:443    │ Staging environment          │
│                                                                 │
│ [ENTER] Connect │ [TAB] Manage Servers │ [ESC] Cancel           │
│                                                                 │
│ Selected: dev → tenant: test-1756112139                        │
└─────────────────────────────────────────────────────────────────┘
```

### **3. New Server Registration**
```
┌─ NEW VAULT CONNECTION REGISTRATION ─────────────────────────────┐
│ Register a new Vault-Tec facility for network access           │
│                                                                 │
│ CONNECTION DETAILS:                                             │
│ Server Name:  [production_east_______] (internal reference)    │
│ Hostname:     [vault-prod-east.corp__] (server address)        │
│ Port:         [443] Protocol: [https ▼]                       │
│ Description:  [Production East Coast Facility______]          │
│                                                                 │
│ INITIAL AUTHENTICATION:                                         │
│ Tenant (Vault): [vault_111_____________] (vault identifier)    │
│ Username:       [root__________________] (vault officer)       │
│ Password:       [••••••••••••••••••••••] (security key)       │
│                                                                 │
│ CONNECTION TEST:                                                │
│ ○ Not tested │ Testing... │ ✅ Connection successful           │
│                                                                 │
│ [▶ TEST CONNECTION] [◉ SAVE & AUTHENTICATE] [○ CANCEL]         │
│                                                                 │
│ Note: Connection will be saved and JWT token stored on success │
└─────────────────────────────────────────────────────────────────┘
```

### **4. Re-authentication Screen (Expired/Missing JWT)**
```
┌─ VAULT ACCESS RE-AUTHENTICATION ────────────────────────────────┐
│ Session expired for: dev (localhost:9001)                      │
│ 📋 "Authentication credentials required for facility access."   │
│                                                                 │
│ VAULT CONNECTION:                                               │
│ Server: dev (localhost:9001)                                   │
│ Status: ●ONLINE │ Last successful connection: 2025-08-22       │
│                                                                 │
│ RE-AUTHENTICATION REQUIRED:                                     │
│ Tenant (Vault): [test-1756112139______] (from saved config)    │
│ Username:       [root__________________] (default)             │
│ Password:       [••••••••••••••••••••••] (enter credentials)   │
│                                                                 │
│ ☑ Remember authentication (store JWT token)                   │
│ ☐ Set as default vault connection                             │
│                                                                 │
│ [▶ RE-AUTHENTICATE] [◉ CANCEL] [○ REMOVE SERVER]              │
│                                                                 │
│ Previous session expired: Token validation failed              │
│ Estimated session duration: 24 hours                          │
└─────────────────────────────────────────────────────────────────┘
```

### **5. Authentication in Progress**
```
┌─ ESTABLISHING VAULT CONNECTION ─────────────────────────────────┐
│ 📡 Connecting to vault facility...                             │
│                                                                 │
│ CONNECTION STATUS:                                              │
│ Server: dev (localhost:9001)                                   │
│ Tenant: test-1756112139                                        │
│ User: root                                                     │
│                                                                 │
│ AUTHENTICATION PHASES:                                          │
│ ✅ Network connection established                               │
│ ✅ Server handshake completed                                  │  
│ ⏳ Validating credentials...                                   │
│ ⏳ Retrieving security clearance...                            │
│ ⏳ Initializing vault session...                               │
│                                                                 │
│ [◉ CANCEL AUTHENTICATION]                                       │
│                                                                 │
│ Please wait while your security clearance is verified...       │
└─────────────────────────────────────────────────────────────────┘
```

### **6. Authentication Success**
```
┌─ VAULT ACCESS GRANTED ──────────────────────────────────────────┐
│ ✅ Successfully authenticated to vault facility                │
│                                                                 │
│ SECURITY CLEARANCE CONFIRMED:                                   │
│ Vault: test-1756112139                                         │
│ Officer: root                                                  │
│ Clearance Level: OVERSEER                                      │
│ Session Valid Until: 2025-08-23 01:30:00                      │
│                                                                 │
│ AVAILABLE VAULT SERVICES:                                       │
│ ✅ Personnel Management System                                  │
│ ✅ Schema Laboratory Access                                     │
│ ✅ Security Protocol Monitoring                                 │
│ ✅ Wasteland Testing Facility                                   │
│ ⚠️  Administrative Functions (Limited)                          │
│                                                                 │
│ [▶ ENTER VAULT FACILITY] [◉ CHANGE VAULT] [○ LOGOUT]          │
│                                                                 │
│ Welcome to Vault-Tec Enterprise Suite™                         │
│ "Building Tomorrow's Business Solutions... Yesterday's Way"     │
└─────────────────────────────────────────────────────────────────┘
```

### **7. Server Management Interface**
```
┌─ VAULT CONNECTION MANAGEMENT ───────────────────────────────────┐
│ Manage saved vault facility connections                        │
│                                                                 │
│ ┌─ CONFIGURED SERVERS ──────────────────────────────────────────┐ │
│ │ NAME    │ ADDRESS        │ STATUS │ AUTHENTICATED │ ACTIONS   │ │
│ │ dev     │ localhost:9001 │ ●UP    │ ✅ VALID      │ [E][T][X] │ │
│ │ local   │ localhost:9001 │ ●UP    │ ❌ NONE       │ [E][T][X] │ │
│ │ test    │ localhost:3009 │ ●UP    │ ❌ NONE       │ [E][T][X] │ │
│ │ (empty) │ localhost:3001 │ ◐DOWN  │ ❌ NONE       │ [E][T][X] │ │
│ └─────────────────────────────────────────────────────────────── │ │
│                                                                 │
│ SELECTED SERVER DETAILS: dev                                    │
│ Description: Development server                                 │
│ Added: 2025-08-22 01:25:19                                     │
│ Last Ping: 2025-08-22 01:29:59                                │
│ JWT Status: Valid (expires in 23h 45m)                        │
│                                                                 │
│ [▶ ADD SERVER] [◉ AUTHENTICATE] [○ REMOVE] [⚠ TEST CONNECTION] │
│                                                                 │
│ Actions: [E]dit [T]est [X]remove                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⌨️ **KEYBOARD SHORTCUTS**

### **Authentication Dashboard**
```
NAVIGATION:
↑/↓ Arrow Keys    - Select server from list
Enter             - Connect to selected server (auth if needed)
Tab               - Cycle through interface sections
Escape            - Cancel current operation

QUICK ACTIONS:
Ctrl+N            - Add new server
Ctrl+D            - Remove selected server
Ctrl+E            - Edit selected server
Ctrl+T            - Test server connection
F5                - Refresh server status
F1                - Help/Documentation

SERVER MANAGEMENT:
A                 - Authenticate to selected server
R                 - Re-authenticate (refresh JWT)
M                 - Manage server configurations
S                 - Set as default server
```

### **Authentication Forms**
```
FORM NAVIGATION:
Tab/Shift+Tab     - Next/Previous field
Enter             - Submit form/Continue
Escape            - Cancel authentication
Ctrl+A            - Select all text in field

QUICK ENTRY:
Ctrl+U            - Default username ("root")
Ctrl+P            - Focus password field
Ctrl+T            - Focus tenant field
F2                - Toggle password visibility
```

---

## 🔄 **USER WORKFLOWS**

### **First-Time Setup Flow**
```
1. Application Start → No servers configured
2. Show "Add New Vault" dialog automatically
3. User enters server details + initial auth credentials
4. Test connection and authenticate in one step
5. Save server config + JWT token to servers.json
6. Set as current server and enter main application
```

### **Daily Access Flow (Authenticated)**
```
1. Application Start → Read servers.json
2. Show authenticated servers at top of list
3. User selects server (or auto-select current)
4. Validate JWT token silently
5. If valid: Enter main application immediately
6. If expired: Show re-authentication dialog
```

### **Multi-Server Management Flow**
```
1. User has multiple configured servers
2. Dashboard shows all with auth/connection status
3. Quick selection for authenticated servers
4. Authentication required for new/expired servers
5. Easy switching between authenticated vaults
6. Server management for editing configurations
```

### **Error Recovery Flow**
```
1. Connection failure detected
2. Show clear error message with context
3. Offer recovery options:
   - Retry connection
   - Edit server configuration
   - Test connectivity
   - Remove non-working server
4. Graceful fallback to working servers
```

---

## 🔌 **API INTEGRATION**

### **Authentication Endpoints**
```
POST /auth/login
Request:
{
  "tenant": "vault_identifier",
  "username": "root",
  "password": "user_password"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_at": "2025-08-23T01:30:00Z",
  "user": {
    "id": "user_uuid",
    "username": "root",
    "access_level": "overseer",
    "permissions": ["read", "write", "admin"]
  },
  "tenant": {
    "id": "tenant_uuid", 
    "name": "vault_identifier",
    "database": "monk-api$vault_identifier"
  }
}
```

### **Token Validation**
```
GET /auth/verify
Headers: Authorization: Bearer <jwt_token>

Response:
{
  "valid": true,
  "expires_at": "2025-08-23T01:30:00Z",
  "remaining_seconds": 86400
}
```

### **Connection Testing**
```
GET /ping
Response:
{
  "status": "ok",
  "version": "4.19.1",
  "database": "connected",
  "timestamp": "2025-08-22T01:30:00Z"
}
```

---

## 💾 **DATA MANAGEMENT**

### **Server Configuration Storage**
```javascript
// servers.json structure
{
  "servers": {
    "server_name": {
      "hostname": "string",      // Server hostname/IP
      "port": number,           // Server port
      "protocol": "http|https", // Connection protocol
      "description": "string",  // User-friendly description
      "added_at": "ISO_date",   // When server was added
      "last_ping": "ISO_date",  // Last successful ping
      "status": "up|down",      // Current connection status
      "jwt_token": "string?"    // Stored JWT (when authenticated)
    }
  },
  "current": "server_name"      // Default/last used server
}
```

### **JWT Token Management**
- **Storage**: Tokens stored in server configuration
- **Validation**: Check expiration before each API call
- **Refresh**: Re-authenticate when token expires
- **Security**: Tokens encrypted at rest (implementation detail)
- **Cleanup**: Remove expired tokens on application start

### **Session Persistence**
- **Current Server**: Remember last used server across restarts
- **Auto-Connect**: Skip auth dashboard if single valid session exists
- **Multi-Session**: Support multiple concurrent authenticated servers
- **Timeout**: Configurable session timeout warnings

---

## 🛡️ **SECURITY CONSIDERATIONS**

### **Credential Handling**
- **Password Security**: Never store passwords in plaintext
- **JWT Storage**: Secure token storage in configuration files
- **Auto-Lock**: Optional auto-lock after inactivity period
- **Clear Credentials**: Option to clear all stored authentication

### **Connection Security**
- **HTTPS Enforcement**: Warn about HTTP connections in production
- **Certificate Validation**: Proper SSL/TLS certificate handling
- **Timeout Handling**: Secure handling of connection timeouts
- **Error Sanitization**: Don't expose sensitive data in error messages

### **Session Management**
- **Token Expiration**: Proper handling of expired tokens
- **Automatic Refresh**: Silent token refresh when possible
- **Logout Procedures**: Clean token removal on logout
- **Multi-User**: Support for user switching without full logout

---

**"Remember: Proper authentication protocols ensure vault security while maintaining operational efficiency."**