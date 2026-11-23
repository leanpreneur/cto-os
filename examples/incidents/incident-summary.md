# Example: an incident summary

**Made by:** script output, plus the reading written by hand. The incident file and the action list are invented, for ExampleCo. They are in `skills/incident-response/scripts/examples/`. The block below is kept current by `scripts/build_examples.py --check`.

```bash
python3 skills/incident-response/scripts/incident_check.py summary --incidents skills/incident-response/scripts/examples/incidents-example.csv --actions skills/incident-response/scripts/examples/actions-example.csv --as-of 2026-11-22
```

<!-- output:incident-summary -->
> # Incident summary
>
> **8 incidents**, as of 2026-11-22.
>
> | Severity | Incidents | Detect median | Detect longest | Mitigate median | Mitigate longest | Resolve median | Resolve longest |
> | --- | --- | --- | --- | --- | --- | --- | --- |
> | SEV1 | 1 | 6 min | 6 min | 50 min | 50 min | 2 h 30 min | 2 h 30 min |
> | SEV2 | 3 | 18 min | 1 h 25 min | 1 h | 2 h 10 min | 2 h 45 min | 3 h 30 min |
> | SEV3 | 3 | 25 min | 1 h 10 min | 50 min | 1 h 40 min | 1 h 15 min | 2 h |
> | SEV4 | 1 | 0 min | 0 min | 1 h | 1 h | 1 h | 1 h |
> | All | 8 | 19 min | 1 h 25 min | 55 min | 2 h 10 min | 2 h 05 min | 3 h 30 min |
>
> Times run from impact start. They are Measured from the file you gave, and only as good as its start times.
>
> ## Detection
>
> - Found by monitoring: 5 of 8 (62%)
> - Found by customers: 2 of 8 (25%)
> - Found by employees: 1 of 8 (12%)
>
> ## Repeat contributing factors
>
> - missing-alert: 3 incidents
> - bad-deploy: 2 incidents
> - capacity: 2 incidents
> - no-rollback-plan: 2 incidents
>
> This is a Proxy. It depends on how consistently the factor tags were written.
>
> ## Postmortems
>
> - Owed: 4
> - Published: 3 of 4 (75%)
> - Published within 7 days of resolution: 2 of 4 (50%)
> - Overdue and unpublished: INC-0414
>
> ## Action items
>
> - Total: 10, done: 6, open: 4
> - Open and overdue: 2, the oldest by 20 days
>
> Read the median and the longest value, not a mean. With fewer than 20 incidents, read each case. Do not compare teams by these numbers: a team that reports every incident will look worse than one that hides them.
> Thresholds are defaults of this repository, not standards: a postmortem is published within 7 days of resolution.
<!-- end output -->

## How to read it

- **The most common repeat factor is a missing alert.** It appears in 3 of 8 incidents, and customers found 2 of those 3. One investment in alerting would address the factor that repeats most.
- **A postmortem is overdue.** INC-0414 was resolved on 2026-10-29 and has no published postmortem, 24 days later against a 7-day target.
- **Two action items are overdue**, the older by 20 days. They belong in the next CEO update next to the incident count.
- **Customers found 2 of 8 incidents first.** Every one of those is a monitoring gap, whatever the postmortem says caused the fault.

## What it cannot tell you

- Whether things are getting better. Eight incidents over five months are too few to show a trend. Read each case.
- Whether the start times are right. Time to detect is a Proxy if someone estimated them afterwards.
- Which team does better. A team that reports every incident looks worse than one that hides them. Do not compare teams by these numbers.
