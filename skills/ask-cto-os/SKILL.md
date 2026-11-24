---
name: ask-cto-os
description: Use when an engineering leader describes a situation and does not know which CTO OS skill or document to use, when the request is vague, or when they ask what CTO OS can do. Reads a routing table, names the skill or document to start with, says what they will get, and offers to run it.
---

# ask-cto-os

Route a situation to the right CTO OS skill or document. The routing table is `references/routes.json`. It lists every situation, the skill to start with, what to run next, which documents to read, and what CTO OS does not cover yet. Use only what is in that table.

## Step 1: Get the situation

If the user has already described what is happening, skip this step. Otherwise ask one question and nothing else:

"What is happening, in a sentence or two, and what do you need to have by when?"

## Step 2: Match

Read `references/routes.json`. Choose the one situation that fits best.

Optionally run the keyword matcher for candidates. It needs `python3` only:

```bash
python3 <skill folder>/scripts/check_routes.py match --text "<the user's words>"
```

The matcher counts keywords. It does not understand meaning. If its top result disagrees with what the user means, go with the meaning and say which situation you chose.

If two situations fit equally, name both, say which comes first and why.

If the user asks what CTO OS can do, list the situations in one line each, grouped as: starting a role, working with the CEO and the board, measuring, hiring and leveling, and decisions. Then ask which one is theirs.

## Step 3: Answer

Reply in under 150 words, in this shape:

**Your situation:** one line, in the user's own words.

**Start with:** the skill, written as `/skill-name` (`$skill-name` in Codex, a plain description in Gemini CLI), or the document. One sentence on why.

**You will get:** from `you_get`.

**Then:** at most two next steps from `then`, each with one clause on when to use it.

**To start I need:** the question from `ask_first`.

End with: "Say go and I will run it."

## Step 4: Run it when the user says go

- If `start_with` is a skill, load it with your tool's skill mechanism and follow it. If you cannot load it, tell the user to run `/skill-name`, or `$skill-name` in Codex. In Gemini CLI, tell them to describe the task so the skill activates. Some skills have modes, such as build, measure, level a person, plan and debrief. `you_get` says which mode fits, so tell the skill.
- If `start_with` is null, open the first document in `read` and walk the user through the part that applies, in plain words. The documents live in the cto-os repository. If it is not on disk, give the user the link `https://github.com/leanpreneur/cto-os/blob/main/<path>`.
- Do not run a skill before the user says go, unless the message already asked you to run it.

## When nothing fits

- If the topic matches an entry in `gaps`, say CTO OS does not cover it yet. Name the closest artifact only if the table gives one. Offer ordinary help with the topic, and do not present it as a CTO OS artifact.
- If no situation and no gap fits, say so, ask one question about the user's role and problem, and route again.

## Rules

- Name only skills and documents that appear in `references/routes.json`. Never invent one.
- Plain, direct language. No filler and no hedging.
- Do not guess the user's company stage or role. Ask once if it changes the route.
- Do not recommend a vendor. Recommend practices.
