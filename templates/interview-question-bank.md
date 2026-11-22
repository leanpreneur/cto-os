---
name: interview-question-bank
status: draft
use: pick questions for each interview in the loop plan
---

# Interview Question Bank

Two questions per competency, with follow-ups and what strong and weak answers sound like. Pick the competencies from your [role scorecard](role-scorecard.md). Ask the same questions of every candidate for the role.

How to use it:

- Ask the question as written. Use the follow-ups in order, and stop when you have evidence.
- Ask for the candidate's own part: "what did you do," not "what did the team do."
- Write down what they said and did. Score afterwards against the rubric below.
- The signals are examples. A strong answer that does not match them can still be strong, so score the evidence.

## Rubric for every competency

| Score | Meaning |
| --- | --- |
| 1 | Evidence below the bar for the level, or evidence against |
| 2 | Partial. Some evidence, with gaps in the core of the competency |
| 3 | Meets the bar for the level. Specific, first-person evidence of doing it |
| 4 | Exceeds the bar. Evidence at the next level, confirmed by results |

## Technical judgment

**Q1. Tell me about a technical decision you made where the obvious choice was wrong.**
Follow-ups: What made you look past the obvious choice? What did it cost? What would you do now?
- Strong: names the constraint that changed the answer, the options they dropped and why, and a cost they accepted.
- Weak: describes a tool they liked. No trade-off. No cost.

**Q2. When did you last choose the simpler solution over a better one? Why?**
Follow-ups: Who disagreed? How did you know it was safe to be simple?
- Strong: ties the choice to scale, time or reversibility, and says what would make them revisit it.
- Weak: cannot say what they gave up.

## System design

Use a problem your team really solved, anonymized. State the requirements in two minutes, then let the candidate lead.

**Q1. Design [a system your team built, with its real constraints].**
Follow-ups: Where does it break first? What do you measure? Now double the load. Now the main data store goes down for ten minutes.
- Strong: asks about requirements before drawing, names numbers, finds the bottleneck, discusses failure modes unprompted, changes the design when requirements change.
- Weak: starts with technology names. No numbers. Treats the happy path as the design.

**Q2. Here is a design that has a flaw. Find it.**
Prepare a short design with one real flaw, such as a retry loop that can duplicate a payment.
Follow-ups: How would you fix it? How would you test the fix?
- Strong: finds the flaw by reasoning about failure, asks what the system guarantees, proposes a fix with its own trade-off.
- Weak: comments on style. Misses the flaw.

## Delivery and ownership

**Q1. Tell me about a project that slipped. When did you know, and what did you do?**
Follow-ups: Who did you tell first? What did you cut? What did you change afterwards?
- Strong: knew early, told people early, offered options with costs, changed how they plan.
- Weak: blames others. Learned about the slip when it was due.

**Q2. Describe the last time you cut scope. How did you decide what to cut?**
Follow-ups: What did the customer or product partner say? Did the cut hold?
- Strong: uses the customer problem to choose, agrees the cut with the owner, writes down what is left out.
- Weak: cuts quality, not scope. Decides alone.

## Debugging and production sense

**Q1. After a deploy, p95 latency doubled and a rollback is not possible. Walk me through your next hour.**
Follow-ups: What do you look at first? What do you tell customers or support? When do you stop investigating and act?
- Strong: protects customers first, forms a hypothesis from a recent change, narrows with data, communicates on a schedule.
- Weak: guesses. Changes several things at once. Nobody is told.

**Q2. Tell me about the hardest production bug you found. How did you find it?**
Follow-ups: What did you rule out? What did you change so it would not recur?
- Strong: methodical, names dead ends, leaves behind a test, an alert or a fix to the process.
- Weak: "I just stared at the logs." No lasting change.

## Collaboration and communication

**Q1. Tell me about a technical disagreement with a peer. What happened?**
Follow-ups: What evidence did each of you have? How did it end? What would you change?
- Strong: represents the other view fairly, used evidence, committed after the decision.
- Weak: the other person was wrong. No change in their own behavior.

**Q2. Tell me about a time you gave hard feedback to someone.**
Follow-ups: What did you say, in your words? How did they react? What happened next?
- Strong: specific and kind, about behavior, followed up.
- Weak: avoided it, or delivered it as a verdict.

## Learning and adaptability

**Q1. What is something you were bad at two years ago that you are better at now? How did you get better?**
Follow-ups: How did you know you were bad at it? Who helped?
- Strong: names a concrete skill, the feedback that showed the gap and the practice that closed it.
- Weak: names a strength in disguise.

**Q2. Tell me about the last time you worked in a system or language you did not know.**
Follow-ups: How did you get productive? What did you get wrong?
- Strong: reads the code and the history, asks specific questions, shares what they learned.
- Weak: waited to be taught.

## Engineering with AI

**Q1. Walk me through the last meaningful change you shipped with AI help. What did you give the tool, what did you check, and what did it get wrong?**
Follow-ups: How do you decide whether to trust output in an area you do not know well? What would you do differently if the change touched payments or personal data?
- Strong: names the context they gave (a spec, tests, files, conventions), the checks they ran, one specific error they caught, and what they will not delegate.
- Weak: "It writes most of my code." No verification. Cannot name a mistake.

**Q2. Work sample: review this AI-generated pull request.** Prepare a pull request with planted defects: a silently swallowed error, a test that asserts nothing, a dependency nobody needs, and one requirement the code misses.
Follow-ups: What would you block? What would you ask the author or the agent to change? What would you add to the repository so the agent gets it right next time?
- Strong: finds the empty test and the missed requirement, asks what the requirement was, proposes a context or test change that prevents a repeat.
- Weak: comments on formatting. Approves because the tests pass.

## Product and customer sense

**Q1. Tell me about a time you pushed back on a feature. What evidence did you use?**
Follow-ups: What did the product owner say? What happened?
- Strong: uses customer data or cost, proposes an alternative, accepts the final call.
- Weak: pushes back on taste.

**Q2. Tell me about a customer problem you learned about directly. What did you change because of it?**
Follow-ups: How did you find out? How did you know it was fixed?
- Strong: spoke to or watched a customer, changed priorities, checked the result.
- Weak: relies on someone else's summary. No change.

## Leadership and people (staff and managers)

**Q1. Tell me about someone on your team who was underperforming. What did you do in the first 30 days?**
Follow-ups: What did you write down? What did you say to them? How did it end?
- Strong: gave clear, specific feedback early, set expectations in writing, followed up, made a decision on time.
- Weak: waited. Escalated to HR first. Cannot say what the person was told.

**Q2. Tell me about a hire you regret. What did the loop miss?**
Follow-ups: What did you change in how you hire?
- Strong: owns the miss, names the signal they ignored, changed a practice.
- Weak: no regrets, or blames the candidate.

**Q3 (managers). How do you decide what your team will not do?**
Follow-ups: Who hears about it? Give an example.
- Strong: ranks by outcome, says no in writing with a reason, revisits on a schedule.
- Weak: says yes to everything and works the team harder.

## Motivation and fit (screen only)

**Q1. What would make this role a good move 18 months from now?**
**Q2. What are you looking for that you do not have today?**
Score for clarity and for whether the role can give them what they name. This is not a competency score. It is a go or stop signal.
