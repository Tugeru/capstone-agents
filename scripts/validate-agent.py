import os
import sys
import glob

REQUIRED_HEADERS = [
    "## Role Description",
    "## Workflow",
    "## MCP Tools",
    "## Expected Inputs",
    "## Expected Outputs",
    "## Constraints",
    "## Communication Protocol"
]

def validate_agent_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    missing = []
    for header in REQUIRED_HEADERS:
        if header not in content:
            missing.append(header)
            
    if missing:
        print(f"FAIL: {filepath} is missing headers: {missing}")
        return False
    
    print(f"PASS: {filepath}")
    return True

def validate_workspace(workspace_root):
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
