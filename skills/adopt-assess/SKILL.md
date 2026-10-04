---
name: adopt-assess
description: Use when an engineering leader wants to assess how far their organization has moved from AI tools to AI-native engineering, score it with the ADOPT framework (Align, Design, Orchestrate, Put guardrails, Transform) and get a prioritized plan. Interviews the user, inspects repositories and policy documents for evidence, checks seven foundations, scores five dimensions on a five-level maturity curve and produces a one-page summary.
---

# adopt-assess

Run the ADOPT assessment using `references/adopt-assessment.md`, bundled with this skill. Read it first. It holds the foundations gate, the context practice, the rubric, the constraint rule and the move guide. The framework comes from the essay at https://abbasraza.com/essays/from-copilot-to-autonomous-engineering/. The seven foundation capabilities come from DORA's AI Capabilities Model.

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

- Repository files that configure AI tools: `AGENTS.md`, `CLAUDE.md`, editor rules, skill folders. Count how many repositories have one.
- Pull request template, CODEOWNERS, review standards, CI configuration, and any AI review or generation steps.
- AI policy and acceptable-use documents.
- Metrics: deployment frequency, lead time for changes, change failure rate, time to restore, ticket-to-production cycle time, time in review, usage data, satisfaction scores.
- Incident records that mention AI-generated code.

For the foundations check, also look for:

- Median pull request size, branch age, commit frequency and revert history for the last 90 days.
- Where decisions, runbooks and conventions live, with last-updated dates for a sample of ten.
- How the AI tools connect to internal data (repositories, docs, tickets).
- Time for a new engineer to reach a first production change.
- Ten recent shipped changes and the user problem each traces to.

Record each item with its source. If a source does not exist, record it as **Not found**. Do not guess.

## Step 3: Interview

If the user can answer for others, ask the eleven questions in the playbook. Otherwise give the user the eleven questions to put to two engineering leaders and four engineers separately, and wait for the answers.

## Step 4: Check the foundations

Before scoring any dimension, rate each of the seven capabilities Present, Partial or Absent using the "Present when you can show" column in the playbook.

- Present only when every item has evidence. Partial when some do. Absent when none, or when no evidence was found.
- Treat **Unknown** as Absent for the ceiling, and say so in the output.
- Read the ceiling from the playbook's ceiling rule.
- For the small-batch capability, ask the user for the threshold their team uses. If there is none, use the playbook's default and state that the default is the repository's, not DORA's.

## Step 5: Score the dimensions

Score each of the five dimensions from 1 to 5 using the rubric table in the playbook. Context is part of the D row. Check the instruction files, decision records and runbooks before scoring D.

- Score a level only when evidence supports every observable in that cell. Otherwise score one level lower and say what was missing.
- Quote or cite the evidence behind each score.
- Mark a score **Low confidence** when it rests on one interviewee or on opinion alone.
- Apply the constraint rule: overall level is the lower of the lowest dimension score and the foundations ceiling.
- Report what binds the overall level, the spread and the purgatory check (count of the six failure modes present).

## Step 6: Plan

Choose at most three moves for the quarter, starting with the binding constraint. If the foundations ceiling is below the lowest dimension score, take the moves from the foundations table in the playbook. Give each move an owner role, a date and a metric.

## Step 7: Produce the output

Output these sections, in this order, in one page or less:

1. **Result**: overall level, what binds it, spread, purgatory check count, and one sentence on what it means.
2. **Foundations**: seven rows, each with the capability, the rating and one line of evidence. State the ceiling.
3. **Scores**: table of dimension, score, evidence, confidence.
4. **Constraint**: the weakest dimension or foundation and why it limits the rest.
5. **Three moves**: owner, date, metric.
6. **Baseline metrics**: today's values, with unknowns marked **Unknown**.
7. **Risk if nothing changes**: one paragraph.

## Rules

- Use plain, direct language. No filler and no hedging.
- Never invent numbers, quotes or evidence. Mark unknowns as unknown.
- Attribute figures that appear in the essay to the essay, not to independent research.
- Attribute the names of the seven capabilities to DORA. Say that the evidence tests, the level each capability gates and the ceiling rule are this repository's extensions.
- Say that the rubric, the foundations gate and the context practice extend the essay and have not yet been validated against real engagements.
- Do not recommend a tool or vendor. Recommend practices.
- Offer to reassess in two quarters and to store the scoring sheet beside the first one for comparison.
