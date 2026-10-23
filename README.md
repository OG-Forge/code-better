# Code Better

Skills that make coding agents write less code, clarify before building, test and debug with real feedback loops, review like the person who gets paged, and prove work is done before saying so.

Each skill merges the strongest parts of popular public skill sets: [obra/superpowers](https://github.com/obra/superpowers), [mattpocock/skills](https://github.com/mattpocock/skills), [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), the [Karpathy-inspired guidelines](https://github.com/multica-ai/andrej-karpathy-skills) and [karpathy/autoresearch](https://github.com/karpathy/autoresearch). Where those sets disagree (strict TDD versus proportional testing, one question at a time versus batched rounds, mandatory process versus "just do it"), these skills pick a middle path and say why. Every skill is a plain `SKILL.md` with no scripts or hooks, so it is easy to read before you install it.

## Skills

| Skill | Loads when | What it does |
|---|---|---|
| [lean-coding](skills/lean-coding/SKILL.md) | Writing or changing code | Smallest complete change: reuse first, no speculative code, surgical edits, never cut validation or security, close with what wasn't checked |
| [clarify-first](skills/clarify-first/SKILL.md) | A request leaves real decisions open, or you ask to be grilled | Looks things up before asking; asks open decisions in numbered rounds with a recommended answer each; lays out approaches; gets a yes before building |
| [test-first](skills/test-first/SKILL.md) | Building logic worth testing, or judging tests | Red, watch it fail, green; strictness scaled to risk; tests at the right seam; no tautological tests; mocks only at boundaries |
| [feedback-loop-debugging](skills/feedback-loop-debugging/SKILL.md) | Something is broken, failing, flaky or slow | Builds a fast command that goes red on the bug before theorising; minimises; ranked falsifiable hypotheses; root-cause fix; stops after 3 failed fixes |
| [evidence-before-done](skills/evidence-before-done/SKILL.md) | About to say "done", commit, push or open a PR | Runs the check that proves the claim and shows it; never relays a success report unchecked |
| [ship-review](skills/ship-review/SKILL.md) | Reviewing a diff, PR or whole repo | Reads past the diff; bugs, risk, scale, tests, speed, lean, spec and scope; plain-English findings with the fix and the cost of skipping it |
| [review-feedback](skills/review-feedback/SKILL.md) | You receive review comments | Clarifies everything unclear first, verifies each comment against the code, pushes back with evidence, no performative agreement |
| [build-plan](skills/build-plan/SKILL.md) | Multi-step or long-running work | A plan sized to the work, with exact files, interfaces and tests per task; carries it out with logged rulings instead of stalls |
| [session-handoff](skills/session-handoff/SKILL.md) | Moving work to a new session, tool or person | When to continue, clear, compact or hand off, plus a fixed handoff template |
| [session-retro](skills/session-retro/SKILL.md) | You ask why a session went badly or how to improve the setup | Mines session logs; turns mistakes into checks, pointers and instruction-file fixes |
| [metric-loop](skills/metric-loop/SKILL.md) | You want an unattended loop to improve one number | Modify, measure, keep or revert, log; read-only evaluator, noise threshold, budget, guardrails |
| [keepwarm](skills/keepwarm/SKILL.md) | `/keepwarm 3h`, or "I'm stepping away" | Keeps a long Claude Code session's prompt cache warm while you're away |

The skills reference each other where they meet. For example, `clarify-first` hands an approved design to `build-plan`, and `build-plan` ticks tasks only after `evidence-before-done`.

## Install

**Claude Code**, as two separate commands:

```
/plugin marketplace add OG-Forge/code-better
```
```
/plugin install code-better@code-better
```

Skills then appear as `code-better:<name>`. To try it without installing: `claude --plugin-dir /path/to/code-better`.

**Other agents** (Codex, Cursor, Copilot, Gemini CLI, OpenCode and others that read `SKILL.md`): copy the skill folders you want into that agent's skills folder, for example `~/.codex/skills/`, `~/.cursor/skills/`, or `.agents/skills/` in a repo. `keepwarm` works only in Claude Code; the rest are tool-neutral.

## Using alongside Superpowers or Matt Pocock's skills

These skills cover the same ground as some skills in those sets, so with both installed the agent may load two skills for the same job. Pick one per job:

| Code Better | Superpowers | Matt Pocock |
|---|---|---|
| lean-coding | — | — |
| clarify-first | brainstorming | grilling, grill-me |
| test-first | test-driven-development | tdd |
| feedback-loop-debugging | systematic-debugging | diagnosing-bugs |
| evidence-before-done | verification-before-completion | — |
| ship-review | requesting-code-review | code-review |
| review-feedback | receiving-code-review | — |
| build-plan | writing-plans, executing-plans, subagent-driven-development | to-spec, to-tickets, implement |
| session-handoff | — | handoff |
| session-retro | diagnosing-superpowers | retro |

Superpowers' session-start hook tells the agent to load a Superpowers skill whenever one might apply. If you want Code Better's versions, disable the Superpowers plugin (`/plugin` → Installed → superpowers → Disable) or uninstall it. The skills that have no counterpart there (`metric-loop`, `keepwarm`) combine with anything. `lean-coding` covers the same rules as ponytail and the Karpathy CLAUDE.md: if you already use either, keep one of them, not both.

Claude Code also has a built-in `/code-review` command (bug-focused; it can post PR comments or apply fixes), plus `/security-review` and `/simplify`. Typing `/code-review` runs the built-in. `ship-review` loads on plain-language requests ("review my last commit") and adds reading past the diff, load and scale, lean, spec and scope checks, and plain-English findings. Use one per review.

Worth installing as well, from their own repos: Superpowers' `writing-skills` and Matt Pocock's `writing-for-agents` if you write your own skills; Pocock's `codebase-design` for deep-module design; awesome-llm-apps' [`scope-creep-detector`](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills/scope-creep-detector) and [`commit-archaeologist`](https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills/commit-archaeologist) for script-backed diff and history checks.

## How these were made and checked

Each skill came out of a side-by-side analysis of the source repos. A separate reviewer agent (Claude Opus 5.5) then reviewed each skill for trigger accuracy, overlap, correctness, portability, size and credit, and its findings were fixed. A final reviewer then checked the whole repo. `python scripts/validate.py` runs the structural checks, and [evals/trigger-cases.json](evals/trigger-cases.json) lists the prompts each skill should and should not load on.

## Contributing

Open an issue describing a real session where a skill misfired or misled the agent: what you asked, what the agent did, and what you expected. Pull requests are welcome. Run `python scripts/validate.py` first, and update `evals/trigger-cases.json` when you change a description.

## Credits and licence

MIT. See [LICENSE](LICENSE). The skills adapt work by Jesse Vincent (Superpowers), Matt Pocock, DietrichGebert (ponytail), Jiayuan / forrestchang (Karpathy-inspired guidelines) and Andrej Karpathy (autoresearch), all MIT-licensed. Their copyright notices are in [CREDITS.md](CREDITS.md).
