# test_syncbackup.py
import json
import os

import pytest

import syncbackup as sb


def test_scan_skips_git_folder(sample_tree):
    assert set(sb.scan(sample_tree)) == {"a.txt", "docs/report.md"}


@pytest.mark.parametrize("data, expected", [
    (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
])
def test_sha256_known_values(tmp_path, data, expected):
    f = tmp_path / "f.bin"
    f.write_bytes(data)
    assert sb.sha256(f) == expected


def test_dry_run_copies_nothing(sample_tree, tmp_path):
    dest = tmp_path / "backup"
    assert sb.run(sample_tree, dest, apply=False) == 0
    assert not (dest / "a.txt").exists()


def test_backup_then_change_then_delete(sample_tree, tmp_path):
    dest = tmp_path / "backup"
    sb.run(sample_tree, dest, apply=True)
    assert (dest / "docs" / "report.md").read_text() == "# report"

    (sample_tree / "a.txt").write_text("changed")
    os.utime(sample_tree / "a.txt", (2_000_000_000, 2_000_000_000))   # make the change visible
    (sample_tree / "docs" / "report.md").unlink()
    sb.run(sample_tree, dest, apply=True)

    assert (dest / "a.txt").read_text() == "changed"
    archived = list((dest / sb.ARCHIVE).rglob("*"))
    assert {p.name for p in archived if p.is_file()} == {"a.txt", "report.md"}
    manifest = json.loads((dest / sb.MANIFEST).read_text())
    assert set(manifest) == {"a.txt"}


def test_verify_detects_corruption(sample_tree, tmp_path):
    dest = tmp_path / "backup"
    sb.run(sample_tree, dest, apply=True)
    assert sb.verify(dest) == 0
    (dest / "a.txt").write_text("bit rot!")
    assert sb.verify(dest) == 1
