# Cursor CLI Integration

This guide explains how to use Capstone Agents with [Cursor CLI](https://cursor.sh/).

## Prerequisites

1. **Install Cursor**:
   - Download from [cursor.sh](https://cursor.sh/)
   - Or install via command line (macOS): `brew install cursor`

2. **Enable CLI Access**:
   - Open Cursor IDE
   - Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
   - Type "Install 'cursor' command in PATH"

## Usage

### Running Agents via Python Script

```bash
# Navigate to your workspace
cd /path/to/your/project

# Planning session with coordinator (planning agent)
python scripts/run_agents.py -a coordinator -c cursor -w /path/to/your/project -i -t p

# Implementation session with frontend (implementation agent)
python scripts/run_agents.py -a frontend -c cursor -w /path/to/your/project -i -t impl
```

### Direct Cursor CLI Usage

```bash
# Open workspace in Cursor with agent context
cursor --new-window /path/to/your/project

# The agent files will be available in the sidebar
# Open agents/coordinator/coordinator.md and use it as context
```

## Using Agents in Cursor IDE

### Method 1: Composer (Recommended)

1. Open your project in Cursor.
2. Press `Cmd+I` (macOS) or `Ctrl+I` (Windows) to open Composer.
3. Click the `+` icon to add context.
4. Select the agent file (e.g., `agents/frontend/frontend-planning.md`).
5. Type your request: "Using this agent's role, analyze the project and create a frontend plan."

### Method 2: Chat with File Context

1. Open the agent `.md` file in the editor.
2. Select all content (`Cmd+A` / `Ctrl+A`).
3. Open Cursor Chat (`Cmd+L` / `Ctrl+L`).
4. The selected content will be included as context.
5. Ask: "Act as this agent and perform your workflow."

### Method 3: Rules for AI

Create a `.cursorrules` file in your project root to automatically apply agent behavior.

## Troubleshooting

### Cursor CLI Not Found
```bash
# macOS/Linux: Add to PATH
export PATH="$PATH:/Applications/Cursor.app/Contents/MacOS"
```

### Agent Context Too Long
If the agent file exceeds context limits, split the agent into smaller, focused prompts.
