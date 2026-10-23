---
name: lean-coding
description: Use when writing, changing, fixing or refactoring code in any language, and when choosing whether to add a dependency, abstraction, option or file. Also use when the user complains about over-engineering, bloat, drive-by edits or unrequested changes.
---

# Lean coding

Solve the whole task with the least new code, touch only what the task needs, and prove it works. Small because it is necessary, not because it is golfed. Lazy about the solution, never about reading.

## 1. Understand before you write

- Read the task and the code it touches. Trace the real flow: where data comes in, what is stored, what goes out.
- List every place the change must reach: callers, tests, fixtures, config, exports, docs. That is the scope. Features nobody asked for are not.
- Check what the change could break for users: data it could destroy or expose, callers that would stop working.
- When the request has more than one reasonable reading, or you are making an assumption that changes what gets built, say so in one line and ask, or pick one and state it. Silent guesses are the failure to avoid.
- When a simpler approach than the one requested exists, say so before building.

## 2. Take the first rung that fully works

1. **Does it need to exist?** Skip options, flexibility and "for later" code nobody asked for, and name what you skipped in one line. A vague request gets the smallest version that does the core job.
2. **Already in this codebase?** Reuse the helper, component or pattern the way the surrounding code uses it.
3. **Standard library or platform feature?** Use it, unless the project has its own equivalent. A house component beats a native widget.
4. **An installed dependency?** Use it. Add a new dependency only when it replaces substantial, tricky code.
5. **One clear line?** One line a reader understands at a glance. A one-liner that needs decoding is not short.
6. **Otherwise** write the minimum code that works.

## 3. Change surgically

- Every changed line traces to the request. Match the existing style, structure, layers and naming, even where you would do it differently.
- Leave adjacent code, comments and formatting as they are. Mention unrelated problems or dead code in your reply instead of fixing them.
- Clean up only your own mess: remove imports, variables and functions that your change made unused.
- Bug fix: before editing, search for every caller of the function you touch, then fix the root cause once, in the shared code.
- Code you move or merge keeps its validation and error handling.
- Between two options of equal size, pick the one that is correct on edge cases.
- Comments explain only the why that the code cannot show, in one line.
- A deliberate shortcut with a known limit gets a comment: `shortcut: <the limit>, <when to upgrade>`.

## 4. Never cut

Validation at trust boundaries, error handling that prevents data loss, security, accessibility, anything the user asked for. These are part of "the minimum that works".

## 5. Define done, then check it

- Turn the task into a check: "add validation" becomes "tests for invalid input pass"; "fix the bug" becomes "a test that reproduced it now passes"; "refactor X" becomes "the same tests pass before and after".
- New non-trivial logic (a branch, a loop, a parser, money, security, a new script) leaves one small test or an assert-based self-check behind. Trivial changes need none.
- For multi-step work, state a short plan first: `1. <step> → verify: <check>`.
- Run the checks before saying it works (see `evidence-before-done`).

## 6. Close every reply

End with one or two lines: what you skipped or did not check, and any risk the user should know about.

## Red flags

| Thought | Do instead |
|---|---|
| "I'll make it configurable in case" | Build the one case asked for and name the option you skipped |
| "While I'm here I'll tidy this" | Mention it and leave it |
| "A small wrapper will make it cleaner" | Call the existing thing directly |
| "This needs a new library" | Check the codebase, the standard library and the installed dependencies first |
| "I'll skip the input check to keep it short" | Trust-boundary validation is never cut |
| "200 lines, but it works" | If 50 would do, rewrite it |

---
Adapted from [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) (MIT) and [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT). See CREDITS.md.
