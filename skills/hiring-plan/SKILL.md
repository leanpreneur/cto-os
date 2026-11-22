---
name: hiring-plan
description: Use when an engineering leader is opening an engineering role, designing an interview loop, or running a hiring debrief. Interviews the user, then produces a role scorecard, a structured loop with questions and rubrics, a work sample design and a candidate message, and checks loop coverage with a bundled script. In debrief mode it summarizes interview feedback and flags missing evidence and score gaps.
---

# hiring-plan

Plan a hire, or run its debrief, for an engineering role. Follow `references/hiring.md`. Use `references/role-scorecard.md`, `references/interview-loop-plan.md`, `references/interview-question-bank.md`, `references/interview-feedback-form.md`, `references/hiring-debrief.md` and `references/leveling-ladder.md`. The script at `scripts/loop_check.py` needs `python3` only. It uses no model, so the same input gives the same output.

Ask first which mode the user wants: **Plan** (a role is opening) or **Debrief** (interviews are done). If it is clear from the request, do not ask.

## Plan mode

### Step 1: Interview

Ask in one message. Accept partial answers.

1. Role title, level, team, and who it reports to. If the company has no ladder, say so and use the starter ladder in `references/leveling-ladder.md`.
2. Why the role is open now, and the three results the person must produce in 12 months.
3. The hardest problems the person will meet in the first six months.
4. Stack, and how the team uses AI tools today.
5. Who can interview, by name or role, and who is already trained.
6. Constraints: pay band, location and remote policy, timeline, and a cap on candidate time (default 5 hours).
7. The AI policy for the loop: allowed and observed, allowed with disclosure, or not allowed. Recommend allowed and observed if the job uses AI tools daily.
8. Where the company hires, so the legal notes in Step 8 of the playbook can be checked.

### Step 2: Read what exists

If the user gives a job description, an old scorecard, a ladder or feedback from earlier hires, read them before drafting. Use their words for outcomes and competencies.

### Step 3: Write the scorecard

Fill in the role scorecard. Choose five to seven competencies from the library in the playbook. Mark each must-have or trainable. Where the user did not say which, propose and label it as an assumption. Check each competency: could two interviewers who never spoke agree on whether a candidate showed it? If not, rewrite it as observable behavior.

### Step 4: Design the loop and check it

Start from the default loop in the playbook and adjust it for the role type. Save the plan as JSON in a private folder, outside any public repository, using this shape:

```json
{
  "role": "Senior Backend Engineer", "level": "E3",
  "decision_owner": "hiring-manager", "debrief": true, "ai_policy": "allowed",
  "competencies": [{"id": "judgment", "name": "Technical judgment", "must": true}],
  "interviews": [{"id": "sample", "name": "Work sample", "minutes": 90, "interviewer": "engineer-a",
                  "type": "work_sample", "competencies": ["judgment"]}]
}
```

`ai_policy` is `allowed`, `allowed_with_disclosure` or `not_allowed`. A full example is in `scripts/examples/loop-example.json`.

Run:

```bash
python3 <skill folder>/scripts/loop_check.py coverage --plan <private folder>/loop.json
```

Fix every FAIL and rerun until none remain. Read each WARN and either fix it or tell the user why you left it. Do not edit the numbers or the findings by hand. If the script errors, report the error.

### Step 5: Questions, rubrics and the work sample

For each interview, pick questions from the question bank for the competencies it tests. Keep the follow-ups and the strong and weak signals. Rewrite the signals only to match the role.

- For system design, ask the user for a problem their team really solved. Do not invent company facts. If they have none, offer a clearly generic problem and say it is generic.
- For the work sample, design one of the three exercises in the playbook. For a pull request review, write the planted defects as an answer key for interviewers.

### Step 6: Candidate message and interviewer briefing

Draft both from the loop plan template. State the steps, the time, the AI policy, what to prepare and when the candidate will hear back.

### Step 7: Produce the output

Output exactly these sections, in this order:

1. **Assumptions:** what you assumed and could not confirm.
2. **Role scorecard:** the filled template.
3. **Loop plan:** the table, and the coverage result with the matrix.
4. **Questions and rubrics:** for each interview, the questions, follow-ups and signals.
5. **Work sample:** the exercise, the rubric, and the answer key.
6. **Candidate message.**
7. **Interviewer briefing.**
8. **Open items:** things to check with counsel for the user's location, numbers still Unknown, and the six-month check to put on the calendar.

Offer to save the scorecard and loop plan as files the user can share with interviewers.

## Debrief mode

### Step 1: Collect the feedback

Ask for each interviewer's scores, the evidence behind each score, and their recommendation: `hire`, `hire_other_level` or `no_hire`. Use a candidate ID, never a name. Ask whether each person submitted before reading anyone else's feedback. Ask for the loop plan file, or rebuild it from the interview.

Write the feedback as JSON in a private folder:

```json
{
  "candidate": "C-104", "role": "Senior Backend Engineer", "level": "E3",
  "feedback": [{"interviewer": "engineer-a", "interview": "sample", "submitted_before_debrief": true,
                "recommendation": "hire", "scores": {"judgment": 3},
                "evidence": {"judgment": "Chose a queue over polling and named duplicate delivery as the cost"}}]
}
```

Scores are whole numbers from 1 to 4. Do not fill in a score or evidence the user did not give you. See `scripts/examples/feedback-example.json`.

### Step 2: Run the summary

```bash
python3 <skill folder>/scripts/loop_check.py debrief --feedback <private folder>/feedback.json --plan <private folder>/loop.json
```

### Step 3: Prepare the debrief

Produce, in this order:

1. **Signal:** the script's line on whether the must-have competencies are established. Say it is a summary and the decision owner decides.
2. **Scores by competency:** the table from the script.
3. **Gaps to resolve:** each competency with a gap of two points or more, with the evidence behind each score.
4. **Missing evidence:** scores that did not count, and who should add evidence.
5. **Process notes:** late or duplicate feedback.
6. **Three questions for the meeting,** each tied to a gap or a missing signal.
7. **Draft decision record** for a senior hire, only after the user states the decision. Use `decision-record.md` from the repository.

Then offer the six-month check: would you hire this person again, and at this level?

## Rules

- Plain, direct language. No filler and no hedging.
- Never invent evidence, scores, candidates, interviewers or company facts.
- The decision belongs to the decision owner. Do not recommend hire or no hire.
- Use candidate IDs. Do not ask for, record or use a protected characteristic or a proxy for one.
- Do not rank candidates against each other. Compare each one with the scorecard.
- Keep scorecards, plans and feedback out of any public repository.
- Do not screen or rank résumés with a model. If the user asks, point to Step 8 of the playbook and tell them to check local law with counsel.
- This is not legal advice. Say so when a question touches employment law.
- Do not recommend a vendor. Recommend practices.
