import argparse
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor


def read_agent_file(agent_file):
    """Read and return the content of an agent file."""
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {agent_file}: {e}")
        return None


def run_agent(agent_name, agent_file, cli_tool, workspace):
    print(f"[{agent_name}] Launching using {cli_tool}...")
    
    # Read the agent file content for CLIs that need it
    agent_content = read_agent_file(agent_file)
    if agent_content is None and cli_tool in ["gemini", "qwen", "opencodex"]:
        print(f"[{agent_name}] Failed to read agent file.")
        return
    
    # Construct command based on CLI tool
    cmd = []
    use_shell = False
    
    if cli_tool == "gemini":
        # Gemini CLI: use positional query (one-shot mode) with --yolo for auto-approval
        # This runs the prompt and exits automatically when complete
        prompt = f"You are an AI agent. Read and follow the instructions in this file: {agent_file}\n\nAgent instructions:\n{agent_content[:2000]}"
        cmd = ["gemini", "--yolo", prompt]
        
    elif cli_tool == "cursor":
        # Cursor: open the workspace with the agent file
        cmd = ["cursor", workspace, "--goto", agent_file]
        
    elif cli_tool == "qwen":
        # Qwen CLI (DashScope): use the prompt flag
        prompt = f"You are an AI agent. Follow these instructions:\n\n{agent_content}"
        cmd = ["qwen", "--prompt", prompt]
        
    elif cli_tool == "opencodex":
        # OpenCodex CLI: use prompt with agent instructions
        prompt = f"Follow these agent instructions:\n\n{agent_content}"
        cmd = ["codex", prompt]
        
    elif cli_tool == "vscode":
        # For VS Code, print instructions for manual setup
        print(f"[{agent_name}] === VS Code Copilot Instructions ===")
        print(f"[{agent_name}] 1. Open VS Code in workspace: {workspace}")
        print(f"[{agent_name}] 2. Open Copilot Chat (Ctrl+Shift+I)")
        print(f"[{agent_name}] 3. Copy and paste the agent file content:")
        print(f"[{agent_name}]    {agent_file}")
        print(f"[{agent_name}] 4. Or use @workspace with the agent instructions")
        return
        
    elif cli_tool == "test":
        # Test mode: just echo what would run
        print(f"[{agent_name}] TEST MODE - Would run agent from: {agent_file}")
        print(f"[{agent_name}] Agent content preview: {agent_content[:200] if agent_content else 'N/A'}...")
        return
        
    else:
        # Default fallback
        cmd = ["echo", f"Running {agent_name} from {agent_file}"]

    try:
        print(f"[{agent_name}] Executing: {cmd[0]} ...")
        process = subprocess.Popen(
            cmd, 
            cwd=workspace, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            shell=use_shell
        )
        stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout
        
        if stdout:
            print(f"[{agent_name}] OUTPUT:\n{stdout}")
        if stderr:
            print(f"[{agent_name}] ERROR:\n{stderr}")
        
        if process.returncode != 0:
            print(f"[{agent_name}] Process exited with code: {process.returncode}")
            
    except subprocess.TimeoutExpired:
        print(f"[{agent_name}] Process timed out after 5 minutes")
        process.kill()
    except FileNotFoundError:
        print(f"[{agent_name}] CLI tool '{cmd[0]}' not found. Is it installed and in PATH?")
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
            # Try to find agent file with multiple naming patterns
            possible_files = [
                os.path.join(agents_dir, a, f"{a}-planning.md"),
                os.path.join(agents_dir, a, f"{a}.md"),
                os.path.join(agents_dir, a, f"{a}-implementation.md"),
            ]
            
            for p_file in possible_files:
                if os.path.exists(p_file):
                    agents_to_run.append((a, p_file))
                    break
            else:
                print(f"Warning: No agent file found for '{a}'")
    else:
        # Run Coordinator by default if exists
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
