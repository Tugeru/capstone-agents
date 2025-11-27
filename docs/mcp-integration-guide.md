# MCP Integration Guide

This guide explains how to configure and use Model Context Protocol (MCP) servers with Capstone Agents.

## Overview

MCP (Model Context Protocol) enables AI agents to interact with external tools and services. Each agent role has access to specific MCP tools based on their responsibilities.

## Available MCP Servers

| MCP Server | Purpose | Used By |
|------------|---------|---------|
| **filesystem** | Read/write files in the workspace | All agents |
| **github** | Interact with GitHub repositories | Coordinator, DevOps, Architect, Backend, QA |
| **supabase** | Database operations (PostgreSQL) | Backend, Database Engineer |
| **figma** | Access Figma designs | Designer, Frontend |
| **docker** | Container management | DevOps, Backend |
| **kubernetes** | Kubernetes cluster operations | DevOps |
| **playwright** | Browser automation & testing | QA |
| **browser** | Web browsing capabilities | QA, Frontend, Designer |
| **mermaid** | Generate flowcharts, sequence, ER diagrams | Architect, Designer, DB Engineer, DevOps, Docs |
| **plantuml** | Create UML class, component diagrams | Architect, DB Engineer, DevOps, Blockchain, Docs |
| **excalidraw** | Hand-drawn wireframes and sketches | Designer |
| **memory** | Persistent context across sessions | Coordinator, Architect, PM |
| **fetch** | HTTP requests and API testing | Frontend, Backend, Architect, Blockchain, Docs |
| **sequential-thinking** | Complex reasoning chains | Architect, Backend, DB Engineer, QA, Blockchain |
| **time** | Scheduling and timezone utilities | Coordinator, PM |
| **slack** | Team communication | Coordinator, PM |
| **sentry** | Error tracking and monitoring | DevOps, QA |

## Configuration Files

MCP configurations are stored in the `.mcp/` directory:

```
.mcp/
├── filesystem.json      # File operations
├── github.json          # GitHub integration
├── supabase.json        # PostgreSQL/Supabase
├── figma.json           # Figma designs
├── docker.json          # Docker containers
├── kubernetes.json      # K8s clusters
├── playwright.json      # Browser testing
├── browser.json         # Web browsing
├── mermaid.json         # Diagram generation
├── plantuml.json        # UML diagrams
├── excalidraw.json      # Whiteboard sketches
├── memory.json          # Persistent memory
├── fetch.json           # HTTP requests
├── sequential-thinking.json  # Reasoning chains
├── time.json            # Time utilities
├── slack.json           # Slack messaging
└── sentry.json          # Error tracking
```

## Setting Up MCP Servers

### Prerequisites

- Node.js 18+ installed
- npm or npx available in PATH

### 1. Filesystem MCP

The filesystem MCP provides read/write access to the workspace.

```bash
npx -y @modelcontextprotocol/server-filesystem .
```

**Configuration** (`.mcp/filesystem.json`):
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

### 2. GitHub MCP

Enables interaction with GitHub repositories.

**Setup**:
1. Create a GitHub Personal Access Token (PAT) with `repo` scope.
2. Set the token in your environment or `.env` file.

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxxxxxxxxx
npx -y @modelcontextprotocol/server-github
```

**Configuration** (`.mcp/github.json`):
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    }
  }
}
```

### 3. Supabase MCP (PostgreSQL)

For database operations with Supabase or any PostgreSQL database.

**Setup**:
1. Ensure Supabase is running locally or have a remote connection string.
2. Default local Supabase: `postgresql://postgres:postgres@localhost:54322/postgres`

```bash
npx -y @modelcontextprotocol/server-postgres "postgresql://postgres:postgres@localhost:54322/postgres"
```

**Configuration** (`.mcp/supabase.json`):
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://postgres:postgres@localhost:54322/postgres"]
    }
  }
}
```

### 4. Figma MCP

Access Figma designs for the Designer and Frontend agents.

**Setup**:
1. Get a Figma Personal Access Token from Figma settings.
2. Set the token in your environment.

```bash
export FIGMA_ACCESS_TOKEN=figd_xxxxxxxxxxxx
npx -y @modelcontextprotocol/server-figma
```

### 5. Playwright/Browser MCP

For browser automation and testing (QA agent).

```bash
npx -y @modelcontextprotocol/server-puppeteer
```

---

## Diagram Generation MCP Servers

### 6. Mermaid MCP

Generate flowcharts, sequence diagrams, ER diagrams, and architecture diagrams.

**Best For**: Software Architect, Designer, Database Engineer, Documentation

```bash
npx -y mcp-server-mermaid
```

**Configuration** (`.mcp/mermaid.json`):
```json
{
  "mcpServers": {
    "mermaid": {
      "command": "npx",
      "args": ["-y", "mcp-server-mermaid"]
    }
  }
}
```

**Example Usage**:
```mermaid
graph TD
    A[User] --> B[Frontend]
    B --> C[API Gateway]
    C --> D[Backend Service]
    D --> E[(Database)]
