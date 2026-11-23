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
| Status | draft |

## Summary

Invoice exports failed for about two hours after a deploy. The cause was human error: an engineer did not run the migration. We rolled back and the exports recovered.

## Impact

Many customers could not download invoices. Support received tickets.

## Timeline

| Time (UTC) | Event | Source |
| --- | --- | --- |
| 13:40 | Deploy of release 212 finishes | Deploy log |
| 15:05 | Support reports customers cannot export | Support channel |
| 15:50 | Release 212 rolled back | Deploy log |
| 17:10 | Export queue drained | Queue graph |

## Contributing factors

1. The migration was not run before the deploy.

## What went well

- The rollback took five minutes.

## What went badly

- Nobody noticed for 85 minutes.

## Where we got lucky

- The month-end close was two days away.

## Action items

| # | Action | Type | Owner | Due | Done when | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Remind the team to run migrations | process | | 2026-10-21 | | open |
| 2 | Add a migration check to the deploy pipeline | prevent | Platform lead | | The pipeline fails a deploy with a pending migration | open |
