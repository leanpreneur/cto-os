---
name: leveling-ladder
description: Use when an engineering leader needs a career ladder, wants to measure the shape of the organization from a roster (levels, spans, layers, time in level), or needs to level a person or candidate from evidence. Builds a ladder adapted to the company, runs a bundled script on a roster file, and drafts promotion packets and level conversations.
---

# leveling-ladder

Build a ladder, measure the organization's shape, or level one person. Follow `references/leveling.md`. Use `references/leveling-ladder.md` as the starter ladder and `references/promotion-packet.md` for promotions. The script at `scripts/org_shape.py` needs `python3` only. It uses no model, so the same roster and date always give the same numbers.

Ask first which mode the user wants: **Build**, **Measure** or **Level a person**. If the request makes it clear, do not ask.

## Build mode

### Step 1: Interview

Ask in one message. Accept partial answers.

1. Engineering headcount, and how many are managers.
2. Existing levels and titles, if any. Ask for the ladder or the title list.
3. Which tracks exist: IC, manager, and any specialty such as data, reliability or security.
4. What goes wrong today: disputes over levels, title inflation, stalled promotions, hires who were levelled by negotiation.
5. Whether pay bands exist, and whether levels are visible to everyone.
6. Where the company hires, for pay range rules.
7. The next calibration or review date.

### Step 2: Read what exists

If the user provides a current ladder, titles, job descriptions or past promotion decisions, read them first. Keep their vocabulary where it works.

### Step 3: Draft the ladder

Choose levels from the headcount table in the playbook. Start from the starter ladder. Replace its examples with facts from the user's company. Delete sentences that do not apply. Do not add years of experience. Do not copy from another company's ladder.

Keep every level described on every axis. Mark each sentence you wrote without evidence from the user as an assumption.

### Step 4: Test it

Give the user the placement test: two managers place three real engineers on the ladder alone, and any sentence that let them disagree gets rewritten. Offer to run the test with them, using ids and not names.

### Step 5: Produce the output

Output exactly these sections, in this order:

1. **Assumptions.**
2. **The ladder:** the levels at a glance, then each level on every axis.
3. **Pay band table:** structure only, with the manager and IC relationship to decide. Leave numbers empty unless the user gave them. Never invent pay figures.
4. **Calibration and promotion calendar:** two cycles, with the steps from the playbook.
5. **Manager training outline:** one hour on writing evidence and running calibration.
6. **The three conversations:** "not yet" on a promotion, a level below what a candidate wanted, and title versus level, written for this company.
7. **Open items:** what the user must decide, and what needs counsel.

## Measure mode

### Step 1: Get the roster

Ask for a CSV with the columns `id`, `level`, `track` (IC or M), `manager_id`, and optionally `start_date`, `last_promotion_date`. The ids must be opaque. If the user has names, tell them to replace names with ids before sharing. If the file includes names, pay or performance ratings, stop, say the script does not need them and ask for a version without them. Keep the roster and the report in a private folder, never in a public repository.

### Step 2: Run the script

```bash
python3 <skill folder>/scripts/org_shape.py --roster <private folder>/roster.csv --as-of <today, YYYY-MM-DD>
```

Add `--show-ids` only if the user asks which managers are flagged. Defaults are a thin span under 3, a wide span over 10, time in level over 36 months, and no breakdown of groups under 5 people. They are this repository's defaults, not standards. Change them with flags only if the user asks.

### Step 3: Check and interpret

- Check one number by hand, for example headcount or one manager's span. If it disagrees, stop and find the cause.
- Read the data warnings and say what they change.
- Use the health table in the playbook. These are questions to ask, not verdicts.

Produce, in this order:

1. **Result:** the three findings that matter most, each with the number and the question to ask.
2. **Shape:** the levels table, spans and layers.
3. **Questions for managers,** one per finding.
4. **Unknowns:** measures the roster cannot give, such as promotion rate by group and regretted attrition, each with a source and an owner role.
5. **Caveats:** what small-group hiding does and does not protect.

Never fill an Unknown with an estimate. Do not name or rank individuals.

## Level a person mode

For an employee or a candidate. Ask for the target ladder, the person's current level if any, and dated evidence by axis. For a candidate, the evidence is the loop feedback.

1. Map each piece of evidence to an axis. Use the ladder's sentences.
2. For each axis, say whether the evidence meets the sentence at the current level, the proposed level, or neither. Quote the evidence.
3. Check sustained work: for promotions, how many quarters show work at the proposed level.
4. Output a **level recommendation** with the evidence by axis, the gaps and the evidence that would close each gap. For a promotion, fill in the promotion packet.

This is a recommendation. The manager and the calibration group decide. Do not use years of experience as a reason. Do not use age, sex, race, family status or any protected characteristic or proxy, and ignore it if the user volunteers it.

## Rules

- Plain, direct language. No filler and no hedging.
- Never invent evidence, levels, pay figures or people.
- Use opaque ids. Do not store or repeat names from a roster.
- Do not rank people. Do not evaluate an individual from the roster script.
- Keep rosters, packets and reports out of any public repository.
- This is not legal advice. Say so when a question touches employment or pay law.
- Do not recommend a vendor or tool. Recommend practices.
