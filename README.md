# CrowdCent MCP Server

A Model Context Protocol (MCP) server that provides seamless integration with the [CrowdCent Challenge API](https://docs.crowdcent.com/), enabling AI assistants to interact with CrowdCent's prediction challenges directly.

<div align="center">
  <img src="/assets/startup.png" alt="MCP Server" />
</div>

## Overview

This MCP server allows AI assistants like Claude Desktop and Cursor to:
- Access and manage CrowdCent challenges
- Download training and inference datasets
- Submit predictions
- Monitor submissions
- Access meta models

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- CrowdCent API key (get one at [crowdcent.com](https://crowdcent.com))

## Installation

1. Clone this repository:
```bash
git clone https://github.com/crowdcent/crowdcent-mcp.git
cd crowdcent-mcp
```
2. Install dependencies with uv:
```bash
uv pip install -e .
```

## Configuration

### Setting up your API key

Create a `.env` file in the project root:
```bash
CROWDCENT_API_KEY=your_api_key_here
```

Alternatively, you can initialize the client with your API key when using the MCP server.

### Cursor Setup

Add the following to your Cursor settings (`~/.cursor/config.json` or through Cursor Settings UI):

```json
{
  "mcpServers": {
    "crowdcent-mcp": {
      "command": "/path/to/.cargo/bin/uv",
      "args": ["run", 
        "--directory",
        "/path/to/crowdcent-mcp",
        "server.py"
      ]
    }
  }
}
```

Replace `/path/to/` with your actual paths. For example:
- `/home/username/.cargo/bin/uv` on Linux
- `/Users/username/.cargo/bin/uv` on macOS
- `C:\\Users\\username\\.cargo\\bin\\uv` on Windows

### Claude Desktop Setup

For Claude Desktop, add the following to your configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "crowdcent-mcp": {
      "command": "uv",
      "args": ["run", 
        "--directory",
        "/path/to/crowdcent-mcp",
        "server.py"
      ]
    }
  }
}
```

## Usage Examples

After configuring the MCP server in your AI assistant, you can use natural language to interact with CrowdCent:

### Getting Started
```
"Download data, train a model, and submit predictions to the crowdcent challenge!"
```




```
"Initialize the CrowdCent client with my API key: cc_xxxx"
"Show me all available challenges"
"Get information about the current challenge"
```

### Working with Data
```
"Download the latest training dataset to ./data/training.parquet"
"Check if new inference data is available"
"Download today's inference data and wait if it's not ready yet"
```

### Making Submissions
```
"Submit my predictions from predictions.parquet to slot 1"
"List my recent submissions"

### MCP server not connecting
- Ensure uv is installed and in your PATH
- Check that the directory path in your config is correct
- Verify the server.py file has execute permissions

### API key issues
- Make sure your API key is valid
- Check if it's properly set in .env or passed to init_client

### Submission errors
- Ensure your predictions file has the required columns: `id`, `pred_10d`, `pred_30d`
- Check that all asset IDs match the current inference period
- Verify submission window is still open (within 4 hours of inference data release)

## Resources

- [CrowdCent Documentation](https://docs.crowdcent.com/)
- [Hyperliquid Ranking Challenge](https://docs.crowdcent.com/hyperliquid-ranking/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [CrowdCent Challenge Python Client](https://pypi.org/project/crowdcent-challenge/)

## Support

For issues with:
- **This MCP server**: Open an issue in this repository
- **CrowdCent API**: Email info@crowdcent.com or join our Discord