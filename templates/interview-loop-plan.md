---
name: interview-loop-plan
status: early
use: one per open role, after the role scorecard and before the first interview
---

# Interview Loop Plan: [Role title], [Level]

| Field | Value |
| --- | --- |
| Decision owner | |
| Debrief date | Within two working days of the last interview |
| Candidate time, total | Cap: 5 hours (this repo's default) |
| AI policy | Allowed and observed, allowed with disclosure, or not allowed |
| Note-taking | Verbatim notes, no conclusions until after the interview |

## Loop

Every competency in at least two interviews, run by two different people. No interview scores more than three competencies.

| ID | Interview | Minutes | Interviewer | Format | Competencies tested | Question set | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| screen | Screen | 30 | | Video | | | Go or stop |
| sample | Work sample | 90 | | | | | Scored rubric |
| design | System design | 60 | | | | | Scored rubric |
| collab | Collaboration and ownership | 45 | | | | | Scored rubric |
| manager | Hiring manager deep dive | 45 | | | | | Scored rubric |
| cross | Cross-functional | 30 | | | | | Scored rubric |

## Coverage check

Run it. It reports competencies with fewer than two signals, overloaded interviewers, missing decision owner and missing AI policy.

```bash
python3 skills/hiring-plan/scripts/loop_check.py coverage --plan loop.json
```

Save the plan as `loop.json`. Keep it out of any public repository, because it names your interviewers. The example below is shortened to show the shape. A real plan lists every interview, and the script reports four failures for this one, because most competencies are covered by one interviewer or none. A full plan that passes is in `skills/hiring-plan/scripts/examples/loop-example.json`.

```json
{
  "role": "Senior Backend Engineer",
  "level": "E3",
  "decision_owner": "hiring-manager",
  "debrief": true,
  "ai_policy": "allowed",
  "competencies": [
    {"id": "judgment", "name": "Technical judgment", "must": true},
    {"id": "design", "name": "System design", "must": true},
    {"id": "delivery", "name": "Delivery and ownership", "must": true},
    {"id": "collab", "name": "Collaboration and communication", "must": false},
    {"id": "ai", "name": "Engineering with AI", "must": true}
  ],
  "interviews": [
    {"id": "sample", "name": "Work sample", "minutes": 90, "interviewer": "engineer-a",
     "type": "work_sample", "competencies": ["judgment", "ai", "delivery"]},
    {"id": "design", "name": "System design", "minutes": 60, "interviewer": "engineer-b",
     "type": "design", "competencies": ["design", "judgment"]}
  ]
}
```

## Message to the candidate

Send this before the first interview.

- The steps, who you will meet by role, and how long each takes.
- The AI policy, in one sentence per step.
- What to prepare, and what not to.
- When they will hear from you after the last interview.
- Who to contact with questions or to ask for an adjustment.

## Interviewer briefing

- Read the [role scorecard](role-scorecard.md) and the [question bank](interview-question-bank.md) before you meet the candidate.
- Ask your core questions in order. Use the follow-ups as written.
- Fill in the [feedback form](interview-feedback-form.md) within 24 hours, before you read anyone else's.
- Do not discuss the candidate until the debrief.
