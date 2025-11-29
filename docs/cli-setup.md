# CLI Setup Guide

This guide covers the installation and configuration of all supported CLI tools for Capstone Agents.

## Prerequisites

Before installing any CLI tool, ensure you have:

- **Node.js 18+**: Required for MCP servers
  ```bash
  node --version  # Should be v18.0.0 or higher
  ```
- **Python 3.8+**: Required for automation scripts
  ```bash
  python --version  # Should be 3.8 or higher
  ```
- **Git**: For version control operations
  ```bash
  git --version
  ```

## Environment Setup

Create a `.env` file in your workspace root:

```bash
# Copy the example file
cp .env.example .env

# Edit with your API keys
```

### Required Environment Variables

```bash
# GitHub (for github MCP)
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxxxxxxxxx

# Figma (for figma MCP)
FIGMA_ACCESS_TOKEN=figd_xxxxxxxxxxxx

# Supabase (for supabase MCP)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# Slack (for slack MCP)
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx
SLACK_TEAM_ID=T0XXXXXXX

# Sentry (for sentry MCP)
SENTRY_AUTH_TOKEN=your-sentry-token

# CLI-specific keys
GEMINI_API_KEY=your-gemini-key
OPENAI_API_KEY=sk-xxxxxxxxxxxx
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxx
```

---

## Gemini CLI

### Installation

```bash
# Using npm
npm install -g @anthropic-ai/gemini-cli

# Or using pip
pip install gemini-cli
```

### Configuration

```bash
# Set API key
export GEMINI_API_KEY=your_api_key

# Verify installation
gemini --version
```

### Usage with Capstone Agents

```bash
# Run coordinator agent
python scripts/run_agents.py --cli gemini --agents coordinator

# Direct usage
gemini chat --system-prompt "$(cat agents/coordinator/coordinator.md)"
```

---

## Cursor IDE & CLI

### Installation

