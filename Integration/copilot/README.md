# GitHub Copilot CLI Integration

This guide explains how to use Capstone Agents with [GitHub Copilot CLI](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line).

## Prerequisites

1. **Install GitHub CLI with Copilot Extension**:
   ```bash
   # Install GitHub CLI
   # macOS
   brew install gh
   
   # Windows
   winget install GitHub.cli
   
   # Linux
   sudo apt install gh
   ```

2. **Install Copilot Extension**:
   ```bash
   gh extension install github/gh-copilot
   ```

3. **Authenticate**:
   ```bash
   gh auth login
   gh copilot alias  # Optional: create shell aliases
   ```

## Usage

### Running Agents via Python Script

```bash
# Navigate to your workspace
cd /path/to/your/project

# Run the coordinator agent
python scripts/run_agents.py --cli copilot --agents coordinator
```

### Direct Copilot CLI Usage

GitHub Copilot CLI provides `gh copilot suggest` and `gh copilot explain` commands:

```bash
# Get code suggestions based on agent context
cat agents/frontend/frontend-planning.md | gh copilot suggest "Create a React component structure"

# Explain code using agent perspective
gh copilot explain "$(cat src/App.tsx)"
```

## Agent Workflow with Copilot CLI

### Step 1: Project Analysis

```bash
gh copilot suggest \
  "As a project coordinator, analyze the files in src/ and suggest a development plan" \
  -t shell
```

### Step 2: Code Generation

```bash
gh copilot suggest \
  "As a frontend developer, create a login component with form validation" \
  -t code
```

## Shell Aliases

Set up aliases for quick agent access:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias copilot-coord='gh copilot suggest --context "$(cat agents/coordinator/coordinator.md)"'
alias copilot-front='gh copilot suggest --context "$(cat agents/frontend/frontend-planning.md)"'
```

## Limitations

- Copilot CLI is primarily for suggestions, not full agent execution.
- No native system prompt support (must prepend to query).
- Best suited for quick code generation and shell commands.
- For full agent workflows, consider VS Code Copilot integration instead.

## Troubleshooting

### "Copilot extension not installed"
```bash
gh extension install github/gh-copilot
gh extension upgrade gh-copilot
```

### "Not authenticated"
```bash
gh auth status
gh auth login --web
```
