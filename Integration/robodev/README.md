# RoboDev CLI Integration

This guide explains how to use Capstone Agents with [RoboDev CLI](https://github.com/robodev-ai/robodev-cli).

## Prerequisites

1. **Install RoboDev CLI**:
   ```bash
   npm install -g robodev-cli
   # or
   pip install robodev
   ```

2. **Configure API Access**:
   ```bash
   robodev auth login
   # or set API key
   export ROBODEV_API_KEY=your_api_key
   ```

## Usage

### Running Agents via Python Script

```bash
# Navigate to your workspace
cd /path/to/your/project

# Run the coordinator agent
python scripts/run_agents.py --cli robodev --agents coordinator

# Run multiple agents
python scripts/run_agents.py --cli robodev --agents frontend backend designer
```

### Direct RoboDev CLI Usage

```bash
# Load agent profile
robodev profile load ./integration/robodev/robodev-profile.json

# Run with agent context
robodev run --profile coordinator --query "Analyze the project and create a plan"

# Interactive session
robodev chat --system-file agents/frontend/frontend-planning.md
```

## Agent Profiles

RoboDev uses JSON profiles to define agent behavior. See `integration/robodev/robodev-profile.json`.

## Workflow Example

### 1. Initialize Project

```bash
robodev run \
  --profile coordinator \
  --workspace . \
  --query "Review the project structure and create a development roadmap"
```

### 2. Parallel Planning

```bash
robodev batch \
  --profiles frontend,backend,designer \
  --context coordinator-plan.json \
  --query "Create your role-specific implementation plan" \
  --parallel
```

## MCP Integration

RoboDev has native MCP support:

```bash
robodev mcp add filesystem .mcp/filesystem.json
robodev run --profile backend --enable-mcp
```

## Troubleshooting

### "Profile not found"
```bash
robodev profile list
robodev profile reload
```

### Authentication Issues
```bash
robodev auth logout
robodev auth login
```
