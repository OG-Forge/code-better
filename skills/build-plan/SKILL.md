---
name: build-plan
description: Use when a coding task will take many steps, touch several files or run for a long stretch (an approved design, a spec, a ticket list, or a large feature or migration), before writing the code; and when carrying out such a plan.
---

# Build plan

A plan records the decisions an implementer can't make alone: which files, which names and signatures, which values, which tests prove each step. Size it to the work.

## Pick the size

| The work | The plan |
|---|---|
| A few steps, one area of code | A list in chat: `1. <step> → verify: <check>` |
| Several files or hours of work | A plan file using the template below |
| Several independent parts | One plan per part, each producing working, tested software on its own |

Save plan files where the project keeps docs (ask if unclear), for example `docs/plans/YYYY-MM-DD-<topic>.md`.

## Before writing tasks

- Read the design or spec and the code it touches. Reuse what exists (see `lean-coding`).
- Map the files to create or change and what each is responsible for. Files that change together live together. Follow the existing structure.
- List the project's real commands for test, typecheck, lint and run, taken from its config.

## Plan file template

```markdown
# <Feature> plan

**Goal:** <one sentence>
**Approach:** <two or three sentences>
**Spec:** <path or link to the design/spec this implements>
**Commands:** test `<cmd>` · typecheck `<cmd>` · lint `<cmd>`

## Constraints
<project-wide rules from the spec, one per line, exact values copied>

## Review focus
<up to 5 inputs or failure modes the spec implies but no test below covers, such as empty input,
 a duplicate submit or a timezone edge. Each gets a test added to the task that owns the code.>

### Task 1: <name>
**Files:** create `path/a.ts` · change `path/b.ts` · test `path/a.test.ts`
**Interfaces:** uses `<signature from an earlier task>` · provides `<exact signature later tasks rely on>`
- [ ] Write the failing test `<name>`: asserts `<behaviour with exact values>`
- [ ] Run `<cmd>`, expect FAIL: `<reason>`
- [ ] Implement `<signature>` in `<file>` (<one line on approach, only if the test leaves a real choice>)
- [ ] Run `<cmd>`, expect PASS
- [ ] Commit: `<message>`
```

**Each step lets the implementer write exactly one reasonable thing.** Steps that decide nothing ("handle edge cases", "add validation", "TBD") are gaps: replace them with the specific case and its test. Full function bodies are only for an algorithm the signature and tests don't settle. A plan longer than the code it describes has written the code instead.

**Task size:** the smallest unit with its own test cycle that a reviewer could accept or reject on its own. Fold setup and config steps into the task that needs them.

## Self-check before handing over

1. **Coverage:** every requirement in the spec maps to a task.
2. **Steps:** no step decides nothing; no step copies code the tests already determine.
3. **Names:** signatures and names match across tasks.
4. **Review focus:** each listed risk has a test in a task.
5. **Proportion:** the plan is shorter than the code it describes.

Fix what you find. Then ask the user to review the plan before building, unless they already said to go ahead.

## Carrying out a plan

- Work the tasks in order, ticking each box only after its check has run (see `evidence-before-done`), and commit per task.
- **Rulings, not stalls.** When the plan is ambiguous or wrong in a small way, decide, note it in the plan as `Ruling: <decision> - <why> - <cost if wrong>`, and keep going.
- **Stop and ask only for:** something irreversible or destructive; a security-sensitive action; a side effect outside the working copy that needs permission (pushing to a shared branch, merging, deploying, publishing, messaging people); or a plan so broken that every way forward is a guess.
- When subagents are available and tasks are independent, give each task to a fresh subagent with just that task, the interfaces it needs and the commands. Check its diff and run the tests yourself before ticking the task. Choose the model tier deliberately: a cheap model for mechanical tasks, the strongest for design work and the final review.
- At the end, have the whole change reviewed with fresh eyes (`ship-review`, ideally by a fresh subagent), fix what it finds, run the full suite, and report.

---
Adapted from [obra/superpowers](https://github.com/obra/superpowers) `writing-plans`, `executing-plans` and `subagent-driven-development` (MIT), and the step-to-verify list from [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) (MIT). See CREDITS.md.
