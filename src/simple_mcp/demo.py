#!/usr/bin/env python3
"""
🚀 OpenAI Agent with MCP Tools - Interactive Chat Demo

This script demonstrates a complete OpenAI agent setup with:
- JSON-based MCP server configuration (Claude Desktop style)
- Interactive chat interface with memory
- Multiple MCP servers for filesystem, git, sqlite, and time operations

Usage:
    cd src/simple_mcp
    python demo.py
"""

import asyncio
import json
import os
import sys
from contextlib import AsyncExitStack
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Sequence, cast, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify OpenAI API key is available
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY environment variable not set!")
    sys.exit(1)

from agents import Agent, Runner
from agents.mcp import MCPServerStdio, MCPServer
from agents.mcp.server import MCPServerStdioParams
from simple_mcp.prompts import get_holiday_planner_prompt  # Changed to absolute import


class ChatSession:
    """Manages conversation memory and session state."""
    
    def __init__(self, max_history: int = 10):
        self.history: List[Tuple[str, str]] = []
        self.max_history = max_history
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.debug_history: List[Dict[str, Any]] = []
    
    def add_exchange(self, user_message: str, agent_response: str):
        """Add a user-agent exchange to conversation history."""
        self.history.append((user_message, agent_response))
        
        # Keep only recent history to avoid context overflow
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def add_debug_info(self, result) -> None:
        """Add debug information from a run result."""
        debug_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool_calls": [],
            "usage": {
                "input_tokens": result.context_wrapper.usage.input_tokens,
                "output_tokens": result.context_wrapper.usage.output_tokens,
                "total_tokens": result.context_wrapper.usage.total_tokens,
                "requests": result.context_wrapper.usage.requests
            }
        }
        
        # Process each item in the run result
        for item in result.new_items:
            if hasattr(item, 'type'):
                if item.type == 'tool_call_item':
                    tool_call = {
                        "tool": item.tool.name,
                        "args": item.args,
                        "timestamp": datetime.now().isoformat()
                    }
                    debug_entry["tool_calls"].append(tool_call)
                elif item.type == 'tool_call_output_item':
                    # Find the last tool call and add its output
                    if debug_entry["tool_calls"]:
                        debug_entry["tool_calls"][-1]["output"] = item.output
                        debug_entry["tool_calls"][-1]["output_timestamp"] = datetime.now().isoformat()
        
        self.debug_history.append(debug_entry)
    
    def get_context_summary(self) -> str:
        """Generate a context summary from recent conversation history."""
        if not self.history:
            return ""
        
        context_lines = ["## Recent Conversation Context:"]
        for i, (user_msg, agent_resp) in enumerate(self.history[-5:], 1):
            context_lines.append(f"**Exchange {i}:**")
            context_lines.append(f"User: {user_msg[:100]}{'...' if len(user_msg) > 100 else ''}")
            context_lines.append(f"Assistant: {agent_resp[:100]}{'...' if len(agent_resp) > 100 else ''}")
            context_lines.append("")
        
        return "\n".join(context_lines)
    
    def save_history(self, filepath: Optional[str] = None):
        """Save conversation history to file."""
        if not filepath:
            filepath = f"chat_history_{self.session_id}.json"
        
        with open(filepath, 'w') as f:
            json.dump({
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'history': self.history
            }, f, indent=2)
        
        print(f"💾 Chat history saved to {filepath}")
    
    def save_debug_history(self, filepath: Optional[str] = None):
        """Save debug history to file."""
        if not filepath:
            filepath = f"debug_history_{self.session_id}.json"
        
        with open(filepath, 'w') as f:
            json.dump({
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'debug_history': self.debug_history
            }, f, indent=2)
        
        print(f"🔍 Debug history saved to {filepath}")


class ChatExit(Exception):
    """Custom exception for chat exit."""
    def __init__(self, message: str):
        super().__init__(message)

