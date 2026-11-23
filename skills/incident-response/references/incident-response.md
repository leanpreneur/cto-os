---
name: incident-response
status: early
audience: CTO or engineering leader who needs a written way to run production incidents and learn from them, or who inherited an on-call rota and no process
---

# Incident Response and Blameless Postmortems: Decide Before the Page

**Outcome:** a written severity scale, named incident roles, a first-15-minutes routine, a communication rhythm, and a postmortem that ends in action items with an owner and a date. Customers and the CEO hear from you on a schedule, and the same failure does not happen twice for the same reason.

Most incidents go badly in the first twenty minutes for organizational reasons. Nobody declared it. Five people are debugging and nobody is deciding. Support has no update to give. The CEO learns about it from a customer. This playbook fixes the order: severity, roles, declaration, communication, resolution, postmortem, follow-through, measures. Write the first four down before the next page, not during it.

## Ground rules

1. **Declare early.** A false alarm costs minutes. A late declaration costs hours.
2. **Severity comes from customer impact, not from cause.** Decide it in a minute. When unsure between two levels, take the higher one and review it afterwards.
3. **One incident commander, and the commander does not fix.** The commander decides, assigns and tracks. Someone else changes the system.
4. **Stop the damage first, find the cause second.** Roll back, fail over or switch a feature off before you understand why.
5. **Update on a clock.** Say when the next update will come, and send it then, even if the news is "no change".
6. **Do not guess in public.** Say what you know, what you do not know and what you are doing. Leave cause and blame out of every update.
7. **Write a postmortem for a defined set of incidents.** Define the triggers before an incident, so nobody argues about whether this one counts.
8. **Blameless means you look at conditions, not that nobody is accountable.** An action item always has an owner.
9. **Nothing is done until the action items are done.** A postmortem with open items is a story, not a fix.

## Step 1: Write the severity scale