1. Download from [cursor.sh](https://cursor.sh/)
2. Install the application
3. Enable CLI access:
   - Open Cursor
   - Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
   - Type "Install 'cursor' command in PATH"

### Configuration

```bash
# macOS/Linux: Add to PATH if not automatic
export PATH="$PATH:/Applications/Cursor.app/Contents/MacOS"

# Windows: Added automatically during installation
```

### Verification

```bash
cursor --version
cursor --help
```

### Usage with Capstone Agents

```bash
# Open workspace in Cursor
cursor /path/to/your/project

# Run via script
python scripts/run_agents.py --cli cursor --agents frontend
```

---

## OpenAI OpenCodex CLI

### Installation

```bash
# Using npm
npm install -g @openai/codex-cli

# Or using pip
pip install openai-codex
```

### Configuration

```bash
# Set API key
export OPENAI_API_KEY=sk-xxxxxxxxxxxx

# Verify
codex --version
```

### Usage with Capstone Agents

```bash
# Run agent
python scripts/run_agents.py --cli opencodex --agents backend

# Direct usage
codex run --system "$(cat agents/backend/backend-planning.md)" \
  --prompt "Design the API architecture"
```

---

## QwenCLI

### Installation

```bash
# Using pip
pip install qwen-cli

# Or install DashScope SDK
pip install dashscope
```

### Configuration

```bash
# Set API key (DashScope)
export DASHSCOPE_API_KEY=sk-xxxxxxxxxxxx

# Or Qwen-specific key
export QWEN_API_KEY=your_api_key
```

### Verification

```bash
qwen --version
qwen chat --help
```

### Usage with Capstone Agents

```bash
# Run agent
python scripts/run_agents.py --cli qwen --agents designer

# Direct usage
qwen chat --system-prompt "$(cat agents/designer/designer-planning.md)"
```

---

## RoboDev CLI

### Installation

```bash
# Using npm
npm install -g robodev-cli

# Or using pip
pip install robodev
```

### Configuration

```bash
# Authenticate
robodev auth login

# Or set API key
export ROBODEV_API_KEY=your_api_key
```

### Verification

```bash
robodev --version
robodev profile list
```

### Usage with Capstone Agents

```bash
# Load profiles
robodev profile load ./integration/robodev/robodev-profile.json

# Run agent
python scripts/run_agents.py --cli robodev --agents devops
```

---

## GitHub Copilot CLI

> **Note**: The old `gh copilot` extension is retired. This section covers the new standalone GitHub Copilot CLI.

### Prerequisites

- **Node.js 22+** and **npm 10+**
- **GitHub Copilot subscription** (Pro, Pro+, Business, or Enterprise)

### Installation

```bash
# Install the new GitHub Copilot CLI
npm install -g @github/copilot

# Verify installation
copilot --version
```

### Authentication

```bash
# Launch Copilot CLI and authenticate
copilot
# Then type: /login
```

### Key Features

| Feature | Command |
|---------|---------|
| Interactive mode | `copilot` |
| Programmatic mode | `copilot -p "prompt"` |
| Resume session | `copilot --resume` |
| Reference files | `@path/to/file.md` in chat |
| Run shell commands | `!git status` in chat |

### Usage with Capstone Agents

```bash
# Interactive session with designer agent
python scripts/run_agents.py -c copilot-cli -a designer -i

# Batch mode (auto-execute)
python scripts/run_agents.py -c copilot-cli -a backend

# Direct usage - reference agent file in session
copilot
# Then type: @agents/coordinator/coordinator.md help me plan my project
```

### Windows Note

Native Windows PowerShell support is experimental. For best results on Windows, use WSL:

```bash
wsl
copilot
```

---

## VS Code Copilot

### Installation

1. Install [VS Code](https://code.visualstudio.com/)
2. Install the GitHub Copilot extension from the marketplace
3. Sign in with your GitHub account

### Configuration

```bash
# Run setup script
python scripts/setup_vscode_copilot.py

# This creates:
# - .vscode/tasks.json
# - capstone-agents.code-workspace
```

### Usage with Capstone Agents

1. Open `capstone-agents.code-workspace` in VS Code
2. Press `Ctrl+Shift+P` → "Tasks: Run Task"
3. Select an agent task (e.g., "Run Coordinator Agent")

See [VS Code Copilot Guide](vscode-copilot-guide.md) for detailed instructions.

---

## Quick Reference

| CLI | Install Command | API Key Variable |
|-----|-----------------|------------------|
| Gemini | `npm i -g @anthropic-ai/gemini-cli` | `GEMINI_API_KEY` |
| Cursor | Download from cursor.sh | N/A (uses built-in) |
| OpenCodex | `npm i -g @openai/codex-cli` | `OPENAI_API_KEY` |
| QwenCLI | `pip install qwen-cli` | `DASHSCOPE_API_KEY` |
| RoboDev | `npm i -g robodev-cli` | `ROBODEV_API_KEY` |
| Copilot CLI | `npm i -g @github/copilot` | GitHub Auth (`/login`) |
| VS Code | Download from code.visualstudio.com | GitHub Auth |

---

## Troubleshooting

### "Command not found"

Ensure the CLI is in your PATH:
```bash
# Check PATH
echo $PATH

# Find command location
which gemini  # or cursor, codex, qwen, etc.
```

### "API key not set"

```bash
# Verify environment variable
echo $GEMINI_API_KEY

# Set in current session
export GEMINI_API_KEY=your_key

# Or add to shell profile
echo 'export GEMINI_API_KEY=your_key' >> ~/.bashrc
source ~/.bashrc
```

### "Rate limited"

Add delays between requests:
```bash
python scripts/run_agents.py --cli gemini --agents frontend --delay 5
```

### "MCP server connection failed"

```bash
# Check if Node.js is installed
node --version

# Try running MCP server manually
npx -y @modelcontextprotocol/server-filesystem .
```

### Windows-Specific Issues

```powershell
# Use PowerShell for better compatibility
# Set environment variables
$env:GEMINI_API_KEY = "your_key"

# Or set permanently
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your_key", "User")
```
