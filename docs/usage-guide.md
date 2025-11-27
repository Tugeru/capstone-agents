# Usage Guide

This guide covers everything you need to know to effectively use Capstone Agents in your software development workflow.

## Quick Start

```bash
# 1. Clone and enter the repository
git clone https://github.com/your-org/capstone-agents.git
cd capstone-agents

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 3. Run the Coordinator agent to start
python scripts/run_agents.py --agents coordinator --cli vscode
```

---

## Agent Roles Overview

| Role | Planning Agent | Implementation Agent | Primary Purpose |
|------|----------------|---------------------|-----------------|
| **Coordinator** | ✅ | — | Project planning, task delegation |
| **Software Architect** | ✅ | ✅ | System design, technology selection |
| **Frontend Developer** | ✅ | ✅ | UI implementation, client-side logic |
| **Backend Developer** | ✅ | ✅ | API development, server-side logic |
| **Database Engineer** | ✅ | ✅ | Schema design, query optimization |
| **UI/UX Designer** | ✅ | ✅ | Wireframing, prototyping, design systems |
| **DevOps Engineer** | ✅ | ✅ | CI/CD, infrastructure, containerization |
| **QA Engineer** | ✅ | ✅ | Testing, quality assurance, bug tracking |
| **Documentation** | ✅ | ✅ | Technical writing, API docs, user guides |
| **Project Manager** | ✅ | ✅ | Timeline tracking, milestone management |
| **Blockchain Developer** | ✅ | ✅ | Smart contracts, Web3 integration |

---

## Running Agents

### Single Agent
To run a single agent, use the `launch-agent.sh` script:
```bash
./scripts/launch-agent.sh coordinator
```

Or use Python directly:
```bash
python scripts/run_agents.py --agents coordinator --cli gemini
```

### Multiple Agents
To run multiple agents in parallel, use `run-agents.sh`:
```bash
./scripts/run-agents.sh --agents frontend backend designer
```

Or with Python:
```bash
python scripts/run_agents.py --agents frontend backend designer --cli cursor
```

### CLI Selection
You can specify which CLI tool to use with the `--cli` flag:
```bash
python scripts/run_agents.py --cli cursor --agents designer
```

Supported CLIs:
- `gemini` — Google Gemini CLI
- `cursor` — Cursor IDE/CLI
- `qwen` — QwenCLI (Alibaba)
- `opencodex` — OpenAI Codex CLI
- `copilot` — GitHub Copilot CLI
- `robodev` — RoboDev CLI
- `vscode` — VS Code Copilot (prints instructions)

---

## Workflow

### Standard Development Flow

```mermaid
graph LR
    A[Requirements] --> B[Coordinator]
    B --> C[Planning Agents]
    C --> D[Implementation Agents]
    D --> E[QA Agent]
    E --> F[Documentation]
    F --> G[Delivery]
```

### Step-by-Step

1. **Planning Phase**
   - Coordinator analyzes project requirements
   - Creates master task breakdown
   - Assigns tasks to specialized agents

2. **Design Phase**
   - Software Architect designs system architecture
   - Database Engineer designs schema
   - Designer creates UI/UX wireframes

3. **Implementation Phase**
   - Frontend builds UI components
   - Backend implements API endpoints
   - DevOps sets up infrastructure

4. **Quality Phase**
   - QA writes and runs tests
   - Agents review each other's work
   - Bugs are logged and fixed

5. **Documentation Phase**
   - Technical Writer documents APIs
   - User guides are created
   - README is updated

---

## Output Files

Each agent produces output files in the workspace:

### Plan Files (JSON)

```json
{
  "role": "frontend",
  "version": "1.0",
  "created": "2025-11-27T10:00:00Z",
  "tasks": [
    {
      "id": "fe-task-1",
      "description": "Create login component",
      "status": "pending",
      "dependencies": ["be-task-1"]
    }
  ]
}
```

### Plan Files (Markdown)

