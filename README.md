# Capstone Agents

A fully functional, modular, and workspace-agnostic AI agent repository intended for BS-IT capstone projects and any software development workflow.

## Features
- **10+ Agent Roles**: From Coordinator to Blockchain Developer.
- **Dual-Layer Agents**: Planning and Implementation agents for each role.
- **MCP Support**: Integrated with Model Context Protocol for tools like Figma, Supabase, Docker, etc.
- **Multi-CLI Support**: Works with Gemini, Cursor, OpenCodex, QwenCLI, RoboDev, and VS Code Copilot.
- **Workspace Agnostic**: Can be dropped into any project folder.

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js (for MCP servers)
- A supported CLI tool (optional, but recommended)

### Installation
1. Clone this repository.
2. Install dependencies (if any).
3. Run `python scripts/setup_vscode_copilot.py` to configure VS Code.

### Usage

List available agents:
```bash
python scripts/run_agents.py -l
```

Run an agent interactively on your project:
```bash
# Planning agent (default)
python scripts/run_agents.py -a designer -w /path/to/your/project -i

# Implementation agent
python scripts/run_agents.py -a designer -w /path/to/your/project -i -t impl
```

Or use the bash wrapper:
```bash
./scripts/launch-agent.sh designer /path/to/project gemini
```

See [Usage Guide](docs/usage-guide.md) for the full command cheatsheet.

## VS Code Copilot Integration
See [VS Code Copilot Guide](docs/vscode-copilot-guide.md) for detailed instructions.

## Documentation
- [Usage Guide](docs/usage-guide.md)
- [MCP Integration Guide](docs/mcp-integration-guide.md)
- [Architecture](docs/architecture.md)

## License
MIT
