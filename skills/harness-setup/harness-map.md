# Where each harness layer lives

Tools change their layouts often. Treat this table as a starting point: confirm against the tool's own `--help`, its docs, or what already exists on disk, and prove each piece works (SKILL.md step 5) before trusting it.

## Layers

| Layer | What it is for |
|---|---|
| Instructions | Always-loaded context: project purpose, real commands, pointers to docs. Keep it short |
| Settings and permissions | Which commands and tools run without asking, which are always refused, the default approval mode |
| Hooks | Deterministic scripts on agent events: block a dangerous command, format after an edit, run checks before the agent stops |
| Skills | Instructions and scripts loaded only when a task matches the skill's description |
| Subagents | Separate agents with their own context, tools and model, for isolation, parallel work or fresh-eyes review |
| MCP servers | External tools and data the agent can call |
| Plugins | Installable bundles of skills, agents, hooks and MCP config |
| Sandbox | Limits on what commands can touch (files, network) |
| Checks outside the agent | Lint, typecheck, tests, pre-commit hooks, CI. They apply to humans and agents alike |

## Claude Code

| Layer | Shared (commit) | Personal |
|---|---|---|
| Instructions | `CLAUDE.md` at the repo root (and in subfolders for local rules); `@path` imports other files | `~/.claude/CLAUDE.md` |
| Settings, permissions | `.claude/settings.json`: `permissions.allow`, `ask`, `deny` with patterns such as `Bash(npm test *)` (the older `Bash(npm test:*)` form also works) | `.claude/settings.local.json` (gitignored), `~/.claude/settings.json` |
| Hooks | `hooks` in settings: events such as `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `Stop`, `SubagentStop`. Exit code 2 from a `PreToolUse`, `UserPromptSubmit` or `Stop` hook blocks it and sends stderr back to the agent; on `PostToolUse` the tool has already run, so exit 2 only feeds stderr back | same keys in personal settings |
| Skills | `.claude/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| Subagents | `.claude/agents/<name>.md` (frontmatter: `name`, `description`, `tools`, `model`) | `~/.claude/agents/` |
| MCP | `.mcp.json` at the repo root | `claude mcp add` (user or local scope); check with `/mcp` |
| Plugins | `enabledPlugins` and `extraKnownMarketplaces` in `.claude/settings.json` let a team share them | `/plugin marketplace add <repo>`, `/plugin install <name>@<marketplace>` |
| Sandbox, autonomy | Built-in sandboxing for shell commands (`/sandbox`, `sandbox.enabled`), auto mode, or a devcontainer | same |

Useful commands: `/memory` (loaded instruction files), `/permissions`, `/hooks`, `/agents`, `/mcp`, `/plugin`, `claude -p` (headless, for testing skills and hooks).

## Codex

| Layer | Where |
|---|---|
| Instructions | `AGENTS.md` at the repo root (nested files apply to subfolders); personal `~/.codex/AGENTS.md` |
| Settings, permissions, sandbox | `~/.codex/config.toml`: approval policy and sandbox mode; per-project overrides where supported |
| Hooks | Lifecycle hooks; they must be trusted before they run (`/hooks`) |
| Skills | `.agents/skills/` in the repo (searched from the current folder up to the root) or `~/.agents/skills/` |
| MCP | `[mcp_servers]` in `config.toml` |
| Plugins | `codex plugin marketplace add <repo>`, `codex plugin add <name>@<marketplace>` (verify) |

## Cursor

| Layer | Where |
|---|---|
| Instructions | `.cursor/rules/*.mdc` (always-on or scoped by file pattern); also reads `AGENTS.md` |
| Hooks | `.cursor/hooks.json` |
| Skills | `~/.cursor/skills/` or `.agents/skills/` (verify) |
| MCP | `.cursor/mcp.json` (project) or the user-level equivalent |

## GitHub Copilot (CLI and VS Code)

| Layer | Where |
|---|---|
| Instructions | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `AGENTS.md` |
| Skills | `~/.copilot/skills/`, `.github/skills/`, `.claude/skills/` or `.agents/skills/` |
| MCP | VS Code `.vscode/mcp.json`; the CLI's own MCP config |
| Plugins | `copilot plugin marketplace add <repo>`, `copilot plugin install <name>@<marketplace>` |

## Gemini CLI

| Layer | Where |
|---|---|
| Instructions | `GEMINI.md` (repo and `~/.gemini/`) |
| Settings, MCP | `~/.gemini/settings.json` (`mcpServers`) and project `.gemini/settings.json` |
| Skills, extensions | `.gemini/skills/` or `~/.gemini/skills/`; `gemini skills install …`, `gemini extensions install …` |

## Several tools on one repo

- Keep one source of truth for instructions, usually `AGENTS.md`, which most tools read. Point `CLAUDE.md` at it (`@AGENTS.md`) instead of keeping copies that drift.
- Put shared skills in `.agents/skills/` when the tools you use read it; otherwise keep one copy and link or copy it at install time.
- Keep checks in the repo (lint, tests, pre-commit, CI) rather than in any one tool's hooks, so every tool and every human gets them.
