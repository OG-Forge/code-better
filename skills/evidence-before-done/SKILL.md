---
name: evidence-before-done
description: Use when about to say work is done, fixed, passing, working or ready, before committing, pushing, opening a PR or handing results to the user, and when relaying a subagent's or tool's report of success.
---

# Evidence before done

A claim about the state of the work needs evidence produced after the last change it covers. "It should work" is a guess, not a status.

## The gate

Before any claim of success:

1. **Identify** the command or check that proves the claim.
2. **Run** it now, after your last edit. A run from before a change doesn't count. If the full check is too slow or needs something you lack (CI, credentials, hardware), run the relevant subset and report the full check as not run, with its command.
3. **Read** the result: exit code, pass and fail counts, every failure and warning. For long output, redirect it to a file and read the summary and the failures.
4. **Compare** the output with the claim.
5. **Report** the result with the evidence: the command and the line that proves it. If the output disagrees with the claim, report the actual state.

## What proves what

| Claim | Evidence that proves it | Not enough |
|---|---|---|
| Tests pass | Fresh test run: 0 failures, exit 0 | An earlier run; "the change is small" |
| Build or typecheck succeeds | The build or typecheck command: exit 0 | Lint passing; the editor shows no errors |
| Bug is fixed | The original reproduction now passes | The code changed; a different test passes |
| Regression test works | You saw it fail without the fix (stash or comment out only the fix, then restore it) and pass with it | It passes once |
| Feature works | Ran it the way a user would: the UI, the endpoint, the CLI | Unit tests alone, for a user-visible feature |
| Subagent or tool finished the job | The diff, files or output it produced, checked by you | Its own success message |
| Requirements met | Each requirement checked off, line by line | Tests passing |

## When you can't verify

Say exactly what you could not check and why ("no database in this environment, so the migration was not run"). Give the command the user can run to check it. Never round an unverified item up to "done".

## How to report

- Lead with the true state: what was done and verified, what failed, what was not checked.
- Show the evidence briefly: the command and the decisive output line.
- Skip celebration before verification. "Great, all done!" followed by a failing test costs trust.
- End with one or two lines: what you did not check, and any risk.

## Red flags

| You notice | Do instead |
|---|---|
| "should", "probably", "seems to" in your draft | Run the check, then state the result |
| About to commit, push or open a PR | Run the gate first |
| A subagent said "all tests pass" | Look at the diff and run the tests yourself |
| You ran only the one test you changed | Run the related suite too |
| You are tired of the task and want to wrap up | Run the gate anyway |

---
Adapted from [obra/superpowers](https://github.com/obra/superpowers) `verification-before-completion` (MIT), with the closing line from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT). See CREDITS.md.
