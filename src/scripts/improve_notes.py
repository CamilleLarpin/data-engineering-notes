import os
import sys
from pathlib import Path
import anthropic
from dotenv import load_dotenv
import subprocess

load_dotenv()

SYSTEM_PROMPT = """..."""


def get_staged_diff(filepath: str) -> str:
    """Retourne le diff git staged pour un fichier donné."""
    result = subprocess.run(
        ["git", "diff", "--cached", "-U0", filepath],
        capture_output=True, text=True
    )
    return result.stdout


def extract_added_lines(diff: str) -> list[tuple[int, str]]:
    """Retourne les lignes ajoutées avec leur numéro à partir d'un diff git."""
    lines = []
    line_num = 0
    for line in diff.splitlines():
        if line.startswith("@@"):
            import re
            match = re.search(r'\+(\d+)', line)
            if match:
                line_num = int(match.group(1))
        elif line.startswith("+") and not line.startswith("+++"):
            lines.append((line_num, line[1:]))
            line_num += 1
        elif not line.startswith("-"):
            line_num += 1
    return lines


def improve_lines(lines: list[str]) -> list[str]:
    """Envoie les lignes à l'API Claude et retourne les lignes corrigées."""
    if not lines:
        return lines
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    content = "\n".join(lines)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": content}],
    )
    return message.content[0].text.splitlines()


def apply_corrections(filepath: str, corrections: dict[int, str]):
    """Remplace les lignes d'un fichier par les corrections fournies."""
    path = Path(filepath)
    original_lines = path.read_text(encoding="utf-8").splitlines()
    for line_num, corrected in corrections.items():
        if line_num - 1 < len(original_lines):
            original_lines[line_num - 1] = corrected
    path.write_text("\n".join(original_lines) + "\n", encoding="utf-8")


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

        line_nums, line_texts = zip(*added)
        corrected = improve_lines(list(line_texts))

        corrections = dict(zip(line_nums, corrected))
        apply_corrections(filepath, corrections)
        subprocess.run(["git", "add", filepath])
        print(f"✅ {filepath} — {len(corrections)} lignes corrigées")


if __name__ == "__main__":
    main()