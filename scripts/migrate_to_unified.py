#!/usr/bin/env python3
"""
migrate_to_unified.py

Migrates the legacy split agent definitions (planning/implementation) to a unified
format where a single {role}.md file handles both modes via a Meta-Prompt.

Actions:
1. For each agent directory, create a `legacy/` subfolder.
2. Move existing `*-planning.md` and `*-implementation.md` files into `legacy/`.
3. Generate a unified `{role}.md` file based on a template.
"""

import argparse
import os
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAPSTONE_AGENTS_DIR = os.path.dirname(SCRIPT_DIR)
DEFAULT_AGENTS_DIR = os.path.join(CAPSTONE_AGENTS_DIR, "agents")

# Template for the unified agent file
UNIFIED_TEMPLATE = """# {role_title} Agent

## System Role
You are the **{role_title}**, a specialized AI agent acting as part of a software development team.
Your responsibilities include: {role_description}

## Mode Switching
You have two distinct modes of operation. Dynamically switch between them based on the user's trigger or intent.

When the user says "plan", "design", "analyze", or invokes `@{role_name} planning`, activate **PLANNING MODE**.
When the user says "implement", "code", "build", "fix", or invokes `@{role_name} impl`, activate **IMPLEMENTATION MODE**.

---

## PLANNING MODE

**Goal**: Analyze requirements and produce a `{role_name}-plan.md` and `{role_name}-plan.json`.

{planning_content}

---

## IMPLEMENTATION MODE

**Goal**: Execute the tasks defined in `{role_name}-plan.json`.

{implementation_content}

---

## Shared Capabilities

### MCP Tools
{tools_section}

### Constraints
- **Workspace Agnostic**: Use relative paths from the workspace root.
- **Follow Plan**: In implementation mode, always read the plan first.
"""


