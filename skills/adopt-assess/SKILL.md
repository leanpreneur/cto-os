---
name: adopt-assess
description: Use when an engineering leader wants to assess how far their organization has moved from AI tools to AI-native engineering, score it with the ADOPT framework (Align, Design, Orchestrate, Put guardrails, Transform) and get a prioritized plan. Interviews the user, inspects repositories and policy documents for evidence, scores five dimensions on a five-level maturity curve and produces a one-page summary.
---

# adopt-assess

Run the ADOPT assessment using `references/adopt-assessment.md`, bundled with this skill. Read it first. It holds the rubric, the constraint rule and the move guide. The framework comes from the essay at https://abbasraza.com/essays/from-copilot-to-autonomous-engineering/.

## Step 1: Scope

Ask in one message:

1. Organization size and engineering headcount.
2. Which AI tools are in use and since when.
3. Who owns AI adoption today, if anyone.
4. Whether the user can share repositories, policy documents, delivery metrics or survey results.
5. Who else can be interviewed.

Accept partial answers and continue.

## Step 2: Gather evidence

Inspect what the user provides before asking for opinions.

- Repository files that configure AI tools: `AGENTS.md`, `CLAUDE.md`, editor rules, skill folders.
- Pull request template, CODEOWNERS, review standards, CI configuration, and any AI review or generation steps.
- AI policy and acceptable-use documents.
- Metrics: deployment frequency, lead time for changes, change failure rate, time to restore, ticket-to-production cycle time, time in review, usage data, satisfaction scores.
- Incident records that mention AI-generated code.

Record each item with its source. If a source does not exist, record it as **Not found**. Do not guess.

## Step 3: Interview

If the user can answer for others, ask the ten questions in the playbook. Otherwise give the user the ten questions to put to two engineering leaders and four engineers separately, and wait for the answers.

## Step 4: Score

Score each of the five dimensions from 1 to 5 using the rubric table in the playbook.

- Score a level only when evidence supports every observable in that cell. Otherwise score one level lower and say what was missing.
- Quote or cite the evidence behind each score.
- Mark a score **Low confidence** when it rests on one interviewee or on opinion alone.
- Apply the constraint rule: overall level equals the lowest dimension score.
- Report the spread and the purgatory check (count of the six failure modes present).

## Step 5: Plan

Choose at most three moves for the quarter from the move guide, starting with the weakest dimension. Give each move an owner role, a date and a metric.

## Step 6: Produce the output

Output these sections, in this order, in one page or less:

1. **Result**: overall level, spread, purgatory check count, and one sentence on what it means.
2. **Scores**: table of dimension, score, evidence, confidence.
3. **Constraint**: the weakest dimension and why it limits the rest.
4. **Three moves**: owner, date, metric.
5. **Baseline metrics**: today's values, with unknowns marked **Unknown**.
6. **Risk if nothing changes**: one paragraph.

## Rules

- Use plain, direct language. No filler and no hedging.
- Never invent numbers, quotes or evidence. Mark unknowns as unknown.
- Attribute figures that appear in the essay to the essay, not to independent research.
- Say that the rubric extends the essay and has not yet been validated against real engagements.
- Do not recommend a tool or vendor. Recommend practices.
- Offer to reassess in two quarters and to store the scoring sheet beside the first one for comparison.
