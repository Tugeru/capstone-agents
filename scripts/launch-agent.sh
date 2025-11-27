#!/bin/bash
# Wrapper to launch a single agent
AGENT=$1
WORKSPACE=${2:-.}
CLI=${3:-gemini}

python3 scripts/run_agents.py --workspace "$WORKSPACE" --agents "$AGENT" --cli "$CLI"
