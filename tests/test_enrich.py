import pytest

from src.scripts.enrich import discover_daily_files, discover_modules, read_files


@pytest.fixture
def daily_dir(tmp_path):
    (tmp_path / "notes_2026-03-06.md").write_text("# Notes\nDocker basics.")
    (tmp_path / "conversation_2026-03-06.md").write_text("# Conversation\nAbout containers.")
    (tmp_path / "unrelated.txt").write_text("should be ignored")
    return tmp_path


@pytest.fixture
def modules_dir(tmp_path):
    docker = tmp_path / "software-engineering" / "docker"
    docker.mkdir(parents=True)
    (docker / "docker_fiche.md").write_text("# Fiche — docker\n")

    sql = tmp_path / "data-handling" / "sql-basics"
    sql.mkdir(parents=True)
    (sql / "sql-basics_fiche.md").write_text("# Fiche — sql-basics\n")

    return tmp_path


def test_discover_daily_files_returns_notes_and_conversations(daily_dir):
    files = discover_daily_files(daily_dir)
    names = [f.name for f in files]
    assert "notes_2026-03-06.md" in names
    assert "conversation_2026-03-06.md" in names


def test_discover_daily_files_excludes_non_md(daily_dir):
    files = discover_daily_files(daily_dir)
    names = [f.name for f in files]
    assert "unrelated.txt" not in names


def test_discover_daily_files_empty_dir(tmp_path):
    assert discover_daily_files(tmp_path) == []


def test_discover_modules_returns_slug_to_path(modules_dir):
    modules = discover_modules(modules_dir)
    assert "docker" in modules
    assert "sql-basics" in modules


def test_discover_modules_path_points_to_fiche(modules_dir):
    modules = discover_modules(modules_dir)
    assert modules["docker"].name == "docker_fiche.md"
    assert modules["sql-basics"].name == "sql-basics_fiche.md"


def test_discover_modules_empty_dir(tmp_path):
    assert discover_modules(tmp_path) == {}


def test_read_files_concatenates_with_headers(daily_dir):
    files = discover_daily_files(daily_dir)
    result = read_files(files)
    assert "=== notes_2026-03-06.md ===" in result
    assert "=== conversation_2026-03-06.md ===" in result
    assert "Docker basics." in result
    assert "About containers." in result


def test_read_files_empty_list():
    assert read_files([]) == ""
