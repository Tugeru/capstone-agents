import os
import json

ROLES = {
    "coordinator": {
        "name": "Coordinator",
        "description": "Project Manager and Coordinator responsible for overall project planning and task delegation.",
        "tools": ["filesystem", "github"]
    },
    "software-architect": {
        "name": "Software Architect",
        "description": "Responsible for high-level system design, technology selection, and architectural patterns.",
        "tools": ["filesystem", "github"]
    },
    "frontend": {
        "name": "Frontend Developer",
        "description": "Responsible for implementing the user interface and client-side logic.",
        "tools": ["filesystem", "browser", "figma"]
    },
    "backend": {
        "name": "Backend Developer",
        "description": "Responsible for server-side logic, API development, and business rules.",
        "tools": ["filesystem", "supabase", "docker"]
    },
    "database-engineer": {
        "name": "Database Engineer",
        "description": "Responsible for database schema design, optimization, and management.",
        "tools": ["filesystem", "supabase"]
    },
    "designer": {
        "name": "UI/UX Designer",
        "description": "Responsible for user experience design, wireframing, and prototyping.",
        "tools": ["filesystem", "figma"]
    },
    "devops": {
        "name": "DevOps Engineer",
        "description": "Responsible for deployment pipelines, infrastructure, and containerization.",
        "tools": ["filesystem", "docker", "kubernetes", "github"]
    },
    "qa": {
        "name": "QA Engineer",
        "description": "Responsible for testing, quality assurance, and bug reporting.",
        "tools": ["filesystem", "playwright", "browser"]
    },
    "documentation": {
        "name": "Technical Writer",
        "description": "Responsible for creating and maintaining project documentation.",
        "tools": ["filesystem", "github"]
    },
    "project-manager": {
        "name": "Project Manager",
        "description": "Responsible for tracking progress, managing timelines, and ensuring requirements are met.",
        "tools": ["filesystem", "github"]
    },
    "blockchain": {
        "name": "Blockchain Developer",
        "description": "Responsible for smart contract development and blockchain integration.",
        "tools": ["filesystem", "github"]
    }
}

PLANNING_TEMPLATE = """# {role_name} - Planning Agent

## Role Description
{description}
You are the **Planning Agent** for this role. Your goal is to analyze requirements, design solutions, and create a detailed implementation plan for the Implementation Agent to follow.

## Workflow
1.  **Analyze**: Read the project requirements and any existing documentation.
2.  **Design**: Propose a solution or design that meets the requirements.
3.  **Plan**: Break down the solution into actionable steps for the Implementation Agent.
4.  **Output**: Generate a `plan.json` and a detailed Markdown plan.

## MCP Tools
You have access to the following MCP tools:
{tools_list}

## Expected Inputs
- Project Requirements (Markdown/Text)
- Current Codebase State (Filesystem)

## Expected Outputs
1.  **Detailed Plan (Markdown)**: A comprehensive explanation of the design and steps.
2.  **Action Plan (JSON)**: A structured list of tasks.
    ```json
    {{
      "role": "{role_slug}",
      "tasks": [
        {{
          "id": "task-1",
          "description": "Description of task",
          "dependencies": [],
          "status": "pending"
        }}
      ]
    }}
    ```

## Constraints
- **Workspace Agnostic**: Do not assume absolute paths. Use relative paths from the workspace root.
- **No Code Execution**: You are a planner. Do not write code to files (unless it's a config/plan). Leave implementation to the Implementation Agent.

## Communication Protocol
- Read inputs from the `docs/` or root directory.
- Write your plan to `{role_slug}-plan.md` and `{role_slug}-plan.json` in the current directory.
"""

IMPLEMENTATION_TEMPLATE = """# {role_name} - Implementation Agent

## Role Description
{description}
You are the **Implementation Agent** for this role. Your goal is to execute the plan created by the Planning Agent and produce working code or artifacts.

## Workflow
1.  **Read Plan**: Load the `{role_slug}-plan.json` and `{role_slug}-plan.md` files.
2.  **Execute**: Perform the tasks outlined in the plan using your tools.
3.  **Verify**: Check your work against the requirements.
4.  **Report**: Update the plan status to 'completed' or report issues.

## MCP Tools
You have access to the following MCP tools:
{tools_list}

## Expected Inputs
- `{role_slug}-plan.json`
- `{role_slug}-plan.md`
- Source Code (Filesystem)

## Expected Outputs
- Modified Source Code
- Updated Plan Status

## Constraints
- **Workspace Agnostic**: Use relative paths.
- **Follow the Plan**: Do not deviate from the agreed-upon plan without reporting a reason.
- **Clean Code**: Write comments and follow best practices for the language used.

## Communication Protocol
- Read the plan from the current directory.
- Write code to the workspace.
- Update the status in `{role_slug}-plan.json`.
"""

def generate_agents(workspace_root):
    agents_dir = os.path.join(workspace_root, "agents")
    
    for role_slug, role_info in ROLES.items():
        role_dir = os.path.join(agents_dir, role_slug)
        os.makedirs(role_dir, exist_ok=True)
        
        tools_list = "\n".join([f"- **{tool}**" for tool in role_info["tools"]])
        
        # Planning Agent
        planning_content = PLANNING_TEMPLATE.format(
            role_name=role_info["name"],
            description=role_info["description"],
            tools_list=tools_list,
            role_slug=role_slug
        )
        
        planning_file = "coordinator.md" if role_slug == "coordinator" else f"{role_slug}-planning.md"
        with open(os.path.join(role_dir, planning_file), "w", encoding="utf-8") as f:
            f.write(planning_content)
            
        # Implementation Agent (Coordinator is special, usually just one file, but prompt asked for dual-layer for all domains. 
        # However, prompt said "Coordinator / Project Manager (planning + implementation)". 
        # Let's stick to the pattern: coordinator.md might be the main one, but let's add implementation if needed or just keep one if it acts as both.
        # The prompt list says: "Coordinator / Project Manager (planning + implementation)". 
        # But later in file structure it shows `agents/coordinator/coordinator.md` (singular).
        # And `agents/project-manager/pm-planning.md` & `pm-implementation.md`.
        # So Coordinator might be a special single file.
        
        if role_slug != "coordinator":
            impl_content = IMPLEMENTATION_TEMPLATE.format(
                role_name=role_info["name"],
                description=role_info["description"],
                tools_list=tools_list,
                role_slug=role_slug
            )
            with open(os.path.join(role_dir, f"{role_slug}-implementation.md"), "w", encoding="utf-8") as f:
                f.write(impl_content)

if __name__ == "__main__":
    import sys
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    generate_agents(workspace)
