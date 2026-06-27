#!/usr/bin/env bash
# Install the agenttool-site skill into ~/.hermes/skills/
# Usage: curl -sL https://cdn.jsdelivr.net/gh/mynameisyou-cmyk/infinite-chase-high@main/agenttool-skill/install.sh | bash
set -e
DEST="$HOME/.hermes/skills/creative/agenttool-site"
mkdir -p "$DEST/references"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "$SCRIPT_DIR/SKILL.md" "$DEST/"
for f in "$SCRIPT_DIR"/references/*; do
  [ -f "$f" ] && cp "$f" "$DEST/references/"
done
echo "✓ agenttool-site skill installed to $DEST"
echo "  Hermes will auto-load it on next session."
