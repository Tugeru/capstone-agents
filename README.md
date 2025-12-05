# Capstone Agents

A fully functional, modular, and workspace-agnostic AI agent repository intended for BS-IT capstone projects and any software development workflow.

## Features
- **10+ Agent Roles**: From Coordinator to Blockchain Developer.
- **Dual-Layer Agents**: Planning and Implementation agents for each role.
- **MCP Support**: Integrated with Model Context Protocol for tools like Figma, Supabase, Docker, etc.
- **Multi-CLI & IDE Support**: Works with Gemini, Cursor (CLI & IDE), OpenCodex, QwenCLI, RoboDev, RovoDev, and VS Code Copilot (see Integration Guides).
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

Note: Batch-mode runs that perform programmatic or potentially destructive actions now require an explicit `--auto-approve` flag when invoked via `scripts/run_agents.py`. Use `-i` (interactive) to confirm actions manually when unsure.

For CLI/IDE-specific workflows (Cursor, OpenCodex, QwenCLI, RoboDev, RovoDev, VS Code Copilot), see the [Integration Guides](#integration-guides).


## Documentation
- [Usage Guide](docs/usage-guide.md)
- [Multi-Agent Workflows](docs/multi-agent-workflows.md)
- [MCP Integration Guide](docs/mcp-integration-guide.md)
- [Architecture](docs/architecture.md)

## Integration Guides
- [Gemini CLI Integration](Integration/gemini/README.md) - run Capstone agents via the Gemini CLI.
- [Cursor IDE Multi-Agent Integration](Integration/cursor-ide/README.md) - import all Capstone agents as switchable roles inside Cursor.
- [Cursor CLI Integration](Integration/cursor-cli/) - use Capstone agents with the Cursor terminal agent.
- [OpenCodex CLI Integration](Integration/opencodex/README.md) - run agents via the OpenAI Codex CLI.
- [Qwen CLI Integration (QwenCLI)](Integration/qwencli/) - use QwenCLI with Capstone agents.
- [RoboDev Integration](Integration/robodev/README.md) - connect Capstone agents with RoboDev profiles.
- [RovoDev CLI Integration](Integration/rovodev/README.md) - use Capstone agents with Atlassian's RovoDev CLI.
- [GitHub Copilot CLI Integration](Integration/copilot/README.md) - use Capstone agents with the standalone Copilot CLI.
- [VS Code Copilot Integration](Integration/vscode-copilot/README.md) - configure VS Code for Capstone agent workflows.

## License
MIT
