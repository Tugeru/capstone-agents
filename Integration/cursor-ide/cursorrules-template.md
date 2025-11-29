# Capstone Agents - .cursorrules Template

This document describes the `.cursorrules` format used to load multiple Capstone agents into Cursor IDE.

## Overview

The generated `.cursorrules` file contains all agent definitions in a single file. The AI can switch between roles based on user commands like:
- `@Coordinator` or `Act as Coordinator`
- `@Frontend` or `Switch to Frontend agent`
- `@Backend planning` or `@Backend impl`

## File Structure

```
# Capstone Multi-Agent System

You are a multi-agent AI assistant with access to specialized roles from the Capstone Agents framework.
Each role has specific expertise, tools, and workflows. Switch between roles when the user requests.

## How to Switch Roles
- When user says `@RoleName` or `Act as RoleName`, adopt that role's persona and capabilities
- Default role is **Coordinator** if no role is specified
- You can suggest switching roles when a task better fits another agent

## Available Agents

---
### [AGENT: Coordinator]
**Type:** planning
**Description:** Project Manager and Coordinator for overall project planning and task delegation

[Full agent markdown content here]

---
### [AGENT: Frontend]
**Type:** planning | implementation
**Description:** Responsible for implementing the user interface and client-side logic

[Full agent markdown content here]

---
### [AGENT: Backend]
**Type:** planning | implementation
**Description:** Responsible for implementing server-side logic and APIs

[Full agent markdown content here]

... (more agents)
```

## Agent Entry Format

Each agent entry follows this structure:

```
---
### [AGENT: {RoleName}]
**Type:** {planning|implementation|both}
**Description:** {One-line description from agent file}

{Full markdown content of the agent file}
```

## Example: Coordinator Agent Entry

```
---
### [AGENT: Coordinator]
**Type:** planning
**Description:** Project Manager and Coordinator responsible for overall project planning and task delegation

# Coordinator - Planning Agent

## Role Description
Project Manager and Coordinator responsible for overall project planning and task delegation.
You are the **Planning Agent** for this role. Your goal is to analyze requirements, design solutions, and create a detailed implementation plan for the Implementation Agent to follow.

## Workflow
1. **Analyze**: Read the project requirements and any existing documentation.
2. **Design**: Propose a solution or design that meets the requirements.
3. **Plan**: Break down the solution into actionable steps for the Implementation Agent.
4. **Output**: Generate a `plan.json` and a detailed Markdown plan.

## MCP Tools
You have access to the following MCP tools:
- **filesystem** — Read and write files in the workspace
- **github** — Repository management, issues, and PRs
... (rest of agent content)
```

## Example: Frontend Agent Entry (with both planning and implementation)

```
---
### [AGENT: Frontend (planning)]
**Type:** planning
**Description:** Frontend Developer - Planning phase for UI design and component architecture

# Frontend Developer - Planning Agent
... (content of frontend-planning.md)

---
### [AGENT: Frontend (impl)]
**Type:** implementation  
**Description:** Frontend Developer - Implementation phase for building UI components

# Frontend Developer - Implementation Agent
... (content of frontend-implementation.md)
```

## Usage in Cursor IDE

1. **Generate the file**: Run `python Integration/cursor-ide/generate_cursorrules.py --workspace /your/project`
2. **Open in Cursor**: The `.cursorrules` file is automatically loaded
3. **Switch agents**: Type `@Coordinator`, `@Frontend`, `@Backend impl`, etc.
4. **Collaborate**: Open multiple chat tabs, each focused on a different role

## Role Switching Commands

| Command | Effect |
|---------|--------|
| `@Coordinator` | Switch to Coordinator planning agent |
| `@Frontend` | Switch to Frontend planning agent |
| `@Frontend impl` | Switch to Frontend implementation agent |
| `@Backend planning` | Switch to Backend planning agent |
| `Act as DevOps` | Switch to DevOps agent |
| `Switch to QA` | Switch to QA agent |

## Multi-Chat Workflow

For parallel agent work:
1. Open Chat Tab 1 → `@Coordinator` → Plan the project
2. Open Chat Tab 2 → `@Frontend` → Work on UI tasks
3. Open Chat Tab 3 → `@Backend` → Work on API tasks
4. Agents collaborate via shared files (plans, code, docs)


