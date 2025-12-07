#!/usr/bin/env python3
"""
validate-agent.py

Validates agent definition files for required structure.
Supports both legacy (split) and unified agent formats.
"""

import os
import sys
import glob

# Headers required for legacy split agents (planning/implementation files)
LEGACY_HEADERS = [
    "## Role Description",
    "## Workflow",
    "## MCP Tools",
    "## Expected Inputs",
    "## Expected Outputs",
    "## Constraints",
    "## Communication Protocol"
]

# Headers required for unified agents (single file with mode switching)
UNIFIED_HEADERS = [
    "## System Role",
    "## Mode Switching",
    "## PLANNING MODE",
    "## IMPLEMENTATION MODE"
]


def is_unified_agent(content):
    """Check if the agent file uses the unified format."""
    return "## Mode Switching" in content or "## System Role" in content


def validate_agent_file(filepath):
    """Validate a single agent file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip legacy subfolder files when checking for unified format
    if '/legacy/' in filepath.replace('\\', '/'):
        headers_to_check = LEGACY_HEADERS
        format_type = "legacy"
    elif is_unified_agent(content):
        headers_to_check = UNIFIED_HEADERS
        format_type = "unified"
    else:
        headers_to_check = LEGACY_HEADERS
        format_type = "legacy"

    missing = []
    for header in headers_to_check:
        # Allow flexible header levels (## or ###)
        header_text = header.lstrip('#').strip()
        if header not in content and f"### {header_text}" not in content:
            missing.append(header)

    if missing:
        print(f"FAIL: {filepath} ({format_type}) is missing headers: {missing}")
        return False

    print(f"PASS: {filepath} ({format_type})")
    return True


def validate_workspace(workspace_root):
    """Validate all agent files in the workspace."""
    agents_dir = os.path.join(workspace_root, "agents")
    md_files = glob.glob(os.path.join(agents_dir, "**", "*.md"), recursive=True)

    if not md_files:
        print("No agent files found!")
        return False

    all_pass = True
    for md_file in md_files:
        if not validate_agent_file(md_file):
            all_pass = False

    return all_pass


if __name__ == "__main__":
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    if validate_workspace(workspace):
        print("All agents validated successfully.")
        sys.exit(0)
    else:
        print("Validation failed.")
        sys.exit(1)
