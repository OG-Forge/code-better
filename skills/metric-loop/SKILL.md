---
name: metric-loop
description: Use when the user wants an autonomous experiment loop that keeps trying changes to improve one measurable number (runtime, latency, bundle size, memory, a benchmark, a test pass rate, a model or prompt score) by modify, measure, keep or revert, possibly unattended or overnight.
---

# Metric loop

An autonomous experiment loop: change one thing, measure it, keep the change if the number got better, revert it if not, log every attempt, repeat. It only works with a metric you trust that the agent cannot game.

## Set up (with the user, before the loop starts)

Agree on each of these and write them into `metric-loop.md` in the repo root (or wherever the user prefers):

1. **The metric and its direction**, for example "p95 latency of `bench/api.js`, lower is better", and the exact command that prints it.
2. **The evaluator is read-only:** the benchmark, test data and scoring code are off limits for edits. Changing the ruler is cheating.
3. **The editable surface:** which files or folders the loop may change. Everything else is read-only.
4. **The budget per run:** a time limit for each measurement (kill runs that take twice as long) and an overall limit (number of experiments, hours or spend).
5. **Noise:** run the baseline 3 times. Treat a change as an improvement only if it beats the best baseline by more than the spread between those runs.
6. **Guardrails:** commands that must still pass after every kept change (the test suite, typecheck), and any limits such as memory or dependencies ("no new packages").
7. **Branch:** a fresh branch such as `metric-loop/<tag>`, so the main branch is never touched.

Confirm the setup with the user, then run the baseline.

## The loop

```
repeat until the budget runs out or the user stops it:
  1. pick one idea; change only the editable surface
  2. commit with a message describing the idea
  3. run the measurement with all output redirected to run.log (never stream it into context)
  4. read only the metric lines from run.log (grep); if they are missing, read the last ~50 lines for the error
  5. run the guardrail commands
  6. better beyond noise and guardrails pass → keep the commit
     otherwise → git reset --hard to the previous kept commit
  7. append a row to results.tsv: commit, metric, status (keep / discard / crash), one-line description
```

- Keep `results.tsv` and `run.log` out of git, and never reset them.
- A crash with an obvious fix (typo, missing import): fix and re-run once. A broken idea: log it as `crash` and move on.
- **Simplicity counts:** a tiny gain that adds a lot of complex code is not worth keeping; the same result with less code is a win.
- When ideas run out: re-read the code for new angles, combine near-misses, try a more radical change, or revisit the best discarded ideas.
- If the user asked for an unattended run, keep going until the budget is used up without asking whether to continue. Stop early only for something destructive or outside the editable surface.

## Finish

Report: the baseline and the best result (with the noise range); the kept commits and what each did; the top discarded ideas and why they failed; the path to `results.tsv`. Leave the branch for the user to review and merge. Don't merge it yourself.

---
Adapted from [karpathy/autoresearch](https://github.com/karpathy/autoresearch) `program.md` (MIT), generalised from ML training to any trusted metric. See CREDITS.md.
