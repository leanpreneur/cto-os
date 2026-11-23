---
name: incident-response
description: Use when an engineering leader needs an incident process, is in the middle of a production incident, needs to write or review a blameless postmortem, or wants incident measures such as time to detect, time to restore and overdue action items. Builds the severity guide and roles, helps run the first 15 minutes and the updates, drafts a postmortem from the incident log, and checks it with a bundled script.
---

# incident-response

Prepare an incident process, run an incident, write its postmortem, or measure incidents over time. Follow `references/incident-response.md`. Use `references/incident-severity-guide.md`, `references/incident-status-update.md`, `references/incident-log.md` and `references/postmortem.md`. The script at `scripts/incident_check.py` needs `python3` only. It uses no model, so the same input gives the same output.

Ask first which mode the user wants: **Prepare**, **Run**, **Postmortem** or **Measure**. If the request makes it clear, do not ask. If an incident is happening now, go straight to Run and keep your questions to the four in Step 1.

Rules for every mode:

- Never invent facts about an incident: times, numbers, causes, owners or who did what. Mark unknowns as unknown.
- Use roles, not names, in anything that will be shared. Do not write blame, and do not name a person as the cause.
- Do not give legal advice. If customer data or credentials may be exposed, say to bring in counsel and the security lead now.
- Keep real incident data, customer details and secrets out of any public repository. Save work in a private folder. If the user pastes a secret or customer data, do not repeat it.

## Prepare mode

### Step 1: Interview

Ask in one message. Accept partial answers.

1. Company size, engineering headcount and who is on call today.
2. What customers expect: contract uptime terms, support hours, regions, and the three customers whose outage would hurt most.
3. Tools in use: paging, chat, status page, incident log, monitoring.
4. The last three incidents and what went wrong in handling them.
5. Whether customer data is personal, regulated or financial, and who the legal and security contacts are.
6. Who the CEO wants to hear from, and how fast.
7. Whether postmortems exist today, and where they are kept.

### Step 2: Read what exists

If the user provides runbooks, past postmortems or an on-call policy, read them first. Keep their words for roles and tools.

### Step 3: Draft

Fill in the severity guide with thresholds that use the product's own numbers. If the user does not know a number, propose one and mark it as an assumption. Name the four roles and who fills each, with a backup. Write the postmortem triggers, the update cadence by severity, and a one-page first-15-minutes card from the playbook.

### Step 4: Output

1. **Assumptions:** what you assumed and could not confirm.
2. **Severity guide:** the filled template.
3. **Roles and on-call:** the table and any gaps, such as a single person who is the backup for everything.
4. **First-15-minutes card:** one page.
5. **Update templates:** copied from the status update template with the product's names filled in.
6. **What to agree with the CEO:** response times, who is told, who speaks to customers.
7. **Gaps and the next three actions**, in order.

## Run mode

### Step 1: Get four facts

Ask only these, in one message:

1. What do customers see, in plain words?
2. How many, and since when?
3. What changed recently: a deploy, a config, a vendor, traffic?
4. Who is on the call, and who is incident commander?

### Step 2: Set severity and roles

Propose a severity from the severity guide, or from the playbook defaults if there is none. When unsure, take the higher one. Name the roles. If the person fixing the system is also the commander, say so and suggest a split. If a recent change is the likely cause, suggest rolling it back before investigating.

### Step 3: First updates

Draft the customer, internal and CEO updates from the status update template. State what is known, what is not known and the next update time. Leave out any cause that is not confirmed.

### Step 4: Keep the log

As the user pastes events, keep the incident log: the current picture at the top, then a UTC timeline with who and what. Rewrite the current picture after each change. Do not fill gaps with guesses. Ask what is missing.

### Step 5: On the clock

At each update time, draft the next update from the log. If nothing changed, say so and give the next time.

### Step 6: Close

Draft the closing update, list the open items and temporary workarounds, and name the postmortem owner and review date. Then offer Postmortem mode.

## Postmortem mode

### Step 1: Gather

Ask for the incident log, chat export, alert history, timeline notes and any graphs or numbers the user can describe. Ask for the four times: impact start, detection, mitigation and resolution, and who found it: monitoring, a customer or an employee.

### Step 2: Draft from the template

Fill in `references/postmortem.md`. Every timeline row needs a time in UTC and a source. If the user did not give a source or a time, write what is missing and ask. Replace names with roles.

### Step 3: Contributing factors

Ask for each important action: what did the person know at the time, and why did it make sense? Propose contributing factors from the evidence and label them as proposed. Look at detection, the change process, design, tooling, load and gaps between teams. Do not stop at the first one. "Human error" is not a finding.

### Step 4: Action items

Draft action items with a type, a test for done and a due date. Ask the user for the owner of each. Do not invent owners. If customers found the problem first, include a detect item. Keep the list to eight or fewer.

### Step 5: Check it

Save the postmortem as a markdown file in a private folder, outside any public repository. Run:

```bash
python3 <skill folder>/scripts/incident_check.py postmortem --file <private folder>/postmortem.md
```

Fix every FAIL and rerun until none remain. Read each WARN and either fix it or tell the user why you left it. Do not edit the numbers or the findings by hand. If the script errors, report the error. The blame-phrase check is a Proxy: it finds listed phrases only, so read the document for blame yourself.

### Step 6: Output

1. **Assumptions and unknowns:** what you could not confirm.
2. **The postmortem.**
3. **The check result.**
4. **Questions for the review meeting:** what did each person know and when, and what would have made the right action easier.

## Measure mode

### Step 1: Get the data

Ask for an export from the incident tracker or a list the user keeps. Build a CSV with these columns: `id`, `severity`, `started`, `detected`, `mitigated`, `resolved`, `detected_by`. Optional: `factor` (tags separated by semicolons), `postmortem_required`, `postmortem_published`. Times are UTC, `YYYY-MM-DD HH:MM`. Use opaque ids. For action items, an optional second CSV with `incident_id`, `due` and `status`.

If start times are estimates, tell the user that time to detect is then a Proxy.

### Step 2: Run

```bash
python3 <skill folder>/scripts/incident_check.py summary --incidents <private folder>/incidents.csv --as-of <today> [--actions <private folder>/actions.csv]
```

Use `--since` and `--until` for a quarter. Do not edit the output.

### Step 3: Read it honestly

Report medians and the longest value, not means. With fewer than 20 incidents, read the cases. Say which numbers are Measured and which are Proxy. Do not compare teams. Name one decision the numbers support, such as which detection gap to close first, and one thing they cannot tell the user.

### Step 4: Output

1. The summary the script printed.
2. A plain reading in under 150 words.
3. The three follow-ups with the most effect, each with an owner to be named.
4. A line for the [board update](https://github.com/leanpreneur/cto-os/blob/main/templates/board-update.md): customer-affecting incidents, count and total duration.
