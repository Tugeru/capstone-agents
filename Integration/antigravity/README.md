# Antigravity IDE Integration

Import and use all Capstone Agents inside Google's Antigravity IDE using `@` mentions.

## Quick Start

```bash
# From the capstone-agents repository
python Integration/antigravity/generate_context.py --workspace /path/to/your/project

# Or to output to a specific file
python Integration/antigravity/generate_context.py --workspace /path/to/your/project --output my_agents.md
```

This generates an `antigravity_context.md` file. Load this file into your Antigravity session to enable all agents. You can then invoke any agent by using its `@` trigger.

## Features

- **Universal Agent Import**: Load all 11 Capstone roles into a single session.
- **Dynamic Switching**: Change agents on-the-fly with `@role type` commands.
- **Planning & Implementation**: Both variants available for each role.
- **Workspace Agnostic**: Generated context can be used with any project.

## Usage

### 1. Generate Context File

```bash
python Integration/antigravity/generate_context.py --workspace .
```

### 2. Load Context in Antigravity

Copy the content of `antigravity_context.md` and paste it at the beginning of your Antigravity session, or use the file import feature if available.

### 3. Invoke Agents with `@` Mentions

| Command | Agent |
|---------|-------|
| `@coordinator` | Project planning and task delegation |
| `@frontend planning` | Frontend planning agent |
| `@frontend impl` | Frontend implementation agent |
| `@backend planning` | Backend planning agent |
| `@backend impl` | Backend implementation agent |
| `@devops planning` | DevOps planning agent |
| `@designer planning` | UI/UX design planning |
| `@database-engineer impl` | Database implementation |
| `@software-architect planning` | System architecture |
| `@qa impl` | Testing and QA |
| `@documentation planning` | Technical writing |
| `@project-manager planning` | Timeline tracking |
| `@blockchain impl` | Smart contracts |

### Example Workflow

```
User: @coordinator
      Review the project requirements in docs/ and create a task breakdown.

[Coordinator agent responds with a plan...]

User: @frontend planning
      Based on the coordinator's plan, design the frontend architecture.

[Frontend planning agent responds...]

User: @frontend impl
      Implement the components based on the plan.
```

## Command Reference

```bash
python generate_context.py \
    --workspace /path/to/project \    # Required: target workspace
    --agents-dir /path/to/agents \    # Optional: custom agents location
    --roles coordinator,frontend \    # Optional: filter specific roles
    --output custom-name.md \         # Optional: custom output filename
    --dry-run                         # Optional: preview without writing
```

## How It Works

The `generate_context.py` script reads all agent Markdown files from `agents/` and combines them into a structured document. Each agent section includes:

1.  **Trigger Handle**: The `@` command to invoke the agent (e.g., `@frontend planning`).
2.  **Role Description**: A brief summary of the agent's purpose.
3.  **Full Instructions**: The complete agent definition for context.

When you start a new Antigravity session and load this file, the IDE becomes "primed" with all agent definitions. Typing a trigger like `@backend impl` tells the assistant to adopt that persona.

## See Also

- [Usage Guide](../../docs/usage-guide.md)
- [Multi-Agent Workflows](../../docs/multi-agent-workflows.md)
- [MCP Integration Guide](../../docs/mcp-integration-guide.md)
