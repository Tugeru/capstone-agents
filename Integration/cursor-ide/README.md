# Cursor IDE Multi-Agent Integration

Import and use multiple Capstone agents inside Cursor IDE as switchable AI roles.

## Quick Start

```bash
# From the capstone-agents repository
./Integration/cursor-ide/import.sh /path/to/your/project

# Or using Python directly
python Integration/cursor-ide/generate_cursorrules.py --workspace /path/to/your/project
```

This generates a `.cursorrules` file in your project with all Capstone agents. Open the project in Cursor, and the agents are ready to use.

## Features

- **Multiple Agent Roles**: All 11 Capstone roles available in a single workspace
- **Easy Switching**: Change agents with `@RoleName` commands
- **Planning & Implementation**: Separate variants for design vs coding tasks
- **Parallel Sessions**: Run multiple chat tabs, each with a different agent
- **File-Based Collaboration**: Agents share context via workspace files

## Installation

### Option 1: Shell Script (Recommended)

```bash
# Make executable (first time only)
chmod +x Integration/cursor-ide/import.sh

# Import all agents
./Integration/cursor-ide/import.sh /path/to/your/project

# Import specific roles only
./Integration/cursor-ide/import.sh /path/to/your/project --roles coordinator,frontend,backend

# Planning agents only
./Integration/cursor-ide/import.sh /path/to/your/project --planning-only
```

### Option 2: Python Script

```bash
# All agents
python Integration/cursor-ide/generate_cursorrules.py --workspace /path/to/your/project

# Specific roles
python Integration/cursor-ide/generate_cursorrules.py --workspace . --roles coordinator,frontend,backend,devops

# Planning only
python Integration/cursor-ide/generate_cursorrules.py --workspace . --planning-only

# Implementation only
python Integration/cursor-ide/generate_cursorrules.py --workspace . --impl-only

# Preview without writing
python Integration/cursor-ide/generate_cursorrules.py --workspace . --dry-run
```

## Usage in Cursor IDE

### 1. Open Your Project

```bash
cursor /path/to/your/project
```

### 2. Switch Between Agents

In the Cursor chat, use these commands to activate different agents:

| Command | Agent |
|---------|-------|
| `@Coordinator` | Project planning and task delegation |
| `@Frontend` | Frontend planning agent |
| `@Frontend impl` | Frontend implementation agent |
| `@Backend` | Backend planning agent |
| `@Backend impl` | Backend implementation agent |
| `@DevOps` | DevOps and infrastructure |
| `@Designer` | UI/UX design |
| `@Database Engineer` | Database schema and queries |
| `@Software Architect` | System architecture |
| `@QA` | Testing and quality assurance |
| `@Documentation` | Technical writing |
| `@Project Manager` | Timeline and milestones |
| `@Blockchain` | Smart contracts and Web3 |

### 3. Multi-Agent Workflow

Open multiple chat tabs for parallel agent work:

```
┌─────────────────────────────────────────────────────────────────┐
│ Tab 1: @Coordinator                                             │
│ "Create a project plan for user authentication"                 │
│ → Writes: coordinator-plan.md                                   │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Tab 2: @Backend impl                                            │
│ "Read coordinator-plan.md and implement the auth API"           │
│ → Creates: src/api/auth.ts                                      │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Tab 3: @Frontend impl                                           │
│ "Build the login form based on the backend API"                 │
│ → Creates: src/components/LoginForm.tsx                         │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Reference Files

Use Cursor's `@file` syntax to share context:

```
@coordinator-plan.md What tasks are assigned to frontend?
@src/api/auth.ts Review this endpoint implementation
```

## Available Agents

| Role | Planning | Implementation | Focus |
|------|----------|----------------|-------|
| Coordinator | ✅ | — | Project orchestration |
| Software Architect | ✅ | ✅ | System design |
| Frontend | ✅ | ✅ | UI and client-side |
| Backend | ✅ | ✅ | API and server-side |
| Database Engineer | ✅ | ✅ | Data modeling |
| Designer | ✅ | ✅ | UI/UX design |
| DevOps | ✅ | ✅ | Infrastructure |
| QA | ✅ | ✅ | Testing |
| Documentation | ✅ | ✅ | Technical writing |
| Project Manager | ✅ | ✅ | Timeline tracking |
| Blockchain | ✅ | ✅ | Smart contracts |

## Command Reference

```bash
# Full options
python generate_cursorrules.py \
    --workspace /path/to/project \    # Required: target workspace
    --agents-dir /path/to/agents \    # Optional: custom agents location
    --roles coordinator,frontend \    # Optional: filter specific roles
    --planning-only \                 # Optional: only planning agents
    --impl-only \                     # Optional: only implementation agents
    --output custom-name.cursorrules \ # Optional: custom output filename
    --dry-run                         # Optional: preview without writing
```

## Updating Agents

After modifying agent definitions in `agents/`, re-run the import:

```bash
./Integration/cursor-ide/import.sh /path/to/your/project
```

The `.cursorrules` file will be regenerated with the updated agent content.

## Troubleshooting

### "Agent not responding as expected"
- Ensure you're using the exact `@RoleName` format
- Try `@Coordinator` to reset to the default role
- Check that `.cursorrules` exists in your workspace root

### "Missing agents"
- Re-run the import script to regenerate `.cursorrules`
- Use `--dry-run` to preview which agents will be included

### "File too large"
- Use `--roles` to include only the agents you need
- Use `--planning-only` or `--impl-only` to reduce size

## See Also

- [CLI Setup Guide](../../docs/cli-setup.md) - Setting up CLI tools
- [Usage Guide](../../docs/usage-guide.md) - General usage patterns
- [Multi-Agent Workflows](../../docs/multi-agent-workflows.md) - Coordination patterns


