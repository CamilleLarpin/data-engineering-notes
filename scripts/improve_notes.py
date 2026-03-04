import os
import sys
from pathlib import Path
import anthropic
from dotenv import load_dotenv
import click
import subprocess

load_dotenv()

SYSTEM_PROMPT = """Tu es un expert Data Engineering. Tu corriges et enrichies des fiches de notes de bootcamp en markdown.
1. Corrige les fautes d'orthographe et de compréhension
2. Structure avec des titres clairs (##, ###), reformat si besoin
3. Suit le contenu original — ne supprime d'informations
Réponds UNIQUEMENT avec le contenu markdown amélioré, sans commentaires."""


def improve_note(content: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Améliore cette fiche :\n\n{content}"}],
    )
    return message.content[0].text


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True, help="Affiche sans modifier les fichiers")
def main(files, dry_run):
    for filepath in files:
        if not filepath.endswith(".md"):
            continue
        path = Path(filepath)
        original = path.read_text(encoding="utf-8")
        improved = improve_note(original)
        if dry_run:
            print(improved)
        else:
            path.write_text(improved, encoding="utf-8")
            subprocess.run(["git", "add", filepath])  # auto-stage
            click.echo(f"✅ {filepath} amélioré.")

if __name__ == "__main__":
    main()