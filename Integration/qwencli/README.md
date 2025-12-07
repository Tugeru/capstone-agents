# QwenCLI Integration

This guide explains how to use Capstone Agents with [QwenCLI](https://github.com/QwenLM/qwen-cli) from Alibaba's Qwen AI.

## Prerequisites

1. **Install QwenCLI**:
   Ensure `qwen` is in your PATH.
   ```bash
   pip install qwen-cli
   ```

2. **Configure API Key**:
   ```bash
   export DASHSCOPE_API_KEY=sk-xxxxxxxxxxxx
   # or
   export QWEN_API_KEY=your_api_key
   ```

## Usage

### Interactive Mode (Supports @-mentions)

The interactive mode loads a consolidated context of all agents, allowing you to invoke them dynamically using `@` triggers (e.g., `@frontend`, `@backend implementation`).

```bash
# Start an interactive session with Qwen
python scripts/run_agents.py -a coordinator -c qwen -w /path/to/your/project -i
```
*Internally this runs `qwen -i "System Prompt..."`*

Once inside the chat:
```text
User: @frontend implementation Create a React component for the login form.
Qwen: (Adopts frontend implementation persona) Certainly. Here is the React component...
```

### Batch Mode

Batch mode executes a single agent with a specific task and exits.

```bash
# Run the frontend agent to create a plan
python scripts/run_agents.py -a frontend -c qwen -w /path/to/your/project -t p
```
*Internally this runs `qwen "Agent Instructions..."`*

## Advanced: Manual Context Generation

If you want to generate the system prompt manually for use with other tools or specific Qwen configurations:

```bash
python Integration/qwencli/generate_context.py -w /path/to/your/project -o qwen_context.md
```

Then use it with `qwen-cli`:

```bash
qwen -i "$(cat qwen_context.md)"
```

## Model Selection

| Model | Use Case | Speed | Cost |
|-------|----------|-------|------|
| qwen-turbo | Quick tasks, simple code | Fast | Low |
| qwen-plus | Balanced performance | Medium | Medium |
| qwen-max | Complex reasoning, architecture | Slow | High |
