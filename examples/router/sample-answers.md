# Example: router answers

**Made by:** written by hand, to show the format `/ask-cto-os` uses. These are not recorded sessions. The user messages are invented. The routes come from `skills/ask-cto-os/references/routes.json`. Each answer stays under 150 words.

## 1. A new role

**User:** I start as CTO in two weeks and I need a plan for my first three months.

**Your situation:** New CTO, starting in two weeks, needs a three-month plan.

**Start with:** `/cto-day-one`. It interviews you about the company and writes the plan for your stage and constraints, so it is not a generic template.

**You will get:** A tailored 30, 60 and 90 day plan, a listening tour agenda and a baseline metrics table.

**Then:** `/eng-audit` to fill the metrics table from git history once you have repository access. `/ceo-alignment` to settle decision rights with the CEO before the plan is signed.

**To start I need:** The company stage, and how many engineers there are.

Say go and I will run it.

## 2. A hiring problem

**User:** Our last three hires did not work out, and every interviewer asks different questions.

**Your situation:** Inconsistent interviews and recent hires that did not work out.

**Start with:** `/hiring-plan`. It writes a role scorecard, builds a loop where every competency has two independent interviewers, and gives each interviewer the same questions and rubric.

**You will get:** A role scorecard, an interview loop checked for coverage, questions with rubrics, a work sample and a candidate message.

**Then:** `/leveling-ladder`, if you have no written ladder. The scorecard needs a level to test against.

**To start I need:** The role and level, and who can interview.

Say go and I will run it.

## 3. A topic CTO OS does not cover

**User:** We had a bad outage last night. I need a postmortem process.

CTO OS does not cover incident response or blameless postmortems yet. There is no close match in the table, so I will not point you to an artifact that does not fit.

I can still help you write a blameless postmortem template and a basic incident process here. That would be ordinary help, not a CTO OS artifact. Want me to start with the postmortem template?
