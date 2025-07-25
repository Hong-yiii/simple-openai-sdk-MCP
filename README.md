# Simple MCP - Multi-Model Agent Demo

A minimal demonstration of integrating Model Context Protocol (MCP) tools with multiple LLM providers via LiteLLM. This project serves as a practical example of how to extend AI Agents with external tools using the MCP standard.

## Background

The project provides a lightweight framework for building AI applications with very few abstractions. While it comes with built-in tools, its real power lies in its extensibility. This project demonstrates how to enhance AI Agents with external tools using the Model Context Protocol (MCP) and supports multiple LLM providers through LiteLLM integration.

### What is MCP?

Model Context Protocol (MCP) is a standardized way for AI models to interact with external tools and services. It provides a consistent interface for tools to expose their functionality to AI models, making it easier to extend AI capabilities without changing the core model.

Use `npx @modelcontextprotocol/inspector --config path/to/config.json --server everything` to debug endpoints, the performance of the model is largely affected by the MCP endpoint and how its structured

## 🎯 Project Purpose

This repository demonstrates:
1. How to set up MCP servers alongside AI Agents
2. A minimal configuration for tool integration
3. Basic interactive chat functionality with MCP-enabled tools
4. Integration with multiple LLM providers:
   - Amazon Nova via AWS Bedrock
   - Google Gemini Pro
   - Anthropic Claude
   - OpenAI GPT-4o-mini

## 🌟 Features

- Minimal working example of MCP integration with AI Agents
- Support for multiple LLM providers through LiteLLM
- Simple interactive chat interface
- Basic MCP server configuration:
  - Filesystem operations
  - Sequential thinking capabilities
  - Notion API integration (example of third-party service integration)
- Easy model switching through configuration flags

## 🔧 Prerequisites

- Python 3.8 or higher
- Node.js (for running MCP servers)
- API keys for your chosen model provider:
  - AWS credentials for Nova
  - Google API key for Gemini
  - Anthropic API key for Claude
  - OpenAI API key for GPT models

## 📦 Quick Start

1. Clone and setup:
```bash
git clone [repository-url]
cd simple_mcp
pip install -e .
```

2. Set up your environment variables in `.env`:
```bash
# For Amazon Nova
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION_NAME=your_aws_region

# For Google Gemini
GOOGLE_API_KEY=your_google_api_key

# For Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key

# For OpenAI
OPENAI_API_KEY=your_openai_api_key
```

3. Configure your desired model in `src/simple_mcp/demo.py`:
```python
# Choose ONE model to enable
USE_NOVA = True     # Amazon Nova
USE_GEMINI = False  # Google Gemini
USE_CLAUDE = False  # Anthropic Claude
USE_OPENAI = False  # OpenAI GPT-4o-mini
```

4. Run the demo:
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
│       ├── demo.py            # Interactive demo with MCP tools
│       ├── nova_integration.py    # Amazon Nova integration
│       ├── gemini_integration.py  # Google Gemini integration
│       ├── claude_integration.py  # Anthropic Claude integration
│       └── openai_integration.py  # OpenAI integration
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

2. **Model Integration**: Each model provider has its own integration module that:
   - Validates API credentials
   - Configures the model through LiteLLM
   - Provides consistent interface for the agent

3. **Integration**: The demo script shows how to:
   - Load MCP servers from configuration
   - Create an AI Agent with chosen model
   - Handle interactive chat with tool usage

## 🔒 Dependencies

- `litellm>=1.0.0` - Universal LLM interface
- `httpx>=0.24.0` - HTTP client library
- Various MCP server packages (installed via npx)

## 📖 Learn More

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [AWS Bedrock Documentation](https://aws.amazon.com/bedrock/)
- [Google AI Documentation](https://ai.google.dev/)
- [Anthropic Documentation](https://docs.anthropic.com/)
- [OpenAI Documentation](https://platform.openai.com/docs)

## 🛠️ Development Status

This project is a minimal demonstration and is currently in Beta status. It supports Python versions 3.8 through 3.12.

## 📄 License

[Add license information here]