# Changelog

## v0.6.0 (2026-11-22)

Added
- Hiring playbook (`playbooks/hiring.md`): role scorecard, level decided before sourcing, loop design with two independent signals per competency, work samples that hold up when candidates use AI, a 1 to 4 rubric with evidence required, a 30-minute debrief, offer and close, legal and fairness checks, and measures for the process.
- Hiring templates: role scorecard, interview loop plan, interview question bank (two questions per competency with follow-ups and strong and weak signals), interview feedback form and hiring debrief.
- `hiring-plan` agent skill with a bundled script (`skills/hiring-plan/scripts/loop_check.py`, Python standard library only). `coverage` checks a loop plan for competencies without two different interviewers, overloaded interviewers, candidate time over the cap, and a missing decision owner or AI policy. `debrief` summarizes feedback, counts a score only when it has written evidence, and flags score gaps of two points or more.
- Leveling playbook (`playbooks/leveling.md`): ground rules, level counts by headcount, six axes, staff archetypes, manager spans, pay band structure, calibration, promotions, hard conversations and ladder health measures.
- Leveling ladder template (`templates/leveling-ladder.md`): E1 to E6 and M1 to M4 on six axes, including engineering with AI. Written for this repository.
- Promotion packet template.
- `leveling-ladder` agent skill with a bundled script (`skills/leveling-ladder/scripts/org_shape.py`, Python standard library only). It measures headcount, levels, spans, layers and time in level from a roster file of opaque ids, and does not break out groups under five people.

Changed
- First 90 Days links to the hiring and leveling playbooks.
- README table, run line and Next list.

Tested
- Both scripts have unit tests whose expected values were worked out by hand from small synthetic fixtures (12 tests for `loop_check.py`, 13 for `org_shape.py`). Run `python3 -I test_loop_check.py` and `python3 -I test_org_shape.py` in each script folder.
- The 1 to 4 scale, the five-hour candidate cap, the three-competency limit per interview, the span and time-in-level thresholds and the ladder's level bands are this repository's judgment. They are Draft and not yet validated in real engagements.

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
