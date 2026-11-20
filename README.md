# AI Office Template

A ready-made "company" for Claude Code. One manager, 47 specialist employees (subagents), each doing one thing, with skills, permissions, approval gates, a shared brain, and a website to watch it work.

```
You ──► Office Manager (CLAUDE.md) ──► the fewest employees needed ──► out/<task>/ ──► done/
                    │
                    └── stops and asks you at every gate (plan, send, DB write, push to main, delete, hire)
```

## Quick start

```bash
cd ai-office-template
python3 tools/build_agents.py      # roster → .claude/agents/ (already built; rerun after edits)
claude                             # start Claude Code here
```

Then type requests the way you normally would:

```
/office the export button does nothing on the reports page, fix it
/status
/ship
/reply "Quarterly numbers question"
/hire someone who checks our cloud costs
```

To work on code that lives elsewhere, give the office access to it:

```bash
claude --add-dir ~/path/to/your/projects
```

A handy alias: `alias office='cd ~/ai-office-template && claude --add-dir ~/path/to/your/projects'`

## Watch the office

```bash
python3 tools/build_site.py && open site/index.html
```

Floor plan with every desk (who's working, who's waiting for you), org chart, task board, and each employee's profile with their skills.

## What's inside

| Path | What it is |
|---|---|
| `CLAUDE.md` | The Office Manager: routes every task, holds the gates |
| `office/roster.toml` | **The single source of truth**: departments, roles, presets, skills |
| `office/directory.md` | Who's who (generated) |
| `office/_forms/` | Blank employee form and blank skill form, used by `/hire` |
| `.claude/agents/` | One subagent per role (generated from the roster) |
| `.claude/skills/` | Entry shortcuts: `/office`, `/status`, `/ship`, `/reply`, `/hire` |
| `.claude/settings.json` | Blocks force-push, push to main, `rm -rf`, reading `.env`; asks before any push |
| `brain/` | Rules, glossary and decisions every employee reads |
| `inbox/` `out/` `done/` | Task folders (`task.toml` + `log.md` + outputs). Not committed |
| `tools/` | `build_agents.py`, `build_site.py` |
| `site/` | Website template; `index.html` is built, not committed |

## The company

11 departments: Executive Office, HR, Strategy & Ideas, Product & Design, Software Engineering, Data, Analysis, Quality, Release & Deployment, Communications, Operations. See `office/directory.md`.

Skills come in three layers:
- **Company:** every employee. Pick up a task, ask in plain text, cite sources, self-check, hand off, report back.
- **Department:** shared within a department. For example, Data's `safe-sql` reads freely and writes only after you approve the SQL.
- **Role:** what makes each employee a specialist.

## Make it yours

1. **Name it:** `[company]` in `office/roster.toml`, including your integration branch.
2. **Add your domain:** ask `/hire` (the HR department checks whether an existing role can take a new skill first). You can also copy `office/_forms/employee.toml` into a department yourself and run `python3 tools/build_agents.py`.
3. **Connect mail, chat and drives:** employees get only the tools in their preset. Add your connector's tool names to `extra_tools` under `[presets.mail-read]` and `[presets.mail-draft]`. Add read and draft tools only, never send.
4. **Teach it your rules:** add them to `brain/rules.md` and your words to `brain/glossary.md`, or just correct the office and the Brain Keeper will save the rule.

After changing employees, restart Claude Code (or open `/agents`) so the new ones load.

## How employees report

Every employee ends with:

```
RESULT: done | not done | blocked
OUTPUTS: <files>
GATE: <action waiting for your approval, or none>
QUESTIONS: <numbered, or none>
NEXT: <who should take it next>
```

Employees can't call each other (a Claude Code rule). The Office Manager passes the work along, which keeps every hand-off and gate visible to you.

## Limits

- Per-employee permissions come from each role's tool list plus the shared deny list in `.claude/settings.json`. Claude Code has no separate settings file per agent.
- 47 agent descriptions load when you start Claude in this folder. They don't load in your other projects.
- Requires Python 3.11+ (uses `tomllib`) and Claude Code.
