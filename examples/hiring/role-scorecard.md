# Example: role scorecard

**Made by:** written by hand, to show a filled [role scorecard](../../templates/role-scorecard.md). ExampleCo is invented. The numbers are made up.

## Role Scorecard: Senior Backend Engineer, E3

| Field | Value |
| --- | --- |
| Hiring manager (decision owner) | Head of Platform |
| Team and stack | Billing platform, 6 engineers, Python and Postgres, queue-based workers |
| Level | E3 |
| Pay band | Set from market data, approved before posting |
| Reports to | Head of Platform |
| Opened | 2026-11-02 |
| Target start | 2027-01-18 |

### Mission

Own the billing platform so customers are charged correctly and finance can close the month in two working days.

### Outcomes at 12 months

| # | Outcome | How we will see it |
| --- | --- | --- |
| 1 | The monthly invoice run finishes in under 2 hours, down from about 9 | Run duration in the job dashboard, last three runs |
| 2 | No duplicate customer charges in a quarter, down from 3 in the last quarter | Support tickets tagged "double charge", reviewed monthly |
| 3 | Two other engineers can ship billing changes without help | Two engineers with merged billing pull requests and no escalations |

### Competencies

| Competency | Definition in observable behavior | Meets the bar at E3 | Must-have or trainable | Tested in |
| --- | --- | --- | --- | --- |
| Technical judgment | Picks the simplest design that meets the constraints and says what it gives up | Names the constraint that decided the choice and one cost they accepted | Must-have | sample, design |
| System design | Breaks a problem into parts, finds the bottleneck, plans for failure | Raises duplicate delivery and retries without being asked | Must-have | design, cross |
| Delivery and ownership | Gets work to production, tells people early when it will slip | Splits a multi-month project into releases and reports slips with options | Must-have | sample, collab, manager |
| Engineering with AI | Gives the tool the right context, checks the output, owns what ships | Names a specific error they caught in AI-written code | Must-have | sample, manager |
| Collaboration and communication | Disagrees usefully, explains trade-offs to non-engineers | Explains a trade-off so a product partner can choose | Trainable | collab, manager, cross |

### Not a fit if

- Needs a fully defined backlog every week.
- Wants to work only on new features and avoid on-call.

### What candidates will ask

- Team size, stack and how the team makes decisions: six engineers, decisions written as short decision records.
- On-call and incident load: one week in six, about two pages a week on average. Check the real number before the first interview.
- The biggest problem the team has right now: the invoice run is slow and one engineer holds most of the knowledge.
- Remote and location policy: remote within the US time zones.
- Pay range, as the posting must state it where the law requires: stated in the posting.
- How AI tools are used and the AI policy for this loop: engineers use AI tools daily. The loop allows them and observes how they are used.

### Checks before posting

- [x] Two people who never discussed the role would score each competency the same way.
- [x] Every must-have competency is tested in two interviews, by two different people.
- [x] The level matches the ladder and the outcomes fit that level.
- [x] The pay band is approved.
- [x] The AI policy for the loop is written.
- [x] The interviewers are named and trained.
