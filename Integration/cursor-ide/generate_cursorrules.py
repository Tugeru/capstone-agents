#!/usr/bin/env python3
"""
Generate a .cursorrules file for Cursor IDE with multiple Capstone agents.

Usage:
    python generate_cursorrules.py --workspace /path/to/your/project
    python generate_cursorrules.py --workspace . --roles coordinator,frontend,backend
    python generate_cursorrules.py --workspace . --planning-only
    python generate_cursorrules.py --workspace . --impl-only
"""

import argparse
import os
import sys
from pathlib import Path


# Default path to agents directory (relative to this script)
SCRIPT_DIR = Path(__file__).parent.resolve()
DEFAULT_AGENTS_DIR = SCRIPT_DIR.parent.parent / "agents"


def discover_agents(agents_dir: Path) -> dict:
    """
    Discover all available agents and their files.
    
    Returns:
        dict: {role_name: {"planning": path_or_none, "implementation": path_or_none, "default": path_or_none}}
    """
    agents = {}
    
    if not agents_dir.exists():
        print(f"Error: Agents directory not found: {agents_dir}")
        return agents
    
    for role_dir in sorted(agents_dir.iterdir()):
        if not role_dir.is_dir():
            continue
        
        role_name = role_dir.name
        agents[role_name] = {
            "planning": None,
            "implementation": None,
            "default": None
        }
        
        for md_file in role_dir.glob("*.md"):
            filename = md_file.name.lower()
            if "-planning" in filename:
                agents[role_name]["planning"] = md_file
            elif "-implementation" in filename:
                agents[role_name]["implementation"] = md_file
            else:
                # Single file agent (e.g., coordinator.md)
                agents[role_name]["default"] = md_file
    
    return agents


