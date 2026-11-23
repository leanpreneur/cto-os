---
name: leveling-ladder
status: early
use: starter engineering ladder to adapt, then publish. Written for this repository, not copied from another ladder.
---

# Engineering Leveling Ladder

How to use it:

1. Pick the levels you need from the table in the [leveling playbook](../playbooks/leveling.md).
2. Replace the examples with facts from your company, and delete sentences that do not apply.
3. Test it. Have two managers place three real engineers on it alone. Rewrite any sentence that let them disagree.
4. Add pay bands. Publish it. Train the managers.

Levels describe scope and behavior. They do not describe years of experience. A person does not need every sentence at a level. They need the pattern, sustained over at least two quarters.

## Levels at a glance

| Level | Typical title | Owns | Works mostly with |
| --- | --- | --- | --- |
| E1 | Junior Engineer | A task or small feature | Their team |
| E2 | Engineer | A feature end to end | Their team |
| E3 | Senior Engineer | A system or a multi-month project | Their team and adjacent teams |
| E4 | Staff Engineer | A problem across several teams, or a domain | Several teams and managers |
| E5 | Senior Staff Engineer | A major technical area, for a year or more | Directors |
| E6 | Principal Engineer | Company-wide technical direction | VPs and the CEO |
| M1 | Engineering Manager | One team of 4 to 8 | Product, peers |
| M2 | Senior Engineering Manager | A large team or two teams | Product leaders, other managers |
| M3 | Director | An area, through managers | VPs, finance |
| M4 | VP or Head of Engineering | The engineering function | The CEO and the board |

## Individual contributor track

### E1 Junior Engineer

- **Scope:** A task or a small feature inside one component.
- **Ambiguity:** Requirements and approach are given. Asks for help within a day of being stuck.
- **Delivery:** Finishes assigned work, with review, by the agreed date. Raises a slip when it first appears.
- **Craft:** Writes readable, tested code that follows team conventions. Learns the codebase and the path to production.
- **Influence:** Gives clear status and names blockers. Applies feedback without being told twice.
- **Engineering with AI:** Uses AI tools on assigned tasks. Reads and understands every line before submitting. Checks output against tests.

### E2 Engineer

- **Scope:** A feature end to end inside one team's system.
- **Ambiguity:** The goal is given. Chooses the approach and checks it with a peer.
- **Delivery:** Plans their own work in small pieces and ships predictably without daily guidance.
- **Craft:** Designs a component. Debugs production issues with limited help. Writes tests that catch real faults.
- **Influence:** Gives code review that improves the change. Documents what they build.
- **Engineering with AI:** Decides when to use AI tools and when not to. Writes tests and specifications that constrain the output. Catches the tool's mistakes in review.

### E3 Senior Engineer

- **Scope:** A system, or a project of several months across a team.
- **Ambiguity:** Turns a goal or a customer problem into a plan. Names risks early.
- **Delivery:** Delivers projects with several people. Reports slips with options, early. Owns the result after launch.
- **Craft:** Designs systems that others can extend. Sets the bar in code and design review. Teaches.
- **Influence:** Mentors E1 and E2 engineers. Shapes scope with product and design. Unblocks teammates without being asked.
- **Engineering with AI:** Sets the practices for their area: what context to give the tool, what to review, what not to delegate. Owns what ships, whoever or whatever wrote it.

### E4 Staff Engineer

- **Scope:** A problem that spans several teams, or a technical domain such as data, platform or security.
- **Ambiguity:** Finds the problem worth solving and writes it down so others agree on it.
- **Delivery:** Lands cross-team outcomes through other people. Makes trade-offs visible to leaders.
- **Craft:** Sets technical direction for a domain. Writes designs and decision records that teams follow.
- **Influence:** Aligns teams and leaders without authority. Sponsors E3 engineers.
- **Engineering with AI:** Shapes how several teams use AI. Ties adoption to measured results such as change size, review time and failure rate, not to tool usage.

