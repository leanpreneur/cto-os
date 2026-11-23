---
name: leveling
status: early
audience: CTO or VP Engineering who needs a career ladder, or who inherited levels that nobody can explain
---

# Leveling: One Ladder, Written Down

**Outcome:** a published ladder that describes scope and behavior at each level, a calibration process that applies it the same way to everyone, and a promotion process people trust.

Without a written ladder, levels come from who negotiated best at hire. Titles drift upward, promotions look political, and you cannot tell a candidate what the job is. Leveling comes before [hiring](hiring.md), because every scorecard needs a level to test against.

## Ground rules

1. **Levels describe scope and behavior.** They do not describe tenure, hours or volume of output.
2. **One ladder, written down, visible to everyone** who is levelled by it.
3. **Two tracks with the same standing:** individual contributor and manager. Moving into management is a change of job, not a promotion.
4. **Evidence over impressions.** A level decision rests on dated examples of work.
5. **Promote for sustained work at the next level.** This repo's default is at least two quarters.
6. **Levels are internal. Titles are external.** A title is cheap to give and costly to take back.
7. **Check the results for fairness with data every cycle.**

## Step 1: Choose how many levels

Fewer levels are easier to apply. Add a level only when you can describe how it differs from its neighbors.

| Engineering headcount | Levels to publish | Typical titles |
| --- | --- | --- |
| Under 15 | E2, E3, E4 and M1 | Engineer, Senior Engineer, Staff Engineer, Engineering Manager |
| 15 to 60 | E1 to E5 and M1 to M3 | Adds Junior Engineer, Senior Staff Engineer, Senior Engineering Manager, Director |
| Over 60 | E1 to E6 and M1 to M4 | Adds Principal Engineer, VP Engineering |

These bands are this repo's judgment and are Early.

## Step 2: Define the axes

The [starter ladder](../templates/leveling-ladder.md) uses six axes. Each level is described on every axis.

| Axis | The question it answers |
| --- | --- |
| Scope | How big is the problem this person owns? |
| Ambiguity | How much of the problem do they have to define themselves? |
| Delivery | How reliably do they get results to customers, and how do they handle risk? |
| Craft (managers: People and craft) | How good is the work, and for managers, how well do they build and develop a team? |
| Influence | Whose work do they change, and how? |
| Engineering with AI | Do they direct AI tools well, verify the output and own what ships? |

The AI row expects judgment, not tool usage. Counting prompts or tool seats tells you about spend. At each level it asks the same thing at a bigger scope: verify, own and set the practice. It is one input to the culture and skills dimension of the [ADOPT assessment](adopt-assessment.md).

## Step 3: Write the level descriptions

Start from the starter ladder and replace its examples with facts from your company. Keep each description to what a person at that level does that the level below does not.

**Test before you publish.** Pick three engineers you know well. Have two managers place each one on the ladder alone. If they disagree on a person, find the sentence that let them disagree and rewrite it.

## Step 4: Staff and above

Do not make one shape of staff engineer the standard. Will Larson describes four archetypes: Team Lead, who guides a team's technical approach and delivery, Architect, who owns the direction of a critical domain, Solver, who works on the hardest problems leadership has prioritized, and Right Hand, who extends an executive's reach on organizational problems. The ladder should describe the level of impact. A person can be an Architect now and a Solver next year.

Staff levels are where companies promote by attrition or by politics. Ask of every staff candidate: what problem did the organization have that only this person could have resolved, and how do we know it was resolved?

## Step 5: Managers

Camille Fournier's *The Manager's Path* walks the sequence from mentoring and tech lead through managing a team, managing multiple teams and managing managers. Use it as a map for what changes at each step.

| Level | Typical span | Owns |
| --- | --- | --- |
| M1 Engineering Manager | 4 to 8 engineers | One team |
| M2 Senior Engineering Manager | Up to about 12 to 15 engineers, or two teams | A larger team or two teams |
| M3 Director | 2 to 5 teams, through managers | An area, its budget and org design |
| M4 VP or Head | Several directors | The function, and its story to the CEO and the board |

Spans are this repo's defaults, not standards. Adjust for how senior the engineers are and how much of the manager's time goes to hiring or to hands-on work.

Before anyone moves into management, give them a trial of the work: leading a project with other people's results counting as theirs. Make it easy to move back without loss of standing.

## Step 6: Attach pay bands

1. Set one band per level from market data you collect or buy. Do not copy a number from a public ladder or a salary site without checking it.
2. Overlap adjacent bands. A strong E3 can earn more than a new E4.
3. Decide how manager and IC bands relate, for example that M1 sits in the E3 to E4 range, and write it down.
4. Decide whether levels and bands are visible to everyone. Several US states and cities require pay ranges in job postings. Check the rules where you hire.

