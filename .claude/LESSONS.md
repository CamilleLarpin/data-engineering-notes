# Lessons — Data Engineering Notes

> CONTAINS: mistakes made, patterns discovered, gotchas specific to this project.
> NOT HERE: decisions with rationale (→ DECISIONS.md), general cross-project patterns (→ LESSONS_GLOBAL.md).
> NEVER delete entries.
> Split into category files at 150 lines.
> When a lesson applies beyond this project: flag with `→ PROMOTE: LESSONS_GLOBAL.md — [reason]`
> Load tier: cool

---

## Format
```
## [category] Short title
> YYYY-MM-DD · source: [project or session]
- what happened / what the trap is
- why it matters
- what to do instead
```

---

<!-- Add lessons below as they are discovered. Oldest at top, newest at bottom. -->

## [anthropic-sdk] Wrong model ID produces empty response, not an exception
> 2026-03-06 · source: data-engineering-notes
- Using an invalid Anthropic model ID (e.g. `claude-sonnet-4-20250514`) causes the API to return an empty or malformed response body — `json.loads` then fails with `JSONDecodeError: Expecting value` on an empty string
- The error looks like a JSON parsing bug; the root cause (wrong model ID) is invisible without debug logging
- Always use the exact model ID format: `claude-sonnet-4-6`, `claude-opus-4-6`, `claude-haiku-4-5-20251001`; add a log of the raw response before `json.loads` to surface this faster

## [python] `load_dotenv()` does not override existing env vars — direnv takes precedence
> 2026-03-06 · source: data-engineering-notes
- If direnv is active and sets `ANTHROPIC_API_KEY` via `.envrc`, `load_dotenv()` silently skips it — the shell env var wins
- The `.env` file looks correct but the wrong key is used at runtime; no warning is raised
- To let `.env` win: use `load_dotenv(override=True)`; to debug: `echo $ANTHROPIC_API_KEY` before running the script
