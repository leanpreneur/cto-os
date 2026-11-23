# Example: org shape report

**Made by:** script output, plus the questions at the end, which are written by hand. The report is produced by `skills/leveling-ladder/scripts/org_shape.py` on a synthetic roster of 29 people with opaque ids, and kept current by `scripts/build_examples.py --check`. The roster is `skills/leveling-ladder/scripts/examples/roster-example.csv`.

```bash
python3 skills/leveling-ladder/scripts/org_shape.py \
  --roster skills/leveling-ladder/scripts/examples/roster-example.csv \
  --as-of 2026-11-22 --show-ids
```

`--show-ids` lists the opaque ids of flagged managers. It is off by default. The report hides any group under five people, which is why most levels are combined into one row.

<!-- output:org-shape -->
> # Org shape, as of 2026-11-22
>
> **Headcount:** 29 (23 on the IC track, 6 on the manager track). **Layers:** 4. **Managers with reports:** 6. **ICs per manager:** 3.83.
>
> All numbers are Measured from the roster you gave, and are only as good as the roster.
>
> ## Levels
>
> | Level | People | Share | Median months in level | Share over 36 months in level |
> | --- | --- | --- | --- | --- |
> | E2 | 16 | 55.2% | 18.0 | 0.0% |
> | E3 | 5 | 17.2% | 24.0 | 20.0% |
> | Levels with fewer than 5 people each, combined | 8 | 27.6% | hidden | hidden |
>
> Time in level counts from the last promotion, or the start date if the person was never promoted.
>
> ## Spans and layers
>
> | Measure | Value |
> | --- | --- |
> | Direct reports per manager, min / median / max | 1 / 4.5 / 11 |
> | Managers with fewer than 3 reports | 2 |
> | Managers with more than 10 reports | 1 |
> | Manager track, no reports | 0 |
> | IC track, with reports | 0 |
>
> Layer sizes, top to bottom: layer 4: 23. Layers with fewer than 5 people are not shown.
>
> ## Ids to look at
>
> - thin span: cto, mgrC
> - wide span: mgrD
> - manager track without reports: none
> - ic track with reports: none
>
> ## How to read this
>
> These are questions, not verdicts. Examples: a manager with one report may be a lead who needs a different role; a manager with more than ten reports may have no time for feedback; many people over the time-in-level threshold at one level may mean promotions stall there. Ask the managers before you conclude anything.
>
> Defaults of this repository, not standards: thin span under 3, wide span over 10, time in level over 36 months, and groups under 5 people are not broken out. Hiding small groups stops casual reading. It is not anonymization. Keep this report private.
<!-- end output -->

## Questions this report raises

These are questions for the managers, not conclusions.

1. **`mgrC` has one report.** Is this a lead who will grow a team, or a manager role that does not need to exist yet? The top of the tree also shows up as thin, because it has one report. That one is not a finding.
2. **`mgrD` has 11 reports.** Who gives each of them weekly feedback and reviews their work? Is a tech lead or a second manager needed?
3. **16 of the 29 people are at E2.** The levels table shows only E2 and E3. Eight people sit in groups that the report does not break out. Ask who holds the senior technical roles for design reviews.
4. **One in five E3 engineers has been over 36 months at the level.** With five people, one person moves the share by 20 points. Ask that manager what is happening before you read anything into it.
5. **Four layers for 29 people.** Ask whether each layer between the CTO and the engineers adds something that a direct line would not.

What this report cannot show: promotion rates by group, regretted attrition, and how well anyone performs. Those need other sources, and the `/leveling-ladder` skill lists them as Unknown.
