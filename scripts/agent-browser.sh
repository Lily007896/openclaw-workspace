#!/usr/bin/env bash
set -euo pipefail

# Thin wrapper around agent-browser (project-local via npx).
# Keeps all invocations pinned to this workspace + dependency set.
#
# Examples:
#   ./scripts/agent-browser.sh open https://example.com
#   ./scripts/agent-browser.sh snapshot
#   ./scripts/agent-browser.sh click @e2
#   ./scripts/agent-browser.sh fill @e3 "hello"
#   ./scripts/agent-browser.sh get text @e1
#   ./scripts/agent-browser.sh screenshot /tmp/page.png --annotate
#   ./scripts/agent-browser.sh close

cd /home/allen6qi/.openclaw/workspace
exec npx agent-browser "$@"