Define four levels by what customers experience. Use numbers from your own product: the share of requests failing, the number of accounts affected, minutes of downtime. The [severity guide](https://github.com/leanpreneur/cto-os/blob/main/templates/incident-severity-guide.md) has the table to fill in.

| Level | Meaning | Default response |
| --- | --- | --- |
| SEV1 | Most customers cannot use the product, data is lost, or customer data may be exposed | Commander paged now, CEO told within 30 minutes, customer update every 30 minutes |
| SEV2 | A major feature is unavailable or badly degraded for many customers | Commander paged now, CEO told within 60 minutes, customer update every 60 minutes |
| SEV3 | A minor feature is degraded, or a small share of customers is affected | Owning team handles it, one update at the start and one at the end |
| SEV4 | No customer impact today, but something is wrong | A ticket with an owner |

These cadences and levels are defaults of this repository, not standards. Replace the meanings with your own thresholds and keep the shape. If personal data or credentials may be exposed, treat it as SEV1 until someone shows otherwise.

## Step 2: Name the roles

Four roles cover almost every incident. Names change by company. The jobs do not.

| Role | Does | Does not |
| --- | --- | --- |
| Incident commander | Declares, sets severity, assigns the other roles, holds the current picture, decides what to try next, approves external updates | Debug, or type commands in production |
| Operations lead | Makes the changes to the system, one at a time, and reports what each change did | Decide priorities or talk to customers |
| Communications | Writes internal and customer updates on the clock and answers executive questions | Join the debugging |
| Scribe | Keeps the timeline: what happened, who did it, and when, in UTC | Interpret or editorialize |

Subject matter experts join the operations lead when needed and report in a fixed shape: the condition, the action they took, and what they need.

**Small teams.** Under about 15 engineers, one person can hold communications and scribe, and a second can deputize for the commander. Never let the person fixing the system also be the commander. If you are the CTO and the best debugger in the room, debug and hand command to someone else.

**Handoff.** Commanders hand off at the end of a shift or when they are worn out. The outgoing commander says "you are now the incident commander", and the incoming one says yes. Nobody leaves until the handoff is acknowledged, and the room is told.

**On-call.** Write down who is primary, who is backup and who is the escalation point. Give people time off after a night of pages. A rota that burns out the same three people produces worse incidents.

## Step 3: Declare, then run the first 15 minutes

Declare an incident when any one of these is true:

- Fixing it needs a second team.
- Customers can see it.
- It is still unsolved after an hour of focused work.

Then run the same routine every time.

| Minutes | Do |
| --- | --- |
| 0 to 2 | Declare. Open one channel and one incident log. Set a severity. Name the commander |
| 2 to 5 | Name the operations lead, communications and scribe, out loud |
| 5 to 10 | State the customer impact in plain words and in numbers. Ask what changed recently. If a recent change is the likely cause, roll it back first |
| 10 to 15 | Send the first update with the next update time. Page the subject matter experts who are needed |

After minute 15, loop. State the current picture, name one hypothesis, make one change, watch what it does. Change one thing at a time, so you know what worked. Re-check the severity whenever the picture changes.

Do not paste secrets or customer data into the incident log, a chat channel or an AI tool unless your data policy allows it.

## Step 4: Communicate on a clock

Four audiences need different things. Write the update from the [status update template](https://github.com/leanpreneur/cto-os/blob/main/templates/incident-status-update.md).

| Audience | Needs | Who sends | When |
| --- | --- | --- | --- |
| Responders | The current picture and their next job | Commander | Continuously, in the channel |
| Support and customer success | What customers see, what to tell them, when the next update comes | Communications | At the first update, then on the clock |
| Customers | What is affected, that you are working on it, when they will hear again | Communications, approved by the commander | On the clock for your severity |
| The CEO | Impact, exposure, what is being done, when the next update comes | Commander or CTO, through communications | Within the target for the severity, then on the clock |

Rules for every update:

- Lead with customer impact, in words a customer would use.
- State what you know, what you do not know yet and what you are doing.
- State the time of the next update, and keep it.
- Leave out the cause until you are sure, and never name a person.
- Use UTC, and add local time if customers are in one region.

For the CEO, your job as CTO is to keep the questions away from the responders. Send one update on the agreed cadence, and route executive questions to communications. For what to say afterwards and how to say it, see the bad-news scripts in the [CEO and CTO partnership](https://github.com/leanpreneur/cto-os/blob/main/playbooks/ceo-cto-partnership.md) playbook.

If customer data or credentials may be exposed, bring in counsel and your security lead at once. Many jurisdictions set deadlines for telling regulators and customers about a personal data breach. Ask counsel in advance which ones apply to you, so that you are not looking it up during the incident. This playbook is not legal advice.

## Step 5: Resolve and close

- **Mitigated** means customers are no longer hurt, even if the cause is unknown. **Resolved** means the system is back to normal and watched.
- Name how long you will watch before closing. A default for SEV1 and SEV2 is 30 minutes of normal behavior.
- Send the closing update. Say what happened in one sentence, that it is over and that a postmortem will follow where you owe one.
- Before closing the channel, note anything still broken, any temporary workaround that needs removing, and who owns each.
- Schedule the postmortem review before people disperse.

## Step 6: Decide whether a postmortem is owed

Define the triggers now. These defaults come from the common triggers in Google's SRE book, adjusted:

- Any SEV1 or SEV2.
- Data loss of any kind, or exposure of customer data.
- Customers found it before your monitoring did.
- Time to resolve above a threshold you set, such as four hours.
- A rollback or traffic change that customers could notice.
- Any stakeholder asks for one.

Everything else gets a short note in the incident log. Do not skip a postmortem because the fix was easy. Easy fixes often hide the contributing factors that matter.

## Step 7: Write a blameless postmortem

Use the [postmortem template](https://github.com/leanpreneur/cto-os/blob/main/templates/postmortem.md). The owner is one of the responders, usually the commander, and publishes within a week.

**Blameless does not mean vague.** Write what each person did and why it made sense given what they knew at the time. Use roles, not names. The question is "how did the system let this happen?", not "who did it?". Allspaw calls what you find when you ask why an action made sense at the time "second stories": they explain the conditions around a mistake. "Human error" is not a finding. It is where the investigation starts.

The sections, in order:

1. **Summary:** three sentences. What happened, how long, how it ended.
2. **Impact:** numbers. Customers affected, minutes, failed requests, money, support tickets. Say what you could not measure.
3. **Timeline:** every row has a time in UTC and a source: a graph, a log or a message.
4. **Contributing factors:** several, not one. Look at detection, change process, design, tooling, load, and the gaps between teams.
5. **What went well:** keep these on purpose.
6. **What went badly.**
7. **Where we got lucky:** what could have made it worse and did not.
8. **Action items:** a table with an owner, a due date and a test for done.

Hold a 45-minute review with everyone who took part. Walk the timeline, ask what each person knew and when, and ask what would have made the right action easier. Publish the postmortem as widely as your company allows. Keep it in a private location, because it may contain customer details. Do not use a postmortem as evidence in a performance case. If someone's conduct is a performance matter, handle it separately.

## Step 8: Follow through on action items

Action items come in four types. Name the type, because it shows what you are missing.

| Type | Purpose | Example |
| --- | --- | --- |
| Prevent | Remove the contributing factor | Add a schema check to the deploy pipeline |
| Detect | Find it sooner next time | Alert on queue depth, not just CPU |
| Mitigate | Limit the damage next time | Feature flag to turn the report off |
| Process | Change how people work | Add a rollback step to the release checklist |

Rules:

- Every item has one owner, a due date and a "done when" you can check.
- At most eight items. A long list does not get finished. Rank them and drop the weak ones, or write them down as ideas instead.
- A due date more than 90 days out is a sign the item is too big. Split it.
- If customers found the problem before you did, at least one item is a detect item.
- Review open items monthly. Overdue items go to the CTO and are reported to the CEO with the incident count.

## Step 9: Measure

Run `/incident-response` in Measure mode on a file of incidents. The script reports what the file supports and hides nothing.

| Measure | How | Label |
| --- | --- | --- |
| Incidents by severity per quarter | Count from the log | Measured |
| Time to detect | Impact start to detection | Measured when impact start comes from a metric. Proxy when you estimated it afterwards |
| Time to mitigate and to resolve | Impact start to each | Measured from the log |
| Share found by customers | Incidents with detected by customer, over all | Measured |
| Repeat contributing factors | The same factor tag in two or more incidents | Proxy. It depends on consistent tagging |
| Postmortems published within 7 days | Published over owed | Measured |
| Action items closed on time | Done by due date, over all | Measured |

Use the median and the longest value, not the mean. With under about 20 incidents, read each case. Do not compare teams by these numbers. A team that reports every incident honestly will look worse than one that hides them. The board numbers belong in the customer-affecting incidents row of the [board update](https://github.com/leanpreneur/cto-os/blob/main/templates/board-update.md), and the [engineering baseline](https://github.com/leanpreneur/cto-os/blob/main/playbooks/engineering-baseline.md) lists time to restore as Unknown until you have this data.

## Definition of done

- A severity scale with your own thresholds, agreed with the CEO.
- Named incident roles, with a backup for each.
- Postmortem triggers written down.
- A status update template and a place for the incident log.
- Each postmortem passes the `/incident-response` check with no failures.
- Open action items are reviewed monthly.

## How you will know it worked

- Leading indicator: the share of incidents declared within 15 minutes of the first alert, and the share of postmortems published within 7 days.
- Lagging indicator: time to detect and time to mitigate trending down, fewer repeats of the same contributing factor, and fewer incidents found first by customers. Track each per quarter.

## Sources

- Google, *Site Reliability Engineering*, chapter 14, [Managing Incidents](https://sre.google/sre-book/managing-incidents/) (Andrew Stribblehill): the incident command roles, the clear handoff and the criteria for declaring an incident early.
- Google, *Site Reliability Engineering*, chapter 15, [Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/) (John Lunney and Sue Lueder): the blameless premise, the common postmortem triggers and the elements of a good postmortem. The chapter describes review sessions but no mechanism for tracking action items to completion. The follow-through rules above are this repository's.
- PagerDuty, [Incident Response Guide](https://docs.pagerduty.com/ops-guides/incident-response-guide): roles such as commander, deputy and scribe, and the advice to treat an uncertain severity as the higher one. The guide states a copyright, so nothing here is copied from it. The severity table and the role table were written for this repository.
- John Allspaw, [Blameless PostMortems and a Just Culture](https://www.etsy.com/codeascraft/blameless-postmortems), Etsy Code as Craft, 22 May 2012: the argument that blame hides the detail you need, and the "second stories".
- The severity levels, update cadences, the 15-minute routine, the eight-item and 90-day limits, the 7-day publishing target, the 30-minute watch period and the 20-incident threshold are this repository's judgment. They are Early and have not been validated in real engagements.
