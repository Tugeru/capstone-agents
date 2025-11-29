# OpenCodex CLI Integration

This guide explains how to use Capstone Agents with [OpenCodex CLI](https://github.com/openai/codex).

## Prerequisites

1. **Install OpenCodex CLI**:
   ```bash
   npm install -g @openai/codex-cli
   # or
   pip install openai-codex
   ```

2. **Configure API Key**:
   ```bash
   export OPENAI_API_KEY=sk-xxxxxxxxxxxx
   ```

## Usage

### Running Agents via Python Script

```bash
# Navigate to your workspace
cd /path/to/your/project

# Planning session with coordinator (planning agent)
python scripts/run_agents.py -a coordinator -c codex -w /path/to/your/project -i -t p

# Implementation session with frontend (implementation agent)
python scripts/run_agents.py -a frontend -c codex -w /path/to/your/project -i -t impl
```

### Direct OpenCodex CLI Usage

```bash
# Run with agent as system prompt
codex run --system "$(cat agents/coordinator/coordinator.md)" \
  --prompt "Analyze the project and create a development plan"

# Interactive mode with agent context
codex chat --system-file agents/frontend/frontend-planning.md
```

## Agent Workflow

### 1. Initialize Project with Coordinator

```bash
codex run \
  --system "$(cat agents/coordinator/coordinator.md)" \
  --prompt "Review the project structure and create a task breakdown" \
  --output coordinator-plan.json
```

### 2. Run Planning Agents

```bash
# Frontend Planning
codex run \
  --system "$(cat agents/frontend/frontend-planning.md)" \
  --context coordinator-plan.json \
  --prompt "Create a detailed frontend implementation plan"
```

## MCP Integration

OpenCodex supports MCP servers natively:

```bash
codex run --mcp-config .mcp/filesystem.json \
  --system "$(cat agents/backend/backend-implementation.md)" \
  --prompt "Create the API endpoints"
```

## Troubleshooting

### API Key Not Set
```bash
echo $OPENAI_API_KEY
```

### Rate Limits
Add delays between agent invocations.
