# Example: updates during an incident

**Made by:** written by hand, from the [status update template](../../templates/incident-status-update.md). ExampleCo and the incident are invented. They show the format and the tone, and are not a recorded session.

The incident: after a 14:00 UTC deploy, about a third of checkout attempts fail. The on-call engineer declared SEV2 at 14:20 and named a commander. The severity guide says the CEO hears within 60 minutes and customers hear every 60 minutes.

## First customer update, 14:35 UTC

```
Checkout: some payments are failing

Status: Investigating
Since: 14:05 UTC

What is affected: About one in three checkout attempts fails with an error. Orders already placed are not affected.
What you can do now: Try again in a few minutes. If it keeps failing, contact support and we will take the order for you.
What we are doing: We are looking at a change released at 14:00 UTC.
Next update: 15:35 UTC
```

It says what customers see, what they can do and when they will hear again. It does not name a cause, because none is confirmed. "Looking at a change" is true and is not a claim.

## Internal update, 14:40 UTC

```
INC-0231 SEV2 Investigating
Impact: About 33 percent of checkout attempts fail since 14:05 UTC. 410 failures so far.
Known: Errors began within five minutes of the 14:00 UTC deploy. The payment provider reports no incident.
Not known: Whether the deploy is the cause. Whether any card was charged twice.
Doing: Operations lead is preparing a rollback of the 14:00 release. Communications is briefing support.
Need: Finance to check for duplicate charges once the rollback is done.
Next update: 15:10 UTC
```

## CEO update, 14:45 UTC

```
INC-0231 SEV2
Customers affected: About one third of checkout attempts for 40 minutes. No enterprise customer has reported it yet.
Exposure: Lost orders. We do not yet know whether any customer was charged twice.
What we are doing: Rolling back the 14:00 release.
What I need from you: Nothing now. I will confirm whether to contact the top accounts at the next update.
Next update: 15:15 UTC
```

## Closing update, 15:30 UTC

```
Resolved at 15:25 UTC. Checkout works normally again.
What happened: A release at 14:00 UTC caused some checkout attempts to fail. We rolled it back.
What happens next: We will publish a summary by 2026-12-01. Customers who were charged twice will be refunded without a request.
```

## What the four have in common

- Each opens with what customers or the business experience, and not with what the engineers did.
- Each says what is not known.
- Each gives the time of the next update. The commander keeps that time even when there is no news.
- None names a person or blames a team.
