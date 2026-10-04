---
name: board-update
description: Use when a CTO or engineering leader needs to prepare a quarterly board update on technology, covering business outcomes, investment, delivery health, risk, people and AI. Collects metrics from files or pasted data, applies status rules, drafts the update in a standard structure and prepares the CEO pre-read and board timeline.
---

# board-update

Draft a quarterly technology update for the board. Use `references/board-update.md` as the structure and `references/ceo-cto-partnership.md` for the preparation timeline and the translation table. Both are bundled with this skill.

## Step 1: Scope

Ask in one message. Accept partial answers.

1. Company, quarter and the board meeting date.
2. Last quarter's update, if one exists, so structure and targets carry over.
3. Targets agreed for each metric, and who set them.
4. Where metrics live: dashboards, exports, spreadsheets, repositories.
5. The CEO's top three messages for the board, and the asks the board will be given.
6. Open risks, incidents and audit findings.

## Step 2: Collect data

Read any files the user provides. Record each metric with its value, date and source. When a value is missing, write **Unknown** and the date it will be measured. Never estimate a value to fill a cell.

If the user supplies repository access or delivery exports, compute deployment frequency, lead time for changes, change failure rate and time to restore only when the data supports the definitions in the template. Otherwise mark them Unknown.

## Step 3: Apply status rules

Use the template's rules:

- **Green**: at or better than target.
- **Amber**: worse than target with a recovery plan and a date.
- **Red**: worse than target with no recovery plan, or a risk to a customer or financial commitment.

If a target is missing, mark the status **No target** and add "agree target with CEO" to the questions list. For every Amber and Red, ask the user for the response, or write "response needed."

## Step 4: Draft

Produce the update using the template headings. Write the headline last. Translate technical statements into business terms using the playbook's table, and leave a bracket where a number is needed.

## Step 5: Produce

Output in this order:

1. **The update**: page 1 headline, then Appendices A to F, Next quarter and Metric notes.
2. **CEO pre-read note**: a short message the user can send with the draft, three days before the meeting, naming the three messages and the asks.
3. **Open items**: every Unknown, No target, and response needed.
4. **Preparation timeline** from the playbook, with dates filled in from the meeting date.

## Rules

- Plain, direct language. No filler and no hedging.
- Never invent numbers, targets, incidents or risks.
- Report outcomes, not activity.
- Show conservative forecasts beside targets.
- Offer to convert the update to a slide deck after the user approves the content.
- Remind the user to agree the software capitalization policy with Finance before reporting it.
