---
name: first-90-days
status: draft
audience: CTO or VP Engineering joining a company or taking over an engineering organization
---

# First 90 Days as CTO

**Outcome by day 90:** a written diagnosis, a prioritized plan the CEO has signed, one visible win, and the first structural change running.

## Ground rules

1. **Listen for 30 days before announcing change.** Exceptions: a security or data-loss risk, a broken release process, or a person you cannot afford to lose.
2. **Write everything down.** The diagnosis is a document. Share it, correct it, version it.
3. **Agree on how the CEO measures you before you agree on what you will do.**
4. **Do not judge people in the first two weeks.** Collect observations. Form conclusions with data from several sources.

## Week 0: before day one

Get written answers from the CEO:

- The top three outcomes for the next twelve months.
- What has been tried before and why it failed.
- Your decision rights over hiring, budget, architecture and vendors.
- Meeting rhythm with the CEO and the board.

Request access to:

- Source repositories, CI/CD and deployment tooling.
- Cloud billing and the last twelve months of cost.
- Incident history and postmortems.
- Roadmap, org chart and the last four board decks.
- Customer escalations, security reports and vendor contracts.

## Days 1 to 30: Learn

### 1. Listening tour

Meet every manager, every engineer if the team is under thirty, plus product, design, sales, customer success and finance. Meet the five largest customers if the CEO agrees. Ask everyone the same questions:

1. What should I know that nobody has told me?
2. What slows you down most each week?
3. If you had a free month, what would you fix first?
4. What did we try that failed, and why?
5. Which part of the system do you avoid touching?
6. Who do you go to when you are stuck?
7. What do customers complain about?
8. What should I not change?

Record answers in one shared table. Look for the same answer from unrelated people.

### 2. Read the system

- Ship a small change yourself, start to finish. Note every step and wait.
- Read the last ten incidents and their postmortems, or note that none exist.
- Review twenty recent pull requests for size, review time and test coverage.
- Read the on-call history. Count pages per week and who answers them.
- Read the architecture documentation, then compare it with the code.

### 3. Baseline metrics

| Metric | Why it matters |
| --- | --- |
| Deployment frequency | How often value reaches customers |
| Lead time for changes | Time from commit to production |
| Change failure rate | Share of releases that cause an incident or rollback |
| Time to restore service | How long customers feel an outage |
| Monthly cloud cost and trend | Unit economics and waste |
| Share of unplanned work | Capacity lost to firefighting |
| Twelve-month attrition | Health of the team |
| Open roles and time to fill | Hiring capacity |
| Customer escalations by account | Where quality hurts revenue |

Record the value, the source and the date. Mark anything you cannot measure as **Unknown** and make measuring it a 60-day task.

### 4. Output: Diagnosis v1

Facts only, no recommendations. Sections: system, delivery, people, customers, cost, security and compliance.

## Days 31 to 60: Decide

1. **Diagnosis v2.** Add strengths, ranked risks (likelihood times impact) and root causes. Separate causes from symptoms.
2. **Choose at most three priorities** for the next two quarters. Publish what you will not do.
3. **Assign owners.** Every service, pipeline and recurring process gets a named owner and a backup.
4. **Set the operating cadence:**
   - Weekly engineering leadership meeting.
   - Biweekly roadmap review with product.
   - Monthly metrics review with the CEO.
   - Quarterly planning and a board metrics page.
5. **Start written decisions** with the [Decision Record](https://github.com/leanpreneur/cto-os/blob/main/templates/decision-record.md).
6. **Align with the CEO.** Review priorities, success measures, headcount and budget. Obtain explicit sign-off.

**Output:** a two-page plan the CEO has approved.

## Days 61 to 90: Deliver

1. **Ship one visible win.** Choose from the diagnosis something a customer or the CEO can see within thirty days of effort: a fixed deployment pipeline, removal of the top incident cause, a cleared escalation.
2. **Start the first structural change:** a hiring plan, an on-call rotation, a release process, or an AI-assisted development rollout with a measured pilot. Before an AI rollout, run the [ADOPT assessment](https://github.com/leanpreneur/cto-os/blob/main/playbooks/adopt-assessment.md) to find your starting level.
3. **Deliver the 90-day review** to the CEO, and to the board if asked: baseline against current, plan, risks and asks.
4. **Reset team goals and 1:1 cadence** to match the plan.

**Output:** the 90-day review.

## Adjust for company stage

Typical ranges, not rules.

| Stage | Typical engineering size | Focus first | Common trap |
| --- | --- | --- | --- |
| Seed | Under 10 | Continuous integration, monitoring, backups, security basics, shipping speed | Building process the team does not need yet |
| Series A or B | 10 to 50 | First managers, clear ownership, release reliability | Promoting by tenure without management training |
| Growth | 50 and above | Org design, platform, cost, compliance | Large rewrites and extra management layers |
| Turnaround | Any | Stop incidents and attrition, restore trust | Announcing a vision before fixing the basics |

## Red flags in the first 30 days

| Signal | First action |
| --- | --- |
| Nobody can describe how a change reaches production | Map the path with the team; fix the slowest step |
| No named on-call owner | Create a rotation and a backup this month |
| One engineer holds critical knowledge | Pair a second engineer and write the runbook |
| Roadmap changes weekly on executive request | Agree on a change process with the CEO |
| CEO and board give conflicting goals | Surface the conflict in writing and ask for one ranked list |
| Backups have never been restored | Run a restore test within two weeks |

## CEO expectations: questions to settle in writing

Capture the answers in the [CEO and CTO operating agreement](https://github.com/leanpreneur/cto-os/blob/main/templates/ceo-cto-operating-agreement.md) within your first two weeks.

1. Which three outcomes decide whether this hire worked, and by when?
2. What can I decide alone, and what needs your approval?
3. How do you want bad news delivered, and how fast?
4. What do you expect from me with the board?
5. Which commitments to customers or investors are already made?

## Deliverables checklist

- [ ] Day 30: Diagnosis v1, baseline metrics table, listening tour summary.
- [ ] Day 60: Diagnosis v2, priorities with exclusions, owners assigned, cadence published, CEO sign-off.
- [ ] Day 90: One visible win shipped, first structural change running, 90-day review delivered.
