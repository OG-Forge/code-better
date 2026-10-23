"""Run each trigger case through headless Claude Code and record which skill, if any, it loads.

Usage: python scripts/trigger_test.py [skill ...]
Needs the `claude` CLI on PATH and spends tokens (one short session per prompt).
Prompts written in parentheses describe a moment, not a user message, and are skipped, as are slash
commands (they expand as a prompt, not a Skill call). Disable other skill plugins first: results reflect
every plugin that is enabled. To switch plugins off for this run only, set TRIGGER_SETTINGS to a
settings JSON, e.g. '{"enabledPlugins": {"superpowers@claude-plugins-official": false}}'.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_CALL = re.compile(r'"name":"Skill","input":\{"skill":"([^"]+)"')


def skills_loaded(prompt, workdir):
    cmd = [shutil.which("claude") or "claude", "-p", "--plugin-dir", str(ROOT), "--max-turns", "2",
           "--output-format", "stream-json", "--verbose"]
    if os.environ.get("TRIGGER_SETTINGS"):
        cmd += ["--settings", os.environ["TRIGGER_SETTINGS"]]
    try:
        out = subprocess.run(cmd + [prompt], cwd=workdir, capture_output=True, text=True, stdin=subprocess.DEVNULL,
                             encoding="utf-8", timeout=180).stdout
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
    return SKILL_CALL.findall(out)


def main():
    cases = json.loads((ROOT / "evals" / "trigger-cases.json").read_text(encoding="utf-8"))
    wanted = sys.argv[1:] or [k for k in cases if k != "_about"]
    failures = 0
    with tempfile.TemporaryDirectory() as workdir:
        for skill in wanted:
            for kind in ("should", "should_not"):
                for prompt in cases[skill][kind]:
                    if prompt.startswith(("(", "/")):
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
