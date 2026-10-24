"""Check every skill: frontmatter, name matches folder, description length, size, credits, trigger cases."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_BYTES = 20_000  # Claude Code truncates skills re-attached after compaction at 20k characters
MAX_DESCRIPTION = 1024


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith(" "):
            fields[key.strip()] = value.strip().strip('"')
    return fields


def main():
    errors = []
    cases = json.loads((ROOT / "evals" / "trigger-cases.json").read_text(encoding="utf-8"))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    routing = (ROOT / "hooks" / "routing.md").read_text(encoding="utf-8")
    routed = set(re.findall(r"^- .+: code-better:([a-z0-9-]+)\s*$", routing, re.M))
    skill_dirs = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    for d in skill_dirs:
        path = d / "SKILL.md"
        if not path.exists():
            errors.append(f"{d.name}: no SKILL.md")
            continue
        text = path.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm is None:
            errors.append(f"{d.name}: missing frontmatter")
            continue
        if fm.get("name") != d.name:
            errors.append(f"{d.name}: name '{fm.get('name')}' does not match folder")
        desc = fm.get("description", "")
        if not desc.startswith("Use when"):
            errors.append(f"{d.name}: description should start with 'Use when'")
        if len(desc) > MAX_DESCRIPTION:
            errors.append(f"{d.name}: description is {len(desc)} chars (max {MAX_DESCRIPTION})")
        size = len(text.encode("utf-8"))
        if size >= MAX_BYTES:
            errors.append(f"{d.name}: SKILL.md is {size} bytes (max {MAX_BYTES - 1})")
        if d.name != "keepwarm" and "CREDITS.md" not in text:
            errors.append(f"{d.name}: no credit line pointing to CREDITS.md")
        if d.name not in cases:
            errors.append(f"{d.name}: no entry in evals/trigger-cases.json")
        if d.name != "keepwarm" and d.name not in routed:
            errors.append(f"{d.name}: not listed in hooks/routing.md")
        if f"skills/{d.name}/SKILL.md" not in readme:
            errors.append(f"{d.name}: not linked from README.md")
    for name in cases:
        if name != "_about" and not (ROOT / "skills" / name).is_dir():
            errors.append(f"trigger-cases.json lists unknown skill '{name}'")
    for name in routed - {d.name for d in skill_dirs}:
        errors.append(f"hooks/routing.md lists unknown skill '{name}'")
    for e in errors:
        print("FAIL", e)
    print(f"{len(skill_dirs)} skills checked, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
