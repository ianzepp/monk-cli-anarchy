"""
VAULT-TEC STANDARD KEY CONVENTIONS
Consistent muscle memory across all vault facility modules
"""

from textual.binding import Binding


class StandardKeys:
    """Standard key mappings for all vault facility modules"""
    
    # Core CRUD Operations (Universal)
    FIND = "f"      # Find/Filter/Search records
    CREATE = "c"    # Create new record/item
    DELETE = "d"    # Delete selected record/item  
    UPDATE = "u"    # Update/Edit selected record/item
    
    # Navigation (Universal)
    BACK = "escape"     # Return to previous screen
    REFRESH = "r"       # Refresh current data
    HELP = "h"          # Context help
    
    # Selection Operations (List/Table screens)
    SELECT_ALL = "a"    # Select all items
    SELECT_NONE = "x"   # Clear selection
    ENTER = "enter"     # Default action (usually edit/view)
    
    # Specialized Operations (Context specific)
    EXPORT = "e"        # Export data
    IMPORT = "i"        # Import data
    TEST = "t"          # Test connection/validation
    SAVE = "s"          # Save current work
    CANCEL = "escape"   # Cancel current operation
    
    @staticmethod
    def get_crud_bindings(show_find=True, show_create=True, show_delete=True, show_update=True):
        """Get standard CRUD bindings for a screen"""
        bindings = []
        
        if show_find:
            bindings.append(Binding(StandardKeys.FIND, "find_records", "Find", show=True))
        if show_create:
            bindings.append(Binding(StandardKeys.CREATE, "create_record", "Create", show=True))
        if show_delete:
            bindings.append(Binding(StandardKeys.DELETE, "delete_record", "Delete", show=True))
        if show_update:
            bindings.append(Binding(StandardKeys.UPDATE, "update_record", "Update", show=True))
            
        return bindings
    
    @staticmethod 
    def get_navigation_bindings():
        """Get standard navigation bindings"""
        return [
            Binding(StandardKeys.BACK, "back", "Back", show=True),
            Binding(StandardKeys.REFRESH, "refresh", "Refresh", show=True),
            Binding(StandardKeys.HELP, "help", "Help", show=True),
        ]
    
    @staticmethod
    def get_selection_bindings():
        """Get standard selection bindings for list/table screens"""
        return [
            Binding(StandardKeys.SELECT_ALL, "select_all", "Select All", show=True),
            Binding(StandardKeys.SELECT_NONE, "select_none", "Clear", show=True),
            Binding(StandardKeys.ENTER, "default_action", "Edit", show=True),
        ]


# Standard key convention mapping for monk-cli commands
MONK_COMMAND_KEYS = {
    # Server management  
    "server": {
        StandardKeys.FIND: "server list --json",
        StandardKeys.CREATE: "server add", 
        StandardKeys.DELETE: "server delete",
        StandardKeys.UPDATE: "server use",  # "use" is like updating current selection
        StandardKeys.TEST: "server ping",
    },
    
    # Tenant management
    "tenant": {
        StandardKeys.FIND: "tenant list --json",
        StandardKeys.CREATE: "tenant create",
        StandardKeys.DELETE: "tenant delete", 
        StandardKeys.UPDATE: "tenant use",
    },
    
    # Schema management
    "schema": {
        StandardKeys.FIND: "meta select --json",
        StandardKeys.CREATE: "meta create",
        StandardKeys.DELETE: "meta delete",
        StandardKeys.UPDATE: "meta update",
    },
    
    # Data operations
    "data": {
        StandardKeys.FIND: "data select",
        StandardKeys.CREATE: "data create",
        StandardKeys.DELETE: "data delete", 
        StandardKeys.UPDATE: "data update",
    }
}