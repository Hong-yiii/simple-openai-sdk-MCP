# Simple MCP - OpenAI Agent Demo

A minimal demonstration of integrating Model Context Protocol (MCP) tools with OpenAI's Agent system. This project serves as a practical example of how to extend OpenAI Agents with external tools using the MCP standard.

## Background

The OpenAI Agents SDK provides a lightweight framework for building AI applications with very few abstractions. While it comes with built-in tools, its real power lies in its extensibility. This project demonstrates how to enhance OpenAI Agents with external tools using the Model Context Protocol (MCP).

### What is MCP?

Model Context Protocol (MCP) is a standardized way for AI models to interact with external tools and services. It provides a consistent interface for tools to expose their functionality to AI models, making it easier to extend AI capabilities without changing the core model.

## 🎯 Project Purpose

This repository demonstrates:
1. How to set up MCP servers alongside OpenAI Agents
2. A minimal configuration for tool integration
3. Basic interactive chat functionality with MCP-enabled tools

## 🌟 Features

- Minimal working example of MCP integration with OpenAI Agents
- Simple interactive chat interface
- Basic MCP server configuration:
  - Filesystem operations
  - Sequential thinking capabilities
  - Notion API integration (example of third-party service integration)

## 🔧 Prerequisites

- Python 3.8 or higher
- Node.js (for running MCP servers)
- OpenAI API key

## 📦 Quick Start

1. Clone and setup:
```bash
git clone [repository-url]
cd simple_mcp
pip install -e .
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
# Or create a .env file with:
# OPENAI_API_KEY=your_api_key_here
```

3. Run the demo:
```bash
cd src/simple_mcp
python demo.py
```

## 📚 Project Structure

```
simple_mcp/
├── src/
│   ├── setup.py                 # Package configuration
│   └── simple_mcp/
│       ├── config.json         # MCP server configuration
│       └── demo.py            # Interactive demo with MCP tools
```

## ⚙️ How It Works

1. **Configuration**: `config.json` defines available MCP servers:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", ".", "/tmp"]
    }
    // ... other servers
  }
}
```

2. **Integration**: The demo script shows how to:
- Load MCP servers from configuration
- Create an OpenAI Agent with MCP tools
- Handle interactive chat with tool usage

## 🔒 Dependencies

- `openai-agents>=0.1.0` - OpenAI's agent framework
- `httpx>=0.24.0` - HTTP client library
- Various MCP server packages (installed via npx)

## 📖 Learn More

- [OpenAI Agents Documentation](https://openai.github.io/openai-agents-python/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 🛠️ Development Status

This project is a minimal demonstration and is currently in Beta status. It supports Python versions 3.8 through 3.12.

## 📄 License

[Add license information here]