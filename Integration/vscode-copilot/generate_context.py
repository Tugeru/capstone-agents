#!/usr/bin/env python3
"""
generate_context.py

Generates a consolidated Markdown file containing all Capstone Agent definitions
for use in VS Code Copilot Chat. By attaching the generated file to the chat
context, users can invoke agents with @-mention syntax (e.g., @backend impl).
"""

import argparse
import os
import sys

# Path to the capstone-agents repository (where agent definitions live)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAPSTONE_AGENTS_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DEFAULT_AGENTS_DIR = os.path.join(CAPSTONE_AGENTS_DIR, "agents")


def read_agent_file(filepath: str) -> str | None:
    """Read and return the content of an agent file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")
        return None


def find_agent_files(agents_dir: str, roles: list[str] | None = None) -> list[dict]:
    """
    Discover all agent files in the agents directory.
    Returns a list of dicts with 'role', 'type', and 'filepath'.
    """
    agents = []
    if not os.path.isdir(agents_dir):
        print(f"Error: Agents directory not found: {agents_dir}")
        return agents

    for role_name in sorted(os.listdir(agents_dir)):
        role_path = os.path.join(agents_dir, role_name)
        if not os.path.isdir(role_path):
            continue

        # Filter by roles if specified
        if roles and role_name not in roles:
            continue

        for filename in os.listdir(role_path):
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(role_path, filename)
            
            # Determine agent type (planning or implementation)
            if 'planning' in filename.lower():
                agent_type = 'planning'
            elif 'implementation' in filename.lower():
                agent_type = 'impl'
            else:
                # Default/generic agent file (e.g., coordinator.md)
                agent_type = 'default'

            agents.append({
                'role': role_name,
                'type': agent_type,
                'filepath': filepath,
                'filename': filename
            })
    
    return agents


def generate_trigger(role: str, agent_type: str) -> str:
    """Generate the checkable trigger for an agent."""
    if agent_type == 'default':
        return f"@{role}"
    else:
        return f"@{role} {agent_type}"


def generate_context_file(agents: list[dict], workspace: str) -> str:
    """Generate the contents of the copilot_agent_context.md file."""
    lines = [
        "# VS Code Copilot - Agent Context Definitions",
        "",
        "> **SYSTEM INSTRUCTION**:",
        "> You are an AI assistant in VS Code. The user has explicitly provided this context file",
        "> to define a set of specialized agent roles. ",
        ">",
        "> **YOUR GOAL**: When the user's prompt starts with a specific **trigger** (defined below),",
        "> you MUST completely adopt the persona and instructions of that agent.",
        ">",
        "> **RULES**:",
        "> 1. Check the user's prompt for a trigger like `@backend impl` or `@coordinator`.",
        "> 2. If a trigger is found, ignore your default behavior and strictly follow the Agent Definition below.",
        "> 3. Maintain this persona for the duration of the response.",
        "> 4. If no trigger is found, act as a helpful coding assistant.",
        "",
        f"**Workspace**: `{workspace}`",
        "",
        "## Agent Triggers Index",
        "",
        "| Trigger | Role | Type |",
        "|---------|------|------|",
    ]

    # Add summary table
    for agent in agents:
        trigger = generate_trigger(agent['role'], agent['type'])
        lines.append(f"| `{trigger}` | {agent['role'].replace('-', ' ').title()} | {agent['type'].title()} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Add full agent definitions
    for agent in agents:
        trigger = generate_trigger(agent['role'], agent['type'])
        content = read_agent_file(agent['filepath'])
        
        if content is None:
            continue

        role_title = agent['role'].replace('-', ' ').title()
        type_title = agent['type'].title()

        lines.append(f"## Definition: {role_title} ({type_title})")
        lines.append(f"**Trigger**: `{trigger}`")
        lines.append("")
        lines.append("**Agent Instructions**:")
        lines.append("```markdown")
        lines.append(content.strip())
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate VS Code Copilot context file for Capstone Agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate context for all agents
  python generate_context.py --workspace /path/to/your/project

  # Specific roles only
  python generate_context.py --workspace . --roles coordinator,frontend,backend

  # Custom output file
  python generate_context.py --workspace . --output my_context.md
        """
    )
    parser.add_argument("-w", "--workspace", default=".",
                        help="Path to the target workspace (default: current directory)")
    parser.add_argument("--agents-dir",
                        help="Custom path to agents directory")
    parser.add_argument("--roles",
                        help="Comma-separated list of roles to include")
    parser.add_argument("-o", "--output", default="copilot_agent_context.md",
                        help="Output filename (default: copilot_agent_context.md)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview output without writing to file")

    args = parser.parse_args()

    # Resolve paths
    workspace = os.path.abspath(args.workspace)
    agents_dir = os.path.abspath(args.agents_dir) if args.agents_dir else DEFAULT_AGENTS_DIR
    output_path = os.path.join(workspace, args.output)

    # Parse roles filter
    roles = None
    if args.roles:
        roles = [r.strip() for r in args.roles.split(',')]

    print(f"Workspace: {workspace}")
    print(f"Agents directory: {agents_dir}")
    print(f"Output: {output_path}")
    if roles:
        print(f"Roles filter: {', '.join(roles)}")
    print("-" * 60)

    # Find agent files
    agents = find_agent_files(agents_dir, roles)
    if not agents:
        print("Error: No agent files found.")
        sys.exit(1)

    print(f"Found {len(agents)} agent file(s).")

    # Generate context
    context_content = generate_context_file(agents, workspace)

    if args.dry_run:
        print("DRY RUN - Preview:")
        print("=" * 60)
        print(context_content[:2000])
        print("=" * 60)
    else:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(context_content)
            print(f"Successfully generated: {output_path}")
            print("")
            print("Usage in VS Code Copilot:")
            print(f"1. Open Copilot Chat")
            print(f"2. Attach this file: #file:{args.output} (or drag and drop)")
            print(f"3. Start typing: @coordinator or @backend impl")
        except Exception as e:
            print(f"Error writing output file: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
