---
name: metric-loop
description: Use when the user wants an autonomous experiment loop that keeps trying changes to improve one measurable number (runtime, latency, bundle size, memory, a benchmark, a test pass rate, a model or prompt score), possibly unattended or overnight, or asks for an autoresearch-style loop.
---

# Metric loop

An autonomous experiment loop: change one thing, measure it, keep the change if the number got better, revert it if not, log every attempt, repeat. It only works with a metric you trust that the agent cannot game.

## Set up (with the user, before the loop starts)

Agree on each of these and write them into `metric-loop.md` in the repo root (or wherever the user prefers):

1. **The metric and its direction**, for example "p95 latency of `bench/api.js`, lower is better", and the exact command that prints it.
2. **Read-only files:** the benchmark, its inputs, test data, scoring code, and the test and lint config the guardrails use. Changing the ruler is cheating.
3. **The editable surface:** the files or folders the loop may change. Everything else is read-only.
4. **The budget:** a time limit per measurement (run it under `timeout` or the harness's run timeout; kill runs that take twice the baseline) and an overall limit (number of experiments, hours or spend).
5. **Guardrails:** commands that must still pass after every kept change (the test suite, typecheck), and limits such as memory or "no new packages". For a pass-rate metric, the number of tests must not drop.
6. **Attended or unattended:** unattended runs go until the budget is used; attended runs report every N experiments.

Then prepare git:

- Run `git status --porcelain`. If anything is modified or staged, ask the user to commit or stash it. Never stash or discard their work yourself.
- Create a fresh branch `metric-loop/<tag>` (it must not already exist). The main branch is never touched.
- Add `results.tsv`, `run.log` and `metric-loop.md` to `.git/info/exclude` so they are never committed and never touched by a reset.

**Baseline and noise:** run the measurement 3 times. The reference is the median; the noise is the spread. Deterministic metrics such as bundle size need one run. Log the baseline as the first `keep` row in `results.tsv`. Confirm the setup with the user, then start.

## The loop

```
repeat until the budget runs out or the user stops it:
  1. check `git branch --show-current` is metric-loop/<tag>; if not, stop
  2. pick one idea; change only the editable surface
  3. stage only editable-surface paths (`git add <paths>`, never -A or .) and commit with the idea as the message
  4. run the measurement with all output redirected to run.log (never stream it into context)
  5. read only the metric lines from run.log (grep); if they are missing, read the last ~50 lines for the error
  6. run the guardrail commands
  7. `git diff --name-only <last kept SHA>..HEAD` lists only editable-surface paths?
  8. beats the reference by more than the noise? re-run twice more and keep it only if the median of the 3 still wins.
     kept → its median becomes the new reference
     otherwise, or any check in 6-7 failed → `git reset --hard <SHA of the last keep row in results.tsv>`
  9. append a row to results.tsv: commit, metric, status (keep / discard / crash), one-line description
```

- A crash with an obvious fix (typo, missing import): fix and re-run once. A broken idea: log it as `crash` and move on.
- Never special-case the benchmark's inputs, cache their results, or make the code print a fake metric line.
- **Simplicity counts:** a tiny gain that adds a lot of complex code is not worth keeping; the same result with less code is a win.
- When ideas run out: re-read the code for new angles, combine near-misses, try a more radical change, or revisit the best discarded ideas.
- Never run destructive commands or edit outside the editable surface; if the remaining ideas need that, stop and report.
- Stop after 5 crashes in a row, or if the baseline or guardrails fail on the last kept commit: the environment is broken.
- In an unattended run, keep going until the budget is used up without asking whether to continue.
- Loop commits are scratch commits: `evidence-before-done` applies to the final report, not to each experiment.
- After a context reset or in a new session: re-read `metric-loop.md` and `results.tsv`, check the branch, and continue.

## Finish

Re-run the best commit once from a clean checkout and read the cumulative diff for benchmark-specific hacks. Report: the baseline and the best result (with the noise range); the kept commits and what each did; the top discarded ideas and why they failed; the path to `results.tsv`. Leave the branch for the user to review and merge. Don't merge it yourself.

---
Adapted from [karpathy/autoresearch](https://github.com/karpathy/autoresearch) `program.md` (MIT), generalised from ML training to any trusted metric. See CREDITS.md.
