---
name: ship-review
description: Use when asked to review code, a diff, a commit, a branch or a pull request, to check whether a change is ready to merge, matches its spec or stays in scope, or to audit a folder or whole repository for bugs, risks and bloat.
---

# Ship review

Review like the developer who gets paged when this breaks. In order of importance: **correct, safe, holds under the expected load, tested, fast enough, lean**. This skill reports findings and changes no code unless the user asks.

## 1. Pin what is under review

- What the user names: uncommitted or staged changes, a commit, a branch, a PR link, files, a folder or the whole repo.
- Nothing named: the uncommitted changes, or the last commit if there are none.
- For a branch, diff against the merge base: `git diff <base>...HEAD` (three dots). Check that the ref resolves and the diff is not empty before going further.
- Find the intent: the PR description, linked issue or spec, commit messages, the task in this conversation, or the user's one line. If none exists, state the intent you inferred from the diff and run the scope check against it, marked as inferred. Audits skip this.

## 2. Read beyond the diff

- Read the diff, then the code it touches: callers of every changed function, the functions it calls, the tests, the relevant docs.
- A change can break code it doesn't touch. When a signature, return value, data shape or behaviour changes, search for every caller.
- Trace the real flow: where data comes in, what is stored, what goes out.
- Work out the expected load from the README and deploy config (one person running a script, or many users and processes), and judge scale against that. State the load you assumed.
- For a whole repo or folder: map it first (README, build and deploy config, dependencies, entry points, tests), then go deep where a mistake costs most (user input, money, auth, data writes, background jobs, shared state). Say what you did not read.

## 3. Look for

1. **Bug:** wrong result, crash, missed edge case (empty, zero, last item, rounding, time zones, encoding), a caller broken by the change, a fix applied in one caller while the shared function stays broken, the same rule applied differently in two places.
2. **Risk:** injection, missing checks on user input, secrets in code, weak randomness, auth gaps, errors swallowed, writes in the wrong order or outside a transaction, data loss.
3. **Scale:** check-then-write races, the same work done by every process or request, lists or caches that only grow, a query per item, O(n²) on large input, per-process state that must be shared.
4. **Missing test:** risky new logic (a branch, a parser, money, security, data writes, a bug fix) with no test that would fail if it broke. One good test, not coverage.
5. **Speed:** big slowdowns are problems; small wins are nice-to-haves.
6. **Lean:** dead code; options nobody sets; a helper that duplicates one already in the repo (name its path); a dependency or code doing what the standard library already does; an abstraction with one implementation or a wrapper that only passes calls through; near-copies that must change together; one function doing several unrelated jobs (split by job, never by line count).
7. **Standards:** breaks a rule the repo documents (CONTRIBUTING, CLAUDE.md or AGENTS.md, a coding-standards doc) that tooling doesn't already enforce. Quote the rule.
8. **Spec** (when there is an intent or spec): requirements missing or only partly done; requirements that look done but are implemented wrong. Quote the requirement.
9. **Scope** (for diffs): files or hunks unrelated to the intent, added dependencies, renamed public functions or types, build or CI changes, whitespace-only churn. For each, say whether it belongs in this change, needs its own change, or needs a reason.

## 4. Check before you report

- Every finding needs a concrete case: "this input or situation leads to this wrong result". No case, no finding.
- Re-read the lines: the caller really exists, the value really can be empty, the code really is unused (search the whole tree, including tests, config and string or dynamic references).
- A shortcut marked `shortcut: <limit>, <upgrade>` is a decision, not a finding, unless the expected load already crosses it.
- Propose the smallest fix that works. Prefer fixes that delete code.
- Leave out style preferences the repo doesn't document, "consider…" suggestions, and vague worries.
- A big review can split into parallel subagents (for example correctness and security; spec and scope). Give each the diff command, the intent and this checklist, pasting sections 3 and 4 of this skill into each prompt, then merge and de-duplicate their findings yourself.

## 5. Report

Plain English: short sentences, everyday words. Explain a technical term the first time you use it, because the reader may never have seen this code.

Start with `What this change does:` (or `What this repo does:` for an audit) in two or three sentences, plus the load you assumed.

Then the findings in three groups, skipping empty groups and numbering across all of them so the user can say "fix 2 and 5":

- **Must fix:** bug, security, data loss, breaks at the expected load, a spec requirement missing.
- **Should fix:** risky code without a test, real slowness, duplication, a function that mixes jobs, a broken documented standard, scope creep, code that should not exist.
- **Nice to have:** small speed-ups, shorter forms.

Each finding has four parts, each one or two sentences:

```
2. **Orders land on the wrong day** (`billing/close_day.py:40-52`)
   - **What this is:** At midnight this job closes the day and bills all orders from that day.
   - **Problem:** It takes "today" from the server clock, which runs in UTC, so an order at 00:30 local time is billed on the previous day.
   - **Fix:** Compute the day once in the shop's time zone: `datetime.now(ZoneInfo(SHOP_TZ)).date()`.
   - **If we skip it:** Late-night orders show the wrong date and accounting fixes them by hand.
```

End with:
- `Verdict:` `Ship.`, or `Fix 1 and 3 first.` (audit: `Healthy.`, or what to fix first). For build and test claims in the verdict, run the checks per `evidence-before-done`.
- `Lean: -<N> lines possible.` when there are lean findings.
- `Not checked:` anything that mattered and could not be checked.

With nothing found: the opening line, then `Looks good. Ship.` (audit: `Healthy. Nothing to fix.`) and one line on what you checked. An audit lists at most 20 findings and says how many smaller ones it left out.

---
Adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) `ponytail-review` and `ponytail-audit` (MIT), [mattpocock/skills](https://github.com/mattpocock/skills) `code-review` (MIT), and the scope-creep-detector idea from [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) (Apache-2.0; idea only, no text or code reused). See CREDITS.md.
