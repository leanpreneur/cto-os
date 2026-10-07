---
name: engineering-baseline
status: draft
audience: CTO or VP Engineering who needs delivery numbers in the first 30 days, or before an AI rollout
---

# Engineering Baseline: Numbers Before Opinions

**Outcome:** a dated baseline of how work flows through your repositories, with every number labeled Measured, Proxy or Unknown, so your first conversations start from data.

Most of the delivery numbers the [First 90 Days](first-90-days.md) plan asks for sit in git history: how big changes are, how long branches live, how often work is released, how often it is reverted, who holds knowledge, and what context an engineer or an AI agent can read. This playbook says which numbers to pull, what git can and cannot tell you, how to read the result, and how to avoid misusing it.

## What git can and cannot show

| Metric | Standard meaning | Best source | What git shows | Label |
| --- | --- | --- | --- | --- |
| Deployment frequency | How often code reaches production | CI/CD or deployment tool | Pull request merges per week, and tags | Proxy |
| Lead time for changes | Commit to production | CI/CD or deployment tool | Branch lifetime for merge-commit pull requests, and pull request cycle time from GitHub | Proxy |
| Change failure rate | Share of releases that cause a failure | Incident tracker, rollback records | Share of commits that are reverts | Proxy |
| Time to restore service | How long customers feel a failure | Incident tracker, on-call history | Not in git. Time from a change to its revert is a weak stand-in | Unknown or Proxy |
| Change size | Lines changed per pull request | Git, GitHub | Lines added plus deleted per pull request, without lockfiles and generated output | Measured |
| Review time | Pull request opened to first review | GitHub | Needs GitHub data | Measured with GitHub data |
| Contributor concentration | How many people can change an area | Git | Contributors who account for half of all commits, and folders where one person holds 80% or more | Measured |
| Knowledge freshness | Whether docs are kept current | Git | Share of documentation files changed in the last 12 months | Measured |
| AI traceability | Whether AI-assisted changes can be identified | Git | Commits that name an AI tool in a trailer or message | Measured |
| Context files | What an engineer or agent can read before changing the system | Git tree | Instruction files, decision records, runbooks, CODEOWNERS, pull request template, CI configuration | Measured |

The four delivery metrics follow the classic DORA set (see [Sources](#sources)). A **Proxy** is a number git can show that points toward the standard metric but is not the same thing. Never present a Proxy as the standard metric.

## Run it

1. **Get full history.** Run `git fetch --all --tags`. If the clone is shallow, run `git fetch --unshallow`. The script excludes the commits at the edge of a shallow clone, because git shows them as adding every file.
2. **Agree the change size threshold with the team first.** If there is none, the tool uses 400 changed lines. That default is this repository's, not an industry standard. Decide it before you read the data, so the data does not set the target.
3. **Run the tool.** From a folder that is not inside a public repository:

   ```bash
   python3 skills/eng-audit/scripts/audit.py --repo /path/to/repo --gh --format both --out ./eng-audit-2026-10-06
   ```

   Repeat `--repo` for each repository. Drop `--gh` if the GitHub command line tool is not signed in. The pull request cycle time and first review rows then show Unknown.
4. **Spot check.** Pick one number and verify it with raw git. For example, compare the commit count with `git rev-list --no-merges --count --since=<date> <branch>`.
5. **Keep the report private.** It describes your organization. Do not commit it to a public repository.

The `eng-audit` skill runs these steps with you and writes the summary.

## Read the numbers

These are questions to ask, not verdicts. None of the readings below has been validated.

| What you see | What it may mean | First question |
| --- | --- | --- |
| Median change size above your threshold, or a 90th percentile many times the median | Work is not split small | How is work cut at planning? What did review of the largest change look like? |
| Branch lifetime or pull request cycle time measured in days | Work waits | Where does it wait: review, CI or approval? |
| Many pull requests with no recorded review | Review is optional | Is that policy or habit? |
| Long time to first review | Reviewers are overloaded | Who reviews most, and what else do they own? |
| No tags and no deployment data | The release path is invisible | Can we walk one change to production together? |
| Reverts or hotfixes clustered in one area | Quality escapes there | What did the last three reverts have in common? |
| One person holds 80% or more of commits in a folder | Knowledge is concentrated | Who else can change this, and have they? |
| Few documentation files changed in 12 months | Documentation is not kept | Who owns it? |
| No AI instruction file | Agents guess at conventions | What must an agent know before changing this repository? |
| Almost no commits naming an AI tool, while engineers report heavy AI use | AI use is not traceable | How would we know which changes were AI-assisted? |

## What not to do

- **Do not rank or evaluate people with this.** Contributor labels are anonymous by default. Use names only for your own use, and do not share them. Commit counts do not measure contribution.
- **Do not set targets on Proxies.** A target on a Proxy gets met by changing the Proxy.
- **Do not show a Proxy as the standard metric** to the board or the CEO. Keep the label.
- **Do not read missing AI trailers as missing AI use.** It means the use is not traceable from git.
- **Do not fill an Unknown with an estimate.** Name the source, the owner and a date for measuring it.

## How it feeds other artifacts

- **First 90 Days:** the report produces baseline rows for the metrics table, each with value, source and date. Unknowns become 60-day tasks.
- **ADOPT assessment:** the report gives evidence for the foundations (small batches, version control, healthy data), the context practice and traceability. You still make the Present, Partial or Absent call and the scores yourself.
- **Board update:** the delivery health appendix can use these numbers with their Proxy labels. Rerun before each board meeting.

## Companion tool

[repo-health](https://github.com/leanpreneur/repo-health) gives a quick written read of a public GitHub repository, using a language model over recent issues, pull requests and commits. `eng-audit` computes reproducible numbers from a local clone, including private repositories, with no model involved. Use repo-health to decide where to look. Use eng-audit to measure.

## Definition of done

- The report covers every repository in scope, for one stated window.
- Each number carries a label of Measured, Proxy or Unknown.
- At least one number was checked against raw git.
- Every Unknown has a named source, an owner and a date.
- The baseline rows are in the First 90 Days table.

## How you will know it worked

- Leading indicator: the share of baseline rows that hold a measured value instead of Unknown, rising each quarter as owners close the gaps.
- Lagging indicator: a rerun after 90 days shows movement against the first report on the one metric you chose to improve, such as median change size or branch lifetime.

Rerun every quarter, with the same window and threshold, and keep the old report for comparison.

## Sources

- [DORA metrics](https://dora.dev/guides/dora-metrics/): the delivery metrics this playbook maps to. DORA has since extended its set, so check the site for current definitions.
- The 400-line change size default, the Proxy definitions and the reading table are this repository's judgment. They are Draft and have not been validated against real engagements.
