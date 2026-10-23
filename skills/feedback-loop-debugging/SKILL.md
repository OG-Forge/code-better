---
name: feedback-loop-debugging
description: Use when something is broken, throwing, failing, flaky, slow or behaving unexpectedly (a bug report, a failing test or CI job, a regression, a production error), and before proposing any fix for it.
---

# Feedback-loop debugging

No fix before a cause, and no cause before a loop that shows the bug. With a fast command that goes red on this exact bug, finding the cause is mechanical. Without one, staring at code is guessing.

## Safety first

Redact every secret in what you show: write `<REDACTED>`. Read credentials from environment variables in any script you build. Quote only the log lines that carry the signal. Do not change shared or production systems to debug without asking.

## Phase 1: build a loop that goes red

Find the cheapest way to trigger the bug on demand. Try, roughly in this order:

1. A failing test at whatever level reaches the bug (unit, integration, end-to-end).
2. A curl or HTTP script against a running dev server.
3. A CLI call with a fixture input, diffed against known-good output.
4. A headless browser script (Playwright or similar) that asserts on the DOM, console or network.
5. Replaying a captured request, payload or event log through the code path.
6. A throwaway harness: the smallest slice of the system that runs the failing path.
7. A fuzz or property loop for "sometimes wrong" bugs.
8. A bisect script (`git bisect run`) when the bug appeared between two known states.
9. A differential run: old version against new, or two configs, diffing the output.
10. Last resort: a step-by-step script that asks a human to do the part only they can, and captures the result.

Then tighten it: faster (skip unrelated setup), sharper (assert the exact symptom, not "didn't crash") and deterministic (pin time, seed randomness, isolate files and network). For flaky bugs, raise the reproduction rate (loop it 100×, add load, narrow timing) until it fails often enough to work with.

**Phase 1 is done** when you have one command, already run and shown, that:
- exercises the real code path and asserts the user's exact symptom,
- gives the same verdict every run (or a pinned, high failure rate for flaky bugs),
- runs in seconds and needs no human.

If you catch yourself building a theory from code before this command exists, go back to building the loop. If you truly cannot build one, stop: list what you tried and ask for access to an environment where it reproduces, a redacted artifact (logs, HAR, dump, recording), or permission to add temporary instrumentation.

## Phase 2: reproduce and minimise

- Confirm the loop shows the failure the user described, not a nearby different one.
- Shrink it: remove inputs, steps, config and data one at a time, re-running after each cut, until every remaining piece is needed for the failure.
- Check what changed recently: `git log`, recent diffs, dependency bumps, config and environment differences.

## Phase 3: hypothesise

- Write 3–5 ranked hypotheses before testing any. Each makes a prediction: "If X is the cause, then changing Y makes the bug go away."
- A hypothesis without a prediction is a hunch: sharpen it or drop it.
- Show the ranked list to the user if they are around; they often know something that reorders it. Carry on if they are not.
- In a multi-part system (UI → API → service → DB, or CI → build → deploy), log what enters and leaves each boundary once, to find where the data goes wrong, before reading any one part deeply.

## Phase 4: test one hypothesis at a time

- Change one variable per probe, and make each probe answer one prediction.
- Prefer a debugger or REPL. Otherwise add targeted logs at the boundaries that tell hypotheses apart.
- Tag every temporary log with a unique prefix such as `[DEBUG-7f3a]`, so cleanup is one search.
- Performance bugs: measure a baseline first (timer, profiler, query plan), then bisect. Measure, then fix.

## Phase 5: fix at the root

1. Turn the minimal repro into a failing regression test at a seam where it exercises the real bug pattern. If no such seam exists, say so: that is a design finding, not a reason for a shallow test.
2. Watch it fail.
3. Search for every caller of the code you are about to change. Fix the root cause once, in the shared code, not in one caller.
4. Watch the test pass, then re-run the original Phase 1 loop and the related suite.

**If three fixes have failed, stop.** Each failed fix that reveals a new problem somewhere else points to a design problem, not a missing tweak. Explain what you have learned to the user and discuss the approach before attempting a fourth.

## Phase 6: clean up

- [ ] The original loop no longer reproduces the bug.
- [ ] The regression test passes (or the missing seam is documented).
- [ ] Every `[DEBUG-...]` line and throwaway harness is removed (search for the prefix).
- [ ] The cause that turned out to be right is stated in the commit or PR message.

## Signs you are off track

The user says "is that actually happening?", "stop guessing" or "we're going in circles"; you are trying "one more quick fix"; you are changing several things at once; you are explaining a cause you have not observed. Go back to Phase 1.

---
Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) `diagnosing-bugs` (MIT), [obra/superpowers](https://github.com/obra/superpowers) `systematic-debugging` (MIT) and [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT). See CREDITS.md.
