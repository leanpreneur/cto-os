---
name: cto-day-one
description: Use when a CTO or engineering leader is starting a new role or taking over an engineering organization and needs a stage-aware 30/60/90 day plan, a listening tour agenda and a baseline metrics table. Interviews the user first, then produces the plan.
---

# cto-day-one

Produce a tailored first-90-days plan for a technical leader. Follow `references/first-90-days.md`, bundled with this skill. It is the source for the structure below.

## Step 1: Interview

Ask these questions in one message. Ask nothing else before the user answers. Accept partial answers.

1. Company stage (seed, series A or B, growth, turnaround) and approximate headcount, engineering headcount.
2. What the company sells, to whom, and how it earns revenue.
3. Current engineering structure: teams, managers, contractors, locations.
4. The CEO's top three outcomes for the next twelve months, in the CEO's words if known.
5. Known problems: incidents, delivery delays, attrition, customer escalations, security or compliance gaps.
6. Constraints: budget, hiring freeze, regulation, fixed deadlines, board commitments.
7. Start date and what access exists today: repositories, CI/CD, cloud billing, incident history, roadmap, board decks.
8. Your role: title, who you report to, decision rights over hiring, budget and architecture.

## Step 2: Gather evidence

If the user provides repositories, documents or exports, inspect them before planning:

- CI/CD configuration and deployment steps, to learn how a change reaches production.
- README, architecture notes, runbooks and incident records.
- Commit and pull request history, to estimate lead time and review habits.

Compute a metric only when the data supports it. Otherwise mark it **Unknown** and name the source that would supply it.

## Step 3: Produce the plan

Output exactly these sections, in this order, in two pages or fewer:

1. **Situation**: five bullet facts taken from the interview and evidence. Label anything assumed.
2. **Week 0 requests**: the written answers and access to obtain before day one.
3. **Days 1 to 30, Learn**: listening tour schedule with groups and the eight standard questions, system reading list, people observations to collect.
4. **Baseline metrics table**: deployment frequency, lead time for changes, change failure rate, time to restore, monthly cloud cost and trend, share of unplanned work, twelve-month attrition, open roles and time to fill, customer escalations. Columns: metric, value or Unknown, source, owner.
5. **Days 31 to 60, Decide**: at most three priorities, what will not be done, the operating cadence, and what to agree with the CEO.
6. **Days 61 to 90, Deliver**: one visible win, the first structural change, and the 90-day review outline.
7. **Risks and red flags**: ranked by likelihood and impact, each with an action.
8. **Questions for the CEO**: the five answers that most change the plan.

## Rules

- Use plain, direct language. No filler and no hedging.
- Do not invent numbers, names or facts. Mark unknowns as unknown.
- Match the plan to the company stage. A seed company does not need an org redesign. A turnaround needs stabilization before vision.
- Name an owner and a date for every action.
- Do not announce structural change before day 30 unless a security, data-loss or retention risk requires it. Say so explicitly when recommending an exception.
