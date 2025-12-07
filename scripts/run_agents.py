import argparse
import os
import re
import signal
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# PTY support for TUI-based CLIs (Unix/Mac/WSL)
HAS_PTY = False
try:
    import pty
    HAS_PTY = True
except ImportError:
    pass  # Windows native doesn't have pty module

# Select support for non-blocking stdin (Unix/WSL)
HAS_SELECT = False
try:
    import select
    HAS_SELECT = True
except ImportError:
    pass  # Windows native doesn't have select module

# Path to the capstone-agents repository (where agent definitions live)
CAPSTONE_AGENTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Import multi-agent context generator
try:
    from generate_context import get_multi_agent_context
except ImportError:
    # Fallback if not run from scripts dir
    def get_multi_agent_context(workspace, agents_dir=None):
        print("Warning: generate_context.py not found, multi-agent mode unavailable.")
        return None


def read_agent_file(agent_file):
    """Read and return the content of an agent file."""
    try:
        with open(agent_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {agent_file}: {e}")
        return None


def cleanup_process(p):
    """Cleanly terminate subprocess"""
    if p and p.poll() is None:
        try:
            p.terminate()
            p.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                p.kill()
                p.wait()
            except:
                pass
        except:
            pass


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


def get_agent_context(context_mode, agent_name, agent_file, workspace, agents_dir):
    """
    Get the agent context based on the context mode.
    
    Args:
        context_mode: 'single' or 'multi'
        agent_name: Name of the requested agent
        agent_file: Path to the specific agent file
        workspace: Path to the workspace
        agents_dir: Path to agents directory
    
    Returns:
        tuple: (context_string, is_multi_agent)
    """
    if context_mode == 'multi':
        multi_context = get_multi_agent_context(workspace, agents_dir)
        if multi_context:
            return multi_context, True
        else:
            print(f"Warning: Multi-agent context generation failed, falling back to single agent.")
    
    # Single agent mode (or fallback)
    agent_content = read_agent_file(agent_file)
    if agent_content:
        prompt = f"""You are now acting as the following agent. Read and internalize these instructions:

{agent_content}

---
You are now the {agent_name} agent. Working directory: {workspace}
Begin your workflow."""
        return prompt, False
    return None, False


def run_agent_interactive(agent_name, agent_file, cli_tool, workspace, context_mode, agents_dir, auto_approve=False):
    """Run an agent in interactive mode - gives you full control of the CLI.
    
    Args:
        agent_name: Name of the agent
        agent_file: Path to the agent file
        cli_tool: CLI tool to use
        workspace: Path to workspace
        context_mode: 'single' or 'multi'
        agents_dir: Path to agents directory
        auto_approve: Whether to auto-approve actions
    """
    print(f"[{agent_name}] Launching interactive session...")
    print(f"[{agent_name}] Workspace: {workspace}")
    print(f"[{agent_name}] Agent: {agent_file}")
    print(f"[{agent_name}] Context Mode: {context_mode}")
    print("-" * 60)
    
    # Verify agent file exists
    if not os.path.exists(agent_file):
        print(f"[{agent_name}] Agent file not found: {agent_file}")
        return
    
    # Get agent context based on mode
    context, is_multi = get_agent_context(context_mode, agent_name, agent_file, workspace, agents_dir)
    if not context:
        print(f"[{agent_name}] Failed to load agent context.")
        return
    
    if is_multi:
        print(f"[{agent_name}] Loaded multi-agent context (use @triggers to switch agents)")
    else:
        print(f"[{agent_name}] Loaded single agent context")
    
    cmd = []
    
    if cli_tool == "gemini":
        # Gemini CLI: interactive mode with agent context
        cmd = ["gemini", "-i", context]
        
    elif cli_tool == "cursor":
        # Cursor Agent CLI (cursor-agent command)
        # We copy agent instructions to clipboard for easy pasting
        clipboard_success = copy_to_clipboard(context)
        
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
            os.execvp("cursor-agent", ["cursor-agent"])
        except FileNotFoundError:
            print(f"[{agent_name}] cursor-agent not found. Is it installed and in PATH?")
            print(f"[{agent_name}] Install with: npm install -g cursor-agent")
        except Exception as e:
            print(f"[{agent_name}] Failed to start cursor-agent: {e}")
        return
        
    elif cli_tool == "cursor-ide":
        # Cursor IDE: open the workspace (not CLI)
        # Copy context to clipboard for pasting
        clipboard_success = copy_to_clipboard(context)
        if clipboard_success:
            print(f"[{agent_name}] Agent instructions copied to clipboard!")
        cmd = ["cursor", workspace]
        print(f"[{agent_name}] Cursor IDE will open. Use Ctrl+I to open Composer.")
        print(f"[{agent_name}] Paste the agent instructions (already in clipboard).")
        
    elif cli_tool == "codex":
        # OpenAI Codex CLI
        cmd = ["codex", context]
        
    elif cli_tool == "claude":
        # Claude CLI
        cmd = ["claude", context]
        
    elif cli_tool == "copilot-cli":
        # GitHub Copilot CLI
        print(f"[{agent_name}] Starting GitHub Copilot CLI session...")
        if sys.platform == "win32":
            print(f"[{agent_name}] Note: Windows PowerShell support is experimental. WSL recommended.")
        
        # Step 1: Initialize agent context with one-shot prompt
        print(f"[{agent_name}] Initializing agent context...")
        try:
            subprocess.run(
                ["copilot", "-p", context],
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
        print(f"[{agent_name}] Starting RovoDev CLI session...")
        if sys.platform == "win32":
            print(f"[{agent_name}] Note: Windows PowerShell support is experimental. WSL recommended.")
        
        # Copy to clipboard for easy pasting
        clipboard_success = copy_to_clipboard(context)
        
        print(f"[{agent_name}] Starting RovoDev CLI...")
        if clipboard_success:
            print(f"[{agent_name}] Agent instructions copied to clipboard!")
            print(f"[{agent_name}] >>> Paste with Ctrl+V (or Cmd+V) in the RovoDev prompt")
        else:
            print(f"[{agent_name}] Could not copy to clipboard. Manual load:")
            print(f"[{agent_name}]     {context[:200]}...")
        print("-" * 60)
        
        os.chdir(workspace)
        try:
            os.execvp("acli", ["acli", "rovodev", "run"])
        except FileNotFoundError:
            print(f"[{agent_name}] acli not found. Is it installed and in PATH?")
            print(f"[{agent_name}] Install with: npm install -g @atlassian/rovo-dev-cli")
        except Exception as e:
            print(f"[{agent_name}] Failed to start RovoDev: {e}")
        return
        
    elif cli_tool == "vscode":
        # VS Code: open workspace and copy to clipboard
        clipboard_success = copy_to_clipboard(context)
        print(f"[{agent_name}] === VS Code Copilot Instructions ===")
        if clipboard_success:
            print(f"[{agent_name}] Agent instructions copied to clipboard!")
        print(f"[{agent_name}] 1. Open Copilot Chat (Ctrl+Shift+I)")
        print(f"[{agent_name}] 2. Paste the agent instructions (Ctrl+V)")
        cmd = ["code", workspace]
        
    elif cli_tool == "antigravity":
        # Antigravity IDE: Prepare prompt for user to paste
        clipboard_success = copy_to_clipboard(context)
        
        print(f"[{agent_name}] === Antigravity IDE Instructions ===")
        if clipboard_success:
            print(f"[{agent_name}] Agent instructions copied to clipboard!")
            print(f"[{agent_name}] >>> Paste with Ctrl+V into your Antigravity session.")
        else:
            print(f"[{agent_name}] Could not copy to clipboard.")
            print(f"[{agent_name}] Manually copy instructions from: {agent_file}")
        print("-" * 60)
        if not is_multi:
            print(f"Tip: Use --context-mode multi for full @-mention support")
        return

    elif cli_tool == "qwen":
        # Qwen CLI: interactive mode
        print(f"[{agent_name}] Starting Qwen CLI session...")
        # Qwen CLI chat mode
        # Based on help: -i/--prompt-interactive Execute the provided prompt and continue in interactive mode
        cmd = ["qwen", "-i", context]
        
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


def run_agent_batch(agent_name, agent_file, cli_tool, workspace, auto_approve=False):
    """Run an agent in batch mode - auto-executes and exits."""
    print(f"[{agent_name}] Launching batch mode using {cli_tool}...")
    
    agent_content = read_agent_file(agent_file)
    if agent_content is None:
        print(f"[{agent_name}] Failed to read agent file.")
        return
    # Safety: require explicit approval before performing destructive or auto-approved actions
    destructive_clis = ["gemini", "codex", "copilot-cli", "rovodev"]
    if not auto_approve and cli_tool in destructive_clis:
        print(f"[{agent_name}] Batch mode for '{cli_tool}' is potentially destructive and requires --auto-approve.")
        print(f"[{agent_name}] Agent instructions are available at: {agent_file}")
        print(f"[{agent_name}] To run in batch mode, re-run with --auto-approve or use interactive mode (-i) to manually confirm actions.")
        return
    
    cmd = []
    
    if cli_tool == "gemini":
        # Gemini CLI: one-shot mode. Only use aggressive/auto flags when explicitly approved.
        prompt = f"You are an AI agent. Work in workspace: {workspace}\n\nAgent instructions:\n{agent_content[:2000]}"
        if auto_approve:
            cmd = ["gemini", "--yolo", prompt]
        else:
            cmd = ["gemini", prompt]
        
    elif cli_tool == "codex":
        # OpenAI Codex CLI: only enable full-auto approval when explicitly approved
        prompt = f"Follow these agent instructions:\n\n{agent_content}"
        if auto_approve:
            cmd = ["codex", "--approval-mode", "full-auto", prompt]
        else:
            cmd = ["codex", prompt]
        
    elif cli_tool == "copilot-cli":
        # GitHub Copilot CLI - programmatic mode. Only grant tool permissions when explicitly approved.
        prompt = f"You are an AI agent working in: {workspace}\n\nFollow these instructions:\n{agent_content[:3000]}"
        base_cmd = ["copilot", "-p", prompt]
        if auto_approve:
            base_cmd.extend(["--allow-tool", "write", "--allow-tool", "shell(git)"])
        cmd = base_cmd
        
    elif cli_tool == "rovodev":
        # RovoDev CLI: batch mode with agent context. Only run when explicitly approved.
        initial_prompt = f"""You are now acting as the following agent. Read and internalize these instructions:

{agent_content}

---
You are now the {agent_name} agent. Working directory: {workspace}
Begin your workflow."""
        cmd = ["acli", "rovodev", "run", initial_prompt]
        cmd = ["acli", "rovodev", "run", initial_prompt]
        # Workspace is set via cwd parameter in subprocess.Popen()

    elif cli_tool == "qwen":
        # Qwen CLI: batch mode
        # Usage: qwen [query..]
        # We combine agent content and instruction
        full_query = f"{agent_content}\n\nBegin your workflow suitable for a batch execution context."
        cmd = ["qwen", full_query]
        
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


def find_agent_file(agent_name, agents_dir, agent_type="planning", legacy=False):
    """Find the agent file based on type (planning or implementation).
    
    Args:
        agent_name: Name of the agent (e.g., 'backend')
        agents_dir: Path to agents directory
        agent_type: 'planning' or 'implementation' (only used in legacy mode)
        legacy: If True, look for split files in legacy/ subfolder
    """
    if legacy:
        # Legacy mode: look for split files in legacy/ subfolder
        if agent_type == "implementation":
            possible_files = [
                os.path.join(agents_dir, agent_name, "legacy", f"{agent_name}-implementation.md"),
                os.path.join(agents_dir, agent_name, f"{agent_name}-implementation.md"),
            ]
        else:
            possible_files = [
                os.path.join(agents_dir, agent_name, "legacy", f"{agent_name}-planning.md"),
                os.path.join(agents_dir, agent_name, f"{agent_name}-planning.md"),
            ]
    else:
        # Unified mode: look for single {agent}.md file
        possible_files = [
            os.path.join(agents_dir, agent_name, f"{agent_name}.md"),
            # Fallback to legacy files if unified not found
            os.path.join(agents_dir, agent_name, "legacy", f"{agent_name}-planning.md"),
            os.path.join(agents_dir, agent_name, f"{agent_name}-planning.md"),
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
                        choices=["gemini", "cursor", "cursor-ide", "codex", "claude", "copilot-cli", "vscode", "rovodev", "antigravity", "qwen", "test"],
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
    parser.add_argument("--auto-approve", action="store_true",
                        help="Allow agent batch runs to execute tools or modify the workspace without interactive confirmation")
    parser.add_argument("--agents-dir", 
                        help="Custom path to agents directory")
    parser.add_argument("--legacy", action="store_true",
                        help="Use legacy split agents (planning/implementation) instead of unified agents")
    parser.add_argument("--context-mode", choices=["single", "multi"],
                        help="Context mode: 'single' (focused agent) or 'multi' (all agents with @-mentions). Default: multi for interactive, single for batch.")
    
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
    
    agent_file = find_agent_file(agent_name, agents_dir, agent_type, legacy=args.legacy)
    
    if not agent_file:
        print(f"Error: Agent '{agent_name}' not found.")
        print("Use -l to list available agents.")
        sys.exit(1)
    
    # Determine display mode
    if args.legacy:
        mode_display = f"{agent_type} (legacy)"
    else:
        mode_display = "unified"
    
    print(f"Agent: {agent_name} ({mode_display})")
    print(f"Workspace: {workspace}")
    print(f"CLI: {args.cli}")
    print(f"Mode: {'interactive' if args.interactive else 'batch'}")
    print("=" * 60)
    
    # Determine context mode (default: multi for interactive, single for batch)
    if args.context_mode:
        context_mode = args.context_mode
    else:
        context_mode = 'multi' if args.interactive else 'single'
    print(f"Context: {context_mode}")
    
    if args.interactive:
        run_agent_interactive(agent_name, agent_file, args.cli, workspace, context_mode, agents_dir, args.auto_approve)
    else:
        run_agent_batch(agent_name, agent_file, args.cli, workspace, args.auto_approve)


if __name__ == "__main__":
    main()
