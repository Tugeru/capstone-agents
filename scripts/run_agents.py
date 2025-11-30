import argparse
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

# PTY support for TUI-based CLIs (Unix/Mac/WSL)
HAS_PTY = False
try:
    import pty
    HAS_PTY = True
except ImportError:
    pass  # Windows native doesn't have pty module

# Path to the capstone-agents repository (where agent definitions live)
CAPSTONE_AGENTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_agent_file(agent_file):
    """Read and return the content of an agent file."""
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {agent_file}: {e}")
        return None


def copy_to_clipboard(text):
    """Copy text to system clipboard."""
    import platform
    system = platform.system()
    
    # Detect WSL (Windows Subsystem for Linux)
    is_wsl = False
    if system == "Linux":
        try:
            with open("/proc/version", "r") as f:
                is_wsl = "microsoft" in f.read().lower()
        except Exception:
            pass
    
    try:
        if system == "Darwin":  # macOS
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
        elif system == "Linux" and is_wsl:
            # WSL: use Windows clip.exe
            subprocess.run(["clip.exe"], input=text.encode(), check=True)
        elif system == "Linux":
            # Native Linux: try xclip first, then xsel
            try:
                subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
            except FileNotFoundError:
                subprocess.run(["xsel", "--clipboard", "--input"], input=text.encode(), check=True)
        elif system == "Windows":
            subprocess.run(["clip"], input=text.encode(), check=True, shell=True)
        return True
    except Exception:
        return False


