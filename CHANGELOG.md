# Changelog

## v0.5.0 (2026-10-06)

Added
- Engineering Baseline playbook (`playbooks/engineering-baseline.md`): which delivery numbers git can and cannot show, a Measured, Proxy or Unknown label for every number, a reading table of questions to ask, and rules against misuse.
- `eng-audit` agent skill with a bundled script (`skills/eng-audit/scripts/audit.py`, Python standard library only). It computes change size, branch lifetime, release cadence, reverts, contributor concentration, AI traceability, documentation freshness and context files from git history. It can add pull request cycle time and review time from the GitHub command line tool. It reports baseline rows for the First 90 Days table and evidence for the ADOPT assessment.

Changed
- First 90 Days playbook points to the engineering baseline for the git-derived metrics.
- README install snippet copies all skills in one command.

Tested
- Against synthetic repositories with known answers, and against two public repositories, with counts checked against raw git. Excludes the commits at the edge of a shallow clone, which git shows as adding every file.

## v0.4.0 (2026-10-04)

Added
- ADOPT foundations gate: seven capabilities from DORA's AI Capabilities Model, rated Present, Partial or Absent with evidence tests. A ceiling rule caps the overall level at 2, 3, 4 or 5 depending on which capabilities are Present. The mapping to levels is this repository's judgment and is Draft.
- ADOPT context practice inside dimension D: a five-level scale, a minimum context list for a repository, and matching observables in O (named owner) and P (no secrets in context).
- Eleventh interview question on what a new engineer or agent must read to change the system safely.
- Foundation moves in the move guide, and a foundations table in the scoring sheet.

Changed
- Overall level is now the lower of the lowest dimension score and the foundations ceiling.
- `adopt-assess` skill checks foundations before scoring and reports what binds the overall level.
- One-page CEO output names the binding constraint.

## v0.3.0 (2026-10-03)

Added
- CEO and CTO Partnership playbook (`playbooks/ceo-cto-partnership.md`): six practices, business translation table, bad-news and disagreement scripts, board preparation timeline, sources.
- CEO and CTO Operating Agreement template (`templates/ceo-cto-operating-agreement.md`).
- Board Update template (`templates/board-update.md`): one-page headline plus six appendices, status rules, risk register.
- `ceo-alignment` and `board-update` agent skills.

Changed
- `scripts/sync-skill-references.sh` now bundles templates as well as playbooks.
- First 90 Days playbook links to the operating agreement.

## v0.2.0 (2026-10-03)

Added
- ADOPT assessment playbook (`playbooks/adopt-assessment.md`): five dimensions, five maturity levels, dimension-by-level rubric, constraint rule, move guide, scoring sheet and one-page CEO output.
- `adopt-assess` agent skill that gathers evidence, interviews, scores and produces the one-page result.
- Related work page (`docs/related-work.md`).
- Skills now bundle their playbook in `references/`, with `scripts/sync-skill-references.sh` to keep copies current.

Changed
- README: new positioning, expanded artifact table, Related work section.
- First 90 Days playbook links to the ADOPT assessment for AI rollouts.

## v0.1.0 (2026-10-03)

Initial release: First 90 Days playbook, `cto-day-one` skill, decision record template, principles, profile README draft.
