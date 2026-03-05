import os
import re
import subprocess
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger.remove()
logger.add(sys.stderr, level=log_level)

SYSTEM_PROMPT = """Tu es un assistant de prise de notes pour un bootcamp Data Engineering.

Tu reçois un fichier de notes brutes complet. Tu appliques uniquement :
1. Correction orthographe et grammaire
2. Remplacement de termes vagues (trucs, choses, bidules, machin) par des termes techniques précis et contextuels
3. Résolution des marqueurs incomplets : TBC, TBD, ?, ?? — si tu peux les compléter avec certitude
4. Formatting léger : titres manquants, listes mal formatées
5. Si l'intention est ambiguë et que tu ne peux pas corriger avec certitude : ajoute le marqueur TOCHECK en fin de ligne

Règles strictes :
- Ne jamais réécrire, enrichir ou compléter ce qui est déjà rédigé
- Ne jamais supprimer de contenu
- Ne jamais ajouter d'informations qui ne sont pas dans les notes originales
- Répondre UNIQUEMENT avec le contenu corrigé, sans commentaires"""


def get_staged_diff(filepath: str) -> str:
    """Retourne le diff git staged pour un fichier donné."""
    result = subprocess.run(["git", "diff", "--cached", "-U0", filepath], capture_output=True, text=True)
    logger.debug(f"Diff for {filepath}:\n{result.stdout}")
    return result.stdout


def extract_added_lines(diff: str) -> list[tuple[int, str]]:
    """Retourne les lignes ajoutées avec leur numéro à partir d'un diff git."""
    lines = []
    line_num = 0
    for line in diff.splitlines():
        logger.debug(f"Parsing diff line: {repr(line)}")
        if line.startswith("@@"):
            match = re.search(r"\+(\d+)", line)
            if match:
                line_num = int(match.group(1))
                logger.debug(f"@@ line_num set to: {line_num}")
        elif line.startswith("+") and not line.startswith("+++"):
            lines.append((line_num, line[1:]))
            line_num += 1
        elif not line.startswith("-") and not line.startswith("\\"):
            line_num += 1
    logger.debug(f"Extracted lines: {lines}")
    return lines


def improve_file(content: str) -> str:
    """Envoie le contenu complet d'un fichier à Claude et retourne le contenu corrigé."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    logger.debug(f"Sending to Claude: {len(content.splitlines())} lines")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": content}],
    )
    corrected = message.content[0].text
    logger.debug(f"Received from Claude: {len(corrected.splitlines())} lines")
    return corrected


def main():
    """Point d'entrée : corrige les lignes stagées pour chaque fichier .md passé en argument."""
    files = sys.argv[1:]
    for filepath in files:
        if not filepath.endswith(".md"):
            continue

        diff = get_staged_diff(filepath)
        added = extract_added_lines(diff)
        if not added:
            continue

        path = Path(filepath)
        content = path.read_text(encoding="utf-8")
        corrected = improve_file(content)
        path.write_text(corrected, encoding="utf-8")
        subprocess.run(["git", "add", filepath])
        print(f"✅ {filepath} corrigé")


if __name__ == "__main__":
    main()
