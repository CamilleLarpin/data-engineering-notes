import pytest

from src.scripts.quiz import discover_non_empty_modules


@pytest.fixture
def modules_dir(tmp_path):
    non_empty = tmp_path / "data-handling" / "sql-basics"
    non_empty.mkdir(parents=True)
    (non_empty / "sql-basics_fiche.md").write_text("# Fiche — sql-basics\n\n## Key concepts\nSELECT, FROM, WHERE.\n")

    empty = tmp_path / "software-engineering" / "docker"
    empty.mkdir(parents=True)
    (empty / "docker_fiche.md").write_text("# Fiche — docker\n")

    return tmp_path


def test_non_empty_module_is_included(modules_dir):
    slugs = [slug for slug, _ in discover_non_empty_modules(modules_dir)]
    assert "sql-basics" in slugs


def test_empty_module_is_excluded(modules_dir):
    slugs = [slug for slug, _ in discover_non_empty_modules(modules_dir)]
    assert "docker" not in slugs


def test_path_points_to_fiche(modules_dir):
    modules = {slug: path for slug, path in discover_non_empty_modules(modules_dir)}
    assert modules["sql-basics"].name == "sql-basics_fiche.md"


def test_empty_dir_returns_empty_list(tmp_path):
    assert discover_non_empty_modules(tmp_path) == []
