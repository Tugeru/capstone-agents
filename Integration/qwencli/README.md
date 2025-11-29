# QwenCLI Integration

This guide explains how to use Capstone Agents with [QwenCLI](https://github.com/QwenLM/qwen-cli) from Alibaba's Qwen AI.

## Prerequisites

1. **Install QwenCLI**:
   ```bash
   pip install qwen-cli
   # or
   pip install dashscope  # For DashScope API access
   ```

2. **Configure API Key**:
   ```bash
   export DASHSCOPE_API_KEY=sk-xxxxxxxxxxxx
   # or
   export QWEN_API_KEY=your_api_key
   ```

## Usage

### Running Agents via Python Script

```bash
# Navigate to your workspace
cd /path/to/your/project

# Planning session with coordinator (planning agent)
python scripts/run_agents.py -a coordinator -c qwen -w /path/to/your/project -i -t p

# Implementation session with frontend (implementation agent)
python scripts/run_agents.py -a frontend -c qwen -w /path/to/your/project -i -t impl
```

### Direct QwenCLI Usage

```bash
# Interactive chat with agent context
qwen chat --system-prompt "$(cat agents/coordinator/coordinator.md)"

# Single-shot task execution
qwen run --system "$(cat agents/frontend/frontend-planning.md)" \
  --query "Analyze the project and create a frontend plan"
```

## Agent Workflow with Qwen

### Step 1: Project Initialization

```bash
qwen chat \
  --system-prompt "$(cat agents/coordinator/coordinator.md)" \
  --query "Review the project in the current directory and create a task breakdown"
```

### Step 2: Planning Phase

```bash
# Frontend Planning
qwen run \
  --system "$(cat agents/frontend/frontend-planning.md)" \
  --query "Create a detailed frontend implementation plan" \
  > frontend-plan.json
```

## Model Selection

| Model | Use Case | Speed | Cost |
|-------|----------|-------|------|
| qwen-turbo | Quick tasks, simple code | Fast | Low |
| qwen-plus | Balanced performance | Medium | Medium |
| qwen-max | Complex reasoning, architecture | Slow | High |

## Troubleshooting

### "DashScope API key not found"
```bash
export DASHSCOPE_API_KEY=sk-xxxxxxxx
```

### Connection Timeout
Qwen servers are hosted in China; use a stable connection.
