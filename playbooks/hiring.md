---
name: hiring
status: draft
audience: CTO or engineering manager who is about to hire engineers, or who inherited a hiring process nobody wrote down
---

# Hiring Engineers: Decide the Bar Before You Meet Anyone

**Outcome:** for each open role, a written scorecard, an interview loop in which every competency is tested by at least two people against a written rubric, and a debrief that reaches a decision from evidence in 30 minutes.

Most hiring failures are decided before the first interview. Nobody wrote down what the person must do, so each interviewer tests what they personally like, and the debrief turns into a vote on impressions. This playbook fixes that in order: scorecard, level, loop, work sample, questions, feedback, debrief, offer, measurement. The [leveling](leveling.md) playbook says what each level means, and you need it before you start.

## Ground rules

1. **Write the scorecard before the job post.** If you cannot state the outcomes, you cannot test for them.
2. **Decide the level before sourcing.** Level drives the questions, the pay band and the candidate pool.
3. **Two independent signals per competency.** Two different interviewers, in two different interviews. One person's view is an opinion.
4. **Score before you talk.** Each interviewer writes feedback with evidence and submits it before reading anyone else's.
5. **Same questions, same rubric for every candidate in the role.**
6. **Test the work.** Use a work sample that resembles the job, not puzzles or trivia.
7. **One decision owner.** The hiring manager decides. Everyone else supplies evidence.
8. **Tell candidates the rules in advance:** the steps, the time each takes, whether AI tools are allowed, and when they will hear back.

## Why structure

Google's re:Work guide defines structured interviewing as using uniform methods to assess candidates applying for the same job: the same questions, a standard scale and predetermined qualifications. Its four parts are vetted questions, recorded notes, standardized rubrics, and trained and calibrated interviewers.

