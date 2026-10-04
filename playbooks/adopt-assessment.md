---
name: adopt-assessment
status: draft
author: Abbas Raza
source: https://abbasraza.com/essays/from-copilot-to-autonomous-engineering/
audience: CTO, VP Engineering or engineering leader rolling out AI-assisted development
---

# ADOPT Assessment: Where Is Your Engineering Organization on AI?

ADOPT is a framework for moving an engineering organization from AI tools to an AI-native way of building software. It was introduced in the essay [From Copilot to Autonomous Engineering](https://abbasraza.com/essays/from-copilot-to-autonomous-engineering/). This playbook turns the framework into an assessment you can run in two hours with evidence.

> **What comes from the essay and what is added here.** The five ADOPT dimensions, the five maturity levels, the three operating modes and the six failure modes come from the essay. The dimension-by-level rubric, the constraint rule and the move guide are extensions built for this repository. They are Draft until applied in a real engagement.

## The premise

AI does not fix a software development lifecycle. It exposes it. When coding gets faster, review, testing, release and coordination become the bottleneck. An organization that adds copilots without changing how work flows tends to land in what the essay calls **AI pilot purgatory**: copilots available but inconsistently used, marginal or invisible gains, teams reverting to old habits under pressure, and leadership questioning the return.

## The five dimensions

| Letter | Dimension | The question it answers |
| --- | --- | --- |
| A | Align on outcomes, not tools | What are we optimizing, and how do we measure it? |
| D | Design an AI-native SDLC | Has the whole lifecycle been redesigned, or only the coding step? |
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

## Run the assessment

### Step 1: Collect evidence (one to two hours)

Gather what exists, not what people believe exists.

- Written AI policy, acceptable-use rules, data handling rules.
- Repository files that configure AI tools, such as `AGENTS.md`, `CLAUDE.md` or editor rules.
- Pull request template, review standards and CI configuration, including any AI review steps.
- Seat counts and usage data from AI tool vendors.
- Delivery metrics: deployment frequency, lead time for changes, change failure rate, time to restore, and time from ticket creation to production.
- Time-in-review data and the share of senior engineer time spent reviewing.
- Engineer survey or satisfaction score, if one exists.
- Incident records that involved AI-generated code.

### Step 2: Ask ten questions

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

### Step 3: Score each dimension from 1 to 5

Score a dimension at a level only when you have evidence for **every** observable in that cell. If evidence is missing, score one level lower and note it.

| Dimension | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
| --- | --- | --- | --- | --- | --- |
| **A. Align on outcomes** | No stated goal. Success judged by anecdote. | Goal is adoption (seats, usage). No link to delivery outcomes. | Written outcome targets tied to delivery (for example cycle time, review time, deployment frequency) with baselines, tracked monthly. | Targets set per workflow, including agent-completed work. Cost per merged change tracked. | Leaders set intent and quality standards. Results reviewed against customer, reliability and financial outcomes. |
| **D. Design an AI-native SDLC** | Lifecycle unchanged. Individuals use tools ad hoc. | Coding is faster. Requirements, review, testing and release are unchanged. | Lifecycle mapped stage by stage. AI embedded in requirements, design, review and testing. Downstream bottlenecks identified and managed. A workflow document exists. | Agents run multi-step tasks inside the workflow, from specification to pull request. Humans review at defined gates. Cycle time compression is measured. | Work flows from intent to production through the system with human supervision at policy gates. The workflow is tuned continuously from telemetry. |
| **O. Orchestrate roles** | No agreement on what AI may do. Each person decides. | Informal norms. Engineers still own every line. Roles unchanged. | The three operating modes are defined and assigned to task types. Role descriptions updated toward problem framing, design and evaluation. | Humans direct and review agent work. Reviewers are trained to evaluate. Ownership of agent output is named. | Humans define intent and standards and supervise. Engineers are evaluated as orchestrators. Every agent has a named owner. |
| **P. Put guardrails in place** | No policy. Data handling unclear. | Basic acceptable-use policy. AI code gets the same review as human code. No AI-specific checks. | Review standards for AI output. Security and compliance checks tuned for AI failure patterns. AI-generated changes are traceable. Test requirements calibrated to velocity. | Agent permissions are scoped and logged. Automated gates block unsafe changes. Agent actions are audited. Incident process covers AI faults. | Policy is enforced as code across the system. Audit is continuous. Evidence can be shown to customers and regulators on request. |
| **T. Transform culture and skills** | Self-taught. Skepticism or fear unaddressed. | Tool training at rollout. No shared practice. Trust gaps unmanaged. | Prompting and output verification taught as shared skills, for example regular prompt clinics. A change management plan exists. Incentives reward outcomes, not effort. | Engineers practice orchestration: decomposing work for agents and reviewing agent output. Practitioners maintain internal playbooks. Hiring and leveling reflect the new skills. | A continuous learning loop is in place. Engineers work at the level of intent and quality standards. The organization rewards system outcomes. |

### Step 4: Apply the constraint rule

**Overall level equals the lowest dimension score.** The essay's logic is that when one stage speeds up, the slowest stage becomes the limit. The same holds across dimensions: a Level 4 workflow with Level 2 guardrails is a Level 2 organization, and the gap is a risk.

Report three things:

1. Overall level.
2. Spread: the highest score minus the lowest. A spread of two or more means the program is unbalanced.
3. **Purgatory check.** Count how many of the six failure modes below are present. Two or more means the organization is in AI pilot purgatory regardless of score.

### The six failure modes

1. Copilots rolled out without changing workflows.
2. Coding sped up while every other stage stays slow.
3. AI made optional instead of the default.
4. No skill development on effective use.
5. Trust gaps in AI output left unaddressed.
6. No measurable success targets.

### Step 5: Pick the next moves

Choose moves for the weakest dimension first. Limit the plan to three moves per quarter.

**Level 1 to 2: get everyone on the same footing**
- Standardize on one or two approved tools and publish acceptable-use rules.
- Provide tool training to every engineer.
- Record a baseline for delivery metrics before changing anything.

**Level 2 to 3: where most organizations need to go**
- Write three outcome targets with baselines (A).
- Map the lifecycle, measure where time goes, and write the redesigned workflow (D).
- Assign AI-First, Human-in-Loop and Human-Only modes to task types (O).
- Write review standards for AI-generated code and add AI-specific security checks (P).
- Run a monthly prompt clinic and make AI the default for routine tasks (T).

**Level 3 to 4: add autonomy with control**
- Pilot agents on one workflow with scoped permissions and logging (D, P).
- Train reviewers to evaluate agent output, not only read diffs (T).
- Name an owner for every agent and every agent workflow (O).

**Level 4 to 5: supervise the system**
- Encode policy as automated gates and run continuous audit (P).
- Report AI cost and output against business results (A).
- Move engineer evaluation to intent, quality and system outcomes (T).

## Scoring sheet

| Dimension | Score (1 to 5) | Evidence seen | Evidence missing | Confidence | Next move |
| --- | --- | --- | --- | --- | --- |
| A. Align on outcomes | | | | | |
| D. Design an AI-native SDLC | | | | | |
| O. Orchestrate roles | | | | | |
| P. Put guardrails in place | | | | | |
| T. Transform culture and skills | | | | | |

Overall level: ___  Spread: ___  Purgatory check (count of six): ___

## One-page output for the CEO

1. Overall level and one sentence on what it means.
2. The weakest dimension and why it limits the rest.
3. The three moves for this quarter, each with an owner and a date.
4. The two metrics that will show progress, with today's baseline.
5. The main risk if nothing changes.

## Definition of done

- Every score cites evidence.
- Two leaders and four engineers were interviewed separately.
- The CEO has the one-page output.
- The moves have owners and dates.

## How you will know it worked

- Leading indicator: the share of routine tasks run in AI-First mode, and the share of AI-generated changes that are traceable.
- Lagging indicator: cycle time from ticket creation to production, and engineer satisfaction, both against the baseline you recorded in Step 1.

Reassess every two quarters. Compare scores and keep the old sheet.
