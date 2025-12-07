#!/usr/bin/env python3
"""
generate_context.py

Generates a consolidated Markdown file containing all Capstone Agent definitions.
This allows users to invoke agents with @-mention syntax within a single chat session.

This is a shared utility used by run_agents.py for multi-agent context mode.
"""

import argparse
import os
import sys

# Path to the capstone-agents repository
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAPSTONE_AGENTS_DIR = os.path.dirname(SCRIPT_DIR)  # scripts/ -> root
DEFAULT_AGENTS_DIR = os.path.join(CAPSTONE_AGENTS_DIR, "agents")


def read_agent_file(filepath: str) -> str | None:
    """Read and return the content of an agent file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return None


def find_agent_files(agents_dir: str, roles: list[str] | None = None) -> list[dict]:
    """
    Discover all agent files in the agents directory.
    Returns a list of dicts with 'role', 'type', and 'filepath'.
    """
    agents = []
    if not os.path.isdir(agents_dir):
        print(f"Error: Agents directory not found: {agents_dir}", file=sys.stderr)
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
                'filepath': unified_file
            })
            continue

        # Fall back to legacy files
        for filename in os.listdir(role_path):
            if not filename.endswith('.md'):
                continue
            if filename == 'legacy':
                continue

            filepath = os.path.join(role_path, filename)
            if os.path.isdir(filepath):
                continue
            
            if 'planning' in filename.lower():
                agent_type = 'planning'
            elif 'implementation' in filename.lower():
                agent_type = 'impl'
            else:
                agent_type = 'default'

            agents.append({
                'role': role_name,
                'type': agent_type,
                'filepath': filepath
            })
    
    return agents


def generate_trigger(role: str, agent_type: str) -> str:
    """Generate the @-mention trigger for an agent."""
    if agent_type in ['default', 'unified']:
        return f"@{role}"
    else:
        return f"@{role} {agent_type}"


def generate_system_prompt(agents: list[dict], workspace: str) -> str:
    """Generate the consolidated system prompt."""
    lines = [
        "# Capstone Agents System Prompt",
        "",
        "You are an intelligent development assistant capable of assuming multiple expert roles.",
        "You can invoke a specific agent persona by using its **trigger handle** (e.g., `@frontend`).",
        "",
        "## User Instructions",
        "When you see a trigger like `@role`, you MUST:",
        "1. Adopt the persona and instructions of that agent completely.",
        "2. Ignore previous persona instructions if they conflict.",
        "3. Execute the user's request using that agent's capabilities.",
        "",
        f"**Current Workspace**: `{workspace}`",
        "",
        "---",
        "",
        "## Available Agents",
        ""
    ]

    # Add agent list
    for agent in agents:
        trigger = generate_trigger(agent['role'], agent['type'])
        lines.append(f"- **{trigger}**: {agent['role'].title()} Agent")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Agent Definitions")
    lines.append("")

    # Add full agent definitions
    for agent in agents:
        trigger = generate_trigger(agent['role'], agent['type'])
        content = read_agent_file(agent['filepath'])
        
        if content is None:
            continue

        lines.append(f"### Agent: {agent['role'].title()} ({trigger})")
        lines.append("```markdown")
        lines.append(content.strip())
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def get_multi_agent_context(workspace: str, agents_dir: str | None = None) -> str:
    """
    Generate and return the multi-agent context string.
    This function is meant to be imported by run_agents.py.
    """
    if agents_dir is None:
        agents_dir = DEFAULT_AGENTS_DIR
    agents = find_agent_files(agents_dir)
    return generate_system_prompt(agents, workspace)


def main():
    parser = argparse.ArgumentParser(
        description="Generate multi-agent system prompt for Capstone Agents"
    )
    parser.add_argument("-w", "--workspace", default=".", 
                        help="Path to the target workspace")
    parser.add_argument("--agents-dir", 
                        help="Custom path to agents directory")
    parser.add_argument("-o", "--output", 
                        help="Output filename (optional, prints to stdout if not set)")
    parser.add_argument("--roles",
                        help="Comma-separated list of roles to include")
    
    args = parser.parse_args()

    # Resolve paths
    workspace = os.path.abspath(args.workspace)
    agents_dir = os.path.abspath(args.agents_dir) if args.agents_dir else DEFAULT_AGENTS_DIR

    # Parse roles filter
    roles = None
    if args.roles:
        roles = [r.strip() for r in args.roles.split(',')]

    # Find agent files
    agents = find_agent_files(agents_dir, roles)
    
    if not agents:
        print("Error: No agent files found.", file=sys.stderr)
        sys.exit(1)
    
    # Generate content
    content = generate_system_prompt(agents, workspace)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Generated context file: {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(content)


if __name__ == "__main__":
    main()
