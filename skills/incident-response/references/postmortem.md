---
name: postmortem
use: one per incident that meets a postmortem trigger, published within a week of resolution
---

# Postmortem: [Short title that says what customers experienced]

Lines that start with `>` are guidance. Delete them as you write. The checker ignores them. Use roles, not names. Times are UTC, in the form YYYY-MM-DD HH:MM. Keep this document out of any public repository, because it may contain customer details.

| Field | Value |
| --- | --- |
| Incident id | |
| Severity | SEV1, SEV2, SEV3 or SEV4 |
| Impact started (UTC) | YYYY-MM-DD HH:MM |
| Detected (UTC) | YYYY-MM-DD HH:MM |
| Mitigated (UTC) | YYYY-MM-DD HH:MM |
| Resolved (UTC) | YYYY-MM-DD HH:MM |
| Detected by | monitoring, customer or employee |
| Incident commander | Role or id |
| Postmortem owner | Role or id |
| Status | draft, reviewed or published |

## Summary

> Three sentences. What happened, how long it lasted, how it ended.

## Impact

> Numbers: customers or accounts affected, minutes, failed requests, money, support tickets. Say what you could not measure.

## Timeline

> One row per event, in order. Source is a graph, a log or a message. A time alone, such as 14:05, counts as the same day as the previous row.

| Time (UTC) | Event | Source |
| --- | --- | --- |
| | | |

## Contributing factors

> Several, not one. Look at detection, the change process, design, tooling, load and gaps between teams. Write how the system allowed it, not who did it. "Human error" is not a finding. Ask why each action made sense at the time.

1.
2.

## What went well

> Practices to keep on purpose.

-

## What went badly

-

## Where we got lucky

> What could have made this worse and did not.

-

## Action items

> At most eight. One owner each. Type is prevent, detect, mitigate or process. Due is YYYY-MM-DD. Done when is a test someone else could run. Status is open or done. If customers found the problem before monitoring did, include a detect item.

| # | Action | Type | Owner | Due | Done when | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | open |

## Review

- [ ] The review meeting included everyone who took part, and ran about 45 minutes.
- [ ] We asked what each person knew and when.
- [ ] Every action item has an owner and a date.
- [ ] A reader outside the team can follow the timeline.
- [ ] No sentence blames a person.
- [ ] Customer data is not in the document.

Check it before you publish:

```bash
python3 skills/incident-response/scripts/incident_check.py postmortem --file postmortem.md
```
