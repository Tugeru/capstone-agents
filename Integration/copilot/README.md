# GitHub Copilot CLI Integration

This guide explains how to use Capstone Agents with the new [GitHub Copilot CLI](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-cli).

> **Note**: The old `gh copilot` extension is retired. This guide covers the new standalone Copilot CLI (`@github/copilot` npm package).

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Node.js | 22+ |
| npm | 10+ |
| GitHub Copilot subscription | Pro, Pro+, Business, or Enterprise |

## Installation

```bash
# Install the new GitHub Copilot CLI
npm install -g @github/copilot

# Verify installation
copilot --version
```

## Authentication

```bash
# Launch Copilot CLI
copilot

# Authenticate (first time only)
/login
```

## Usage

### Via run_agents.py Script

```bash
# Interactive planning session
python scripts/run_agents.py -c copilot-cli -a coordinator -i

# Interactive implementation session  
python scripts/run_agents.py -c copilot-cli -a frontend -i -t impl

# Batch mode (programmatic execution)
python scripts/run_agents.py -c copilot-cli -a backend
```

### Direct Copilot CLI Usage

```bash
# Start interactive session
copilot

# Reference an agent file in your prompt
@agents/frontend/frontend-planning.md Create a React component for user login

# Run shell commands
!git status
!npm install

# Resume previous session
copilot --resume
```

### Programmatic Mode (One-shot)

```bash
# Single prompt execution with tool approval
copilot -p "Create a new React component for user dashboard" \
  --allow-tool write \
  --allow-tool "shell(git)"

# Allow all tools (use with caution)
copilot -p "Set up the project structure" --allow-all-tools
```

## Custom Agents

The new Copilot CLI supports custom agents. You can:

1. **Reference agent files directly** in your prompts:
   ```
   @agents/designer/designer-planning.md help me design the UI
   ```

2. **Install custom agents** in standard locations:
   - User-level: `~/.copilot/agents/`
   - Repository-level: `.github/agents/`

3. **Use the provided agent template**:
   ```bash
   # Copy to user agents directory
   cp Integration/copilot/copilot-agent.yaml ~/.copilot/agents/
   
   # Or to repository
   mkdir -p .github/agents
   cp Integration/copilot/copilot-agent.yaml .github/agents/
   ```

## Key Commands & Slash Commands

| Command | Description |
|---------|-------------|
| `/login` | Authenticate with GitHub |
| `/model` | Change the AI model |
| `/mcp` | Manage MCP servers |
| `/usage` | View usage statistics |
| `/add-dir` | Add directory to context |
| `@file.md` | Reference a file |
| `!command` | Run shell command |

## MCP Integration

The Copilot CLI includes a built-in GitHub MCP server and can connect to additional MCP servers:

```bash
# In Copilot CLI session
/mcp add filesystem
/mcp list
```

## Windows Support

⚠️ Native Windows PowerShell support is **experimental**. For best results:

```bash
# Use WSL on Windows
wsl
copilot
```

## Troubleshooting

### "copilot: command not found"

```bash
# Verify npm global bin is in PATH
npm config get prefix
# Add to PATH if needed
export PATH="$PATH:$(npm config get prefix)/bin"
```

### "Not authenticated"

```bash
copilot
/login
```

### "Tool not approved"

Use explicit tool approval flags:
```bash
copilot -p "your prompt" --allow-tool write --allow-tool shell
```

## Migration from gh copilot

If you were using the old `gh copilot` extension:

| Old Command | New Command |
|-------------|-------------|
| `gh copilot suggest "query"` | `copilot -p "query"` |
| `gh copilot explain "code"` | `copilot` then ask to explain |
| `gh auth login` | `/login` in Copilot CLI |

## Resources

- [GitHub Copilot CLI Documentation](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-cli)
- [Copilot CLI npm Package](https://www.npmjs.com/package/@github/copilot)
