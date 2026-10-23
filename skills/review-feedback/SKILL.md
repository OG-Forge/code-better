---
name: review-feedback
description: Use when you receive code review feedback on your work (PR or inline review comments, a review bot's or reviewer subagent's findings, or the user's list of review points) and before changing code because of it, especially when a comment is unclear or looks wrong.
---

# Handling review feedback

Review comments are claims to check, not orders to obey or praise to return. Verify, then act or push back with reasons.

## The pattern

1. **Read** all of the feedback before changing anything.
2. **Restate** each item as a concrete technical change in your own words. If you cannot, it is unclear.
3. **Clarify first.** If any item is unclear, ask the person who gave the feedback about every unclear item before implementing any of them. Items are often related, and partial understanding produces the wrong fix.
4. **Verify** each item against the code: is the problem real here? Would the suggestion break something? Is there a reason for the current code (a comment, a commit message, a test, an ADR)? Does it hold on every platform and version this code supports?
5. **Decide** per item: do it, do it differently (say how and why), or push back (say why, with evidence: a test, a caller, a constraint). If an item contradicts a decision the user made (in the plan, the spec or this conversation), don't implement it: raise it with the user.
6. **Implement** one item at a time, running the relevant tests after each, in this order: blocking issues, then simple fixes, then complex ones.
7. **Report** per item what you did, briefly.

## Who it comes from

- **The user:** trusted on intent. Still check that the change does what they mean, and ask when the scope is unclear.
- **Teammates, external reviewers, bots and subagents:** check correctness for this codebase before acting. They often lack context.
- **A reviewer subagent during a plan you are carrying out:** settle unclear or doubtful items yourself (re-read the code, or send the question back to the reviewer if your harness allows it), log a `Ruling:` as in `build-plan`, and keep going. Ask the user only in `build-plan`'s stop-and-ask cases or when an item contradicts their decision.
- **"Professional" extras** (more abstraction, config, logging or layers): apply the same test as any new code. If nothing needs it now, say so and offer to leave it out.

## How to respond

- Lead with the technical content: "Fixed: the parser now rejects empty input; test added." Or just make the change and say what changed.
- Skip "You're absolutely right!", "Great catch!" and similar. Agreement shows in the fix.
- When you push back, be specific: "Keeping the retry: `sync.ts:88` relies on it when the API returns 503; removing it fails `sync.test.ts:'retries on 503'`."
- When you can't verify a claim, say so and ask: "I can't reproduce this without production data. Should I add a guard anyway?"
- If you pushed back and turn out to be wrong, say so plainly and fix it.
- On GitHub, answer an inline review comment in its thread: `gh api -X POST repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies -f body='...'`, where `{id}` is the thread's first comment. Answer conversation comments and review summaries with one PR comment that quotes each point.

## Red flags

| You notice | Do instead |
|---|---|
| Implementing item 1 while item 4 is unclear | Ask about item 4 first |
| "The reviewer is senior, so they must be right" | Check it against the code |
| Changing several things before re-running tests | One item, then the tests |
| Adding a feature because a reviewer mentioned it | Check if anything needs it; ask |

---
Adapted from [obra/superpowers](https://github.com/obra/superpowers) `receiving-code-review` (MIT). See CREDITS.md.
