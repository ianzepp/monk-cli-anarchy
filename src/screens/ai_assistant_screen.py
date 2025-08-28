"""
VAULT-TEC AI ASSISTANT
Global Help and Query Interface
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Static, TextArea

from widgets.vault_container import VaultContainer


class AIAssistantScreen(Screen):
    """Global AI Assistant for vault operations help"""
    
    CSS = """
    .centering-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }
    
    .assistant-container {
        width: 80;
        height: auto;
        max-height: 80%;
        border: solid #22c55e;
        border-title-color: #22c55e;
        border-title-style: bold;
        overflow-y: auto;
        padding: 0 2;
    }
    
    .ai-prompt {
        color: #22c55e;
        text-style: bold;
        text-align: center;
        margin: 1 0;
    }
    
    .ai-input {
        height: 4;
        margin: 1 0;
        background: #1a1a1a;
        color: #ffffff;
        border: solid #22c55e;
    }
    
    .examples-section {
        background: #0a0a0a;
        margin: 1 0;
        padding: 1;
        max-height: 8;
        overflow-y: auto;
    }
    
    .example-item {
        color: #6b7280;
        text-style: italic;
        margin: 0 0;
        height: 1;
    }
    
    .response-section {
        background: #1a1a1a;
        margin: 1 0;
        padding: 1;
        min-height: 4;
    }
    
    .ai-response {
        color: #ffb000;
        margin: 0 0;
    }
    
    .action-buttons {
        height: 1;
        margin: 1 0;
        align: center middle;
    }
    
    .system-note {
        color: #1e3a8a;
        text-style: italic;
        text-align: center;
        margin: 1 0;
    }
    """
    
    BINDINGS = [
        Binding("escape", "close_assistant", "Close", show=True),
        Binding("enter", "ask_ai", "Ask AI", show=True),
        Binding("?", "show_examples", "Examples", show=True),
        Binding("x", "execute_suggestion", "Execute", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.current_response = ""
        self.suggested_action = None
        self.text_cleared = False

    def compose(self) -> ComposeResult:
        """Build the AI assistant interface"""
        with Container(classes="centering-container"):
            with Container(classes="assistant-container") as container:
                container.border_title = "VAULT-TEC AI ASSISTANT"
                
                with Vertical():
                    yield Label(
                        "Ask anything about your vault operations in plain English:",
                        classes="ai-prompt"
                    )
                    
                    # AI query input
                    ai_input = TextArea(
                        text="Type your question here...",
                        id="ai_input",
                        classes="ai-input"
                    )
                    ai_input.show_line_numbers = False
                    ai_input.wrap = True
                    yield ai_input
                    
                    # Quick examples
                    with Container(classes="examples-section"):
                        yield Label("EXAMPLE QUERIES:", classes="section-label")
                        yield Label("• What are my servers?", classes="example-item")
                        yield Label("• How big is my vault?", classes="example-item") 
                        yield Label("• Show me suspended engineering staff", classes="example-item")
                        yield Label("• Who was hired in the last 30 days?", classes="example-item")
                        yield Label("• What schemas do I have?", classes="example-item")
                        yield Label("• Find all records with missing email addresses", classes="example-item")
                    
                    # AI response section
                    with Container(classes="response-section"):
                        yield Label("AI RESPONSE:", classes="section-label")
                        yield Static(
                            "Ask a question above and I'll help you navigate to the right information or build the appropriate query.",
                            id="ai_response",
                            classes="ai-response"
                        )
                    
                    # Action buttons with killbox notation
                    with Horizontal(classes="action-buttons"):
                        yield Button("[ENTER] ASK AI", variant="primary", id="ask_btn")
                        yield Button("[x] EXECUTE", variant="default", id="execute_btn")
                        yield Button("[?] EXAMPLES", variant="default", id="examples_btn")
                        yield Button("[ESC] CLOSE", variant="default", id="close_btn")
                    
                    yield Label(
                        '"Ask about servers, vaults, data, or operations"',
                        classes="system-note"
                    )

    def on_mount(self) -> None:
        """Focus the AI input on startup"""
        self.call_later(self.focus_ai_input)
        
    def focus_ai_input(self) -> None:
        """Focus the AI textarea and select all text"""
        try:
            ai_input = self.query_one("#ai_input", TextArea)
            ai_input.focus()
            # Select all text so typing replaces instead of inserting
            ai_input.select_all()
        except:
            pass
            
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle text area content changes"""
        if event.text_area.id == "ai_input":
            current_text = event.text_area.text.strip()
            examples_container = self.query_one(".examples-section", Container)
            
            # Clear placeholder text on first edit
            if not self.text_cleared and current_text.startswith("Type your question here..."):
                # User started typing over placeholder - clear it
                event.text_area.text = ""
                self.text_cleared = True
                examples_container.display = False
                return
            
            # Hide examples when user has actual content
            if current_text and current_text != "Type your question here...":
                # User is typing - hide examples
                examples_container.display = False
            else:
                # Empty text - show examples
                examples_container.display = True

    def action_close_assistant(self) -> None:
        """Close AI assistant and return"""
        self.app.pop_screen()
        
    def action_ask_ai(self) -> None:
        """Process AI query and provide response"""
        ai_input = self.query_one("#ai_input", TextArea)
        query = ai_input.text.strip()
        
        if not query:
            self.app.bell()
            return
            
        # Process the query and generate response
        response, action = self.process_ai_query(query)
        
        # Update response display
        response_widget = self.query_one("#ai_response", Static)
        response_widget.update(response)
        
        # Store suggested action
        self.suggested_action = action
        self.current_response = response
        
        self.app.bell()
        
    def process_ai_query(self, query: str) -> tuple[str, dict]:
        """Process natural language query and return response + suggested action"""
        query = query.lower()
        
        # Server-related queries
        if "server" in query:
            if "what" in query or "list" in query or "show" in query:
                return (
                    "I can show you all configured servers. Navigate to Department Registry (Module 1) to see server list, status, and authentication details.",
                    {"action": "navigate", "module": 1, "description": "Open Department Registry"}
                )
        
        # Vault size/population queries
        if any(word in query for word in ["big", "size", "population", "how many", "count"]):
            return (
                "Vault population info is shown in the header. For detailed population management, navigate to Population Management (Module 3) to see all records.",
                {"action": "navigate", "module": 3, "description": "Open Population Management"}
            )
        
        # Schema-related queries
        if "schema" in query:
            return (
                "Schema information is available in the Schema Laboratory (Module 2). You can view all schemas, create new ones, and manage data structures.",
                {"action": "navigate", "module": 2, "description": "Open Schema Laboratory"}
            )
        
        # Staff/people queries with filters
        if any(word in query for word in ["who", "people", "staff", "employee"]):
            filter_hints = []
            
            if "engineering" in query:
                filter_hints.append('{"department": "engineering"}')
            if "suspended" in query:
                filter_hints.append('{"status": "suspended"}')
            if "died" in query or "deceased" in query:
                filter_hints.append('{"status": "terminated"}')
            if "hired" in query and ("last" in query or "recent" in query):
                filter_hints.append('{"hire_date": {"$gte": "2025-08-01"}}')
                
            if filter_hints:
                filter_example = " AND ".join(filter_hints)
                return (
                    f"I can help you find specific people. Navigate to Population Management (Module 3), then use [f] FIND to build this filter: {filter_example}",
                    {"action": "navigate", "module": 3, "subaction": "filter", "filter": filter_hints}
                )
            else:
                return (
                    "Navigate to Population Management (Module 3) to browse all personnel records or use [f] FIND to search for specific people.",
                    {"action": "navigate", "module": 3, "description": "Open Population Management"}
                )
        
        # Default response
        return (
            "I can help you navigate vault operations. Try asking about 'servers', 'schemas', 'population', or specific data queries. Available modules: 1=Servers, 2=Schemas, 3=Population, 4=Security, 5=Files, 6=Testing",
            {"action": "help", "description": "General navigation help"}
        )

    def action_execute_suggestion(self) -> None:
        """Execute the AI's suggested action"""
        if not self.suggested_action:
            self.app.bell()
            return
            
        action = self.suggested_action
        
        if action.get("action") == "navigate":
            module = action.get("module")
            
            # Close AI assistant
            self.app.pop_screen()
            
            # Navigate to appropriate module
            if module == 1:
                from screens.department_registry_screen import DepartmentRegistryScreen
                self.app.push_screen(DepartmentRegistryScreen())
            elif module == 2:
                from screens.schema_lab_screen import SchemaLabScreen
                self.app.push_screen(SchemaLabScreen())
            elif module == 3:
                from screens.population_management_screen import PopulationManagementScreen
                screen = PopulationManagementScreen()
                self.app.push_screen(screen)
                
                # If there's a subaction for filtering
                if action.get("subaction") == "filter":
                    # TODO: Could auto-trigger filter builder with suggested filters
                    pass
        else:
            self.app.bell()

    def action_show_examples(self) -> None:
        """Show more query examples"""
        examples = [
            "What schemas are deployed?",
            "Show me all inactive users", 
            "Who has elevated security clearance?",
            "What's the status of my test environments?",
            "Find records created this week",
            "Show me all database connection errors"
        ]
        
        # Cycle through examples in the AI input
        current_text = self.query_one("#ai_input", TextArea).text.strip()
        
        try:
            current_index = examples.index(current_text)
            next_index = (current_index + 1) % len(examples)
        except ValueError:
            next_index = 0
            
        self.query_one("#ai_input", TextArea).text = examples[next_index]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "ask_btn":
            self.action_ask_ai()
        elif event.button.id == "execute_btn":
            self.action_execute_suggestion()
        elif event.button.id == "examples_btn":
            self.action_show_examples()
        elif event.button.id == "close_btn":
            self.action_close_assistant()