# Capstone Agents Implementation Plan

## Phase 1: Core Infrastructure & Templates
- [x] **Define Master Agent Template**: Create a standardized Markdown template for all agents (Role, Context, MCP Tools, Workflow, Inputs/Outputs).
- [x] **Verify MCP Configurations**: Ensure `.mcp/*.json` files contain valid server configurations for Figma, Supabase, Docker, etc.
- [x] **Scaffold Agent Files**: Use the master template to populate the empty `*-planning.md` and `*-implementation.md` files for all 10 roles.

## Phase 2: Automation Scripts (Python & Bash)
- [x] **Implement `generate-agent.py`**: Create script to generate new agent files from the master template.
- [x] **Implement `validate-agent.py`**: Create script to parse agent `.md` files and validate structure, required sections, and JSON schemas.
- [x] **Implement `run_agents.py`**: Develop the main Python driver to handle CLI arguments (`--workspace`, `--cli`) and spawn agent processes.
- [x] **Implement Bash Wrappers**: Write `run-agents.sh` and `launch-agent.sh` to wrap the Python script for easy terminal usage.

## Phase 3: VS Code Copilot Integration
- [x] **Create `setup_vscode_copilot.py`**: Implement the helper script to generate `.code-workspace` files and snippet payloads.
- [x] **Build Integration Assets**: Populate `integration/vscode-copilot/` with `tasks.json` examples, system prompt templates, and usage guides.
- [x] **Develop Copilot Guide**: Write `docs/vscode-copilot-guide.md` detailing how to paste agent contexts and use the integration scripts.

## Phase 4: CLI & IDE Compatibility
- [x] **Populate Integration Folders**: Create import scripts and config files for Gemini, Cursor, OpenCodex, QwenCLI, and RoboDev in their respective `integration/` subfolders.
- [x] **Update `run_agents.py` for CLIs**: Ensure the script can detect and adapt to the specific environment (e.g., formatting output for Cursor vs. Terminal).

## Phase 5: Documentation & CI
- [x] **Write Core Documentation**: Fill `README.md`, `docs/usage-guide.md`, and `docs/mcp-integration-guide.md`.
- [x] **Setup CI/CD**: Configure `.github/workflows/validate.yml` to run `validate-agent.py` on push.
- [x] **Final Verification**: Perform a manual test run of the "Coordinator" agent in VS Code Copilot to verify the end-to-end flow.

## Phase 6: Enhanced MCP Tool Integration
- [x] **Add Diagram Generation MCP Tools**: Configure `mermaid.json`, `plantuml.json`, and `excalidraw.json` for visual diagram creation.
- [x] **Add Utility MCP Tools**: Configure `memory.json`, `fetch.json`, `time.json`, and `sequential-thinking.json` for enhanced agent capabilities.
- [x] **Add Communication MCP Tools**: Configure `slack.json` and `sentry.json` for team collaboration and error tracking.
- [x] **Update Agent Files**: Expand MCP tool lists in all agent definitions with role-appropriate tools and descriptions.

---

## MCP Tools Summary by Agent Role

| Agent | Core Tools | Diagram Tools | Utility Tools |
|-------|-----------|---------------|---------------|
| **Coordinator** | filesystem, github | mermaid | memory, time, slack |
| **Software Architect** | filesystem, github | mermaid, plantuml | sequential-thinking, memory, fetch |
| **Frontend Developer** | filesystem, browser, figma | mermaid | fetch, puppeteer |
| **Backend Developer** | filesystem, supabase, docker | mermaid | github, fetch, sequential-thinking |
| **Database Engineer** | filesystem, supabase | mermaid, plantuml | sequential-thinking, github |
| **UI/UX Designer** | filesystem, figma | mermaid, excalidraw | browser, fetch |
| **DevOps Engineer** | filesystem, docker, kubernetes, github | mermaid, plantuml | sentry |
| **QA Engineer** | filesystem, playwright, browser | — | puppeteer, fetch, github, sentry, sequential-thinking |
| **Blockchain Developer** | filesystem, github | mermaid, plantuml | fetch, sequential-thinking |
| **Project Manager** | filesystem, github | mermaid | memory, time, slack |
| **Documentation** | filesystem, github | mermaid, plantuml | fetch, browser |