class MCPAgentDemo:
    """Main demo class for MCP-enabled OpenAI agent."""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.mcp_servers: Sequence[MCPServerStdio] = []
        self.agent: Optional[Agent] = None
        self.chat_session = ChatSession()
        self._shutting_down = False
    
    async def load_mcp_servers(self) -> Sequence[MCPServerStdio]:
        """Load and initialize MCP servers from JSON configuration."""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            print(f"❌ Configuration file {config_file} not found!")
            return []
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            servers = []
            mcp_config = config.get('mcpServers', {})
            
            print(f"🔧 Loading {len(mcp_config)} MCP servers...")
            
            for server_name, server_config in mcp_config.items():
                try:
                    print(f"  📡 Initializing {server_name}...")
                    
                    # Handle environment variables that contain JSON
                    server_params: MCPServerStdioParams = {
                        "command": server_config["command"],
                        "args": server_config["args"]
                    }
                    
                    if "env" in server_config:
                        server_params["env"] = {}
                        for key, value in server_config["env"].items():
                            # If the value is a JSON string, ensure it's properly escaped
                            if key == "OPENAPI_MCP_HEADERS" and isinstance(value, str):
                                try:
                                    # Parse the JSON string to ensure it's valid
                                    headers = json.loads(value)
                                    # Re-encode with proper escaping
                                    server_params["env"][key] = json.dumps(headers)
                                except json.JSONDecodeError:
                                    # If it's not valid JSON, use as is
                                    server_params["env"][key] = value
                            else:
                                server_params["env"][key] = value
                    
                    # Create server instance
                    server = MCPServerStdio(
                        params=server_params,
                        cache_tools_list=True
                    )
                    
                    servers.append(server)
                    print(f"  ✅ {server_name} server ready")
                    
                except Exception as e:
                    print(f"  ❌ Failed to initialize {server_name}: {e}")
                    continue
            
            print(f"🎉 Successfully loaded {len(servers)} MCP servers\n")
            return servers
            
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return []
    
    async def cleanup_servers(self):
        """Cleanup MCP servers properly."""
        # This method is now only used for error handling
        if not self.mcp_servers:
            return
            
        print("\n🔧 Cleaning up servers...")
        for server in self.mcp_servers:
            try:
                await server.cleanup()
            except Exception as e:
                print(f"❌ Error cleaning up server: {e}")
        
        self.mcp_servers = []
        print("✅ Cleanup complete")
    
    async def create_agent(self) -> Agent:
        """Create the OpenAI agent with MCP servers and memory context."""
        
        # Get the base prompt
        base_instructions = get_holiday_planner_prompt()
        
        # Add conversation context if available
        context_summary = self.chat_session.get_context_summary()
        if context_summary:
            instructions = f"{base_instructions}\n\n{context_summary}"
        else:
            instructions = base_instructions
        
        agent = Agent(
            name="HolidayPlanner-v1",
            model="gpt-4o-mini",
            instructions=instructions,
            mcp_servers=cast(List[MCPServer], self.mcp_servers)
        )
        
        return agent
    
    async def process_user_input(self, user_input: str) -> str:
        """Process user input and return agent response."""
        
        # Handle special commands
        if user_input.startswith('/'):
            return await self.handle_command(user_input)
        
        try:
            # Create agent with current context
            self.agent = await self.create_agent()
            
            # Run the agent
            result = await Runner.run(self.agent, user_input, max_turns=20)
            
            # Extract response
            response = result.final_output
            
            # Print token usage from context wrapper
            usage = result.context_wrapper.usage
            print(f"\n📊 Token Usage:")
            print(f"  • Input tokens:  {usage.input_tokens}")
            print(f"  • Output tokens: {usage.output_tokens}")
            print(f"  • Total tokens:  {usage.total_tokens}")
            print(f"  • Total requests: {usage.requests}")
            
            # Add debug information
            self.chat_session.add_debug_info(result)
            
            # Add to conversation history
            self.chat_session.add_exchange(user_input, response)
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Error processing request: {str(e)}"
            self.chat_session.add_exchange(user_input, error_msg)
            return error_msg
    
    async def handle_command(self, command: str) -> str:
        """Handle special chat commands."""
        cmd = command.lower().strip()
        
        if cmd == '/help':
            return """
🤖 **Available Commands:**
• `/help` - Show this help message
• `/clear` - Clear conversation history
• `/history` - Show recent conversation history
• `/save` - Save conversation to file
• `/debug` - Save debug information (tool calls, usage) to file
• `/tools` - List available MCP tools
• `/quit` or `/exit` - Exit the chat
• Any other message - Chat with the assistant
            """.strip()
        
        elif cmd == '/clear':
            self.chat_session.history.clear()
            self.chat_session.debug_history.clear()
            return "🧹 Conversation and debug history cleared!"
        
        elif cmd == '/history':
            if not self.chat_session.history:
                return "📝 No conversation history yet."
            
            history_text = ["📝 **Recent Conversation History:**\n"]
            for i, (user_msg, agent_resp) in enumerate(self.chat_session.history, 1):
                history_text.append(f"**{i}. User:** {user_msg}")
                history_text.append(f"**Assistant:** {agent_resp[:200]}{'...' if len(agent_resp) > 200 else ''}\n")
            
            return "\n".join(history_text)
        
        elif cmd == '/save':
            self.chat_session.save_history()
            return "💾 Conversation history saved!"
        
        elif cmd == '/debug':
            self.chat_session.save_debug_history()
            return "🔍 Debug history saved!"
        
        elif cmd == '/tools':
            if not self.mcp_servers:
                return "🔧 No MCP servers loaded."
            
            tools_info = ["🛠️ **Available MCP Tools:**\n"]
            for i, server in enumerate(self.mcp_servers, 1):
                try:
                    # This would require the server to be started
                    tools_info.append(f"{i}. MCP Server (tools available when running)")
                except:
                    tools_info.append(f"{i}. MCP Server (unable to list tools)")
            
            return "\n".join(tools_info)
        
        elif cmd in ['/quit', '/exit']:
            if not self._shutting_down:
                self._shutting_down = True
                print("👋 Goodbye! Have a great day!")
                response = "Exiting chat..."
                raise ChatExit(response)
            return "Already shutting down..."
        
        else:
            return f"❓ Unknown command: {command}. Type `/help` for available commands."
    
    def print_welcome(self):
        """Print welcome message and status."""
        print("🚀 OpenAI Agent with MCP Tools - Interactive Chat")
        print("=" * 55)
        print(f"📂 Config: {self.config_path}")
        print(f"🔗 MCP Servers: {len(self.mcp_servers)} loaded")
        print(f"🧠 Memory: {self.chat_session.max_history} exchanges")
        print("\n💡 Type '/help' for commands or just start chatting!")
        print("🎯 Example: 'List files in current directory' or 'What's the current time?'")
        print("-" * 55)
    
    async def interactive_chat(self):
        """Main interactive chat loop."""
        self.print_welcome()
        
        while True:
            try:
                # Get user input
                user_input = input("\n🗣️  You: ").strip()
                
                if not user_input:
                    continue
                
                print("🤔 Thinking...")
                
                # Process input and get response
                response = await self.process_user_input(user_input)
                
                # Display response
                print(f"🤖 Assistant: {response}")
                
            except ChatExit as e:
                # Save conversation before exit
                print("\n\n👋 Chat ended. Goodbye!")
                break
                # if self.chat_session.history:
                #     self.chat_session.save_history()
                # break
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Chat ended. Goodbye!")
                break
            except Exception as e:
                print(f"\n💥 Unexpected error: {e}")
                if self._shutting_down:
                    break
                continue
    
    async def run(self):
        """Initialize and run the demo."""
        # Load MCP server configurations
        self.mcp_servers = await self.load_mcp_servers()
        
        # Use async context managers to properly handle server lifecycles
        async with AsyncExitStack() as stack:
            # Enter each server's context
            for server in self.mcp_servers:
                await stack.enter_async_context(server)
            
            try:
                await self.interactive_chat()
            except Exception as e:
                if not isinstance(e, ChatExit):
                    print(f"\n💥 Unexpected error during chat: {e}")
                # Let the async context manager handle cleanup


async def main():
    """Main entry point."""
    # Change to script directory to find config.json
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    demo = MCPAgentDemo()
    
    try:
        await demo.run()
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Demo stopped by user")
    except Exception as e:
        if not isinstance(e, ChatExit):
            print(f"💥 Fatal error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 