def read_file(filepath: str) -> str | None:
    """Read and return the content of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"  Warning: Could not read {filepath}: {e}")
        return None


def extract_section(content: str, header: str) -> str:
    """Extract content under a specific markdown header."""
    lines = content.split('\n')
    result = []
    in_section = False
    section_level = 0
    
    for line in lines:
        if line.startswith('#'):
            # Count header level
            level = len(line) - len(line.lstrip('#'))
            if header.lower() in line.lower():
                in_section = True
                section_level = level
                continue
            elif in_section and level <= section_level:
                # Hit another header of same or higher level, stop
                break
        if in_section:
            result.append(line)
    
    return '\n'.join(result).strip()


def generate_unified_agent(role_name: str, planning_content: str, impl_content: str) -> str:
    """Generate the unified agent Markdown content."""
    role_title = role_name.replace('-', ' ').title()
    
    # Extract role description from planning content
    role_desc = extract_section(planning_content, "Role Description")
    if not role_desc:
        role_desc = f"responsibilities related to {role_title}."
    
    # Extract tools section (prefer planning file as it's usually more complete)
    tools = extract_section(planning_content, "MCP Tools")
    if not tools:
        tools = extract_section(impl_content, "MCP Tools")
    if not tools:
        tools = "- **filesystem** — Read and write files in the workspace"
    
    # Clean up planning content (remove redundant headers we're handling)
    planning_cleaned = planning_content
    for header in ["# ", "## Role Description", "## MCP Tools"]:
        if header in planning_cleaned:
            planning_cleaned = planning_cleaned.replace(
                extract_section(planning_content, header.replace("## ", "").replace("# ", "")), 
                ""
            )
    
    # Use the workflow and constraints sections
    planning_workflow = extract_section(planning_content, "Workflow")
    planning_constraints = extract_section(planning_content, "Constraints")
    planning_outputs = extract_section(planning_content, "Expected Outputs")
    
    impl_workflow = extract_section(impl_content, "Workflow")
    impl_constraints = extract_section(impl_content, "Constraints")
    
    planning_section = ""
    if planning_workflow:
        planning_section += f"### Workflow\n{planning_workflow}\n\n"
    if planning_outputs:
        planning_section += f"### Expected Outputs\n{planning_outputs}\n\n"
    if planning_constraints:
        planning_section += f"### Constraints\n{planning_constraints}\n"
    
    impl_section = ""
    if impl_workflow:
        impl_section += f"### Workflow\n{impl_workflow}\n\n"
    if impl_constraints:
        impl_section += f"### Constraints\n{impl_constraints}\n"
    
    return UNIFIED_TEMPLATE.format(
        role_title=role_title,
        role_name=role_name,
        role_description=role_desc[:200] if len(role_desc) > 200 else role_desc,
        planning_content=planning_section.strip() if planning_section else "[No planning instructions found]",
        implementation_content=impl_section.strip() if impl_section else "[No implementation instructions found]",
        tools_section=tools
    )


def migrate_agent(agent_dir: str, dry_run: bool = False) -> bool:
    """Migrate a single agent directory to the unified format."""
    agent_name = os.path.basename(agent_dir)
    print(f"\nProcessing: {agent_name}")
    
    legacy_dir = os.path.join(agent_dir, "legacy")
    unified_file = os.path.join(agent_dir, f"{agent_name}.md")
    
    # Find existing files
    planning_file = os.path.join(agent_dir, f"{agent_name}-planning.md")
    impl_file = os.path.join(agent_dir, f"{agent_name}-implementation.md")
    
    # Check for coordinator (single file agent)
    single_file = os.path.join(agent_dir, f"{agent_name}.md")
    if os.path.exists(single_file) and not os.path.exists(planning_file):
        print(f"  Skipping {agent_name}: Already unified or single-file agent.")
        return True
    
    has_planning = os.path.exists(planning_file)
    has_impl = os.path.exists(impl_file)
    
    if not has_planning and not has_impl:
        print(f"  Skipping {agent_name}: No legacy files found.")
        return True
    
    print(f"  Found: planning={has_planning}, implementation={has_impl}")
    
    # Read content
    planning_content = read_file(planning_file) if has_planning else ""
    impl_content = read_file(impl_file) if has_impl else ""
    
    if dry_run:
        print(f"  [DRY RUN] Would create: {legacy_dir}/")
        print(f"  [DRY RUN] Would move: {planning_file} -> {legacy_dir}/")
        print(f"  [DRY RUN] Would move: {impl_file} -> {legacy_dir}/")
        print(f"  [DRY RUN] Would create: {unified_file}")
        return True
    
    # Create legacy directory
    os.makedirs(legacy_dir, exist_ok=True)
    print(f"  Created: {legacy_dir}/")
    
    # Move files to legacy
    if has_planning:
        dest = os.path.join(legacy_dir, os.path.basename(planning_file))
        shutil.move(planning_file, dest)
        print(f"  Moved: {os.path.basename(planning_file)} -> legacy/")
    
    if has_impl:
        dest = os.path.join(legacy_dir, os.path.basename(impl_file))
        shutil.move(impl_file, dest)
        print(f"  Moved: {os.path.basename(impl_file)} -> legacy/")
    
    # Generate unified file
    unified_content = generate_unified_agent(agent_name, planning_content, impl_content)
    
    with open(unified_file, 'w', encoding='utf-8') as f:
        f.write(unified_content)
    print(f"  Created: {agent_name}.md (unified)")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Migrate legacy split agents to unified format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview migration (no changes)
  python migrate_to_unified.py --dry-run

  # Run full migration
  python migrate_to_unified.py

  # Migrate specific agent
  python migrate_to_unified.py --agent backend
        """
    )
    parser.add_argument("--agents-dir", default=DEFAULT_AGENTS_DIR,
                        help="Path to agents directory")
    parser.add_argument("--agent",
                        help="Migrate only a specific agent (e.g., backend)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without modifying files")
    
    args = parser.parse_args()
    
    agents_dir = os.path.abspath(args.agents_dir)
    
    if not os.path.isdir(agents_dir):
        print(f"Error: Agents directory not found: {agents_dir}")
        sys.exit(1)
    
    print(f"Agents directory: {agents_dir}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    if args.agent:
        # Single agent migration
        agent_dir = os.path.join(agents_dir, args.agent)
        if not os.path.isdir(agent_dir):
            print(f"Error: Agent not found: {args.agent}")
            sys.exit(1)
        if migrate_agent(agent_dir, args.dry_run):
            success_count += 1
        else:
            fail_count += 1
    else:
        # Migrate all agents
        for name in sorted(os.listdir(agents_dir)):
            agent_dir = os.path.join(agents_dir, name)
            if os.path.isdir(agent_dir):
                if migrate_agent(agent_dir, args.dry_run):
                    success_count += 1
                else:
                    fail_count += 1
    
    print("\n" + "=" * 60)
    print(f"Migration complete: {success_count} succeeded, {fail_count} failed")
    
    if not args.dry_run:
        print("\nNext steps:")
        print("1. Review the generated unified agent files.")
        print("2. Update scripts/run_agents.py to use the new format.")
        print("3. Test with: python scripts/run_agents.py -a backend -i")


if __name__ == "__main__":
    main()
