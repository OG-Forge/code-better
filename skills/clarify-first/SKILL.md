---
name: clarify-first
description: Use when a request to build or change something leaves open decisions that would change what gets built (scope, behaviour, data, users, UX, approach), or when the user asks to be grilled, interviewed or questioned about a plan, idea or design before work starts.
---

# Clarify first

Find out what the user actually wants, and why, before building. Clear tasks skip this skill; the cost of a wrong build is what it prevents.

## 0. Decide whether to run at all

- **Everything that matters is in the request** ("rename this field", "make the button blue"): don't use this skill. Do the task.
- **Something non-trivial is open:** run the steps below.
- If the user did not ask for questions, end your first message with a one-line offer: "Or say 'go' and I'll proceed with the recommended answers." If they take it, state your choices in one line each and start.

## 1. Look before you ask

Facts are your job; decisions are the user's. Before the first question, read what they pointed at and the code or material it connects to, until you can explain how things work today and what the change would touch. Never ask something the code, docs or earlier conversation already answers. When a question depends on a fact you could look up, look it up (use a subagent for a long search), and ask only the questions that don't depend on it while it runs.

## 2. Ask in rounds

Map the open decisions as a tree: some decisions only make sense once others are settled. The **frontier** is every open decision whose prerequisites are settled.

Each round, ask the whole frontier at once, numbered, each with your recommended answer and a one-line reason, and word each question so "yes" accepts your recommendation:

```
**Q1. <short title>.** <question, with the options if there are a few>
→ Recommended: <answer>, because <reason>.

**Q2. ...**
```

- Make every question specific to their project and to what you found. Say what the answer would change.
- Keep a round to the decisions that are actually open now; questions that depend on an unanswered one wait for the next round.
- After each round, recompute the frontier from the answers and ask the next round. Stop when the frontier is empty.

## 3. Lay out the approaches

Once you know what they want, put the ways to build it in a message of its own: two or three real options grounded in the existing code, what each one trades off, and which one you recommend and why. If only one sensible way exists, say so and say why the others don't fit.

## 4. Write it down and get a yes

Size the write-up to the work:

- **Small change:** a short note in chat: what will be built, the chosen approach, what is out of scope.
- **Bigger piece of work:** a short design doc: goal and why; goals and non-goals; constraints; the chosen approach and the rejected ones; decisions made, marking the ones that were your call; what is left to the implementer. Save it where the project keeps docs, or ask where.

Anything you filled in yourself is marked as your proposal, not as something they agreed to. Build nothing (no code, scaffolding or dependency installs) until the user approves the note or doc. Reading and exploring are fine. A throwaway spike they said yes to is fine, and keeping it is a new request.

For multi-step work, hand the approved design to `build-plan`.

## Red flags

| Thought | Do instead |
|---|---|
| "I'll ask what framework they use" | Look it up in the repo |
| "I'll fill in sensible defaults quietly" | Say each default out loud as a recommendation |
| "They said 'sounds good', so it's approved" | Approval covers only what you showed them |
| "One question at a time is gentler" | Batch the frontier; the user can answer what they want and say "yes" to the rest |
| "This could be done ten ways, I'll list them all" | Two or three real options, with a recommendation |

---
Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) `grilling` (MIT) and [obra/superpowers](https://github.com/obra/superpowers) `brainstorming` (MIT). See CREDITS.md.