def read_agent_file(filepath: Path) -> str:
    """Read agent markdown file content."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")
        return ""


def extract_description(content: str) -> str:
    """Extract the first meaningful description line from agent content."""
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        # Skip headers and empty lines
        if line.startswith("#") or not line:
            continue
        # Skip "## Role Description" type headers
        if line.startswith("**") or line.startswith("You are"):
            continue
        # Found a description line
        if len(line) > 10:
            # Truncate if too long
            return line[:150] + "..." if len(line) > 150 else line
    return "Specialized agent role"


def format_role_name(role: str) -> str:
    """Format role name for display (e.g., 'software-architect' -> 'Software Architect')."""
    return role.replace("-", " ").title()


def generate_cursorrules(
    agents: dict,
    agents_dir: Path,
    roles_filter: list = None,
    planning_only: bool = False,
    impl_only: bool = False
) -> str:
    """
    Generate the .cursorrules content with all agents.
    
    Args:
        agents: Dictionary of discovered agents
        agents_dir: Path to agents directory
        roles_filter: Optional list of roles to include
        planning_only: Only include planning agents
        impl_only: Only include implementation agents
    
    Returns:
        str: Complete .cursorrules file content
    """
    
    # Header
    output = []
    output.append("# Capstone Multi-Agent System")
    output.append("")
    output.append("You are a multi-agent AI assistant with access to specialized roles from the Capstone Agents framework.")
    output.append("Each role has specific expertise, tools, and workflows. Switch between roles when the user requests.")
    output.append("")
    output.append("## How to Switch Roles")
    output.append("- When user says `@RoleName` or `Act as RoleName`, adopt that role's persona and capabilities")
    output.append("- For roles with planning/impl variants, use `@RoleName planning` or `@RoleName impl`")
    output.append("- Default role is **Coordinator** if no role is specified")
    output.append("- You can suggest switching roles when a task better fits another agent")
    output.append("")
    output.append("## Available Agents")
    output.append("")
    
    # List available roles for quick reference
    available_roles = []
    for role_name, files in sorted(agents.items()):
        if roles_filter and role_name not in roles_filter:
            continue
        display_name = format_role_name(role_name)
        variants = []
        if files["planning"] or files["default"]:
            if not impl_only:
                variants.append("planning")
        if files["implementation"]:
            if not planning_only:
                variants.append("impl")
        if variants:
            available_roles.append(f"- **{display_name}**: {', '.join(variants)}")
    
    output.extend(available_roles)
    output.append("")
    output.append("---")
    output.append("")
    
    # Agent definitions
    for role_name, files in sorted(agents.items()):
        if roles_filter and role_name not in roles_filter:
            continue
        
        display_name = format_role_name(role_name)
        
        # Planning agent
        planning_file = files["planning"] or files["default"]
        if planning_file and not impl_only:
            content = read_agent_file(planning_file)
            if content:
                description = extract_description(content)
                output.append(f"### [AGENT: {display_name}]")
                output.append(f"**Type:** planning")
                output.append(f"**Description:** {description}")
                output.append("")
                output.append(content)
                output.append("")
                output.append("---")
                output.append("")
        
        # Implementation agent (if separate file exists)
        if files["implementation"] and not planning_only:
            content = read_agent_file(files["implementation"])
            if content:
                description = extract_description(content)
                output.append(f"### [AGENT: {display_name} (impl)]")
                output.append(f"**Type:** implementation")
                output.append(f"**Description:** {description}")
                output.append("")
                output.append(content)
                output.append("")
                output.append("---")
                output.append("")
    
    # Footer with usage tips
    output.append("## Multi-Agent Collaboration Tips")
    output.append("")
    output.append("1. **Coordinator First**: Start with `@Coordinator` to create a project plan")
    output.append("2. **Delegate Tasks**: Let Coordinator assign tasks to specialized agents")
    output.append("3. **File-Based Handoff**: Agents communicate via plan files (e.g., `coordinator-plan.md`)")
    output.append("4. **Parallel Work**: Open multiple chat tabs, each with a different agent")
    output.append("5. **Reference Files**: Use `@filename` to share context between agents")
    output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Generate .cursorrules for Cursor IDE with Capstone agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate for current directory with all agents
  python generate_cursorrules.py --workspace .
  
  # Generate for a specific project
  python generate_cursorrules.py --workspace /path/to/your/project
  
  # Only include specific roles
  python generate_cursorrules.py --workspace . --roles coordinator,frontend,backend
  
  # Only planning agents
  python generate_cursorrules.py --workspace . --planning-only
  
  # Only implementation agents
  python generate_cursorrules.py --workspace . --impl-only
  
  # Custom agents directory
  python generate_cursorrules.py --workspace . --agents-dir /path/to/agents
        """
    )
    
    parser.add_argument(
        "--workspace", "-w",
        required=True,
        help="Path to the target workspace where .cursorrules will be created"
    )
    parser.add_argument(
        "--agents-dir", "-a",
        default=str(DEFAULT_AGENTS_DIR),
        help=f"Path to agents directory (default: {DEFAULT_AGENTS_DIR})"
    )
    parser.add_argument(
        "--roles", "-r",
        help="Comma-separated list of roles to include (e.g., coordinator,frontend,backend)"
    )
    parser.add_argument(
        "--planning-only", "-p",
        action="store_true",
        help="Only include planning agents"
    )
    parser.add_argument(
        "--impl-only", "-i",
        action="store_true",
        help="Only include implementation agents"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output filename (default: .cursorrules in workspace)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print output instead of writing to file"
    )
    
    args = parser.parse_args()
    
    # Validate workspace
    workspace = Path(args.workspace).resolve()
    if not workspace.exists():
        print(f"Error: Workspace does not exist: {workspace}")
        sys.exit(1)
    
    # Parse agents directory
    agents_dir = Path(args.agents_dir).resolve()
    
    # Parse roles filter
    roles_filter = None
    if args.roles:
        roles_filter = [r.strip().lower() for r in args.roles.split(",")]
    
    # Discover agents
    print(f"Scanning agents in: {agents_dir}")
    agents = discover_agents(agents_dir)
    
    if not agents:
        print("Error: No agents found!")
        sys.exit(1)
    
    print(f"Found {len(agents)} agent roles:")
    for role in sorted(agents.keys()):
        files = agents[role]
        types = []
        if files["planning"]:
            types.append("planning")
        if files["implementation"]:
            types.append("impl")
        if files["default"]:
            types.append("default")
        print(f"  - {role}: {', '.join(types)}")
    
    # Generate content
    print("\nGenerating .cursorrules...")
    content = generate_cursorrules(
        agents=agents,
        agents_dir=agents_dir,
        roles_filter=roles_filter,
        planning_only=args.planning_only,
        impl_only=args.impl_only
    )
    
    if args.dry_run:
        print("\n--- DRY RUN OUTPUT ---")
        print(content[:2000])
        print(f"\n... ({len(content)} total characters)")
        return
    
    # Write output
    output_file = Path(args.output) if args.output else workspace / ".cursorrules"
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\nSuccess! Created: {output_file}")
        print(f"  - File size: {len(content):,} characters")
        print(f"  - Agents included: {len([r for r in agents if not roles_filter or r in roles_filter])}")
        print(f"\nNext steps:")
        print(f"  1. Open workspace in Cursor: cursor {workspace}")
        print(f"  2. The agents are now available via @RoleName commands")
        print(f"  3. Try: @Coordinator, @Frontend, @Backend impl, etc.")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


