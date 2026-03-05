from src.scripts.improve_notes import extract_added_lines
from src.scripts import improve_notes as sut
from unittest.mock import MagicMock, patch


def test_extract_added_lines_simple():
    """Vérifie que les lignes ajoutées sont extraites avec le bon numéro de ligne."""
    diff = "@@ -0,0 +1,3 @@\n+line one\n+line two\n+line three\n"
    result = extract_added_lines(diff)
    assert result == [(1, "line one"), (2, "line two"), (3, "line three")]


def test_apply_corrections_simple(tmp_path):
    """Vérifie qu'une correction est bien appliquée à la bonne ligne."""
    f = tmp_path / "notes.md"
    f.write_text("line 1\nline 2\nline 3\n", encoding="utf-8")
    sut.apply_corrections(str(f), {2: "CORRECTED"})
    lines = f.read_text(encoding="utf-8").splitlines()
    assert lines[1] == "CORRECTED"


def test_apply_corrections_out_of_range(tmp_path):
    """Vérifie qu'une correction hors-range est ignorée sans erreur."""
    f = tmp_path / "notes.md"
    f.write_text("only one line\n", encoding="utf-8")
    sut.apply_corrections(str(f), {99: "ghost"})
    assert f.read_text(encoding="utf-8").strip() == "only one line"

def test_get_staged_diff_returns_stdout():
    """Vérifie que get_staged_diff retourne le stdout du diff git."""
    mock_result = MagicMock(stdout="diff output")
    with patch("src.scripts.improve_notes.subprocess.run", return_value=mock_result):
        result = sut.get_staged_diff("notes/foo.md")
    assert result == "diff output"

def test_improve_lines_returns_corrected_lines():
    """Vérifie que improve_lines retourne les lignes corrigées par l'API."""
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="corrected one\ncorrected two")]
    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message

    with patch("src.scripts.improve_notes.anthropic.Anthropic", return_value=mock_client):
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            result = sut.improve_lines(["line one", "line two"])

    assert result == ["corrected one", "corrected two"]


def test_improve_lines_empty_input():
    """Vérifie que improve_lines retourne une liste vide si l'input est vide."""
    assert sut.improve_lines([]) == []