```

### 7. PlantUML MCP

Create UML class diagrams, component diagrams, sequence diagrams, and deployment diagrams.

**Best For**: Software Architect, Database Engineer, DevOps, Blockchain

```bash
npx -y mcp-server-plantuml
```

**Configuration** (`.mcp/plantuml.json`):
```json
{
  "mcpServers": {
    "plantuml": {
      "command": "npx",
      "args": ["-y", "mcp-server-plantuml"]
    }
  }
}
```

**Example Usage**:
```plantuml
@startuml
class User {
  +id: UUID
  +email: String
  +passwordHash: String
  +login()
  +logout()
}

class AuthService {
  +validateCredentials()
  +generateToken()
}

User --> AuthService
@enduml
```

### 8. Excalidraw MCP

Create hand-drawn style diagrams, wireframes, and whiteboard sketches.

**Best For**: Designer, collaborative brainstorming

```bash
npx -y mcp-server-excalidraw
```

**Configuration** (`.mcp/excalidraw.json`):
```json
{
  "mcpServers": {
    "excalidraw": {
      "command": "npx",
      "args": ["-y", "mcp-server-excalidraw"]
    }
  }
}
```

---

## Utility MCP Servers

### 9. Memory MCP

Persistent memory for maintaining context across sessions.

**Best For**: Coordinator, Architect, Project Manager

```bash
npx -y @modelcontextprotocol/server-memory
```

**Configuration** (`.mcp/memory.json`):
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

**Use Cases**:
- Store architectural decisions (ADRs)
- Track project state across sessions
- Remember user preferences

### 10. Fetch MCP

HTTP client for API testing and external data retrieval.

**Best For**: Frontend, Backend, Architect, Blockchain, Documentation

```bash
npx -y @modelcontextprotocol/server-fetch
```

**Configuration** (`.mcp/fetch.json`):
```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

**Use Cases**:
- Test API endpoints
- Fetch external documentation
- Verify webhook integrations

### 11. Sequential Thinking MCP

Complex reasoning chains for architectural and optimization decisions.

**Best For**: Architect, Backend, Database Engineer, QA, Blockchain

```bash
npx -y @modelcontextprotocol/server-sequential-thinking
```

**Configuration** (`.mcp/sequential-thinking.json`):
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

**Use Cases**:
- Break down complex architecture decisions
- Optimize database queries step-by-step
- Reason through security vulnerabilities

### 12. Time MCP

Time utilities for scheduling, timestamps, and timezone handling.

**Best For**: Coordinator, Project Manager

```bash
npx -y @modelcontextprotocol/server-time
```

**Configuration** (`.mcp/time.json`):
```json
{
  "mcpServers": {
    "time": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-time"]
    }
  }
}
```

---

## Communication & Monitoring MCP Servers

### 13. Slack MCP

Team communication and notifications.

**Best For**: Coordinator, Project Manager

**Setup**:
1. Create a Slack app with Bot Token
2. Set environment variables

```bash
export SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx
export SLACK_TEAM_ID=T0XXXXXXX
npx -y @modelcontextprotocol/server-slack
```

**Configuration** (`.mcp/slack.json`):
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "<YOUR_SLACK_BOT_TOKEN>",
        "SLACK_TEAM_ID": "<YOUR_SLACK_TEAM_ID>"
      }
    }
  }
}
```

### 14. Sentry MCP

Error tracking and monitoring integration.

**Best For**: DevOps, QA

**Setup**:
1. Create a Sentry auth token
2. Set environment variable

```bash
export SENTRY_AUTH_TOKEN=your-sentry-token
npx -y @sentry/mcp-server-sentry
```

**Configuration** (`.mcp/sentry.json`):
```json
{
  "mcpServers": {
    "sentry": {
      "command": "npx",
      "args": ["-y", "@sentry/mcp-server-sentry"],
      "env": {
        "SENTRY_AUTH_TOKEN": "<YOUR_SENTRY_AUTH_TOKEN>"
      }
    }
  }
}
```

## Using MCP in Agent Prompts

Each agent's `.md` file specifies which MCP tools it can use. For example, the Backend agent:

```markdown
## MCP Tools
You have access to the following MCP tools:
- **filesystem** — Read and write source code files
- **supabase** — Query and modify the database
- **docker** — Build and manage containers
```

When an agent runs, it can invoke these tools to perform actions.

## Environment Variables

Create a `.env` file in the workspace root:

```bash
# GitHub
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxxxxxxxxx

# Figma
FIGMA_ACCESS_TOKEN=figd_xxxxxxxxxxxx

# Supabase (if using remote)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
```

## Troubleshooting

### MCP Server Not Starting

1. Ensure Node.js 18+ is installed: `node --version`
2. Clear npm cache: `npm cache clean --force`
3. Try installing globally: `npm install -g @modelcontextprotocol/server-filesystem`

### Permission Denied

- On Linux/macOS, ensure the MCP server has execute permissions.
- On Windows, run the terminal as Administrator if needed.

### Connection Refused (Supabase)

- Verify Supabase is running: `supabase status`
- Check the connection string and port.

## Further Reading

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [Supabase CLI Guide](https://supabase.com/docs/guides/cli)
- [Figma API Documentation](https://www.figma.com/developers/api)
