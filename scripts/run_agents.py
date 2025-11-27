import argparse
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

def run_agent(agent_name, agent_file, cli_tool, workspace):
    print(f"[{agent_name}] Launching using {cli_tool}...")
    
    # Construct command based on CLI tool
    cmd = []
    if cli_tool == "gemini":
        cmd = ["gemini", "run", "-f", agent_file]
    elif cli_tool == "cursor":
        cmd = ["cursor", "--new-window", agent_file] # Example
    elif cli_tool == "qwen":
        cmd = ["qwen", "chat", "-f", agent_file]
    elif cli_tool == "opencodex":
        cmd = ["codex", "run", agent_file]
    elif cli_tool == "vscode":
        # For VS Code, we might just print instructions or try to open it
        print(f"[{agent_name}] Please open {agent_file} in VS Code Copilot Chat.")
        return
    else:
        # Default fallback or echo for testing
        cmd = ["echo", f"Running {agent_name} from {agent_file}"]

    try:
        # In a real scenario, we might want to capture output or interact
        # For now, we just spawn it
        process = subprocess.Popen(cmd, cwd=workspace, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        
        if stdout:
            print(f"[{agent_name}] OUTPUT:\n{stdout}")
        if stderr:
            print(f"[{agent_name}] ERROR:\n{stderr}")
            
    except Exception as e:
        print(f"[{agent_name}] Failed to start: {e}")

def main():
    parser = argparse.ArgumentParser(description="Capstone Agents Runner")
    parser.add_argument("--workspace", default=".", help="Path to the workspace")
    parser.add_argument("--cli", default="gemini", choices=["gemini", "cursor", "qwen", "opencodex", "vscode", "test"], help="CLI tool to use")
    parser.add_argument("--agents", nargs="+", help="Specific agents to run (e.g. frontend backend)")
    
    args = parser.parse_args()
    workspace = os.path.abspath(args.workspace)
    
    print(f"Starting Capstone Agents in {workspace} using {args.cli}...")
    
    agents_dir = os.path.join(workspace, "agents")
    if not os.path.exists(agents_dir):
        print(f"Error: agents directory not found in {workspace}")
        sys.exit(1)

    # Discover agents
    agents_to_run = []
    if args.agents:
        for a in args.agents:
            # Try to find planning or implementation file
            p_file = os.path.join(agents_dir, a, f"{a}-planning.md")
            if os.path.exists(p_file):
                agents_to_run.append((a, p_file))
    else:
        # Run all planning agents by default? Or just Coordinator?
        # Let's default to Coordinator if exists
        coord_file = os.path.join(agents_dir, "coordinator", "coordinator.md")
        if os.path.exists(coord_file):
            agents_to_run.append(("coordinator", coord_file))
    
    if not agents_to_run:
        print("No agents found to run.")
        sys.exit(1)

    # Run in parallel
    with ThreadPoolExecutor(max_workers=len(agents_to_run)) as executor:
        futures = [executor.submit(run_agent, name, path, args.cli, workspace) for name, path in agents_to_run]
        
        for future in futures:
            future.result()

    print("All agents finished.")

if __name__ == "__main__":
    main()
