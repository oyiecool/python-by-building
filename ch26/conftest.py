# conftest.py
import pytest


@pytest.fixture
def sample_tree(tmp_path):
    """A small folder of files to back up; tmp_path is a fresh temporary folder per test."""
    src = tmp_path / "src"
    (src / "docs").mkdir(parents=True)
    (src / "a.txt").write_text("hello")
    (src / "docs" / "report.md").write_text("# report")
    (src / ".git").mkdir()
    (src / ".git" / "config").write_text("ignored")
    return src
