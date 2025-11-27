import os
import json
import sys

def setup_vscode_copilot(workspace_root):
    vscode_dir = os.path.join(workspace_root, ".vscode")
    os.makedirs(vscode_dir, exist_ok=True)
    
    # 1. Create tasks.json
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Run Coordinator Agent",
                "type": "shell",
                "command": "python scripts/run_agents.py --agents coordinator --cli vscode",
                "problemMatcher": []
            },
            {
                "label": "Validate Agents",
                "type": "shell",
                "command": "python scripts/validate-agent.py .",
                "problemMatcher": []
            }
        ]
    }
    
    with open(os.path.join(vscode_dir, "tasks.json"), "w") as f:
        json.dump(tasks_config, f, indent=4)
    print(f"Created {os.path.join(vscode_dir, 'tasks.json')}")

    # 2. Create a workspace file
    workspace_config = {
        "folders": [
            {
                "path": "."
            }
        ],
        "settings": {
            "github.copilot.chat.welcomeMessage": "Welcome to Capstone Agents! Open an agent file (e.g., agents/coordinator/coordinator.md) and paste it here to start.",
            "terminal.integrated.env.windows": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    }
    
    with open(os.path.join(workspace_root, "capstone-agents.code-workspace"), "w") as f:
        json.dump(workspace_config, f, indent=4)
    print(f"Created {os.path.join(workspace_root, 'capstone-agents.code-workspace')}")
    
    # 3. Generate Snippets / Instructions
    print("\n--- VS Code Copilot Setup Complete ---")
    print("To use an agent in Copilot Chat:")
    print("1. Open the agent's Markdown file (e.g., agents/coordinator/coordinator.md).")
    print("2. Copy the content.")
    print("3. Open Copilot Chat (Ctrl+I or Sidebar).")
    print("4. Type '@workspace' (optional) and paste the content as your system prompt.")
    print("5. Ask the agent to 'Analyze requirements' or 'Generate plan'.")

if __name__ == "__main__":
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    setup_vscode_copilot(workspace)
