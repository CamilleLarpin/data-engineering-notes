from unittest.mock import MagicMock, patch

from src.scripts import improve_notes as sut
from src.scripts.improve_notes import extract_added_lines


def test_extract_added_lines_simple():
    """Vérifie que les lignes ajoutées sont extraites avec le bon numéro de ligne."""
    diff = "@@ -0,0 +1,3 @@\n+line one\n+line two\n+line three\n"
    result = extract_added_lines(diff)
    assert result == [(1, "line one"), (2, "line two"), (3, "line three")]


def test_extract_added_lines_no_newline():
    """Vérifie que la ligne '\\ No newline at end of file' n'incrémente pas le compteur."""
    diff = "@@ -136 +136,3 @@\n-old line\n\\ No newline at end of file\n+old line\n+\n+new line\n"
    result = extract_added_lines(diff)
    assert result == [(136, "old line"), (137, ""), (138, "new line")]


def test_extract_added_lines_middle():
    """Vérifie que les lignes ajoutées au milieu d'un fichier sont correctement indexées."""
    diff = "@@ -3,0 +4,2 @@\n+new line 1\n+new line 2\n"
    result = extract_added_lines(diff)
    assert result == [(4, "new line 1"), (5, "new line 2")]


def test_get_staged_diff_returns_stdout():
    """Vérifie que get_staged_diff retourne le stdout du diff git."""
    mock_result = MagicMock(stdout="diff output")
    with patch("src.scripts.improve_notes.subprocess.run", return_value=mock_result):
        result = sut.get_staged_diff("notes/foo.md")
    assert result == "diff output"


def test_improve_file_returns_corrected_content():
    """Vérifie que improve_file retourne le contenu corrigé par l'API."""
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="corrected content")]
    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message

    with patch("src.scripts.improve_notes.anthropic.Anthropic", return_value=mock_client):
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            result = sut.improve_file("original content")

    assert result == "corrected content"
