---
name: eng-audit
description: Use when an engineering leader wants a numeric baseline of delivery health from git history: change size, branch lifetime, release cadence, reverts, contributor concentration, AI traceability and context files. Runs a bundled script, labels every number Measured, Proxy or Unknown, and produces baseline rows for the First 90 Days plan and evidence for the ADOPT assessment.
---

# eng-audit

Compute an engineering baseline from git history with the bundled script at `scripts/audit.py`. Use `references/engineering-baseline.md` for definitions, the reading table and the rules on misuse. The script needs `python3` and `git` only. It uses no model, so the same repository and window always give the same numbers.

## Step 1: Scope

Ask in one message. Accept partial answers.

1. The repositories: local paths, or GitHub URLs to clone.
2. The window. Default 90 days.
3. The branch, if it is not the default branch.
4. Whether the GitHub command line tool is signed in (`gh auth status`). If it is, add `--gh` for pull request cycle time and review time.
5. The team's change size threshold in lines. If there is none, use 400 and say it is a default of this repository, not a standard.
6. Where the report may be saved. It describes the organization, so it must not go into a public repository.

## Step 2: Prepare

- For a GitHub URL, clone into a new empty directory outside this project. Do not run anything from inside the cloned repository.
- Run `git fetch --all --tags` in each repository. If it is shallow, run `git fetch --unshallow`.
- Check that `python3 --version` and `git --version` work.

## Step 3: Run

```bash
python3 <skill folder>/scripts/audit.py --repo <path> [--repo <path2>] --days 90 --threshold 400 [--gh] --format both --out <private folder>
```

Add `--branch <name>` when needed. Add `--names` only if the user asks for contributor names for their own use.

## Step 4: Check

- Read the whole report, including the warnings at the top. A shallow clone, a short history or a stale branch changes what the numbers mean. Say so.
- Spot check one number against raw git, for example `git rev-list --no-merges --count --since=<date> <branch>`. If it disagrees, say so and stop until the cause is found.

## Step 5: Interpret

Use the reading table in the playbook. Never fill an Unknown with an estimate.

Produce, in this order:

1. **Result:** the three findings that matter most, each with the number, its label and the question to ask the team.
2. **Baseline rows for the First 90 Days table:** metric, value, source and date. Keep Proxy labels. Turn each Unknown into a 60-day task with an owner role.
3. **Evidence for ADOPT:** one line per foundation capability and for the context practice and traceability, as evidence only. Do not rate or score. The user makes that call.
4. **Unknowns:** each with the source that would answer it and an owner role.
5. **Caveats:** the report's warnings, restated in plain words.

## Step 6: Offer next steps

Offer to carry the evidence into `/adopt-assess`, the baseline rows into `/cto-day-one`, or the numbers into `/board-update` with their Proxy labels. Offer to rerun in a quarter with the same window and threshold.

## Rules

- Plain, direct language. No filler and no hedging.
- Never invent numbers, and never present a Proxy as the standard metric.
- Do not evaluate or rank people. Commit counts are not contribution.
- Do not save the report in the cto-os repository or any public repository.
- Do not recommend a tool or vendor. Recommend practices.
- If the script fails or the output looks wrong, report the error and the raw git check you ran. Do not patch the numbers by hand.
