# VS Code Copilot Integration

Enable Capstone Agents support in VS Code Copilot Chat with dynamic `@` mentions.

## Quick Start

1. **Generate Context File**:
   ```bash
   python Integration/vscode-copilot/generate_context.py --workspace .
   ```
   This creates a `copilot_agent_context.md` file in your workspace.

2. **Use in Copilot Chat**:
   - Open Copilot Chat (`Ctrl+I` or Sidebar).
   - **Attach the file**: Type `#file:copilot_agent_context.md` or drag and drop the file into the chat input.
   - **Invoke Agent**: Type your prompt starting with an agent trigger.

   ```text
   #file:copilot_agent_context.md @backend Plan and then implement a login API.
   ```

## Features

- **Context-Aware Routing**: The unified context file instructs Copilot to adopt the persona of the requested agent.
- **Support for All Roles**: Includes definitions for all 11 Capstone roles (Planning and Implementation).
- **Zero Extension Required**: Works with the standard GitHub Copilot Chat extension.

## Available Triggers

| Trigger | Agent Role | Type |
|---------|------------|------|
| `@backend` | Backend Developer | Unified |
| `@blockchain` | Blockchain Developer | Unified |
| `@coordinator` | Coordinator | Lead |
| `@database-engineer` | Database Engineer | Unified |
| `@designer` | UI/UX Designer | Unified |
| `@devops` | DevOps Engineer | Unified |
| `@documentation` | Documentation Specialist | Unified |
| `@frontend` | Frontend Developer | Unified |
| `@project-manager` | Project Manager | Unified |
| `@qa` | QA Engineer | Unified |
| `@software-architect` | Software Architect | Unified |

## How It Works

VS Code Copilot allows you to bring files into your chat context (`#file`). The `generate_context.py` script aggregates all agent instructions into a single Markdown file with a **Meta-Prompt**. This prompt instructs the AI to:

1. Look for triggers like `@backend` or `@coordinator`.
2. Ignore default behavior.
3. Adopt the instructions found in the context file for that specific role.

## Setup Script

You can also run the full setup script to configure tasks and workspace settings:

```bash
python scripts/setup_vscode_copilot.py
```