### E5 Senior Staff Engineer

- **Scope:** A problem that shapes a major part of the company's technology over a year or more.
- **Ambiguity:** Sets technical strategy for an area with a director or VP. Decides what not to build.
- **Delivery:** Results show up in company metrics and last after the person moves on.
- **Craft:** Known inside and outside the company for judgment. Settles technical disputes that other staff engineers cannot.
- **Influence:** Partner to directors. Grows staff engineers.
- **Engineering with AI:** Defines the guardrails and the measures for AI-assisted work across engineering. Advises the CTO on risk.

### E6 Principal Engineer

- **Scope:** Company-wide technical direction, with decisions that stand for years.
- **Ambiguity:** Works on problems nobody has framed yet. Reads the technology, the market and the business together.
- **Delivery:** Company-level results: cost, reliability, speed, or a new product line.
- **Craft:** Sets the standard for engineering judgment across the company.
- **Influence:** A peer of VPs. The CEO and the board rely on them for technical risk.
- **Engineering with AI:** Shapes the company's position on AI, in its product and in how it builds.

## Manager track

### M1 Engineering Manager

- **Scope:** One team of 4 to 8 engineers.
- **Ambiguity:** Turns a quarterly goal into a team plan.
- **Delivery:** The team meets its commitments, and stakeholders hear early when it will not.
- **People and craft:** Hires, onboards and gives feedback every week. Deals with underperformance in the first month. Knows the code well enough to judge a design.
- **Influence:** Works with product and peer managers. Resolves conflicts inside the team.
- **Engineering with AI:** Sets team norms for AI use. Watches change size, review time and quality, not tool usage.

### M2 Senior Engineering Manager

- **Scope:** A large or complex team, or two teams.
- **Ambiguity:** Decides how a roadmap area is split between teams.
- **Delivery:** Delivers a roadmap area across teams and manages dependencies before they block.
- **People and craft:** Develops tech leads and new managers. Handles the hard hiring and the hard exits.
- **Influence:** Represents engineering with product leaders. Trades off between teams openly.
- **Engineering with AI:** Standardizes AI practices across their teams and removes blockers such as access, data rules and review load.

### M3 Director

- **Scope:** An area of two to five teams, through managers.
- **Ambiguity:** Sets the plan for the area from company goals and says what the area will not do.
- **Delivery:** Owns the area's results, budget and risks. Reports them in terms the CEO uses.
- **People and craft:** Chooses, coaches and when needed replaces managers. Designs the structure of the area.
- **Influence:** Partner to product, finance and the other directors. Resolves cross-team conflicts.
- **Engineering with AI:** Funds and measures AI adoption in the area against outcomes. Owns the area's AI risk.

### M4 VP or Head of Engineering

- **Scope:** The engineering function.
- **Ambiguity:** Sets engineering strategy with the CEO. Works on problems the company has not yet named.
- **Delivery:** Owns the function's results, cost and risk, and tells the board where they stand.
- **People and craft:** Builds the leadership team and the hiring plan. Owns the ladder and how it is applied.
- **Influence:** Peer to the CEO's team. Trusted with the company's technical commitments.
- **Engineering with AI:** Sets how the company builds with AI, the guardrails and the measures, and reports them to the board.

## Pay bands

Set from market data you collect or buy. Overlap adjacent bands. State how manager and IC bands relate.

| Level | Band minimum | Midpoint | Band maximum | Notes |
| --- | --- | --- | --- | --- |
| E1 | | | | |
| E2 | | | | |
| E3 | | | | |
| E4 | | | | |
| M1 | | | | Sits in the ___ to ___ range |

## Review

- [ ] Two managers placed three real engineers on this ladder alone, and agreed.
- [ ] Each level differs from its neighbors on at least four axes.
- [ ] No level mentions years of experience.
- [ ] Pay bands are set and the manager and IC relationship is written down.
- [ ] Calibration and promotion dates are on the calendar.