Do not let pay set the level. If someone cannot be paid at their level, say so and fix the band.

## Step 7: Calibrate twice a year

Calibration is the meeting where managers compare people to the ladder, so that Team A's E3 and Team B's E3 mean the same thing.

1. **Before:** each manager writes evidence for each person against the ladder. Use the [promotion packet](../templates/promotion-packet.md) for anyone proposed to move.
2. **In the room:** a director or the CTO chairs. Read evidence level by level. Compare each person to the ladder, not to each other.
3. **Challenge the evidence, not the manager.** "What is the dated example of that?" is the standard question.
4. **Check the shape:** the count by level, and by team. Look at where promotions concentrate.
5. **After:** record decisions and reasons. Tell each person, in a conversation, before anything is published.

Calibrate before compensation decisions, never after.

## Step 8: Run promotions

1. **Fixed dates, twice a year.** Off-cycle promotions only as a documented exception, such as a retention case.
2. **Nominate:** the manager or the person starts it.
3. **Write the packet:** evidence by axis, dated, with outcomes. Three to five peer inputs, at least one from another team.
4. **Decide against the ladder.** The question is "has this person worked at the next level for two quarters or more?" and not "do they deserve it?"
5. **Tell everyone.** People who are not promoted get the gaps in writing, with the specific evidence that would change the answer.

## Step 9: Level candidates and new hires

Level the candidate from [loop](hiring.md) evidence against the same ladder. Decide the level before the offer, and tell the candidate the level and why in the pre-offer call. Do not raise a level because the candidate pushes. Raise it only if they give new evidence. If you offer below the level they asked for, say so early and explain what evidence would reach the higher level.

## Hard conversations

**"Not yet" on a promotion.** Say the decision first. Then the evidence at the current level that is strong. Then the one or two gaps against the next level, with a dated example of each. Then what evidence would change the answer, and when you will look again. Do not give a reason you cannot support with an example.

**A level below the one the candidate wanted.** "We would put this role at E3 for these reasons: [evidence from the loop]. For E4 we would need to see [specific evidence]. Here is how we would look at that in six months."

**Title and level differ.** If you give a title above the level, you will take it back later or live with it. Do not do it.

## Check the health of the ladder

| Measure | What to look for |
| --- | --- |
| Count by level | A shape that is top-heavy, or has no level between junior and senior |
| Time since last promotion, by level | Many people stuck, or promotions at a steady pace with no one stuck |
| Promotion rate per cycle, by group, where collected lawfully | Gaps that persist across cycles |
| Regretted attrition by level | One level that people leave at much more often |
| Hired in versus promoted, by level | A level you can only fill from outside, or only from inside |
| Span of control, and layers | Managers with one or two reports, or with more than ten |

The `/leveling-ladder` skill computes the count, span, layers and time-in-level measures from a roster file, labels each as Measured, and does not print anything about a group smaller than five people. The thresholds are defaults of this repository, not standards, and the readings above are Early.

## What not to do

- **Do not use the ladder as a checklist.** A person does not need every sentence at a level. They need the pattern.
- **Do not count years.** Time in role is a health measure, not an entry rule.
- **Do not promote to retain someone,** except as a recorded exception with the reason.
- **Do not level people in secret.** People should know their level and what next-level evidence looks like.
- **Do not hand managers the ladder without training.** One hour on how to write evidence and run calibration is enough to start.

## Definition of done

- The ladder is written, with every level described on every axis.
- Three real engineers were placed by two managers independently, and the results agree.
- Each level has a pay band, and the manager and IC relationship is written down.
- Calibration and promotion dates are on the calendar for the next two cycles.
- Managers have been trained.

## How you will know it worked

- Leading indicator: the share of promotion packets that carry dated evidence against the ladder for every axis, and the share of people who can say their level and what evidence the next one needs.
- Lagging indicator: regretted attrition by level, and the agreement between two managers placing the same person, checked each cycle.

## Sources

- Camille Fournier, *The Manager's Path* (O'Reilly, 2017): chapters on mentoring, tech lead, managing a team, managing multiple teams and managing managers.
- Will Larson, [Staff engineer archetypes](https://lethain.com/staff-engineer-archetypes/): Team Lead, Architect, Solver and Right Hand.
- Dropbox, [Engineering Career Framework](https://dropbox.github.io/dbx-career-framework): a public ladder for comparison. Its page states no license, so the starter ladder in this repo was written without copying it.
- swyx, [Every public engineering career ladder](https://swyx.io/career-ladders): an index of public ladders.
- The level bands by headcount, the typical spans, the two-quarter default, the six axes and the health readings are this repository's judgment. They are Early and have not been validated in real engagements.
