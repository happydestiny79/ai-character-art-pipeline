#!/usr/bin/env bash
set -euo pipefail

# AI Character Art Pipeline — Install Script
# Usage: bash install.sh [target-dir]

SKILL_NAME="ai-character-art-pipeline"
DEFAULT_TARGET="${HERMES_SKILLS_DIR:-$HOME/.hermes/skills}"
TARGET="${1:-$DEFAULT_TARGET/$SKILL_NAME}"

echo "🔧 Installing AI Character Art Pipeline..."

# Create target directory
mkdir -p "$TARGET"

# Copy skill files
cp SKILL.md "$TARGET/"
cp README.md "$TARGET/" 2>/dev/null || true

echo "✅ Skill installed to: $TARGET"
echo ""
echo "Load it with: hermes skill load $SKILL_NAME"
echo "Or just paste in your agent chat:"
echo '  "Load the ai-character-art-pipeline skill"'