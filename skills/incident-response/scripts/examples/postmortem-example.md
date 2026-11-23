# Postmortem: Customers could not export invoices

| Field | Value |
| --- | --- |
| Incident id | INC-0412 |
| Severity | SEV2 |
| Impact started (UTC) | 2026-10-14 13:40 |
| Detected (UTC) | 2026-10-14 15:05 |
| Mitigated (UTC) | 2026-10-14 15:50 |
| Resolved (UTC) | 2026-10-14 17:10 |
| Detected by | customer |
| Incident commander | Engineering manager, billing |
| Postmortem owner | Engineering manager, billing |
| Status | reviewed |

## Summary

Invoice exports failed for 3 hours 30 minutes after release 212. Customers found it before we did. We rolled back at 15:50, and the export backlog was cleared by 17:10.

## Impact

About 340 of 2,100 active accounts tried to export an invoice during the window and 1,180 export requests failed. Support logged 27 tickets. Nobody lost data, and no invoice was wrong. We could not measure how many customers gave up without trying again.

## Timeline

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 2026-10-14 13:40 | Release 212 finishes deploying. Export errors begin | Deploy log, error graph |
| 14:10 | Error rate on the export endpoint passes 40 percent. No alert fires, because the alert covers the website and not this endpoint | Error graph |
| 15:05 | Support tells the on-call engineer that customers cannot export | Support channel |
| 15:08 | On-call engineer declares SEV2 and takes command | Incident channel |
| 15:20 | Operations lead finds the new query needs a column that has no migration applied | Application log |
| 15:30 | Team decides to roll back instead of fixing forward, after ten minutes of discussion | Incident channel |
| 15:35 | Support posts a workaround to customers: request an export through support | Support channel |
| 15:50 | Operations lead completes the rollback of release 212. New exports succeed | Deploy log |
| 15:55 | First customer update posted | Status page |
| 17:10 | Backlog of failed requests replayed and the queue empty | Queue graph |

## Contributing factors

1. The release included a migration, and the deploy pipeline does not check whether pending migrations have run. Running it was a manual step that a release note mentioned once.
2. The export endpoint had no alert of its own. The error rate was above 40 percent for 55 minutes before a person noticed.
3. The release checklist has no rollback criteria, so the on-call engineer spent ten minutes asking whether to roll back or fix forward.
4. Staging had the migration applied by hand two days earlier, so the test run there passed.

## What went well

- The on-call engineer declared the incident within three minutes of the report and named an operations lead.
- The rollback worked the first time.
- Support gave customers a workaround within 30 minutes of the report.

## What went badly

- Customers found the failure 85 minutes after it began.
- The first customer update went out at 15:55, 50 minutes after the report.
- The team spent ten minutes deciding between a rollback and a fix because no rollback criteria existed.
- The failed requests had to be replayed by hand.

## Where we got lucky

- The month-end close was two days away, so few customers were exporting.
- The new query only read data. A write would have needed a data repair.

## Action items

| # | Action | Type | Owner | Due | Done when | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Fail the deploy when a migration is pending | prevent | Platform lead | 2026-11-04 | A test release with an unapplied migration is blocked by the pipeline | open |
| 2 | Alert when the export error rate passes 5 percent for 5 minutes | detect | Billing tech lead | 2026-10-21 | The alert fires in staging when the endpoint is made to fail | done |
| 3 | Add rollback criteria to the release checklist | process | Engineering manager, billing | 2026-10-28 | The checklist says when to roll back and who decides | done |
| 4 | Replay failed export requests automatically | mitigate | Billing tech lead | 2026-12-02 | A failed export is retried without a person | open |
| 5 | Rebuild staging from the migration history each week | prevent | Platform lead | 2026-12-16 | A staging rebuild runs on a schedule and its last run is green | open |
