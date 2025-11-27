#!/bin/bash
# Wrapper to launch a single agent interactively
# Usage: ./launch-agent.sh <agent> [workspace] [cli] [type]
# Example: ./launch-agent.sh designer ~/my-project gemini impl

AGENT=${1:-coordinator}
WORKSPACE=${2:-.}
CLI=${3:-gemini}
TYPE=${4:-planning}

python3 scripts/run_agents.py -a "$AGENT" -w "$WORKSPACE" -c "$CLI" -t "$TYPE" -i
