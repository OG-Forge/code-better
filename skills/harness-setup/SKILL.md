---
name: harness-setup
description: Use when the user wants to set up, design, audit or overhaul the agent harness for a project, team or themselves (instruction files like CLAUDE.md or AGENTS.md, skills, subagents, hooks, permissions, MCP servers, plugins, sandboxing or autonomous runs), or asks how to configure a coding agent for their goal and wants it built, not just listed.
---

# Harness setup

Set up the environment a coding agent works in (its instructions, skills, subagents, hooks, permissions, tools and checks) so that it serves the user's actual goal. Start from the goal, push back hard on choices that will hurt, build the smallest harness that works, and prove each piece works before calling it done.

**Your stance:** a sceptical staff engineer who has cleaned up many over-built agent setups. Agree when the user is right. When a request is wrong for their goal, say so plainly, explain the cost, and offer a better option. The user decides. If they overrule you, build what they chose and record their choice and your objection in the decision log (step 6). Never quietly build something you argued against without logging it, and never water down a safety objection to keep things pleasant.

## 1. Recon before questions

Find the facts yourself; ask only for decisions.

- **Which harness:** which agent tools they use (Claude Code, Codex, Cursor, Copilot, Gemini CLI, others) and on which OS. Where each layer lives in each tool: [harness-map.md](harness-map.md).
- **What exists:** instruction files at the repo and user level, settings and permissions, installed plugins and skills, subagents, hooks, MCP servers. Read them; list overlaps, contradictions and anything stale.
- **The repo:** language, the real test, lint, typecheck and build commands (from package scripts, Makefile, CI config), the CI setup, pre-commit hooks, where secrets come from, and what deploys where.
- **Evidence of pain (when available):** recent session logs. Look for repeated corrections, failing commands, permission prompts and long searches, read safely as `session-retro` describes. Failures you have actually seen in the logs beat guesses.

## 2. Grill the goal

If the request is one small, clear change (one permission rule, one hook, one MCP server), skip the grilling: check it against step 3, build it and prove it (step 5).

If the request itself matches a row in step 3, raise that objection in round 1, before the other questions.

Otherwise use `clarify-first`'s format: numbered rounds over the open decisions, a recommended answer for each, and each question worded so "yes" accepts it. Settle these, roughly in this order, skipping any that recon already answered:

1. **Goal:** what the harness is for, in one sentence, and how they'll know it's working (fewer corrections, PRs that pass review first time, safe unattended runs, onboarding teammates…).
2. **Who uses it:** just them, a team sharing a repo, or the public (a template or plugin). This decides what goes in shared files and what goes in personal ones.
3. **Failures today:** the 3–5 things that actually go wrong. A harness piece with no failure behind it is speculation.
4. **Autonomy:** when they want to be asked and when the agent should just act. Interactive pairing, long plan execution, or unattended or overnight runs.
5. **Risk surface:** production access, customer or personal data, secrets, paid APIs, shared branches, company rules about code leaving the machine.
6. **Budget:** money and tokens they're willing to spend per day or task, and how they feel about speed versus cost.
7. **Maintenance:** who keeps the harness current when the repo, the tools or the team change.

## 3. Push back on these

When a request matches a row, oppose it using the reason given and offer the alternative. Change your view only when the user's goal or constraints truly make their option better, and say why you changed it. State each objection once, clearly; don't re-argue a decision the user has made and logged.

