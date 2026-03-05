import os
import re
import subprocess
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

SYSTEM_PROMPT = """Tu es un assistant de prise de notes pour un bootcamp Data Engineering.

Tu reçois des lignes modifiées d'un fichier de notes brutes. Tu appliques uniquement :
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


def get_committed_lines(filepath: str) -> list[str]:
    """Retourne les lignes du fichier tel qu'il est dans le dernier commit."""
    result = subprocess.run(["git", "show", f"HEAD:{filepath}"], capture_output=True, text=True)
    return result.stdout.splitlines()


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


def improve_lines(lines: list[str]) -> list[str]:
    """Envoie les lignes à l'API Claude et retourne les lignes corrigées."""
    if not lines:
        return lines
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    content = "\n".join(lines)
    logger.debug(f"Sending to Claude:\n{content}")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": content}],
    )
    corrected = message.content[0].text.splitlines()
    logger.debug(f"Received from Claude:\n{corrected}")
    return corrected


def apply_corrections(filepath: str, corrections: dict[int, str]):
    """Remplace les lignes d'un fichier par les corrections fournies."""
    path = Path(filepath)
    original_lines = path.read_text(encoding="utf-8").splitlines()
    for line_num, corrected in corrections.items():
        logger.debug(f"Applying correction at line {line_num}: {corrected}")
        if line_num - 1 < len(original_lines):
            original_lines[line_num - 1] = corrected
    path.write_text("\n".join(original_lines) + "\n", encoding="utf-8")


def filter_new_lines(added: list[tuple[int, str]], committed_lines: list[str]) -> list[tuple[int, str]]:
    """Filtre les lignes vraiment nouvelles — exclut les lignes vides et celles déjà committées."""
    return [(n, t) for n, t in added if t.strip() != "" and (n > len(committed_lines) or committed_lines[n - 1] != t)]


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

        committed_lines = get_committed_lines(filepath)
        added = filter_new_lines(added, committed_lines)

        if not added:
            continue

        line_nums, line_texts = zip(*added)
        corrected = improve_lines(list(line_texts))

        corrections = dict(zip(line_nums, corrected))
        apply_corrections(filepath, corrections)
        subprocess.run(["git", "add", filepath])
        print(f"✅ {filepath} — {len(corrections)} lignes corrigées")


if __name__ == "__main__":
    main()
