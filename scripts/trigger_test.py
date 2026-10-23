"""Run each trigger case through headless Claude Code and record which skill, if any, it loads.

Usage: python scripts/trigger_test.py [skill ...]
Needs the `claude` CLI on PATH and spends tokens (one short session per prompt).
Prompts written in parentheses describe a moment, not a user message, and are skipped.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_CALL = re.compile(r'"name":"Skill","input":\{"skill":"([^"]+)"')


def skills_loaded(prompt, workdir):
    out = subprocess.run(
        ["claude", "-p", "--plugin-dir", str(ROOT), "--max-turns", "2",
         "--output-format", "stream-json", "--verbose", prompt],
        cwd=workdir, capture_output=True, text=True, encoding="utf-8", timeout=300,
    ).stdout
    return SKILL_CALL.findall(out)


def main():
    cases = json.loads((ROOT / "evals" / "trigger-cases.json").read_text(encoding="utf-8"))
    wanted = sys.argv[1:] or [k for k in cases if k != "_about"]
    failures = 0
    with tempfile.TemporaryDirectory() as workdir:
        for skill in wanted:
            for kind in ("should", "should_not"):
                for prompt in cases[skill][kind]:
                    if prompt.startswith("("):
                        continue
                    loaded = skills_loaded(prompt, workdir)
                    hit = f"code-better:{skill}" in loaded
                    ok = hit if kind == "should" else not hit
                    failures += not ok
                    print(f"{'PASS' if ok else 'FAIL'}  {skill:<24} {kind:<10} {prompt!r} -> {loaded or 'none'}")
    print(f"{failures} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
