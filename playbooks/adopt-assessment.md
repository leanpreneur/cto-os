---
name: adopt-assessment
status: draft
author: Abbas Raza
source: https://abbasraza.com/essays/from-copilot-to-autonomous-engineering/
audience: CTO, VP Engineering or engineering leader rolling out AI-assisted development
---

# ADOPT Assessment: Where Is Your Engineering Organization on AI?

ADOPT is a framework for moving an engineering organization from AI tools to an AI-native way of building software. It was introduced in the essay [From Copilot to Autonomous Engineering](https://abbasraza.com/essays/from-copilot-to-autonomous-engineering/). This playbook turns the framework into an assessment you can run in two hours with evidence.

> **What comes from the essay and what is added here.** The five ADOPT dimensions, the five maturity levels, the three operating modes and the six failure modes come from the essay. The dimension-by-level rubric, the constraint rule, the move guide, the foundations gate and the context practice are extensions built for this repository. The seven foundation capabilities are named by DORA (see [Sources](#sources)). How they map to ADOPT levels is this repository's judgment. All extensions are Draft until applied in a real engagement.

## The premise

AI does not fix a software development lifecycle. It exposes it. When coding gets faster, review, testing, release and coordination become the bottleneck. An organization that adds copilots without changing how work flows tends to land in what the essay calls **AI pilot purgatory**: copilots available but inconsistently used, marginal or invisible gains, teams reverting to old habits under pressure, and leadership questioning the return.

## The five dimensions

| Letter | Dimension | The question it answers |
| --- | --- | --- |
| A | Align on outcomes, not tools | What are we optimizing, and how do we measure it? |
| D | Design an AI-native SDLC | Has the whole lifecycle been redesigned, or only the coding step? Does the AI have the context it needs? |
| O | Orchestrate human and AI roles | Who owns what, and when does AI act, assist or stay out? |
| P | Put guardrails in place | What makes acceleration safe at scale? |
| T | Transform culture and skills | Can people use, verify and direct AI well? |

### Operating modes (dimension O)

| Mode | Definition | Typical work |
| --- | --- | --- |
| AI-First | AI drafts, a human approves in under two minutes. Default for routine tasks. | Boilerplate, test generation, documentation |
| Human-in-Loop | AI assists, the human drives. Used when judgment is required. | Feature implementation, architecture decisions |
| Human-Only | AI is not involved. | Security-sensitive logic, production incidents, customer data handling |

## The five maturity levels

| Level | Name | Description |
| --- | --- | --- |
| 1 | Experimentation | Ad hoc AI use by individuals. No coordination, measurement or workflow change. |
| 2 | Assisted Development | Copilots broadly adopted. Engineers are faster in isolation, but the SDLC has not changed. |
| 3 | Integrated AI SDLC | AI is embedded across the lifecycle. Bottlenecks are managed. Metrics are defined and tracked. |
| 4 | Agentic Engineering | AI executes multi-step tasks. Humans review and direct. Cycle time compresses significantly. |
| 5 | Autonomous Software Factory | Humans supervise and AI builds. Leaders define intent and quality standards and the system executes. |

The essay states that most organizations today sit at Level 1 or Level 2, and that Level 3 is where real productivity gains become visible.

## Foundations: the gate before the scores

The five dimensions measure what you have built for AI. The foundations measure whether the organization underneath can carry it. DORA's AI Capabilities Model names seven organizational capabilities that increase the impact of AI-assisted development. ADOPT uses them as a gate. They set the highest level an organization can reach, however well the five dimensions score. A strong workflow on weak foundations produces faster code that lands in a system that cannot absorb it.

| # | Capability (DORA) | Gates | Present when you can show |
| --- | --- | --- | --- |
| 1 | Clear and communicated AI stance | Level 3 | A written position on expected AI use, permitted tools and support for experimentation, and engineers can describe it unprompted in interviews. |
| 4 | Strong version control practices | Level 3 | Protected main branch, frequent commits, short-lived branches, and a revert or rollback path that has been used in the last 90 days. |
| 5 | Working in small batches | Level 3 | Pull request size and release size are tracked, the median is under the threshold the team set before looking at data, and work is split at planning. |
| 2 | Healthy data ecosystems | Level 4 | Internal knowledge (docs, decisions, runbooks, schemas, tickets) lives in a small number of known places, has named owners, and a sample of ten items shows most were updated in the last 12 months. |
| 3 | AI-accessible internal data | Level 4 | Approved AI tools are connected to repositories, docs and tickets, and an engineer can ask the tool about an internal system and get an answer grounded in your sources. |
| 7 | Quality internal platforms | Level 4 | Self-service paths for build, test, environments and deploy, a named platform owner, and a measured time for a new engineer to reach a first production change. |
| 6 | User-centric focus | Level 5 | Teams can name their users, shipped work traces to a user problem, and user feedback reaches the team on a fixed cadence. Check ten recent shipped changes. |

The numbers follow DORA's list. The table is ordered by the level each capability gates.

### Rate each capability

- **Present**: every item in the "Present when you can show" cell has evidence.
- **Partial**: some items have evidence.
- **Absent**: no evidence, or the evidence was not found. **Unknown counts as Absent** until measured.

On the small-batch threshold: agree it with the team before you look at the data. If you have no number, use a median pull request under 400 changed lines as a starting default. That default is this repository's, not DORA's. Change it to fit your stack.

### The ceiling rule

| Foundations state | Ceiling on overall level |
| --- | --- |
| Any of capabilities 1, 4 or 5 is not Present | Level 2 |
| 1, 4 and 5 Present, and any of 2, 3 or 7 is not Present | Level 3 |
| 1 to 5 and 7 Present, and 6 is not Present | Level 4 |
| All seven Present | Level 5 |

Why these lines. Level 3 puts AI across the lifecycle at a speed the team must be able to review, roll back and absorb in small pieces. Level 4 asks agents to do multi-step work, which needs company context they can reach and a platform to run on. Level 5 puts intent in the hands of leaders, which needs a firm grip on the user's problem. DORA does not define these gates. The mapping is judgment and has not been validated.

## The context practice

Context is the written knowledge an engineer or an AI agent needs to change your system correctly: how to build and test it, the conventions, the boundaries, the architecture decisions and the domain rules. Without it, every person re-explains the system to the tool every time, and agents guess.

ADOPT treats context as an explicit practice inside dimension D, because it is the part of lifecycle redesign that most teams skip. It is scored in D, owned under O (a named owner) and kept safe under P (no secrets or customer data in context files).

How it differs from foundations 2 and 3: the foundations ask whether the knowledge exists and the tools can reach it. The context practice asks whether the team writes it for AI use, keeps it current and checks it inside the workflow.

| Level | What context looks like |
| --- | --- |
| 1 | None. Each person explains the system to the tool from scratch. |
| 2 | Personal instruction files in some repositories. No shared standard. |
| 3 | Shared standard. Every repository has an instruction file. Decisions and runbooks are findable. A named owner keeps them current, and review checks them. |
| 4 | Instruction files and decision records are versioned and loaded by agents automatically. Every agent failure caused by missing context is logged and fixed. |
| 5 | Coverage and freshness of context are measured. Agent failures are traced to context defects and fixed by the system with human approval. |

**Minimum context for a repository**

- Purpose and boundaries of the service.
- Commands to build, test and run it.
- Conventions and patterns to follow.
- Areas not to touch without a human (security logic, data migrations, generated code).
- Where decisions and runbooks live.
- Who to ask.

## Run the assessment

### Step 1: Collect evidence (one to two hours)

Gather what exists, not what people believe exists.

- Written AI policy, acceptable-use rules, data handling rules.
- Repository files that configure AI tools, such as `AGENTS.md`, `CLAUDE.md` or editor rules, and how many repositories have one.
- Pull request template, review standards and CI configuration, including any AI review steps.
- Seat counts and usage data from AI tool vendors.
- Delivery metrics: deployment frequency, lead time for changes, change failure rate, time to restore, and time from ticket creation to production.
- Time-in-review data and the share of senior engineer time spent reviewing.
- Engineer survey or satisfaction score, if one exists.
- Incident records that involved AI-generated code.

For the foundations check, also gather:

- Median pull request size, branch age, commit frequency and revert history for the last 90 days.
- Where decisions, runbooks and conventions live, with last-updated dates for a sample of ten.
- How the AI tools connect to internal data (repositories, docs, tickets).
- The time for a new engineer to reach a first production change.
- Ten recent shipped changes and the user problem each one traces to.

### Step 2: Ask eleven questions

Put the same questions to two engineering leaders and four engineers separately. Compare the answers.

1. What outcome are we trying to improve with AI, and how do we know it moved? (A)
2. Which stages of our lifecycle changed because of AI, apart from writing code? (D)
3. Where did the bottleneck move after AI sped up coding? (D)
4. Which tasks must AI never do here, and who decided? (O)
5. Which tasks is AI expected to start by default? (O)
6. How is AI-generated code reviewed differently from human code? (P)
7. Can we trace which changes were AI-generated? (P)
8. What happened the last time AI output was wrong in production? (P)
9. How did you learn to use these tools well, and who teaches it? (T)
10. How much do you trust the output, and what do you check before you merge? (T)
11. What does a new engineer, or an AI agent, need to read before changing this system safely, and who keeps it current? (D)

### Step 3: Check the foundations

Rate each of the seven capabilities Present, Partial or Absent, with the evidence behind each rating. Read off the ceiling from the ceiling rule. Do this before scoring the dimensions, so the ceiling is not influenced by how good the workflow looks.

### Step 4: Score each dimension from 1 to 5

Score a dimension at a level only when you have evidence for **every** observable in that cell. If evidence is missing, score one level lower and note it. The context practice is part of the D row.

| Dimension | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
| --- | --- | --- | --- | --- | --- |
| **A. Align on outcomes** | No stated goal. Success judged by anecdote. | Goal is adoption (seats, usage). No link to delivery outcomes. | Written outcome targets tied to delivery (for example cycle time, review time, deployment frequency) with baselines, tracked monthly. | Targets set per workflow, including agent-completed work. Cost per merged change tracked. | Leaders set intent and quality standards. Results reviewed against customer, reliability and financial outcomes. |
| **D. Design an AI-native SDLC** | Lifecycle unchanged. Individuals use tools ad hoc. Context: each person explains the system to the tool from scratch. | Coding is faster. Requirements, review, testing and release are unchanged. Context: personal instruction files in some repositories, no shared standard. | Lifecycle mapped stage by stage. AI embedded in requirements, design, review and testing. Downstream bottlenecks identified and managed. A workflow document exists. Context: every repository has an instruction file with build and test commands, conventions and boundaries. Decisions and runbooks are findable and a named owner keeps them current. | Agents run multi-step tasks inside the workflow, from specification to pull request. Humans review at defined gates. Cycle time compression is measured. Context: instruction files and decision records are versioned and loaded by agents automatically. Agent failures caused by missing context are logged and fixed. | Work flows from intent to production through the system with human supervision at policy gates. The workflow is tuned continuously from telemetry. Context: coverage and freshness are measured, and agent failures are traced to context defects and fixed with human approval. |
| **O. Orchestrate roles** | No agreement on what AI may do. Each person decides. | Informal norms. Engineers still own every line. Roles unchanged. | The three operating modes are defined and assigned to task types. Role descriptions updated toward problem framing, design and evaluation. Shared context has a named owner. | Humans direct and review agent work. Reviewers are trained to evaluate. Ownership of agent output is named. | Humans define intent and standards and supervise. Engineers are evaluated as orchestrators. Every agent has a named owner. |
| **P. Put guardrails in place** | No policy. Data handling unclear. | Basic acceptable-use policy. AI code gets the same review as human code. No AI-specific checks. | Review standards for AI output. Security and compliance checks tuned for AI failure patterns. AI-generated changes are traceable. Test requirements calibrated to velocity. Context files and connected data sources are checked for secrets and customer data. | Agent permissions are scoped and logged. Automated gates block unsafe changes. Agent actions are audited. Incident process covers AI faults. | Policy is enforced as code across the system. Audit is continuous. Evidence can be shown to customers and regulators on request. |
| **T. Transform culture and skills** | Self-taught. Skepticism or fear unaddressed. | Tool training at rollout. No shared practice. Trust gaps unmanaged. | Prompting and output verification taught as shared skills, for example regular prompt clinics. A change management plan exists. Incentives reward outcomes, not effort. | Engineers practice orchestration: decomposing work for agents and reviewing agent output. Practitioners maintain internal playbooks. Hiring and leveling reflect the new skills. | A continuous learning loop is in place. Engineers work at the level of intent and quality standards. The organization rewards system outcomes. |

### Step 5: Apply the constraint rule

**Overall level equals the lower of two numbers: the lowest dimension score and the foundations ceiling.** The essay's logic is that when one stage speeds up, the slowest stage becomes the limit. The same holds across dimensions: a Level 4 workflow with Level 2 guardrails is a Level 2 organization, and the gap is a risk. It also holds below the dimensions: a Level 4 workflow on Level 2 foundations is a Level 2 organization.

Report four things:

1. Overall level, and what binds it: a named dimension or the foundations.
2. Foundations ceiling, with the capabilities that are not Present.
3. Spread: the highest dimension score minus the lowest. A spread of two or more means the program is unbalanced.
4. **Purgatory check.** Count how many of the six failure modes below are present. Two or more means the organization is in AI pilot purgatory regardless of score.

### The six failure modes

1. Copilots rolled out without changing workflows.
2. Coding sped up while every other stage stays slow.
3. AI made optional instead of the default.
4. No skill development on effective use.
5. Trust gaps in AI output left unaddressed.
6. No measurable success targets.

### Step 6: Pick the next moves

Choose moves for the binding constraint first. If the foundations ceiling is below the lowest dimension score, the foundations bind, and the moves come from the foundations table below. Limit the plan to three moves per quarter.

**Fix a foundation**

| Capability not Present | First move |
| --- | --- |
| 1. AI stance | Publish a one-page stance: what is expected, which tools are permitted, what is off-limits, how to ask for an exception. Each manager walks their team through it. |
| 2. Healthy data | Name an owner for engineering knowledge, choose one home for decisions and runbooks, and archive the stale ones. |
| 3. AI-accessible data | Connect approved AI tools to repositories, docs and tickets with read-only scope first. |
| 4. Version control | Protect main, require pull requests, set a maximum branch age, and rehearse a revert. |
| 5. Small batches | Set a pull request size guideline, track the median, and split work at planning. |
| 6. User focus | Add a user-problem field to the work-item template and review user feedback on a fixed cadence. |
| 7. Platform | Time a new engineer from laptop to deployed change, remove the slowest step, and name a platform owner. |

**Level 1 to 2: get everyone on the same footing**
- Standardize on one or two approved tools and publish acceptable-use rules.
- Provide tool training to every engineer.
- Record a baseline for delivery metrics before changing anything.

**Level 2 to 3: where most organizations need to go**
- Write three outcome targets with baselines (A).
- Map the lifecycle, measure where time goes, and write the redesigned workflow (D).
- Add an instruction file to every repository and name an owner for shared context (D, O).
- Assign AI-First, Human-in-Loop and Human-Only modes to task types (O).
- Write review standards for AI-generated code and add AI-specific security checks (P).
- Run a monthly prompt clinic and make AI the default for routine tasks (T).

**Level 3 to 4: add autonomy with control**
- Pilot agents on one workflow with scoped permissions and logging (D, P).
- Log every agent failure caused by missing context and fix the context (D).
- Train reviewers to evaluate agent output, not only read diffs (T).
- Name an owner for every agent and every agent workflow (O).

**Level 4 to 5: supervise the system**
- Encode policy as automated gates and run continuous audit (P).
- Measure context coverage and freshness (D).
- Report AI cost and output against business results (A).
- Move engineer evaluation to intent, quality and system outcomes (T).

## Scoring sheet

**Foundations**

| # | Capability | Present, Partial or Absent | Evidence seen | Evidence missing |
| --- | --- | --- | --- | --- |
| 1 | Clear and communicated AI stance | | | |
| 2 | Healthy data ecosystems | | | |
| 3 | AI-accessible internal data | | | |
| 4 | Strong version control practices | | | |
| 5 | Working in small batches | | | |
| 6 | User-centric focus | | | |
| 7 | Quality internal platforms | | | |

Foundations ceiling: ___

**Dimensions**

| Dimension | Score (1 to 5) | Evidence seen | Evidence missing | Confidence | Next move |
| --- | --- | --- | --- | --- | --- |
| A. Align on outcomes | | | | | |
| D. Design an AI-native SDLC (including context) | | | | | |
| O. Orchestrate roles | | | | | |
| P. Put guardrails in place | | | | | |
| T. Transform culture and skills | | | | | |

Lowest dimension: ___  Overall level (lower of that and the ceiling): ___  Binding constraint: ___  Spread: ___  Purgatory check (count of six): ___

## One-page output for the CEO

1. Overall level, what binds it (a dimension or the foundations), and one sentence on what it means.
2. The weakest dimension or foundation and why it limits the rest.
3. The three moves for this quarter, each with an owner and a date.
4. The two metrics that will show progress, with today's baseline.
5. The main risk if nothing changes.

## Definition of done

- Every score and every foundation rating cites evidence.
- Unknowns are marked, and counted as Absent for the ceiling.
- Two leaders and four engineers were interviewed separately.
- The CEO has the one-page output.
- The moves have owners and dates.

## How you will know it worked

- Leading indicator: the share of routine tasks run in AI-First mode, the share of AI-generated changes that are traceable, and the share of repositories with a current instruction file.
- Lagging indicator: cycle time from ticket creation to production, and engineer satisfaction, both against the baseline you recorded in Step 1.

Reassess every two quarters. Compare scores and keep the old sheet.

## Sources

- [From Copilot to Autonomous Engineering](https://abbasraza.com/essays/from-copilot-to-autonomous-engineering/), Abbas Raza. Source of the five dimensions, five levels, three modes and six failure modes.
- [Introducing DORA's inaugural AI Capabilities Model](https://cloud.google.com/blog/products/ai-machine-learning/introducing-doras-inaugural-ai-capabilities-model), Kevin M. Storer and Derek DeBellis, Google Cloud, 23 September 2025. Source of the names and descriptions of the seven capabilities. The "Present when you can show" evidence tests, the level each capability gates and the ceiling rule are this repository's extensions. They are not part of DORA's model and have not been validated. The capability names were taken from the blog post, not from the full DORA report.
