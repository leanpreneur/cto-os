# Example: a loop that fails the coverage check, and the fix

**Made by:** script output. The two reports below are produced by `skills/hiring-plan/scripts/loop_check.py coverage`, and are kept current by `scripts/build_examples.py --check`. The commentary is written by hand. ExampleCo is invented.

## The first draft

A hiring manager puts the loop together quickly. One long technical interview covers most of the competencies, and the same engineer runs the work sample.

```bash
python3 skills/hiring-plan/scripts/loop_check.py coverage --plan skills/hiring-plan/scripts/examples/loop-draft.json
```

<!-- output:loop-draft -->
> # Loop coverage: Senior Backend Engineer E3
>
> **Result: FAIL** (3 failures, 4 warnings). Candidate time: 4.8 hours.
>
> | Competency | screen | tech | sample | manager | Interviewers |
> | --- | --- | --- | --- | --- | --- |
> | Technical judgment* |  | X | X |  | 1 |
> | System design* |  | X |  |  | 1 |
> | Delivery and ownership* |  | X |  | X | 2 |
> | Collaboration and communication |  |  |  | X | 1 |
> | Engineering with AI* |  | X | X |  | 1 |
>
> `*` marks a must-have competency.
>
> ## Findings
>
> - **FAIL** (thin-coverage): Competency 'Engineering with AI' (must-have) has 1 interviewer across 2 interviews. It needs 2 different interviewers.
> - **FAIL** (thin-coverage): Competency 'System design' (must-have) has 1 interviewer across 1 interview. It needs 2 different interviewers.
> - **FAIL** (thin-coverage): Competency 'Technical judgment' (must-have) has 1 interviewer across 2 interviews. It needs 2 different interviewers.
> - **WARN** (no-ai-policy): No valid 'ai_policy'. Use one of: allowed, allowed_with_disclosure, not_allowed. Candidates must be told in advance.
> - **WARN** (no-debrief): The plan does not schedule a debrief ('debrief': true).
> - **WARN** (thin-coverage): Competency 'Collaboration and communication' (trainable) has 1 interviewer across 1 interview. It needs 2 different interviewers.
> - **WARN** (too-many-competencies): Interview 'tech' scores 4 competencies. More than 3 cannot be probed in one interview.
>
> Thresholds are defaults of this repository, not standards: 2 different interviewers per competency, at most 3 competencies per interview, at most 2 interviews per person, at most 5 candidate hours.
<!-- end output -->

What the report caught:

- Three must-have competencies rest on one person's opinion, because only one engineer tests each of them.
- The 120-minute technical interview scores four competencies. No interviewer can probe four in one sitting.
- There is no AI policy and no debrief, so candidates would not know the rules.

## The fix

The design question moves to a second engineer. A cross-functional interview adds a second view on design and collaboration. The hiring manager's deep dive picks up the AI competency. The plan names an AI policy and schedules a debrief.

```bash
python3 skills/hiring-plan/scripts/loop_check.py coverage --plan skills/hiring-plan/scripts/examples/loop-example.json
```

<!-- output:loop-fixed -->
> # Loop coverage: Senior Backend Engineer E3
>
> **Result: PASS** (0 failures, 0 warnings). Candidate time: 5.0 hours.
>
> | Competency | screen | sample | design | collab | manager | cross | Interviewers |
> | --- | --- | --- | --- | --- | --- | --- | --- |
> | Technical judgment* |  | X | X |  |  |  | 2 |
> | System design* |  |  | X |  |  | X | 2 |
> | Delivery and ownership* |  | X |  | X | X |  | 3 |
> | Collaboration and communication |  |  |  | X | X | X | 3 |
> | Engineering with AI* |  | X |  |  | X |  | 2 |
>
> `*` marks a must-have competency.
>
> No findings.
>
> Thresholds are defaults of this repository, not standards: 2 different interviewers per competency, at most 3 competencies per interview, at most 2 interviews per person, at most 5 candidate hours.
<!-- end output -->

Every must-have competency now has two different interviewers, no interview scores more than three, and candidate time is exactly the five-hour default. The checks are defaults of this repository, not standards.
