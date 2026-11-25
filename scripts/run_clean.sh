#!/usr/bin/env bash
# Run a last30days command with a clean environment, so no paid or LLM keys
# from your shell reach the engine. Only free, keyless sources are used.
#
#   scripts/run_clean.sh python3 skills/last30days/scripts/last30days.py --preflight
exec env -i HOME="$HOME" PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin" \
  LANG=C.UTF-8 TERM="${TERM:-xterm-256color}" \
  LAST30DAYS_MEMORY_DIR="$HOME/Documents/Last30Days" "$@"
