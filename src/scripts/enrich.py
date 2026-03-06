import json
import os
import sys
from pathlib import Path

import anthropic
import click
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger.remove()
logger.add(sys.stderr, level=log_level)

MODULES_ROOT = Path(__file__).parent.parent.parent / "modules"

SYSTEM_PROMPT = """You are a data engineering bootcamp notes assistant.

You receive daily notes and conversations from a student, along with a list of module fiches (revision sheets).

Your task:
1. Identify which modules from the list are meaningfully covered in the daily content.
2. For each identified module, extract new insights to append to the existing fiche.

Rules for the appended insights:
- Fill conceptual gaps with concise explanations — no examples
- Do not add information that is not present in the daily content
- Keep the content in English

Use this exact structure for each module's appended block:

---

## Session — <YYYY-MM-DD>
<one-line TLDR of what was covered>

### <Concept name>
<concise explanation>

### <Concept name>
<concise explanation>

Respond with a JSON object only, no commentary:
{
  "appended_insights": {
    "<slug>": "<markdown block to append>",
    ...
  }
}

If no modules are covered, respond with: {"appended_insights": {}}"""


def discover_daily_files(daily_path: Path) -> list[Path]:
    """Return all notes and conversation files in a daily directory."""
    files = []
    for pattern in ["notes_*.md", "conversation_*.md"]:
        files.extend(daily_path.glob(pattern))
    return sorted(files)


def discover_modules(modules_root: Path) -> dict[str, Path]:
    """Return a dict of slug -> fiche path for all existing modules."""
    modules = {}
    for fiche in modules_root.rglob("*_fiche.md"):
        slug = fiche.stem.replace("_fiche", "")
        modules[slug] = fiche
    return modules


def read_files(files: list[Path]) -> str:
    """Concatenate the content of multiple files with headers."""
    parts = []
    for f in files:
        parts.append(f"=== {f.name} ===\n{f.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def build_user_message(daily_content: str, modules: dict[str, Path], session_date: str) -> str:
    """Build the user message with daily content, session date, and available module slugs."""
    slugs_list = "\n".join(f"- {slug}" for slug in sorted(modules.keys()))

    return f"""Session date: {session_date}

## Daily notes and conversations

{daily_content}

## Available module slugs

{slugs_list}"""


def call_claude(
    client: anthropic.Anthropic, daily_content: str, modules: dict[str, Path], session_date: str
) -> dict[str, str]:
    """Call Claude once to identify and append insights to relevant fiches."""
    user_message = build_user_message(daily_content, modules, session_date)
    logger.debug(f"Sending {len(user_message)} chars to Claude")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    response = message.content[0].text.strip()
    if response.startswith("```"):
        response = response.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    logger.debug(f"Claude response: {response[:200]}...")

    if not response:
        logger.error("Claude returned an empty response")
        raise ValueError("Empty response from Claude")

    data = json.loads(response)
    return data.get("appended_insights", {})


@click.command()
@click.argument("daily_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
def main(daily_dir: Path):
    """Enrich module fiches from a daily notes directory."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    daily_files = discover_daily_files(daily_dir)
    if not daily_files:
        logger.warning(f"No notes or conversation files found in {daily_dir}")
        return

    logger.info(f"Found {len(daily_files)} file(s): {[f.name for f in daily_files]}")

    session_date = daily_dir.name
    daily_content = read_files(daily_files)
    modules = discover_modules(MODULES_ROOT)
    logger.debug(f"Available modules: {sorted(modules.keys())}")

    updated_fiches = call_claude(client, daily_content, modules, session_date)

    if not updated_fiches:
        logger.info("No matching modules found in daily content.")
        return

    updated = []
    for slug, content in updated_fiches.items():
        if slug not in modules:
            logger.warning(f"Claude returned unknown slug '{slug}' — skipping")
            continue
        with modules[slug].open("a", encoding="utf-8") as f:
            f.write(f"\n{content}\n")
        updated.append(slug)
        logger.info(f"✅ {slug} updated")

    print(f"\nEnriched {len(updated)} fiche(s): {', '.join(updated)}")
    print("Review changes with: git diff modules/")


if __name__ == "__main__":
    main()