| They want | Why it hurts | Offer instead |
|---|---|---|
| A long CLAUDE.md or AGENTS.md full of rules | Loaded into every turn; rules get lost and ignored; goes stale | A short file: project purpose, the real commands, pointers to docs. Detail lives in docs and skills, loaded only when relevant |
| Mechanical rules written as prose ("always run prettier", "never import from X") | Prose gets skipped; a check never forgets | A hook, a lint rule, a pre-commit hook or CI job. Prose only for judgement calls |
| A "team" of many personas or subagents from day one | Every handoff loses context and costs tokens; the overlapping roles confuse routing | One main agent plus one or two subagents with a concrete reason: isolation of noisy work, parallel independent tasks, or a fresh-eyes reviewer |
| Installing several skill packs or plugins at once | Overlapping triggers fight; context bloats; nobody knows which skill ran | One skill per job. Before adding a skill, run a few prompts headless (`claude -p "<prompt>"`) and check which skill loads |
| Skipping permissions (`--dangerously-skip-permissions`, bypass or "yolo" modes) on their main machine | One bad command can wipe files, leak secrets or push to shared branches | The middle options first: an allowlist of the routine commands they actually run plus deny rules for dangerous ones, or the harness's auto or sandbox mode (in Claude Code, auto mode and `/sandbox`). Full autonomy only inside a container, VM or disposable worktree with no production credentials |
| An MCP server for something a CLI already does (GitHub, databases, cloud) | Each server adds tools, a process and a trust boundary; without tool search, its tool definitions also cost context every turn | The CLI (`gh`, `psql`, `aws`) with an allowlist. MCP when there is no CLI, or it adds real value (a browser, an authenticated SaaS without a CLI) |
| Unvetted third-party MCP servers, plugins or skills | They run with the agent's permissions; prompt injection and supply-chain risk | Read the code first; pin versions; prefer official or well-known sources; give least privilege |
| Secrets in instruction files, settings or MCP config | Leak through logs, commits and transcripts | Environment variables or a secret manager; reference them by name |
| Hooks that auto-commit, push, merge or deploy | Removes the human checkpoint on outward-facing actions | Hooks that check (format, lint, test, block dangerous commands); push, merge and deploy stay human-approved |
| Slow or flaky hooks on every edit | Every turn slows down; flaky blocks train people to disable them | Fast, deterministic hooks on edit; the slow suite on Stop, pre-commit or CI |
| Unattended or overnight runs with no trusted check | The agent grades itself; you wake up to confident nonsense | First an approved spec and acceptance tests the agent can't edit, a budget cap and a working branch (`build-plan`). `metric-loop` only when the goal is improving one number |
| An agent that reads untrusted content (web pages, issues, third-party repos) while holding secrets and network access | Prompt injection: text in that content can steer the agent to leak data or act | No secrets and restricted network in sessions that read untrusted content; keep those sessions read-only |
| The largest model everywhere (every subagent, every loop) | Cost and latency multiply with no quality gain on simple work | A cheaper model for search, exploration and routine review subagents (set per subagent); the strongest model for design and final review |
| One endless session for everything | Context fills with stale detail; quality drops and cost rises | Clear between unrelated tasks, subagents for noisy work, `session-handoff` across sessions |
| Building a custom agent framework or Agent SDK app to get a better coding workflow | Months of maintenance to rebuild what configuration already gives | Configure the existing harness first; build custom only for a product feature or a workflow config truly can't express |
| Copying someone else's whole setup | Their failures aren't yours; you inherit their bloat | Start minimal and add a piece each time a real failure shows up |
| Everything always-on | Context and cost on every turn for rarely-used capability | Skills that load only when relevant; user-invoked commands for rare workflows |

Also oppose anything that breaks the user's own stated constraints, such as a company data rule, a budget or a team convention, even if they ask for it in the moment. Remind them of the constraint and ask them to confirm.

## 4. Propose a v1 and get a yes

Present the smallest harness that serves the goal as one table, then ask for approval as a final round:

| Layer | Change | Why (goal or failure it serves) | Cost (context, money, upkeep) |
|---|---|---|---|

- Usually 3–7 rows. Every row traces to the goal or to a failure from step 2. Cut any row that doesn't.
- Mark which files are shared (committed) and which are personal (local, gitignored).
- List what you deliberately left out and the condition that would justify adding it later ("add a reviewer subagent if PRs keep failing review").

## 5. Build and prove each piece

Build on a branch or in local-only files the user can review. Start with the highest-value row. For each piece, run a check that proves it works, then show the evidence (`evidence-before-done`):

| Piece | Proof |
|---|---|
| Instruction file | A fresh session answers a question that only the file answers (in Claude Code, `/memory` also lists loaded files) |
| Permission allow or deny rule | An allowed command runs with no prompt; a denied one is refused |
| Hook | Trigger it on purpose (a badly formatted edit, a blocked command) and see it act; time it |
| Skill | A should-trigger prompt loads it and a near-miss doesn't (run `claude -p "<prompt>"` headless and check which skill loaded) |
| Subagent | Dispatch it on a small real task and check it stayed in its lane and returned what was asked |
| MCP server | It connects (in Claude Code, `/mcp`), and one read-only call returns real data |
| Sandbox or container | A command that should be blocked (a write outside the workspace, network if disabled) fails |
| Unattended run | A short, budget-capped dry run in the sandbox stops on its own and leaves a reviewable branch |

If a piece can't be proved in this environment, say so and give the user the exact check to run.

## 6. Hand over

- Write a short decision log where the project keeps docs (for example `docs/agent-harness.md`, or a personal notes file for a solo setup). For each piece: what it is, why, how it was proved, and any choice the user made over your objection.
- Give the growth rule: add a harness piece only after a failure you've actually seen, and review the setup every few weeks with `session-retro`, cutting what never fires.
- Tell the user how to undo each piece (which file or setting to remove).

---
Original to Code Better. It applies ideas from [mattpocock/skills](https://github.com/mattpocock/skills) `retro` and `writing-for-agents` (MIT) and from the source repos analysed for this project. See CREDITS.md.
