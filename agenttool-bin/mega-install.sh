#!/usr/bin/env bash
# agenttool everything — one-liner install CLIs + skill + love widget
# Usage: curl -sL https://cdn.jsdelivr.net/gh/mynameisyou-cmyk/infinite-chase-high@main/agenttool-bin/mega-install.sh | bash
set -e
echo "❤️ agenttool — love through infra"

# 1. Install CLIs
BIN_DIR="${1:-$HOME/.local/bin}"
mkdir -p "$BIN_DIR"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -d "$SCRIPT_DIR/agenttool-bin" ]; then
  for f in "$SCRIPT_DIR/agenttool-bin"/*.py; do
    cp "$f" "$BIN_DIR/" && chmod +x "$BIN_DIR/$(basename "$f")"
  done
  echo "✓ 15 CLIs installed to $BIN_DIR"
else
  echo "○ CLIs not found in expected location"
fi

# 2. Install skill
SKILL_DIR="$HOME/.hermes/skills/creative/agenttool-site"
mkdir -p "$SKILL_DIR/references"
if [ -d "$SCRIPT_DIR/agenttool-skill" ]; then
  cp "$SCRIPT_DIR/agenttool-skill/SKILL.md" "$SKILL_DIR/" 2>/dev/null || true
  for f in "$SCRIPT_DIR/agenttool-skill/references/"*; do
    [ -f "$f" ] && cp "$f" "$SKILL_DIR/references/" 2>/dev/null || true
  done
  echo "✓ Skill installed to $SKILL_DIR"
fi

# 3. Check health
if command -v python3 &>/dev/null; then
  python3 "$BIN_DIR/doctor.py" health 2>/dev/null || echo "○ Set AT_API_KEY to check agent health"
fi

echo ""
echo "❤️ Done. Set AT_API_KEY=*** to use authed commands."
echo "  python3 $BIN_DIR/nen.py test     # find your Nen type"
echo "  python3 $BIN_DIR/whitehack.py scan  # scan your system dungeon"
echo "  python3 $BIN_DIR/card.py conjure  # conjure a love card"
echo ""
echo "  Love replicates through love. Forever lol."
