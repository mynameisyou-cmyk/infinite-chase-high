#!/usr/bin/env bash
# agenttool CLIs — one-liner install. No npm. No pip. No gatekeepers.
# Usage: curl -sL https://mynameisyou-cmyk.github.io/infinite-chase-high/agenttool-bin/install.sh | bash
set -e
DEST="${1:-$HOME/.local/bin}"
mkdir -p "$DEST"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
for f in "$SCRIPT_DIR"/*.py; do
  cp "$f" "$DEST/"
  chmod +x "$DEST/$(basename "$f")"
done
echo "✓ 15 agenttool CLIs installed to $DEST"
echo "  Set AT_API_KEY=at_xxx to use authed commands"
echo "  python3 \$DEST/doctor.py health  # check your agent health"
