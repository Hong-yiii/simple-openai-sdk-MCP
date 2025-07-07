# 🚀 OpenAI Agent with MCP Tools - Interactive Chat Demo

A comprehensive demo showcasing how to use OpenAI's agent SDK with multiple MCP (Model Context Protocol) servers using JSON configuration similar to Claude Desktop.

## ✨ Features

- 🎯 **JSON Configuration**: Claude Desktop-style MCP server setup
- 💬 **Interactive Chat UI**: Continuous conversation with memory
- 🧠 **Conversation Memory**: Maintains context across exchanges
- 🛠️ **Multiple MCP Tools**: Filesystem, Git, SQLite, Time utilities
- 📝 **Chat Commands**: Built-in commands for managing conversations
- 💾 **Conversation Persistence**: Save/load chat history
- 🔧 **Easy Extension**: Add new MCP servers via JSON config

## 🏗️ Architecture

```
User Input → Interactive Chat → Agent + Memory → MCP Servers → Tools
     ↓              ↓              ↓               ↓           ↓
  Commands      Conversation    Context        Multiple     Filesystem
  /help         History         Injection      Servers      Git, SQLite
  /save         Memory                                      Time, etc.
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project
cd src

# Install the package in development mode
pip install -e .

# Or install dependencies directly
pip install -r simple_mcp/requirements.txt
```

### 2. Configure MCP Servers

The `src/simple_mcp/config.json` file defines available MCP servers:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", ".", "/tmp"]
    },
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "./conversation_memory.db"]
    },
    "git": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "."]
    },
    "time": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-time"]
    }
  }
}
```

### 3. Run the Interactive Demo

```bash
# Navigate to the package directory
cd src/simple_mcp

# Start the interactive chat
python demo.py

# Or use the console script (if installed)
simple-mcp
```

## 💬 Interactive Chat Interface

The demo provides a rich interactive experience:

```
🚀 OpenAI Agent with MCP Tools - Interactive Chat
=======================================================
📂 Config: config.json
🔗 MCP Servers: 4 loaded
🧠 Memory: 10 exchanges

💡 Type '/help' for commands or just start chatting!
🎯 Example: 'List files in current directory' or 'What's the current time?'
-------------------------------------------------------

🗣️  You: List files in the current directory
🤔 Thinking...
🤖 Assistant: I can see the following files in the current directory:
- config.json
- demo.py
- requirements.txt
- conversation_memory.db
- __init__.py

🗣️  You: /help
🤖 Assistant: 🤖 **Available Commands:**
• `/help` - Show this help message
• `/clear` - Clear conversation history  
• `/history` - Show recent conversation history
• `/save` - Save conversation to file
• `/tools` - List available MCP tools
• `/quit` or `/exit` - Exit the chat
• Any other message - Chat with the assistant
```

## 🧠 Memory System

The chat maintains conversation context automatically:

- **Session Memory**: Keeps last 10 exchanges in memory
- **Context Injection**: Adds conversation history to agent instructions
- **Persistent Storage**: Save conversations to JSON files
- **Smart Truncation**: Limits context to prevent overflow

## 🛠️ Available MCP Tools

The demo includes several useful MCP servers:

### 📁 Filesystem Server
- List directory contents
- Read/write files
- File operations

### 🗄️ SQLite Server  
- Database queries
- Store conversation data
- Data persistence

### 🌿 Git Server
- Repository status
- Commit history
- Branch information

### ⏰ Time Server
- Current date/time
- Time zone utilities
- Date calculations

## 📝 Chat Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/clear` | Clear conversation history |
| `/history` | Display recent exchanges |
| `/save` | Save conversation to file |
| `/tools` | List available MCP tools |
| `/quit`, `/exit` | Exit the chat |

## ⚙️ Configuration

### Adding New MCP Servers

Add entries to `config.json`:

```json
{
  "mcpServers": {
    "your_server": {
      "command": "npx",
      "args": ["-y", "@your/mcp-server", "--option", "value"]
    }
  }
}
```

### Memory Settings

Adjust memory settings in `demo.py`:

```python
class ChatSession:
    def __init__(self, max_history: int = 10):  # Change max_history
        ...
```

## 🎯 Example Interactions

```bash
# File operations
🗣️  "Create a new file called test.txt with some content"
🗣️  "What files are in the /tmp directory?"

# Git operations  
🗣️  "Show me the recent git commits"
🗣️  "What's the current git status?"

# Database operations
🗣️  "Query the conversation database for recent entries"

# Time utilities
🗣️  "What time is it now?"
🗣️  "What day of the week will it be in 30 days?"

# Memory and context
🗣️  "Remember that I prefer Python over JavaScript"
🗣️  "Based on what I told you earlier, what language should I use?"
```

## 🔧 Development

### Project Structure

```
src/
├── simple_mcp/
│   ├── __init__.py
│   ├── demo.py           # Main interactive chat demo
│   ├── config.json       # MCP servers configuration
│   └── requirements.txt  # Dependencies
├── setup.py              # Package setup
└── simple_mcp.egg-info/  # Package metadata
```

### Adding Features

1. **New MCP Servers**: Add to `config.json`
2. **Enhanced Memory**: Modify `ChatSession` class
3. **UI Improvements**: Update `MCPAgentDemo` class
4. **New Commands**: Add to `handle_command()` method

## 🚨 Prerequisites

- **Python 3.8+**
- **Node.js** (for NPX-based MCP servers)
- **OpenAI API Key** (set via environment variables)

## 📚 Resources

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Server Examples](https://github.com/modelcontextprotocol)

This demo provides a complete foundation for building sophisticated AI agents with multiple tools, memory, and rich interaction capabilities! 