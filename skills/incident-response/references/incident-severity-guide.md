---
name: incident-severity-guide
status: early
use: one page, agreed with the CEO before the next incident, pinned where responders work
---

# Incident Severity Guide: [Company]

| Field | Value |
| --- | --- |
| Owner | |
| Agreed with (CEO) | |
| Date | YYYY-MM-DD |
| Review again | YYYY-MM-DD, twice a year |

Severity comes from what customers experience, not from the cause. When unsure between two levels, choose the higher one and review it in the postmortem. Do not debate severity during an incident.

## Levels

Replace each meaning with a threshold from your own product. Use numbers: the share of requests failing, accounts affected, minutes of downtime.

| Level | Meaning for us (with numbers) | Who is paged | Commander | CEO told within | Customer update every | Postmortem |
| --- | --- | --- | --- | --- | --- | --- |
| SEV1 | | | Yes, now | 30 minutes | 30 minutes | Always |
| SEV2 | | | Yes, now | 60 minutes | 60 minutes | Always |
| SEV3 | | | No, owning team leads | Next business day | At start and end | If a trigger applies |
| SEV4 | | | No | Not needed | Not needed | No |

The cadences are defaults of the cto-os repository. Change them to fit your customers and contracts.

Example of a threshold, to show the shape and not to copy: "SEV2: checkout fails for more than 5 percent of attempts for 10 minutes, or any single enterprise customer cannot sign in."

## Always SEV1 until shown otherwise

- Customer data or credentials may be exposed.
- Data loss that cannot be undone.
- A security incident in progress.

## Postmortem triggers

A postmortem is owed when any of these is true. Add your own.

- [ ] SEV1 or SEV2
- [ ] Data loss of any kind, or exposure of customer data
- [ ] Customers found it before monitoring did
- [ ] Time to resolve above [4] hours
- [ ] A rollback or traffic change that customers could notice
- [ ] Any stakeholder asks for one

## Roles and who fills them

| Role | Primary | Backup |
| --- | --- | --- |
| Incident commander | | |
| Operations lead | | |
| Communications | | |
| Scribe | | |

## Where things live

- Incident channel naming:
- Incident log location:
- Status page owner:
- Executive update channel:
- Legal and security contacts:
- Postmortem folder (private):

## Checks

- [ ] A new engineer could pick a severity from this page alone, in a minute.
- [ ] Each threshold has a number.
- [ ] The CEO has agreed to the response times.
- [ ] Every role has a primary and a backup.
- [ ] On-call people know the page and where it lives.
