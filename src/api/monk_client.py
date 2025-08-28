"""
MONK CLI ANARCHY
Monk CLI Command Execution Utility

"Bridging the gap between beautiful UIs and powerful CLIs"
"""

import json
import yaml
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from config import config


@dataclass
class MonkCommandResult:
    """Result from a monk command execution"""
    success: bool
    data: Any = None
    error: str = ""
    raw_output: str = ""
    exit_code: int = 0


class MonkClient:
    """Execute monk CLI commands and parse results"""
    
    def __init__(self, monk_binary: str = None):
        self.monk_binary = monk_binary or config.monk_executable
        self.send_trace = None
        self.recv_trace = None
    
    def set_trace_widgets(self, send_trace, recv_trace):
        """Set trace widgets for command/response display"""
        self.send_trace = send_trace
        self.recv_trace = recv_trace
        
    def _execute_command(self, args: List[str], timeout: int = 5, trace_data: dict = None) -> MonkCommandResult:
        """Execute a monk command and return structured result"""
        try:
            # Build full command
            cmd = [self.monk_binary] + args
            
            # Show command trace if widget is available
            command_str = " ".join(args)
            if self.send_trace and hasattr(self.send_trace, 'show_send_trace'):
                self.send_trace.show_send_trace(command_str, trace_data)
            elif self.send_trace and hasattr(self.send_trace, 'show_command'):
                self.send_trace.show_command(command_str, trace_data)
            
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False  # Don't raise exception on non-zero exit
            )
            
            # Try to parse JSON/YAML output, fall back to raw text
            data = None
            if result.stdout.strip():
                try:
                    # Try JSON first
                    data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    try:
                        # Try YAML
                        data = yaml.safe_load(result.stdout)
                    except yaml.YAMLError:
                        # Not structured data, use raw output
                        data = result.stdout.strip()
            
            # Show response trace if widget is available
            if self.recv_trace and data:
                if hasattr(self.recv_trace, 'show_recv_trace'):
                    self.recv_trace.show_recv_trace(data)
                elif hasattr(self.recv_trace, 'show_response'):
                    self.recv_trace.show_response(data)
            
            return MonkCommandResult(
                success=result.returncode == 0,
                data=data,
                error=result.stderr.strip() if result.stderr else "",
                raw_output=result.stdout.strip(),
                exit_code=result.returncode
            )
            
        except subprocess.TimeoutExpired:
            return MonkCommandResult(
                success=False,
                error=f"Command timed out after {timeout} seconds",
                exit_code=-1
            )
        except FileNotFoundError:
            return MonkCommandResult(
                success=False,
                error=f"monk command not found: {self.monk_binary}",
                exit_code=-1
            )
        except Exception as e:
            return MonkCommandResult(
                success=False,
                error=f"Unexpected error: {str(e)}",
                exit_code=-1
            )
    
    # Server Management Commands
    
    def server_list(self) -> MonkCommandResult:
        """Execute: monk server list --json"""
        return self._execute_command(["server", "list", "--json"])
    
    def server_add(self, name: str, url: str, description: str = "") -> MonkCommandResult:
        """Execute: monk server add <name> <url> [description]"""
        args = ["server", "add", name, url]
        if description:
            args.append(description)
        return self._execute_command(args)
    
    def server_delete(self, name: str) -> MonkCommandResult:
        """Execute: monk server delete <name>"""
        return self._execute_command(["server", "delete", name])
    
    def server_use(self, name: str) -> MonkCommandResult:
        """Execute: monk server use <name>"""
        return self._execute_command(["server", "use", name])
    
    def server_current(self) -> MonkCommandResult:
        """Execute: monk server current"""
        return self._execute_command(["server", "current"])
    
    def server_ping(self, name: Optional[str] = None) -> MonkCommandResult:
        """Execute: monk server ping [name]"""
        args = ["server", "ping"]
        if name:
            args.append(name)
        return self._execute_command(args)
    
    def server_ping_all(self) -> MonkCommandResult:
        """Execute: monk server ping-all"""
        return self._execute_command(["server", "ping-all"])
    
    # Tenant Management Commands
    
    def tenant_list(self) -> MonkCommandResult:
        """Execute: monk tenant list"""
        return self._execute_command(["tenant", "list"])
    
    def tenant_create(self, name: str) -> MonkCommandResult:
        """Execute: monk tenant create <name>"""
        return self._execute_command(["tenant", "create", name])
    
    def tenant_delete(self, name: str) -> MonkCommandResult:
        """Execute: monk tenant delete <name>"""
        return self._execute_command(["tenant", "delete", name])
    
    def tenant_use(self, name: str) -> MonkCommandResult:
        """Execute: monk tenant use <name>"""
        return self._execute_command(["tenant", "use", name])
    
    def tenant_init(self, name: str) -> MonkCommandResult:
        """Execute: monk tenant init <name>"""
        return self._execute_command(["tenant", "init", name])
    
    # Authentication Commands
    
    def auth_login(self, tenant: str, username: str, password: str) -> MonkCommandResult:
        """Execute: monk auth login <tenant> <username> <password>"""
        return self._execute_command(["auth", "login", tenant, username, password])
    
    def auth_logout(self) -> MonkCommandResult:
        """Execute: monk auth logout"""
        return self._execute_command(["auth", "logout"])
    
    def auth_status(self) -> MonkCommandResult:
        """Execute: monk auth status --json"""
        return self._execute_command(["auth", "status", "--json"])
    
    def auth_ping(self) -> MonkCommandResult:
        """Execute: monk auth ping --json"""
        return self._execute_command(["auth", "ping", "--json"])
    
    def auth_info(self) -> MonkCommandResult:
        """Execute: monk auth info --json"""
        return self._execute_command(["auth", "info", "--json"])
    
    def auth_expires(self) -> MonkCommandResult:
        """Execute: monk auth expires (returns raw timestamp)"""
        return self._execute_command(["auth", "expires"])
    
    def auth_expired(self) -> MonkCommandResult:
        """Execute: monk auth expired (returns success/error)"""
        return self._execute_command(["auth", "expired"])
    
    # Data Operations (for future modules)
    
    def data_select(self, schema: str, filters: Optional[Dict] = None) -> MonkCommandResult:
        """Execute: monk data select <schema> [filters]"""
        args = ["data", "select", schema]
        if filters:
            args.extend(["--filter", json.dumps(filters)])
        return self._execute_command(args)
    
    def data_create(self, schema: str, data: Dict) -> MonkCommandResult:
        """Execute: monk data create <schema> <data>"""
        return self._execute_command(["data", "create", schema, json.dumps(data)])
    
    def data_update(self, schema: str, id_or_data: str, data: Optional[Dict] = None) -> MonkCommandResult:
        """Execute: monk data update <schema> <id> [data]"""
        args = ["data", "update", schema, id_or_data]
        if data:
            args.append(json.dumps(data))
        return self._execute_command(args)
    
    def data_delete(self, schema: str, record_id: str) -> MonkCommandResult:
        """Execute: monk data delete <schema> <id>"""
        return self._execute_command(["data", "delete", schema, record_id])
    
    # Meta/Schema Operations (for Schema Laboratory)
    
    def meta_select(self, schema: Optional[str] = None) -> MonkCommandResult:
        """Execute: monk meta select [schema]"""
        args = ["meta", "select"]
        if schema:
            args.append(schema)
        return self._execute_command(args)
    
    def meta_create(self, schema: str, definition: Dict) -> MonkCommandResult:
        """Execute: monk meta create <schema> <definition>"""
        return self._execute_command(["meta", "create", schema, json.dumps(definition)])
    
    def meta_update(self, schema: str, definition: Dict) -> MonkCommandResult:
        """Execute: monk meta update <schema> <definition>"""
        return self._execute_command(["meta", "update", schema, json.dumps(definition)])
    
    def meta_delete(self, schema: str) -> MonkCommandResult:
        """Execute: monk meta delete <schema>"""
        return self._execute_command(["meta", "delete", schema])


# Global client instance
monk = MonkClient()