Sackett and colleagues (2022) re-estimated how well selection methods predict job performance. They report mean operational validities of .42 for structured interviews, .33 for work sample tests and .31 for cognitive ability tests, which puts structured interviews first. These are averages over many jobs and studies. They support structure as a practice. They do not predict how any one candidate will do. See [Sources](#sources).

## Step 1: Write the role scorecard

Use the [role scorecard](../templates/role-scorecard.md). It has five parts:

- **Mission:** one sentence on why the role exists.
- **Outcomes:** three to five results the person must produce in 12 months, each with a number or something you can observe.
- **Competencies:** five to seven behaviors, each with a definition and what meeting the bar looks like at this level.
- **Must-have or trainable:** mark each competency. Must-haves must be shown in the loop. Trainable ones you will teach.
- **Not a fit if:** two to four honest lines. "Needs a defined backlog every week" is useful.

The mission, outcomes and competencies structure comes from Geoff Smart and Randy Street's book *Who*.

**Test:** could two interviewers who never spoke agree on whether a candidate showed competency X? If not, rewrite the competency as observable behavior. "Strong communicator" fails this test. "Explains a technical trade-off to a non-engineer so that they can choose" passes it.

Pick competencies from this library, and add your own only when the role needs one.

| Competency | Plain definition |
| --- | --- |
| Technical judgment | Chooses the simplest solution that meets the constraints and can say what it gives up |
| System design | Breaks a problem into components, names the bottleneck and the failure modes, adapts when requirements change |
| Delivery and ownership | Gets work to production, tells people early when it will slip, finishes what they start |
| Debugging and production sense | Narrows a fault methodically and protects customers first |
| Collaboration and communication | Disagrees usefully, explains clearly, takes feedback |
| Learning and adaptability | Picks up unfamiliar areas fast and can say what they were bad at |
| Engineering with AI | Directs AI tools with the right context, verifies the output, and owns what ships |
| Product and customer sense | Connects the work to a customer problem and pushes back with evidence |
| Leadership and people (staff and managers) | Sets direction, develops others, handles performance and hiring |

## Step 2: Decide the level

Take the level from the [leveling ladder](../templates/leveling-ladder.md). Write down what a person at this level does that the level below does not. If you cannot, you are not ready to interview for it. Set the pay band now, before any candidate has an opinion about it. A candidate who lands between two levels is the hardest case. Decide in advance what evidence would put them at each.

## Step 3: Design the loop

A loop is the set of interviews a candidate sits. Use the [interview loop plan](../templates/interview-loop-plan.md). The default for a senior engineer is five hours of candidate time:

| Stage | Minutes | Who | Tests | Output |
| --- | --- | --- | --- | --- |
| Screen | 30 | Hiring manager | Motivation, level fit, pay expectations, logistics | Go or stop |
| Work sample | 90 | Engineer | Technical judgment, engineering with AI, delivery | Scored rubric |
| System design | 60 | Senior engineer | System design, technical judgment | Scored rubric |
| Collaboration and ownership | 45 | Engineer from another team | Collaboration, delivery, learning | Scored rubric |
| Hiring manager deep dive | 45 | Hiring manager | Scope, motivation, growth fit | Scored rubric |
| Cross-functional | 30 | Product or design partner | Product sense, communication | Scored rubric |

Rules for the loop:

1. **Every competency in at least two interviews, run by two different people.**
2. **No interview scores more than three competencies.** An interviewer cannot probe more than that in 45 minutes.
3. **Cheap stages first.** Do not spend five hours of your team's time on someone the screen should have stopped.
4. **Cap candidate time.** This repo's default is five hours total. Pay for any take-home work and keep it under two hours.
5. **Fix the interviewers before you open the role.** Train each one. A new interviewer shadows twice, then is shadowed once.
6. **The hiring manager never interviews alone.** Their view carries weight, so it needs a counterweight.

Change the loop for the role:

| Role | Change |
| --- | --- |
| First engineering hire | Drop system design depth. Add a long conversation on ambiguity, product sense and working with the founder. The person will make decisions with no review. |
| Mid-level engineer | Shorten system design to 45 minutes and score it against the level below senior. Weight learning and collaboration more. |
| Staff engineer | Replace the work sample with a design review of a real problem from your company, and add an interview on influence across teams. |
| Engineering manager | Add an interview on performance management and one on hiring and team building. Keep one technical depth conversation so they can judge designs. |

## Step 4: Work sample, and AI in the loop

State the AI policy to candidates before the first interview. Assume you cannot reliably tell whether a candidate used AI in work done on their own time, so design the loop so it does not matter.

| Policy | Use when | Cost |
| --- | --- | --- |
| Allowed and observed (default) | The job involves AI tools every day | You must score how they use the tool, which takes a rubric |
| Allowed with disclosure | Take-home work | Candidates differ in how much they disclose |
| Not allowed | A narrow check of fundamentals, live and supervised | Does not match the job. Keep it short |

Three work sample designs that work under the default policy:

1. **Pair on a small feature (75 minutes).** The candidate uses their own editor and tools on a small, real-looking codebase. Score how they frame the task, what context they give the tool, what they check and how they explain the result.
2. **Review an AI-generated pull request (45 minutes).** Prepare a pull request with planted defects: an error that is silently swallowed, a test that asserts nothing, a dependency nobody needs, and one requirement the code misses. Score what they find, what they ask and what they would block.
3. **Debug a failing service (60 minutes).** Give logs, a dashboard screenshot and a recent change list. Score how they narrow the fault and what they do for customers first.

Under all three, the candidate must be able to explain every line they submit. Do not score speed or typing. Do not use puzzles that no one on your team would ever meet.

If you screen résumés or rank candidates with software, read [Step 8](#step-8-legal-and-fairness) first.

## Step 5: Questions and rubrics

Use the [question bank](../templates/interview-question-bank.md). It has two questions per competency, with follow-ups and what strong and weak answers sound like. Prefer questions about what the candidate did over questions about what they would do, because past behavior is harder to invent. Draw design problems from something your team really solved.

Score each competency on one scale:

| Score | Meaning |
| --- | --- |
| 1 | Evidence below the bar for the level, or evidence against |
| 2 | Partial. Some evidence, but gaps in the core of the competency |
| 3 | Meets the bar for the level. Specific, first-person evidence of doing it |
| 4 | Exceeds the bar. Evidence at the next level, confirmed by results |

There is no midpoint on purpose. Every score needs evidence: what the candidate said or did, in a sentence or two. A score without evidence does not count.

Rules for interviewers:

- Take notes on what the candidate said and did. Write conclusions after the interview, not during it.
- Ask the same core questions in the same order. Use the follow-ups as written.
- Do not hint at the answer you want.
- Leave 10 minutes for the candidate's questions. Answer them honestly, including about problems.
- Do not discuss the candidate with anyone until you have submitted your feedback.

## Step 6: Feedback and debrief

**Feedback.** Each interviewer fills in the [feedback form](../templates/interview-feedback-form.md) within 24 hours and before reading anyone else's. It has a score and evidence for each competency, plus a recommendation: hire or no hire at the target level.

**Debrief.** Run the [debrief](../templates/hiring-debrief.md) within two working days of the last interview. It takes 30 minutes:

1. Read all feedback in silence (5 minutes).
2. Each interviewer states their score and strongest evidence, most junior first (10 minutes).
3. Take the competencies where scores differ by two points or more. Resolve them with evidence, not seniority (10 minutes).
4. The decision owner decides and states the reasons. Record the decision and the level (5 minutes).

Decision options are hire at this level, hire at another level, no hire, or more evidence. "More evidence" must name the single question that another conversation would answer, who will ask it and by when. Allow one extra conversation at most.

Do not accept these in a debrief: "culture fit" with no named behavior, "gut feel" with no evidence, and "I would not want to work with them" with no observation. Ask for what the candidate did or said.

For senior hires, write a [decision record](../templates/decision-record.md) with the options considered and the reason.

**Calibrate interviewers every quarter.** Give every interviewer the same written candidate answer, have each score it alone, then compare scores and talk through the gaps. That is the "train and calibrate" part of Google's four parts.

The `/hiring-plan` skill has a script that summarizes the feedback and flags missing evidence and large score gaps before the debrief.

## Step 7: Offer and close

1. **Set level and band before the loop.** Do not negotiate level after the offer.
2. **Call before you write.** Tell the candidate the level, why, and what they would own. Say what you heard that they care about.
3. **Move fast.** This repo's default is an offer within 48 hours of the debrief.
4. **Give a decision window that lets them talk to the people who matter to them.** A week is normal.
5. **Check two references,** at least one a former manager. Ask the same questions of every candidate: what did they own, how did they handle disagreement, what would you have them do differently, would you hire them again.
6. **Answer open questions in writing.** If the candidate declines, ask why, and record the reason.
7. **Tell the people who were not chosen, and how they did, fairly and promptly.**

## Step 8: Legal and fairness

This is not legal advice. Talk to counsel where you hire.

- Ask about the job. Do not ask about, or use as a proxy for, protected characteristics: age, race, religion, national origin, sex, pregnancy, family plans, marital status, disability, health, sexual orientation or gender identity. Ask whether they can work in the country as the law requires, and no more.
- Several US states and cities limit questions about pay history and criminal history, and require pay ranges in job postings. Check yours before you write the posting.
- If you use software to screen or rank candidates, including a language model, check local law first. New York City's Local Law 144 requires a bias audit and notice for automated employment decision tools used on candidates for jobs in the city. Enforcement began on 5 July 2023. Other jurisdictions have their own rules. Keep a person accountable for every decision.
- Keep scorecards and feedback for the period your local law requires.

Same questions and one rubric reduce the room for personal preference to decide. They do not remove it. Check the numbers in Step 9.

## Step 9: Measure the process

| Measure | How | Why |
| --- | --- | --- |
| Pass-through rate by stage | Candidates who advance from each stage, divided by candidates who entered | Shows where the loop is too strict or too loose |
| Pass-through by group | The same rate by group, where you collect that data lawfully | A large gap is a reason to look at the stage and the questions |
| Time to fill | Role opened to offer accepted | Hiring capacity, one of the First 90 Days rows |
| Offer acceptance rate | Accepted divided by offers made | Low rates point to band, level or the close |
| Hours of employee time per hire | Interview, debrief and prep hours | The cost of the loop |
| Feedback on time | Share of feedback submitted within 24 hours | Late feedback gets worse |
| Six-month check | Manager answers: would you hire this person again, and at this level? | The only real outcome measure you will have for years |
| Score against outcome | Interview scores next to the six-month answers | Tells you whether the rubric predicts anything in your company |

Do not claim quality of hire from fewer than about 20 hires. With a handful, read each case. Mark the numbers you cannot yet compute as Unknown.

## Definition of done

- A scorecard exists for every open role, with outcomes and competencies.
- The loop plan covers every must-have competency with two different interviewers. The `/hiring-plan` script reports no failures.
- Every interviewer is trained and has the rubric.
- The AI policy is written and sent to candidates.
- Each decision is recorded with the evidence, the level and the reason.

## How you will know it worked

- Leading indicator: the share of feedback that arrives on time with evidence for every score, and the share of debriefs that end with a decision in 30 minutes.
- Lagging indicator: the six-month answer to "would you hire this person again, at this level" across hires, and offer acceptance rate. Track both per quarter.

## Sources

- Google re:Work, [guide to structured interviewing](https://rework.withgoogle.com/intl/en/guides/a-guide-to-structured-interviewing-for-better-hiring-practices): the definition and the four parts above. The guide also cites Google's own results, which it gives without sample sizes, so treat them as unverified.
- Sackett, Zhang, Berry and Lievens (2022), "Revisiting meta-analytic estimates of validity in personnel selection: Addressing systematic overcorrection for restriction of range," *Journal of Applied Psychology* 107(11), 2040 to 2068 ([record](https://ink.library.smu.edu.sg/lkcsb_research/6894)). The figures above are as reported in a [summary from the Society for Industrial and Organizational Psychology](https://www.siop.org/tip-article/is-cognitive-ability-the-best-predictor-of-job-performance). The paper itself has not been checked line by line.
- Geoff Smart and Randy Street, *Who: The A Method for Hiring* (2008): the scorecard structure.
- New York City Local Law 144 of 2021 on automated employment decision tools, enforced from 5 July 2023.
- The five-hour cap, the 48-hour offer target, the three-competency limit per interview, the 1 to 4 scale and the 20-hire threshold are this repository's judgment. They are Draft and have not been validated in real engagements.
