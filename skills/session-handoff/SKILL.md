---
name: session-handoff
description: Use when the user asks for a handoff, a summary for a fresh session, or to continue the work elsewhere (another session, machine, tool, agent or person), or says the context is filling up and asks to set up the next session.
---

# Session handoff

Write a short document that lets a fresh agent, with none of this conversation, carry on the work without re-asking or re-doing anything.

## If the user asked for a handoff

Write it. The list below is only for when you are choosing what to do at the end of a phase, or the user asks which move to make.

## Choosing at a phase boundary

Mid-phase there is no choice to make: carry on, or split the rest into subagents. At the end of a phase, rule these out in order:

1. **Continue:** the next phase needs this conversation as its source, or there is plenty of room. Costs nothing.
2. **Clear:** nothing here matters to what comes next. Cheapest, but if it did matter, the "why" is lost for good.
3. **Handoff:** the work moves to a new tool, machine, folder or person, or a side task is forked off mid-phase.
4. **Subagent:** a tightly scoped task that can run with nobody steering, reporting back here.
5. **Compact:** the default when nothing above fits; say what the next phase needs kept.

You can't clear or compact yourself. Tell the user which command to run and why (in Claude Code, `/clear`, or `/compact <what to keep>`).

## Where to save it

The OS temp folder (`$TMPDIR` or `/tmp`; `%TEMP%` on Windows), named `handoff-<topic>-<YYYYMMDD-HHMM>.md`, unless the user names a place. When the work moves to another machine or a colleague, also offer a place they can reach (a repo branch, a shared folder, or paste the content), if the user agrees. Tell the user the full path and a one-line prompt to start the next session, for example: "Read <path> and continue from Next steps."

## What goes in

```markdown
# Handoff: <topic>

## Goal
<what the user wants and why, in their words where possible>

## State
- Done (verified): <item> - <how it was verified>
- Done (not verified): <item>
- In progress: <item> - <exactly where it stopped>
- Not started: <item>

## Decisions made
<decision> - <reason> - <who decided: the user or the agent>

## Open questions and risks
<anything unresolved, with what is known about it>

## Next steps
1. <the very next action, specific enough to start without asking>
2. ...

## Pointers
<paths, branches, commits, PRs, issues, specs, plans, commands to run>

## Suggested skills
<skills the next agent should load, e.g. build-plan, feedback-loop-debugging>
```

## Rules

- Under Pointers, reference artifacts that already exist (specs, plans, diffs, issues, commits) instead of repeating them.
- Keep the user's corrections and preferences from this session: they are what the next agent most needs and least can guess.
- Redact secrets, credentials, tokens and personal or customer data.
- If the user said what the next session is for, tailor the document to that and leave out the rest.
- Keep it under about 150 lines. A long handoff gets skimmed.

---
Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) `handoff` and its phase-boundary guidance (MIT). See CREDITS.md.