def run_agent_interactive(agent_name, agent_file, cli_tool, workspace):
    """Run an agent in interactive mode - gives you full control of the CLI."""
    print(f"[{agent_name}] Launching interactive session...")
    print(f"[{agent_name}] Workspace: {workspace}")
    print(f"[{agent_name}] Agent: {agent_file}")
    print("-" * 60)
    
    # Verify agent file exists
    if not os.path.exists(agent_file):
        print(f"[{agent_name}] Agent file not found: {agent_file}")
        return
    
    cmd = []
    
    if cli_tool == "gemini":
        # Gemini CLI: interactive mode with agent context
        # Note: Gemini can only read files within the workspace, so we pass agent content directly
        agent_content = read_agent_file(agent_file)
        if agent_content is None:
            print(f"[{agent_name}] Failed to read agent file.")
            return
        
        prompt = f"""You are now acting as the following agent. Read and internalize these instructions:

{agent_content}

---
You are now the {agent_name} agent. Working directory: {workspace}
Begin your workflow."""
        cmd = ["gemini", "-i", prompt]
        
    elif cli_tool == "cursor":
        # Cursor Agent CLI (cursor-agent command)
        # Note: cursor-agent is a TUI tool without headless mode
        # We copy agent instructions to clipboard for easy pasting
        agent_content = read_agent_file(agent_file)
        if agent_content is None:
            print(f"[{agent_name}] Failed to read agent file.")
            return
        
        prompt = f"""You are now acting as the following agent. Read and internalize these instructions:

{agent_content}

---
You are now the {agent_name} agent. Working directory: {workspace}
Begin your workflow."""
        
        clipboard_success = copy_to_clipboard(prompt)
        
        print(f"[{agent_name}] Starting cursor-agent...")
        if clipboard_success:
            print(f"[{agent_name}] Agent instructions copied to clipboard!")
            print(f"[{agent_name}] >>> Paste with Ctrl+V (or Cmd+V) in the chat")
        else:
            print(f"[{agent_name}] Could not copy to clipboard. Manual load:")
        print(f"[{agent_name}]     @{agent_file} follow these instructions")
        print("-" * 60)
        
        os.chdir(workspace)
        try:
            # execvp replaces this process entirely - gives cursor-agent full terminal control
            os.execvp("cursor-agent", ["cursor-agent"])
        except FileNotFoundError:
            print(f"[{agent_name}] cursor-agent not found. Is it installed and in PATH?")
            print(f"[{agent_name}] Install with: npm install -g cursor-agent")
        except Exception as e:
            print(f"[{agent_name}] Failed to start cursor-agent: {e}")
        return  # Only reached if execvp fails
        
    elif cli_tool == "cursor-ide":
        # Cursor IDE: open the workspace (not CLI)
        cmd = ["cursor", workspace]
        print(f"[{agent_name}] Cursor IDE will open. Use Ctrl+I to open Composer.")
        print(f"[{agent_name}] Paste the agent instructions from: {agent_file}")
        
    elif cli_tool == "codex":
        # OpenAI Codex CLI
        prompt = f"You are an AI agent working in: {workspace}. Read and follow the agent instructions from: {agent_file}"
        cmd = ["codex", prompt]
        
    elif cli_tool == "claude":
        # Claude CLI
        prompt = f"You are an AI agent working in: {workspace}. Read and follow the agent instructions from: {agent_file}"
        cmd = ["claude", prompt]
        
    elif cli_tool == "copilot-cli":
        # GitHub Copilot CLI (npm @github/copilot)
        # Read agent content to pass as initial context
        agent_content = read_agent_file(agent_file)
        if agent_content is None:
            print(f"[{agent_name}] Failed to read agent file.")
            return
        
        print(f"[{agent_name}] Starting GitHub Copilot CLI session...")
        if sys.platform == "win32":
            print(f"[{agent_name}] Note: Windows PowerShell support is experimental. WSL recommended.")
        
        # Pass agent instructions as initial prompt
        initial_prompt = f"""You are now acting as the following agent. Read and internalize these instructions:

{agent_content}

---
You are now the {agent_name} agent. Working directory: {workspace}
Confirm your role briefly."""
        
        # Step 1: Initialize agent context with one-shot prompt
        print(f"[{agent_name}] Initializing agent context...")
        try:
            subprocess.run(
                ["copilot", "-p", initial_prompt],
                cwd=workspace,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"[{agent_name}] Initialization failed with exit code {e.returncode}")
            return
        except Exception as e:
            print(f"[{agent_name}] Failed to initialize: {e}")
            return
        
        # Step 2: Continue with interactive session
        print("-" * 60)
        print(f"[{agent_name}] Continuing interactive session (Ctrl+C to exit)...")
        print("-" * 60)
        cmd = ["copilot", "--continue"]
        
    elif cli_tool == "rovodev":
        # RovoDev CLI: interactive mode
        # Read agent content for validation
        agent_content = read_agent_file(agent_file)
        if agent_content is None:
            print(f"[{agent_name}] Failed to read agent file.")
            return
        
        print(f"[{agent_name}] Starting RovoDev CLI session...")
        # RovoDev CLI: acli rovodev run with instruction executes it first, then continues interactively
        initial_prompt = f"""You are now acting as the following agent. Read and internalize these instructions:

{agent_content}

---
You are now the {agent_name} agent. Working directory: {workspace}
Begin your workflow."""
        cmd = ["acli", "rovodev", "run", initial_prompt]
        # Workspace is set via cwd parameter in subprocess.run()
        
    elif cli_tool == "vscode":
        # VS Code: open workspace and show instructions
        print(f"[{agent_name}] === VS Code Copilot Instructions ===")
        print(f"[{agent_name}] 1. Open Copilot Chat (Ctrl+Shift+I)")
        print(f"[{agent_name}] 2. Paste the agent file content from:")
        print(f"[{agent_name}]    {agent_file}")
        print(f"[{agent_name}] 3. Or use @workspace with the agent instructions")
        cmd = ["code", workspace]
        
    else:
        print(f"[{agent_name}] CLI '{cli_tool}' not supported for interactive mode.")
        return

    try:
        # Run interactively - explicit stdin/stdout/stderr for proper TTY handling
        subprocess.run(cmd, cwd=workspace, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    except FileNotFoundError:
        print(f"[{agent_name}] CLI tool '{cmd[0]}' not found. Is it installed and in PATH?")
    except KeyboardInterrupt:
        print(f"\n[{agent_name}] Session ended.")
    except Exception as e:
        print(f"[{agent_name}] Failed to start: {e}")


def run_agent_batch(agent_name, agent_file, cli_tool, workspace):
    """Run an agent in batch mode - auto-executes and exits."""
    print(f"[{agent_name}] Launching batch mode using {cli_tool}...")
    
    agent_content = read_agent_file(agent_file)
    if agent_content is None:
        print(f"[{agent_name}] Failed to read agent file.")
        return
    
    cmd = []
    
    if cli_tool == "gemini":
        # Gemini CLI: one-shot mode with auto-approval
        prompt = f"You are an AI agent. Work in workspace: {workspace}\n\nAgent instructions:\n{agent_content[:2000]}"
        cmd = ["gemini", "--yolo", prompt]
        
    elif cli_tool == "codex":
        # OpenAI Codex CLI: full-auto mode
        prompt = f"Follow these agent instructions:\n\n{agent_content}"
        cmd = ["codex", "--approval-mode", "full-auto", prompt]
        
    elif cli_tool == "copilot-cli":
        # GitHub Copilot CLI - programmatic mode
        prompt = f"You are an AI agent working in: {workspace}\n\nFollow these instructions:\n{agent_content[:3000]}"
        cmd = ["copilot", "-p", prompt, "--allow-tool", "write", "--allow-tool", "shell(git)"]
        
    elif cli_tool == "rovodev":
        # RovoDev CLI: batch mode with agent context
        initial_prompt = f"""You are now acting as the following agent. Read and internalize these instructions:

{agent_content}

---
You are now the {agent_name} agent. Working directory: {workspace}
Begin your workflow."""
        cmd = ["acli", "rovodev", "run", initial_prompt]
        # Workspace is set via cwd parameter in subprocess.Popen()
        
    elif cli_tool == "test":
        # Test mode: just echo what would run
        print(f"[{agent_name}] TEST MODE - Would run agent from: {agent_file}")
        print(f"[{agent_name}] Workspace: {workspace}")
        print(f"[{agent_name}] Preview: {agent_content[:300] if agent_content else 'N/A'}...")
        return
        
    else:
        print(f"[{agent_name}] CLI '{cli_tool}' not supported for batch mode. Use -i for interactive.")
        return

    try:
        print(f"[{agent_name}] Executing: {cmd[0]} ...")
        process = subprocess.Popen(
            cmd, 
            cwd=workspace, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        stdout, stderr = process.communicate(timeout=600)
        
        if stdout:
            print(f"[{agent_name}] OUTPUT:\n{stdout}")
        if stderr:
            print(f"[{agent_name}] ERROR:\n{stderr}")
        
        if process.returncode != 0:
            print(f"[{agent_name}] Exited with code: {process.returncode}")
            
    except subprocess.TimeoutExpired:
        print(f"[{agent_name}] Timed out after 10 minutes")
        process.kill()
    except FileNotFoundError:
        print(f"[{agent_name}] CLI tool '{cmd[0]}' not found. Is it installed and in PATH?")
    except Exception as e:
        print(f"[{agent_name}] Failed: {e}")


def find_agent_file(agent_name, agents_dir, agent_type="planning"):
    """Find the agent file based on type (planning or implementation)."""
    if agent_type == "implementation":
        # Prioritize implementation file
        possible_files = [
            os.path.join(agents_dir, agent_name, f"{agent_name}-implementation.md"),
            os.path.join(agents_dir, agent_name, f"{agent_name}.md"),
        ]
    else:
        # Default: prioritize planning file
        possible_files = [
            os.path.join(agents_dir, agent_name, f"{agent_name}-planning.md"),
            os.path.join(agents_dir, agent_name, f"{agent_name}.md"),
            os.path.join(agents_dir, agent_name, f"{agent_name}-implementation.md"),
        ]
    
    for p_file in possible_files:
        if os.path.exists(p_file):
            return p_file
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Capstone Agents Runner - Load AI agents into CLI tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive planning session
  python run_agents.py -a designer -w /path/to/your/project -i
  
  # Interactive implementation session
  python run_agents.py -a designer -w /path/to/your/project -i --type impl
  
  # Batch mode - auto-run and exit
  python run_agents.py -a backend -w /path/to/project -c gemini
  
  # List available agents
  python run_agents.py -l
  
  # Test mode
  python run_agents.py -a coordinator -c test
        """
    )
    parser.add_argument("-w", "--workspace", default=".", 
                        help="Path to YOUR project workspace (where the agent will work)")
    parser.add_argument("-c", "--cli", default="gemini", 
                        choices=["gemini", "cursor", "cursor-ide", "codex", "claude", "copilot-cli", "vscode", "rovodev", "test"],
                        help="CLI tool to use (default: gemini)")
    parser.add_argument("-a", "--agent", 
                        help="Agent to run (e.g., designer, frontend, backend, coordinator)")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Run in interactive mode (stay open for conversation)")
    parser.add_argument("-t", "--type", default="planning",
                        choices=["planning", "plan", "p", "implementation", "impl", "i"],
                        help="Agent type: planning (default) or implementation")
    parser.add_argument("-l", "--list", action="store_true",
                        help="List available agents")
    parser.add_argument("--agents-dir", 
                        help="Custom path to agents directory")
    
    args = parser.parse_args()
    
    # Determine agents directory
    if args.agents_dir:
        agents_dir = os.path.abspath(args.agents_dir)
    else:
        agents_dir = os.path.join(CAPSTONE_AGENTS_DIR, "agents")
    
    # List agents if requested
    if args.list:
        print("Available agents:")
        if os.path.exists(agents_dir):
            for agent in sorted(os.listdir(agents_dir)):
                agent_path = os.path.join(agents_dir, agent)
                if os.path.isdir(agent_path):
                    print(f"  - {agent}")
        else:
            print(f"  Agents directory not found: {agents_dir}")
        return
    
    workspace = os.path.abspath(args.workspace)
    
    if not os.path.exists(agents_dir):
        print(f"Error: Agents directory not found: {agents_dir}")
        print("Use --agents-dir to specify the path to your agents folder.")
        sys.exit(1)
    
    # Get agent to run
    agent_name = args.agent or "coordinator"
    
    # Normalize agent type
    agent_type = "implementation" if args.type in ["implementation", "impl", "i"] else "planning"
    
    agent_file = find_agent_file(agent_name, agents_dir, agent_type)
    
    if not agent_file:
        print(f"Error: Agent '{agent_name}' ({agent_type}) not found.")
        print("Use -l to list available agents.")
        sys.exit(1)
    
    print(f"Agent: {agent_name} ({agent_type})")
    print(f"Workspace: {workspace}")
    print(f"CLI: {args.cli}")
    print(f"Mode: {'interactive' if args.interactive else 'batch'}")
    print("=" * 60)
    
    if args.interactive:
        run_agent_interactive(agent_name, agent_file, args.cli, workspace)
    else:
        run_agent_batch(agent_name, agent_file, args.cli, workspace)


if __name__ == "__main__":
    main()