```markdown
# Frontend Development Plan

## Overview
This plan outlines the frontend implementation strategy...

## Tasks

### 1. Create Login Component
- Build form with email/password fields
- Add validation
- Connect to auth API

### 2. Implement Dashboard
...
```

### Status Values

| Status | Description |
|--------|-------------|
| `pending` | Not yet started |
| `in-progress` | Currently being worked on |
| `completed` | Successfully finished |
| `blocked` | Waiting on a dependency |
| `failed` | Encountered an error |

---

## Agent Scripts

### `run_agents.py`

The main script for running agents.

```bash
# Basic usage
python scripts/run_agents.py --agents <agent_names> --cli <cli_tool>

# Examples
python scripts/run_agents.py --agents coordinator
python scripts/run_agents.py --agents frontend backend --cli cursor
python scripts/run_agents.py --agents qa --cli gemini --workspace /path/to/project
```

**Arguments**:
- `--agents`: Space-separated list of agent names
- `--cli`: CLI tool to use (default: gemini)
- `--workspace`: Path to workspace (default: current directory)

### `generate-agent.py`

Scaffold new agent files.

```bash
python scripts/generate-agent.py /path/to/workspace
```

### `validate-agent.py`

Validate agent file structure.

```bash
python scripts/validate-agent.py /path/to/workspace

# Expected output:
# PASS: agents/coordinator/coordinator.md
# PASS: agents/frontend/frontend-planning.md
# ...
# All agents validated successfully.
```

### `setup_vscode_copilot.py`

Configure VS Code for Copilot integration.

```bash
python scripts/setup_vscode_copilot.py /path/to/workspace
```

---

## Best Practices

### 1. Start with the Coordinator
Always begin your workflow with the Coordinator agent to establish a project plan.

### 2. Run Planning Before Implementation
Execute planning agents before their corresponding implementation agents.

### 3. Check Plan Files
Review generated plan files between agent runs to ensure alignment.

### 4. Use the Right CLI for the Task
- **Gemini/Cursor**: Best for complex reasoning tasks
- **OpenCodex**: Good for code generation
- **VS Code Copilot**: Best for iterative development

### 5. Validate Regularly
Run `validate-agent.py` after making changes to agent files.

---

## Troubleshooting

### "Agent not found"
```bash
# Check available agents
ls agents/

# Verify agent file exists
cat agents/frontend/frontend-planning.md
```

### "CLI not available"
```bash
# Check CLI installation
which gemini  # or cursor, codex, qwen

# See CLI setup guide
cat docs/cli-setup.md
```

### "Plan file parsing error"
```bash
# Validate JSON syntax
python -m json.tool frontend-plan.json

# Check for common issues:
# - Trailing commas
# - Missing quotes
# - Invalid escape characters
```

### "MCP server connection failed"
```bash
# Ensure Node.js is installed
node --version

# Test MCP server manually
npx -y @modelcontextprotocol/server-filesystem .
```

---

## Examples

### Example 1: Create a New Feature

```bash
# Step 1: Coordinator plans the feature
python scripts/run_agents.py --agents coordinator --cli vscode

# Step 2: Architect designs the solution
python scripts/run_agents.py --agents software-architect --cli cursor

# Step 3: Development (parallel)
python scripts/run_agents.py --agents frontend backend --cli cursor

# Step 4: Testing
python scripts/run_agents.py --agents qa --cli vscode

# Step 5: Documentation
python scripts/run_agents.py --agents documentation --cli vscode
```

### Example 2: Bug Fix Workflow

```bash
# QA identifies and documents the bug
python scripts/run_agents.py --agents qa --cli vscode

# Relevant developer fixes it
python scripts/run_agents.py --agents backend --cli cursor

# QA verifies the fix
python scripts/run_agents.py --agents qa --cli vscode
```

### Example 3: Design Review

```bash
# Designer creates wireframes
python scripts/run_agents.py --agents designer --cli cursor

# Architect reviews for feasibility
python scripts/run_agents.py --agents software-architect --cli cursor

# Frontend plans implementation
python scripts/run_agents.py --agents frontend --cli cursor
```
