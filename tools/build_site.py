"""Build the office website from office/roster.toml and the task folders.

Writes site/index.html (a single self-contained page). Open it with:
  python3 tools/build_site.py && open site/index.html
"""

from __future__ import annotations

import datetime
import json
import pathlib
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "site" / "template.html"
OUT = ROOT / "site" / "index.html"
TRAYS = ("inbox", "out", "done")


def read_tasks() -> tuple[list[dict], list[str]]:
    """Every task folder in inbox/, out/ and done/. The folder decides the status."""
    tasks, problems = [], []
    for tray in TRAYS:
        (ROOT / tray).mkdir(exist_ok=True)
        for folder in sorted((ROOT / tray).iterdir()):
            meta = folder / "task.toml"
            if not folder.is_dir() or not meta.exists():
                continue
            try:
                with meta.open("rb") as f:
                    t = tomllib.load(f)
            except (tomllib.TOMLDecodeError, UnicodeDecodeError) as e:
                problems.append(f"{tray}/{folder.name}/task.toml: {e}")
                continue
            log = folder / "log.md"
            lines = [ln.strip() for ln in log.read_text(encoding="utf-8").splitlines()
                     if ln.strip().startswith("- ")] if log.exists() else []
            chain = t.get("chain", [])
            chain = [chain] if isinstance(chain, str) else list(chain)
            try:
                step = int(t.get("step", 0))
            except (TypeError, ValueError):
                problems.append(f"{tray}/{folder.name}/task.toml: step is not a number, using 0")
                step = 0
            tasks.append({
                "id": t.get("id", folder.name),
                "title": t.get("title", folder.name),
                "request": t.get("request", ""),
                "created": str(t.get("created", "")),
                "status": tray,
                "chain": chain,
                "step": step,
                "current": t.get("current", ""),
                "waiting_for_you": t.get("waiting_for_you", ""),
                "result": t.get("result", ""),
                "log": lines[-20:],
            })
    return tasks, problems


def main() -> int:
    with (ROOT / "office" / "roster.toml").open("rb") as f:
        roster = tomllib.load(f)
    tasks, problems = read_tasks()
    data = {
        "company": roster["company"],
        "presets": roster["presets"],
        "company_skills": roster.get("company_skills", []),
        "departments": [{**d, "roles": [r for r in d["roles"] if r.get("status") != "retired"]}
                        for d in roster["departments"]],
        "skills": roster["skills"],
        "tasks": tasks,
        "built": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    # Escape every "<" so task text can never end or break the <script> block.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    template = TEMPLATE.read_text(encoding="utf-8")
    if "/*OFFICE_JSON*/" not in template:
        print("site/template.html is missing the /*OFFICE_JSON*/ placeholder; nothing written.")
        return 1
    OUT.write_text(template.replace("/*OFFICE_JSON*/", payload), encoding="utf-8")
    roles = sum(len(d["roles"]) for d in roster["departments"])
    print(f"site/index.html: {roles} roles, {len(tasks)} tasks")
    for p in problems:
        print("  skipped:", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
