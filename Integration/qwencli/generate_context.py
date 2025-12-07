#!/usr/bin/env python3
"""
generate_context.py

Generates a consolidated Markdown file containing all Capstone Agent definitions
for use with QwenCLI. This allows users to invoke agents with @-mention syntax
within a single chat session.
"""

import argparse
import os
import sys

# Path to the capstone-agents repository
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAPSTONE_AGENTS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))  # ../../..
# Fix: Adjust path calculation based on depth. 
# SCRIPT_DIR is d:\capstone-agents\Integration\qwencli
# CAPSTONE_AGENTS_DIR should be d:\capstone-agents
CAPSTONE_AGENTS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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


def main():
    parser = argparse.ArgumentParser(
        description="Generate QwenCLI system prompt for Capstone Agents"
    )
    parser.add_argument("-w", "--workspace", default=".", 
                        help="Path to the target workspace")
    parser.add_argument("--agents-dir", 
                        help="Custom path to agents directory")
    parser.add_argument("-o", "--output", 
                        help="Output filename (optional, prints to stdout if not set)")
    
    args = parser.parse_args()

    # Resolve paths
    workspace = os.path.abspath(args.workspace)
    if args.agents_dir:
        agents_dir = os.path.abspath(args.agents_dir)
    else:
        # Fallback logic to find agents dir relative to this script
        # Scripts at: Integration/qwencli/generate_context.py
        # Root at: ../../
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        agents_dir = os.path.join(root_dir, "agents")

    # Find agent files
    agents = find_agent_files(agents_dir)
    
    # Generate content
    content = generate_system_prompt(agents, workspace)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Generated context file: {args.output}")
        except Exception as e:
            print(f"Error writing file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(content)


if __name__ == "__main__":
    main()
