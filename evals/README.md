# Evals

- `trigger-cases.json`: for every skill, prompts that should load it and near-misses that should not. Update it whenever a skill's `description` changes.
- `python scripts/validate.py`: structural checks (frontmatter, name matches folder, description starts with "Use when", size under 20 KB, credit line, README link, trigger cases present). CI runs it.

## Checking triggers by hand

Install the plugin locally, start a fresh session, paste a prompt, and see whether the skill loads:

```bash
claude --plugin-dir /path/to/code-better
```

Or headless, one prompt at a time:

```bash
claude -p --plugin-dir /path/to/code-better "Review my last commit" --output-format stream-json --verbose | grep -o '"skill":"[^"]*"'
```

A `should` prompt passes when its skill loads. A `should_not` prompt passes when that skill stays quiet.
