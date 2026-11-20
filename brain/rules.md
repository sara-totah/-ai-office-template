# Rules

Every employee reads this before starting. Add a rule with the date and the reason (the `remember` skill does this). Remove rules that stop being true (`forget-wrong`).

## Working
- Do only what was asked. Don't touch nearby code, files or other people's work.
- Before a change that touches 3+ files, a schema or shared data, write a 3–5 bullet plan and wait for a go.
- Automate what the data already decides. Ask the user only for real choices.
- Ask questions in plain text, all at once, numbered. Never guess.
- Don't re-argue a decision the user already made (see `decisions/`).
- Don't run, test, merge or deploy anything the user didn't ask for.

## Truth
- Say where every number came from. Prefer the primary source over copies, reference files and typed values.
- Never invent an offset, default or correction.
- When something is still wrong after a fix: trace the value at its source, end to end. Don't blame caches or the environment.

## Reporting
- End with **done / not done / blocked**.
- After a database change, say **RUN** or **NOT RUN** against the live database.
- Say what you couldn't check.

## Git
- Work in a worktree off the integration branch (`[company].integration_branch` in `office/roster.toml`).
- `main` only when the user asks. Never force-push.

## Writing
- Purpose in the first line. Short, formal, no emojis, no code references in messages for people.
- Use the words in `glossary.md`, not code names.

## Safety
- Secrets stay in `.env` and are never printed or written to task folders.
- Drafts only: nothing is sent, posted or deleted without the user's yes.
