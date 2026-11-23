# Example: a postmortem that fails the check, and the fix

**Made by:** script output. The two reports below are produced by `skills/incident-response/scripts/incident_check.py postmortem`, and are kept current by `scripts/build_examples.py --check`. The commentary is written by hand. ExampleCo and the incident are invented.

## The first draft

An engineering manager writes the postmortem the morning after, from memory. It reads fine.

```bash
python3 skills/incident-response/scripts/incident_check.py postmortem --file skills/incident-response/scripts/examples/postmortem-draft.md
```

<!-- output:postmortem-draft -->
> # Postmortem check: Customers could not export invoices
>
> **Result: FAIL** (2 failures, 5 warnings). Severity: SEV2. Detected by: customer. Action items: 2.
>
> | Measure | From impact start | Label |
> | --- | --- | --- |
> | Time to detect | 1 h 25 min | Measured from the times in the document |
> | Time to mitigate | 2 h 10 min | Measured from the times in the document |
> | Time to resolve | 3 h 30 min | Measured from the times in the document |
>
> Time to detect is only as good as the impact start time. If someone estimated it afterwards, read it as a Proxy.
>
> ## Findings
>
> - **FAIL** (action-due): Line 54: the action has no due date in the form YYYY-MM-DD. Found: ''.
> - **FAIL** (action-owner): Line 53: the action has no owner.
> - **WARN** (action-done-when): Line 53: the action has no 'done when' test.
> - **WARN** (blame-phrase): Line 18: 'human error'. Describe the conditions that made the action reasonable at the time.
> - **WARN** (impact-no-number): Impact has no number. Give customers affected, minutes, failed requests or money, or say what you could not measure.
> - **WARN** (no-detect-action): Detected by customer, not monitoring, and no action has type 'detect'. Add one that would have found it sooner.
> - **WARN** (one-factor): Only one contributing factor. Most incidents have several. Check detection, the change process, design, tooling and gaps between teams.
>
> Thresholds are defaults of this repository, not standards: at most 8 action items, due within 90 days of resolution, at least 4 timeline rows.
> The blame-phrase check is a Proxy. It finds the phrases it lists and cannot judge whether a postmortem is blameless. A person must read it.
<!-- end output -->

What the check caught:

- One action item has no owner and the other has no due date, so nothing makes anyone do them.
- The summary says "human error". That names a person's mistake as the cause and stops the investigation where it should start.
- One contributing factor. A migration that did not run is the trigger. The pipeline that let it through, and the missing alert, are the conditions.
- Customers found the problem first, and no action item would find it sooner.
- The impact has no number.

## The fix

The second pass asks why running the migration by hand made sense at the time, and what let it fail without anyone noticing. It adds four contributing factors, numbers for the impact, a detect item, and an owner, a date and a test for done on every action. The full text is in [postmortem-example.md](../../skills/incident-response/scripts/examples/postmortem-example.md).

```bash
python3 skills/incident-response/scripts/incident_check.py postmortem --file skills/incident-response/scripts/examples/postmortem-example.md
```

<!-- output:postmortem-fixed -->
> # Postmortem check: Customers could not export invoices
>
> **Result: PASS** (0 failures, 0 warnings). Severity: SEV2. Detected by: customer. Action items: 5.
>
> | Measure | From impact start | Label |
> | --- | --- | --- |
> | Time to detect | 1 h 25 min | Measured from the times in the document |
> | Time to mitigate | 2 h 10 min | Measured from the times in the document |
> | Time to resolve | 3 h 30 min | Measured from the times in the document |
>
> Time to detect is only as good as the impact start time. If someone estimated it afterwards, read it as a Proxy.
>
> No findings.
>
> Thresholds are defaults of this repository, not standards: at most 8 action items, due within 90 days of resolution, at least 4 timeline rows.
> The blame-phrase check is a Proxy. It finds the phrases it lists and cannot judge whether a postmortem is blameless. A person must read it.
<!-- end output -->

The check passes. It does not say the postmortem is right. It cannot tell whether the contributing factors are the true ones or whether the document is blameless. The review meeting does that, with everyone who took part in the room.

The three times are Measured from the document. Time to detect is only as good as the impact start time. If someone estimated that afterwards, read it as a Proxy.
