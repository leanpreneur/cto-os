# CTO OS

**The operating system for technical leaders.** Playbooks, templates and agent skills for the first 90 days, the team, the process, the architecture, AI-native engineering and the board.

> Other CTO resources tell you what good looks like. CTO OS measures where you are and produces the plan.

By [Abbas Raza](https://abbasraza.com), CTO at ReFocus AI. Over fifteen years leading engineering and product, including twelve years at SAP SuccessFactors.

## Why this exists

Popular agent skill collections focus on how a coding agent writes, reviews and ships code. The person accountable for the whole engineering organization has a different job: what to learn in week one, which decisions to write down, how to report to the CEO and the board, how to build a team and keep it shipping, and how to move the organization from AI tools to an AI-native way of working.

CTO OS covers that job. Every artifact exists in two forms: a document you can read and adapt, and an agent skill that runs it with you. Skills interview you and read your own repositories and documents, so the output reflects your organization instead of a generic target.

## Start here

| Artifact | What you get | Form |
| --- | --- | --- |
| [First 90 Days](playbooks/first-90-days.md) | Stage-aware plan: listening tour, baseline metrics, priorities, CEO alignment, first win | Playbook |
| [cto-day-one](skills/cto-day-one/SKILL.md) | Interviews you about the company, then produces a tailored 30/60/90 plan | Agent skill |
| [ADOPT Assessment](playbooks/adopt-assessment.md) | Checks seven foundations from DORA, then scores your organization from 1 to 5 on AI-native engineering across five dimensions, with evidence and a move plan | Playbook |
| [adopt-assess](skills/adopt-assess/SKILL.md) | Gathers evidence from your repos and documents, checks foundations, scores, and writes the one-page result for the CEO | Agent skill |
| [CEO and CTO Partnership](playbooks/ceo-cto-partnership.md) | Six practices, a business translation table, bad-news and disagreement scripts, and a board preparation timeline | Playbook |
| [CEO and CTO Operating Agreement](templates/ceo-cto-operating-agreement.md) | Outcomes, decision rights, rhythm, communication rules and reset triggers, written and signed | Template |
| [ceo-alignment](skills/ceo-alignment/SKILL.md) | Interviews you and drafts the operating agreement, with the questions to settle and a 20-minute meeting plan | Agent skill |
| [Board Update](templates/board-update.md) | Quarterly structure: headline, outcomes, investment, delivery, risk, people, AI, asks | Template |
| [board-update](skills/board-update/SKILL.md) | Collects your metrics, applies status rules, drafts the update and the CEO pre-read | Agent skill |
| [Decision Record](templates/decision-record.md) | One-page template for architecture and organization decisions | Template |
| [Principles](PRINCIPLES.md) | The ten rules the rest of the repo follows | Reference |

## Use the skills with Claude Code

```bash
git clone https://github.com/leanpreneur/cto-os.git
cp -r cto-os/skills/cto-day-one ~/.claude/skills/
cp -r cto-os/skills/adopt-assess ~/.claude/skills/
cp -r cto-os/skills/ceo-alignment ~/.claude/skills/
cp -r cto-os/skills/board-update ~/.claude/skills/
```

Open Claude Code in any folder and run `/cto-day-one`, `/adopt-assess`, `/ceo-alignment` or `/board-update`. Each skill bundles its own copy of the playbook it uses, so nothing else is needed.

## ADOPT

ADOPT is the author's framework for AI transformation maturity: **A**lign on outcomes, **D**esign an AI-native SDLC, **O**rchestrate human and AI roles, **P**ut guardrails in place, **T**ransform culture and skills. It is described in the essay [From Copilot to Autonomous Engineering](https://abbasraza.com/essays/from-copilot-to-autonomous-engineering/). The assessment in this repo extends the essay with a scoring rubric, a foundations gate built on the seven capabilities in [DORA's AI Capabilities Model](https://cloud.google.com/blog/products/ai-machine-learning/introducing-doras-inaugural-ai-capabilities-model), and an explicit context practice inside D. All three extensions are Draft.

## Status labels

Every artifact declares a status in its header.

- **Draft**: written, not yet applied in a real engagement.
- **Used**: applied in a real engagement.
- **Proven**: applied more than once and revised from what was learned.

## Next

Hiring kit with leveling and scorecards, incident response and blameless postmortem, a repository audit skill that computes delivery metrics from your own history, a CTO scorecard with a 360 question set, and a situation router that points you to the right artifact.

## Related work

- [awesome-cto](https://github.com/kuchin/awesome-cto): curated reading list for CTOs.
- [claude-code-templates](https://github.com/davila7/claude-code-templates): includes a cto-advisor reference skill.
- [claude-skills](https://github.com/alirezarezvani/claude-skills): large library with executive persona skills.

CTO OS differs in three ways: its skills produce finished artifacts instead of advice, it adapts to company stage and measures your own baseline, and each artifact is labeled Draft, Used or Proven. See [docs/related-work.md](docs/related-work.md).

## About

- Writing: [abbasraza.com](https://abbasraza.com)
- Community: [Shine Labs](https://shinelabs.io), a professional networking and mentorship organization
- More from this account: [talks](https://github.com/leanpreneur/talks), [repo-health](https://github.com/leanpreneur/repo-health)

## Maintaining

Playbooks are the source of truth. After editing one, run `scripts/sync-skill-references.sh` to refresh the copy bundled with its skill.

## License

MIT. Use it, adapt it, share it. Attribution is appreciated.

Nothing in this repository contains employer data, customer data or confidential material. Examples are anonymized.
