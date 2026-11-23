---
name: incident-status-update
status: early
use: copy for every update, on the clock set by the severity
---

# Incident Status Update

Send each update at the time you promised, even when nothing changed. Lead with customer impact in words a customer would use. Leave out the cause until you are sure. Never name a person. Use UTC.

## Customer update

```
[Product]: [what customers cannot do or what is slow]

Status: Investigating | Identified | Monitoring | Resolved
Since: [HH:MM UTC]

What is affected: [features, share of customers, regions]
What you can do now: [workaround, or "nothing needed"]
What we are doing: [one sentence]
Next update: [HH:MM UTC]
```

Closing update:

```
Resolved at [HH:MM UTC]. [Product] works normally again.
What happened: [one sentence, no blame, no guesses]
What happens next: We will publish a summary by [date]. | No further action is needed.
```

## Internal update

```
[Incident id] [SEV level] [Status]
Impact: [what customers see, with numbers]
Known: [what we know]
Not known: [what we do not know yet]
Doing: [current action and who is doing it]
Need: [anything blocked, and who can unblock it]
Next update: [HH:MM UTC]
```

## CEO update

```
[Incident id] [SEV level]
Customers affected: [number or share, and which ones that matter]
Exposure: [contracts, money, data, press, or none known]
What we are doing: [one sentence]
What I need from you: [a decision, or nothing]
Next update: [HH:MM UTC]
```

## Checks before you send

- [ ] The first line says what customers experience.
- [ ] I say what we do not know.
- [ ] The next update time is in the message.
- [ ] No cause is stated unless it is confirmed.
- [ ] No person is named, and no blame is implied.
- [ ] No secrets, customer data or internal hostnames.
