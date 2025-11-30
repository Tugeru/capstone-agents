# RovoDev CLI Integration

This guide explains how to use Capstone Agents with [RovoDev CLI](https://www.atlassian.com/software/rovo-dev) from Atlassian.

## Prerequisites

1. **Install RovoDev CLI**:
   ```bash
   npm install -g @atlassian/rovo-dev-cli
   ```

2. **Authenticate**:
   ```bash
   acli auth login
   ```

## Usage

### Running Agents via Python Script

```bash
# Navigate to your workspace
cd /path/to/your/project

# Planning session with coordinator (planning agent)
python scripts/run_agents.py -a coordinator -c rovodev -w /path/to/your/project -i -t p

# Implementation session with frontend (implementation agent)
python scripts/run_agents.py -a frontend -c rovodev -w /path/to/your/project -i -t impl
```

### How It Works

When you run an agent with RovoDev:
1. Agent instructions are automatically copied to your clipboard
2. RovoDev CLI starts in interactive mode
3. Paste the instructions (Ctrl+V / Cmd+V) into the RovoDev prompt
4. Continue your conversation with the agent

### Direct RovoDev CLI Usage

```bash
# Start interactive session
acli rovodev run

# Then manually paste agent instructions when prompted
```

## Troubleshooting

### "acli not found"
```bash
# Verify installation
npm list -g @atlassian/rovo-dev-cli

# Add to PATH if needed
export PATH="$PATH:$(npm config get prefix)/bin"
```

### Clipboard not working
If clipboard copy fails, the instructions will be displayed in the terminal. Copy them manually.

### Windows/WSL Note
For best results on Windows, use WSL (Windows Subsystem for Linux). Native Windows PowerShell support may have limitations.

