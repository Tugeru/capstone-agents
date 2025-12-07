#!/usr/bin/env python3
"""
generate_context.py

Generates a consolidated Markdown file containing all Capstone Agent definitions
for use in Google's Antigravity IDE. The generated file allows users to invoke
agents with @-mention syntax.
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
    
    Prefers unified agent files ({role}.md) over legacy split files.
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

        # Check for unified agent file first
        unified_file = os.path.join(role_path, f"{role_name}.md")
        if os.path.exists(unified_file):
            agents.append({
                'role': role_name,
                'type': 'unified',
                'filepath': unified_file,
                'filename': f"{role_name}.md"
            })
            continue  # Skip legacy files if unified exists

        # Fall back to legacy files (not in legacy/ subfolder for backwards compat)
        for filename in os.listdir(role_path):
            if not filename.endswith('.md'):
                continue
            # Skip legacy subfolder
            if filename == 'legacy':
                continue

            filepath = os.path.join(role_path, filename)
            if os.path.isdir(filepath):
                continue
            
            # Determine agent type (planning or implementation)
            if 'planning' in filename.lower():
                agent_type = 'planning'
            elif 'implementation' in filename.lower():
                agent_type = 'impl'
            else:
                agent_type = 'default'

            agents.append({
                'role': role_name,
                'type': agent_type,
                'filepath': filepath,
                'filename': filename
            })
    
    return agents



def generate_trigger(role: str, agent_type: str) -> str:
    """Generate the @-mention trigger for an agent."""
    if agent_type in ['default', 'unified']:
        return f"@{role}"
    else:
        return f"@{role} {agent_type}"


def generate_context_file(agents: list[dict], workspace: str) -> str:
    """Generate the contents of the antigravity_context.md file."""
    lines = [
        "# Capstone Agents - Antigravity Context",
        "",
        "This file contains the definitions for all Capstone Agents.",
        "You can invoke an agent by using its **trigger handle** (e.g., `@frontend planning`).",
        "",
        "When the user types a trigger, you MUST adopt the persona and follow the instructions",
        "for that agent role. Continue acting as that agent until the user invokes a different trigger.",
        "",
        f"**Current Workspace**: `{workspace}`",
        "",
        "---",
        "",
        "## Available Agents",
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

        lines.append(f"## Agent: {role_title} ({type_title})")
        lines.append("")
        lines.append(f"**Trigger**: `{trigger}`")
        lines.append("")
        lines.append("**Instructions**:")
        lines.append("")
        lines.append("<details>")
        lines.append(f"<summary>View full instructions for {trigger}</summary>")
        lines.append("")
        lines.append(content.strip())
        lines.append("")
        lines.append("</details>")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Antigravity context file for Capstone Agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate context for all agents
  python generate_context.py --workspace /path/to/your/project

  # Specific roles only
  python generate_context.py --workspace . --roles coordinator,frontend,backend

  # Custom output file
  python generate_context.py --workspace . --output my_agents_context.md

  # Preview without writing
  python generate_context.py --workspace . --dry-run
        """
    )
    parser.add_argument("-w", "--workspace", default=".",
                        help="Path to the target workspace (default: current directory)")
    parser.add_argument("--agents-dir",
                        help="Custom path to agents directory")
    parser.add_argument("--roles",
                        help="Comma-separated list of roles to include (e.g., coordinator,frontend,backend)")
    parser.add_argument("-o", "--output", default="antigravity_context.md",
                        help="Output filename (default: antigravity_context.md)")
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

    print(f"Found {len(agents)} agent file(s):")
    for agent in agents:
        trigger = generate_trigger(agent['role'], agent['type'])
        print(f"  - {trigger}")
    print("-" * 60)

    # Generate context
    context_content = generate_context_file(agents, workspace)

    if args.dry_run:
        print("DRY RUN - Would generate:")
        print("=" * 60)
        # Print first 2000 chars as preview
        print(context_content[:2000])
        if len(context_content) > 2000:
            print(f"\n... ({len(context_content) - 2000} more characters)")
        print("=" * 60)
        print(f"Total size: {len(context_content)} characters")
    else:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(context_content)
            print(f"Successfully generated: {output_path}")
            print(f"Total size: {len(context_content)} characters")
            print("")
            print("Next steps:")
            print(f"  1. Open your Antigravity IDE session")
            print(f"  2. Load or paste the contents of: {output_path}")
            print(f"  3. Use @-mentions to invoke agents (e.g., @coordinator)")
        except Exception as e:
            print(f"Error writing output file: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
