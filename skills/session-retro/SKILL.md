---
name: session-retro
description: Use when the user asks for a retrospective or retro on a coding session or a set of past sessions, asks why an agent session went badly or took so long, or wants to improve the agent's setup (instruction files, checks, tooling, skills) based on what happened.
---

# Session retro

Look back at what happened in one or more agent sessions and propose changes to the **environment** (checks, instruction files, docs, tooling, skills) so the next session goes better. The code itself is not the subject.

## 1. Gather the evidence

- Default to the current session. If the user names a past session or a time range, read the logs. Claude Code: `~/.claude/projects/<working directory with every character other than a letter or digit turned into ->/<session-id>.jsonl` (one JSON event per line), plus subagent logs in `<session-id>/subagents/`. Codex: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`. For other tools, find their history folder or ask. Confirm a past session by its first prompt and timestamp, not by recency alone; if several match, ask.
- Logs are large and one line can exceed 1 MB. Measure first (`wc -lc`). Never print a log or whole grep matches: get line numbers (`grep -n ... | cut -d: -f1`), then pull small pieces from those lines (`sed -n '<N>p' file | cut -c1-500`, or `jq` for single fields). Never modify a session file.
- Only prompts the human typed count as the user. Tool results, hook output and system reminders also appear as user records; in a subagent's log, "user" is the parent agent.
- Look for the user correcting or repeating an instruction, tool errors, edits that were reverted, the same command failing repeatedly, long stretches spent searching for something, claims of "done" followed by failures, and expensive tool calls.
- Read the repo's instruction files (CLAUDE.md, AGENTS.md, rules folders) and the user's global ones (`~/.claude/CLAUDE.md`, memory files, `~/.codex/AGENTS.md`), its check commands (package scripts, Makefile, pre-commit, CI workflow) and the skills that were loaded.
- Redact secrets and personal or customer data in anything you quote.

## 2. Find the candidates

Check each category; skip the ones with no evidence.

- **Automated checks.** Could a lint rule, type check, test, pre-commit hook or CI job have caught a mistake the agent made? Check whether such a check already exists but isn't wired up or is broken; that is the finding then. A repo with no pre-commit hook and no CI running its lint, typecheck and tests is a finding by itself. **Mechanical rules** (a banned API, an import shape, a file location, a required command) become checks, not prose.
- **Navigation.** Did the agent spend a long time finding a file, a command or a concept? One pointer line in the instruction file or a short doc would fix it.
- **Instruction files.** Instructions the agent ignored (reword them as the positive behaviour you want, or turn them into a check); instructions that change nothing the agent wouldn't do anyway (delete them); a file so long that rules get lost (move detail into docs it points to).
- **Coding standards.** Judgement-call rules the reviewer should apply; better enforced at review time than loaded into every session.
- **Information access.** Something the agent needed but could not see: dev server logs, a test database, read-only access to a service, docs.
- **Tool economy.** Tool calls or commands that dumped huge output or were repeated: redirect output to a file, add a narrower script, or write a cheaper command.
- **Skills.** A recurring workflow that deserves a skill, or a skill that fired when it shouldn't (or didn't fire when it should).

## 3. Report

Most severe first. For each candidate:

```
N. **<short title>** (<category>)
   - What happened: <one or two sentences, with a session reference or a short redacted quote>
   - Cost: <time, tokens, rework or risk it caused; take figures from log timestamps and usage fields, or say "not measured">
   - Change: <the exact change: the rule text, the hook command, the pointer line, the script>
   - Where: <the file it goes in>
```

End with the three changes that would help most. Make changes only after the user picks them. Then make the smallest version of each, and verify any new check by running it.

---
Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) `retro` (MIT), with log-reading safety from [obra/superpowers](https://github.com/obra/superpowers) `diagnosing-superpowers` (MIT). See CREDITS.md.
