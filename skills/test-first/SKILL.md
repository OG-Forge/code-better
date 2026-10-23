---
name: test-first
description: Use when implementing a feature, bug fix or behaviour change that has logic worth testing, when the user asks for TDD or red-green-refactor, or when writing or judging tests and deciding what to mock.
---

# Test first

Write the test, watch it fail for the right reason, write the least code that makes it pass, repeat. A test you never saw fail proves nothing.

## How strict to be

| The code | Rule |
|---|---|
| Money, security, auth, data writes or deletes, parsers, concurrency, bug fixes | Strict: no production code without a failing test first. Code written before its test is set aside and rewritten from the test |
| Ordinary logic (a branch, a loop, a calculation) | Test first, one good test per behaviour |
| Config, generated code, copy changes, throwaway prototypes | No new test needed; say so in the reply |

The user can relax or tighten this. When unsure, use the stricter row.

## Before the first test: pick the seam

A **seam** is the public interface where you observe behaviour without reaching inside: a function's signature, a module's exports, an HTTP endpoint, a CLI command. Tests live at seams, never against internals.

- Prefer an existing seam over a new one, and the highest seam that still runs fast.
- For non-trivial work, name the seams you plan to test, with one line on what each catches and misses, and confirm them with the user if they are around. Proceed with your choice if they are not.
- Reuse the project's test runner, folder layout and helpers. Find them before writing anything.

## The loop, one vertical slice at a time

1. **Red.** Write one test for one behaviour, named for what it proves ("rejects an expired token"). Before writing it, name the production change that would make it fail.
2. **Watch it fail.** Run it. It must fail because the behaviour is missing, not because of a typo or import error. If it passes, it tests existing behaviour: fix the test.
3. **Green.** Write the simplest code that passes. Nothing for future tests.
4. **Watch it pass.** Run it and the related suite. The output is clean: no new warnings or errors.
5. **Tidy.** Refactor only the code you just wrote, and only while the tests stay green.
6. **Next slice.** Let what this slice taught you shape the next test.

Writing all the tests first and all the code after (horizontal slicing) tests imagined behaviour. Go one slice at a time.

## What a good test is

- **Behaviour through the public interface.** It survives a refactor that keeps the behaviour. It reads like a specification.
- **Independent expected values.** The expected value comes from a known literal, a worked example or the spec, never from recomputing it the way the code does (`expect(total(items)).toBe(15)`, not `toBe(items.reduce(...))`).
- **Verifies through the interface.** "createUser then getUser returns Alice", not "createUser then query the users table".
- **One behaviour per test.** An "and" in the name means two tests.
- **Mocks only at system boundaries:** external APIs, time, randomness, sometimes the database or filesystem. Never mock your own modules or internal collaborators; pass dependencies in so the boundary is easy to replace.
- **Assert on real results, not on mock calls.** "Payment status is confirmed", not "paymentService.process was called once".

## When a test is hard to write

That is design feedback: the interface is hard to use. Simplify the interface (fewer parameters, return a value instead of mutating state, accept dependencies instead of creating them) before forcing the test.

## Done means

- Every new behaviour has a test you watched fail and then pass.
- The full relevant suite passes, run fresh, with the command and result shown.
- Anything you chose not to test is listed with a reason.

## Red flags

| Thought | Do instead |
|---|---|
| "I'll add tests after" | Tests written after pass immediately and prove nothing about the gap they cover |
| "It's too simple to test" | Then the test takes thirty seconds. Write it, or say why the rule table exempts it |
| "I tested it manually" | Manual checks are not repeatable. Automate the one that matters |
| "I'll mock this class to isolate it" | Test through the real thing; mock only at the system boundary |
| "The test passed first time" | It never went red. Check it can fail |

---
Adapted from [obra/superpowers](https://github.com/obra/superpowers) `test-driven-development` (MIT), [mattpocock/skills](https://github.com/mattpocock/skills) `tdd` (MIT) and [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT). See CREDITS.md.
