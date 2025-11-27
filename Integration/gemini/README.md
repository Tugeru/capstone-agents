# Gemini CLI Integration

This guide explains how to use Capstone Agents with [Gemini CLI](https://github.com/google-gemini/gemini-cli).

## Prerequisites

1. **Install Gemini CLI**:
   ```bash
   npm install -g @anthropic-ai/gemini-cli
   # or
   pip install gemini-cli
   ```

2. **Configure API Key**:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Running a Single Agent

```bash
# Navigate to your workspace
cd /path/to/your/project

# Run the coordinator agent
python scripts/run_agents.py --cli gemini --agents coordinator

# Or use the bash wrapper
./scripts/launch-agent.sh coordinator . gemini
```

### Running Multiple Agents

```bash
python scripts/run_agents.py --cli gemini --agents frontend backend designer
```

### Direct Gemini CLI Usage

You can also invoke Gemini CLI directly with an agent prompt:

```bash
# Load the agent context into Gemini
gemini chat --system-prompt "$(cat agents/coordinator/coordinator.md)"

# Or run a specific task
gemini run --file agents/frontend/frontend-planning.md --prompt "Analyze the project and create a frontend plan"
```

## Agent Workflow with Gemini

1. **Start the Coordinator**:
   ```bash
   gemini chat --system-prompt "$(cat agents/coordinator/coordinator.md)" \
     --prompt "Review the project requirements in docs/ and create a task breakdown"
   ```

2. **Invoke Planning Agents**:
   ```bash
   gemini chat --system-prompt "$(cat agents/frontend/frontend-planning.md)" \
     --prompt "Based on the coordinator's plan, design the frontend architecture"
   ```

3. **Execute Implementation Agents**:
   ```bash
   gemini chat --system-prompt "$(cat agents/frontend/frontend-implementation.md)" \
     --prompt "Implement the frontend based on the plan in frontend-plan.json"
   ```

## MCP Integration

Gemini CLI supports MCP servers. To enable MCP tools:

```bash
# Start MCP server in the background
npx -y @modelcontextprotocol/server-filesystem . &

# Run agent with MCP context
gemini chat --mcp-config .mcp/filesystem.json \
  --system-prompt "$(cat agents/backend/backend-planning.md)"
```

## Troubleshooting

### "Command not found: gemini"
Ensure Gemini CLI is installed and in your PATH:
```bash
which gemini
```

### API Rate Limits
If you hit rate limits, add delays between agent calls.
