#!/usr/bin/env bash
# Copies each playbook or template into the skills that use it, so an installed skill is self-contained.
# Files in /playbooks and /templates are the source of truth. Run this after editing one.
# Relative links in the copies are rewritten to absolute GitHub URLs so they still resolve.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
base="https://github.com/leanpreneur/cto-os/blob/main"

# usage: sync <source dir> <file> <skill>
sync() {
  local dir="$1" file="$2" skill="$3"
  local dest="$root/skills/$skill/references/$file"
  mkdir -p "$root/skills/$skill/references"
  sed -E \
    -e "s#\]\(\.\./([^)]+)\)#](${base}/\1)#g" \
    -e "s#\]\(([A-Za-z0-9_-]+\.md)\)#](${base}/${dir}/\1)#g" \
    "$root/$dir/$file" > "$dest"
}

sync playbooks first-90-days.md cto-day-one
sync playbooks adopt-assessment.md adopt-assess

sync playbooks ceo-cto-partnership.md ceo-alignment
sync templates ceo-cto-operating-agreement.md ceo-alignment

sync playbooks ceo-cto-partnership.md board-update
sync templates board-update.md board-update

sync playbooks engineering-baseline.md eng-audit

sync playbooks hiring.md hiring-plan
sync templates role-scorecard.md hiring-plan
sync templates interview-loop-plan.md hiring-plan
sync templates interview-question-bank.md hiring-plan
sync templates interview-feedback-form.md hiring-plan
sync templates hiring-debrief.md hiring-plan
sync templates leveling-ladder.md hiring-plan

sync playbooks leveling.md leveling-ladder
sync templates leveling-ladder.md leveling-ladder
sync templates promotion-packet.md leveling-ladder

# The routing table is the source for the situations page.
python3 "$root/skills/ask-cto-os/scripts/check_routes.py" render > "$root/docs/situations.md"

echo "Skill references synced."
