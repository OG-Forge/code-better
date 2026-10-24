# Changelog

## 0.1.0 (2026-10-24)

- Public release. `main` is protected: changes go through a pull request with a code-owner approval and a passing `validate` check; force pushes and deletion are blocked.
- Repo hygiene: GitHub Actions pinned to commit SHAs, CODEOWNERS, Dependabot for Actions, SECURITY.md with private vulnerability reporting.
- SessionStart routing note (`hooks/routing.md`) so skills load on everyday requests; opt out with `CODE_BETTER_NO_ROUTER=1`.
- harness-setup: goal-first, opinionated setup of agent harnesses, with proof that each piece works.
- First set of 12 skills: lean-coding, clarify-first, test-first, feedback-loop-debugging, evidence-before-done, ship-review, review-feedback, build-plan, session-handoff, session-retro, metric-loop, keepwarm.
- Claude Code plugin and marketplace manifests.
- `scripts/validate.py` structural checks, `evals/trigger-cases.json`, and `scripts/trigger_test.py` (headless trigger checks).
