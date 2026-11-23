# Example: a debrief summary

**Made by:** script output, plus the questions at the end, which are written by hand. The summary is produced by `skills/hiring-plan/scripts/loop_check.py debrief` and kept current by `scripts/build_examples.py --check`. Candidate C-104 and the interviewers are invented.

Five interviewers submitted feedback for a senior backend engineer. The feedback file is `skills/hiring-plan/scripts/examples/feedback-example.json`.

```bash
python3 skills/hiring-plan/scripts/loop_check.py debrief \
  --feedback skills/hiring-plan/scripts/examples/feedback-example.json \
  --plan skills/hiring-plan/scripts/examples/loop-example.json
```

<!-- output:debrief -->
> # Debrief summary: C-104 Senior Backend Engineer E3
>
> **Signal:** Not established on: Engineering with AI. This is a summary. The decision owner decides.
>
> | Competency | Must | Scores counted | Mean | Spread | Flags |
> | --- | --- | --- | --- | --- | --- |
> | Technical judgment | yes | engineer-a: 3, engineer-b: 3 | 3.00 | 0 |  |
> | System design | yes | engineer-b: 2, product-partner: 4 | 3.00 | 2 | DISCUSS: scores differ by 2 |
> | Delivery and ownership | yes | engineer-a: 3, hiring-manager: 3, engineer-c: 3 | 3.00 | 0 |  |
> | Collaboration and communication | no | product-partner: 3, hiring-manager: 3, engineer-c: 3 | 3.00 | 0 |  |
> | Engineering with AI | yes | engineer-a: 4 | 4.00 | 0 | NO EVIDENCE: hiring-manager; INSUFFICIENT: fewer than 2 interviewers with evidence |
>
> Recommendations: hire 4, hire at another level 0, no hire 1.
>
> ## Evidence behind the gaps
>
> **System design**
> - engineer-b, score 2: Drew the happy path only and skipped failure modes
> - product-partner, score 4: Found the duplicate delivery flaw and proposed an idempotency key
>
> ## Process notes
>
> - Feedback not marked as submitted before the debrief: hiring-manager.
>
> Rules: a score counts only with at least 4 words of written evidence. The bar is a mean of 3 on a 1 to 4 scale with no score of 1. A gap of 2 points or more goes to discussion. These are defaults of this repository, not standards.
<!-- end output -->

## How the meeting would use it

The summary does not decide anything. It tells the decision owner where to spend the 30 minutes.

1. **Engineering with AI has one scored signal.** The hiring manager scored it 3 with the note "Seemed capable", which is too thin to count. Ask the hiring manager for the observation behind the score before the meeting. If there is none, treat the competency as not yet tested and decide whether one more conversation would settle it.
2. **System design: a 2 and a 4.** One engineer saw only the happy path. The product partner saw the candidate find the duplicate delivery flaw. Ask which prompt each interviewer used. If they used different prompts, the scores are not comparable, and that is a calibration problem to fix after this hire.
3. **Four hire recommendations and one no hire.** Ask the product partner for the specific thing the candidate said or did that led to no hire. Settle it with evidence, not with the count of votes.
4. **One piece of feedback was not submitted before the debrief.** Note it, and remind the interviewer that written feedback before the meeting is what stops everyone anchoring on the first opinion in the room.
