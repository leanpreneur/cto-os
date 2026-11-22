---
name: hiring-debrief
status: draft
use: one per candidate, run within two working days of the last interview, 30 minutes
---

# Hiring Debrief: [Candidate ID], [Role], [Level]

| Field | Value |
| --- | --- |
| Decision owner | |
| Interviewers present | |
| Date | YYYY-MM-DD |
| All feedback submitted before the debrief? | Yes or no, and who was late |

## Before the meeting

Run the summary. It lists scores by competency, flags scores with no evidence and flags gaps of two points or more. Send it to the interviewers with their own feedback forms.

```bash
python3 skills/hiring-plan/scripts/loop_check.py debrief --feedback feedback.json --plan loop.json
```

## Agenda (30 minutes)

| Minutes | Step | Rule |
| --- | --- | --- |
| 5 | Read the summary and all feedback in silence | No discussion yet |
| 10 | Each interviewer states their score and strongest evidence | Most junior first, decision owner last |
| 10 | Resolve gaps of two points or more | Evidence settles it, not seniority |
| 5 | Decision owner decides and states the reasons | Record it below |

## Scores by competency

Paste the summary table here, or fill it in.

| Competency | Must-have | Scores | Spread | Evidence gaps |
| --- | --- | --- | --- | --- |
| | | | | |

## Gaps to resolve

| Competency | Scores and who | The evidence behind each | What settled it |
| --- | --- | --- | --- |
| | | | |

## Decision

- [ ] Hire at the target level
- [ ] Hire at a different level: ___
- [ ] No hire
- [ ] More evidence. The single question to answer: ___. Who asks it: ___. By when: ___. One extra conversation at most.

**Reasons, in the decision owner's words, tied to the evidence:**

**Concerns we accept and how we will manage them in the first 90 days:**

## Not allowed in this meeting

- "Culture fit" with no named behavior.
- "Gut feel" with no evidence.
- "I would not want to work with them" with no observation.

Ask what the candidate did or said.

## After the meeting

- [ ] Decision and level recorded. For senior hires, write a [decision record](https://github.com/leanpreneur/cto-os/blob/main/templates/decision-record.md).
- [ ] Candidate told within 48 hours.
- [ ] Notes kept for the period local law requires, in a private location.
- [ ] A six-month check is on the calendar: would you hire this person again, and at this level?
