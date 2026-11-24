# Changelog

## v0.8.0 (2026-11-23)

Added
- Incident response playbook (`playbooks/incident-response.md`): a severity scale written from customer impact, four incident roles, declaring early, a first-15-minutes routine, a communication clock for responders, support, customers and the CEO, resolving and closing, postmortem triggers, a blameless postmortem, action item follow-through, and measures with Measured and Proxy labels.
- Incident templates: severity guide, status update (customer, internal and CEO), incident log and postmortem.
- `incident-response` agent skill with four modes. Prepare builds the process. Run helps in the first 15 minutes of a live incident, drafts updates on a clock and keeps the log. Postmortem drafts from your log and checks the result. Measure summarizes incidents from a file.
- `incident_check.py` (Python standard library only), bundled with the skill. `postmortem` checks a postmortem written from the template: missing sections, times that go backwards, action items with no owner or due date, one contributing factor, impact with no number, a customer-found incident with no detect item, and a list of blame phrases. It also measures time to detect, mitigate and resolve. `summary` reads a CSV of incidents and reports counts by severity, medians and longest times, who found each incident, repeat contributing factors, postmortems published within 7 days and overdue action items.
- Examples in `examples/incidents/`: a postmortem that fails the check and its fix, an incident summary, and a set of updates during an invented incident. The script output blocks are refreshed and checked by `scripts/build_examples.py`.
- Three router situations: an incident happening now, a missing or chaotic incident process, and a postmortem or incident measures.

Changed
- The router's example for a topic CTO OS does not cover is now SOC 2, because incident response is covered. Security and compliance programs are still listed as not covered.
- The first 90 days and engineering baseline playbooks link to the incident response playbook.
- README: three rows in the artifact table, the example links, the run line, and the Next list. Install steps now cover Codex and Gemini CLI as well as Claude Code, and say that the skills have been run in Claude Code and not yet in the other two.
- The router names no tool-specific mechanism. It tells Codex users to write `$skill-name`, and Gemini CLI users to describe the task.
- `scripts/sync-skill-references.sh` bundles the playbook and templates with the new skill.

Tested
- 35 unit tests (`python3 -I test_incident_check.py` in `skills/incident-response/scripts`), including the fixtures for the failing draft and the passing example. 15 router tests, with a regression phrase for each of the 17 situations.
- Early. The severity levels, update cadences, the 15-minute routine, the eight-item and 90-day limits and the 7-day publishing target are this repository's judgment and have not been validated in a real engagement.

## v0.7.1 (2026-11-22)

Added
- `examples/`: synthetic examples of what the skills produce. A filled role scorecard, an interview loop that fails the coverage check and the fixed version, a debrief summary with a missing-evidence flag and a score gap, an org shape report, a promotion packet that ends in "not yet", and three router answers including one for a topic CTO OS does not cover. Each example says whether it is script output or written by hand. No real company, candidate or employee appears.
- `scripts/build_examples.py`: refreshes the script output shown in the examples, and with `--check` fails if any of it no longer matches what the scripts print.
- `loop-draft.json` fixture and a test that it fails in the documented way (3 failures, 4 warnings).

Changed
- Status labels renamed: Draft is now Early, and Used is now Field-tested. Proven is unchanged. The meanings are the same. Early means written and not yet applied in a real engagement. Field-tested means applied in a real engagement. Every caveat about thresholds, rubrics and readings that have not been validated stays. Earlier entries below use the new names. No artifact is Field-tested yet.
- README: a "See what it produces" section above the artifact table, and a note that every artifact is Early today.
- Router asks "What is the company stage, and how many engineers are there?" for a new role.
- `scripts/sync-skill-references.sh` also refreshes the examples.

## v0.7.0 (2026-11-22)

Added
- `ask-cto-os` agent skill: the front door. You describe a situation and it names the skill or document to start with, what you will get and what to run next. It reads a routing table (`skills/ask-cto-os/references/routes.json`) with 14 situations, and says plainly what CTO OS does not cover yet.
- Situations page (`docs/situations.md`), generated from the routing table, so the same routes can be read without running a skill.
- `check_routes.py` (Python standard library only) with three commands. `check` fails if any skill, playbook or template cannot be reached from a situation, or if a route points to something that does not exist. `render` writes the situations page. `match` ranks situations by keyword signals, as candidates for the skill to judge.

Changed
- README: the router is the first row of the artifact table, the run line starts with `/ask-cto-os`, the Next list drops the router, and Maintaining says to add every new artifact to the routing table.
- `scripts/sync-skill-references.sh` regenerates `docs/situations.md`.

Tested
- 15 unit tests (`python3 -I test_check_routes.py` in `skills/ask-cto-os/scripts`), including a check that the real repository is fully reachable and a regression phrase for each of the 14 situations. The keyword matcher is a convenience and counts words. The skill itself routes on meaning.

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
- The 1 to 4 scale, the five-hour candidate cap, the three-competency limit per interview, the span and time-in-level thresholds and the ladder's level bands are this repository's judgment. They are Early and not yet validated in real engagements.

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
- ADOPT foundations gate: seven capabilities from DORA's AI Capabilities Model, rated Present, Partial or Absent with evidence tests. A ceiling rule caps the overall level at 2, 3, 4 or 5 depending on which capabilities are Present. The mapping to levels is this repository's judgment and is Early.
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
