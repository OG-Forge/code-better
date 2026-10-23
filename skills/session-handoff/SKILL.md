---
name: session-handoff
description: Use when the user asks for a handoff, a summary for a fresh session, or to continue the work elsewhere (another session, machine, tool, agent or person), or when the context window is nearly full mid-task and the work must carry on in a new session.
---

# Session handoff

Write a short document that lets a fresh agent, with none of this conversation, carry on the work without re-asking or re-doing anything.

## When a handoff is the right move

At the end of a phase you have five choices; pick the first that fits:

1. **Continue:** the next step needs what is in context and there is room. Costs nothing.
2. **Subagent:** a self-contained side task can run in its own context and report back.
3. **Clear:** nothing in this context matters to what comes next.
4. **Compact:** the same work continues in this tool and the history mostly matters as a summary.
5. **Handoff:** the work moves to a new tool, machine, folder or person, or a side task is being forked off mid-phase, or the user asked for one.

## Where to save it

The OS temp folder (`$TMPDIR` or `/tmp`; `%TEMP%` on Windows), named `handoff-<topic>-<YYYYMMDD-HHMM>.md`, unless the user names a place. A handoff for a colleague can go somewhere they can reach, if the user agrees. Tell the user the full path.

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
<paths, branches, commits, PRs, issues, specs, plans, commands to run; reference them, don't copy them>

## Suggested skills
<skills the next agent should load, e.g. build-plan, feedback-loop-debugging>
```

## Rules

- Reference artifacts that already exist (specs, plans, diffs, issues, commits) by path or link instead of repeating them.
- Keep the user's corrections and preferences from this session: they are what the next agent most needs and least can guess.
- Redact secrets, credentials, tokens and personal or customer data.
- If the user said what the next session is for, tailor the document to that and leave out the rest.
- Keep it under about 150 lines. A long handoff gets skimmed.

---
Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) `handoff` and its phase-boundary guidance (MIT). See CREDITS.md.
