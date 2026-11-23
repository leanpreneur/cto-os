---
name: incident-log
status: early
use: the scribe fills this in live, one per incident, then the postmortem timeline is built from it
---

# Incident Log: [Incident id]

| Field | Value |
| --- | --- |
| Declared (UTC) | YYYY-MM-DD HH:MM |
| Severity | SEV1, SEV2, SEV3 or SEV4 |
| Incident commander | |
| Operations lead | |
| Communications | |
| Scribe | |
| Channel | |
| Next update due (UTC) | HH:MM |

Keep secrets and customer data out of this log. Use UTC. Record what happened, who did it and when, even when it turns out to be wrong.

## Current picture

Rewrite this block every time it changes. Anyone joining reads this first.

- What customers see:
- How many, and since when:
- What we think is happening (mark each as fact or guess):
- What we have tried:
- What we are doing now, and who:
- What is blocked:

## Log

| Time (UTC) | Who (role) | What happened or was decided | Source |
| --- | --- | --- | --- |
| | | | |

Record these without being asked: first alert, who noticed, declaration, severity changes, every change made to the system, every update sent, handoffs, mitigation, resolution.

## Open items at close

- [ ] Temporary workarounds to remove, with owners:
- [ ] Anything still broken:
- [ ] Postmortem owner and review date:
